"""
Gradio Search Interface.

Provides a chat-style interface for semantic document search
with parent document retrieval.

Search flow (the index is metadata-only, so reranking happens after the
parent-document pull):
    vector search (k x multiplier candidates)
    -> parallel parent document fetch from source databases
    -> recover matched chunk text by slicing at stored char offsets
    -> CrossEncoder rerank
    -> dedup by parent document -> top-k
"""

import gradio as gr

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import SearchConfig, Settings
from phase0_infra.habitat_logging import get_logger

from src.shared.chromadb_client import ChromaDBClient
from src.shared.database import DatabaseConnectionManager
from src.shared.embedding_model import EmbeddingModelManager

from .feedback import FeedbackCollector
from .parent_document_fetcher import (
    MockParentDocumentFetcher,
    ParentDocumentFetcher,
    SearchResultWithDocument,
)
from .reranker import SearchReranker
from .retriever import SemanticRetriever

logger = get_logger(__name__)

# Candidate over-fetch when reranking is disabled (dedup still needs slack)
_DEDUP_CANDIDATE_MULTIPLIER = 3
# Context window reranked when stored chunk offsets don't fit the document
_FALLBACK_WINDOW = 1000
# Chunks are ~512 chars; offsets spanning more than this are stale metadata
_MAX_PLAUSIBLE_CHUNK = 8192


def format_result(result: SearchResultWithDocument, index: int) -> str:
    """Format a single search result for display."""
    sr = result.search_result
    doc = result.parent_document

    output = f"### Result {index + 1}\n\n"
    rerank_score = sr.metadata.get("rerank_score")
    if rerank_score is not None:
        output += (
            f"**Score:** {rerank_score:.4f} (reranked; "
            f"vector similarity {sr.similarity_score:.4f})\n\n"
        )
    else:
        output += f"**Score:** {sr.similarity_score:.4f}\n\n"
    output += f"**Source:** `{sr.source_db}` / `{sr.source_table}` / `{sr.parent_doc_id}`\n\n"

    if doc:
        # Show excerpt
        excerpt = doc.get_excerpt(800)
        output += f"**Content:**\n\n{excerpt}\n\n"

        # Show metadata if available
        if doc.metadata:
            meta_items = [f"- **{k}:** {v}" for k, v in doc.metadata.items() if v]
            if meta_items:
                output += "**Metadata:**\n" + "\n".join(meta_items) + "\n\n"
    else:
        output += f"*Document not found: {result.error}*\n\n"

    output += "---\n\n"
    return output


class SearchApp:
    """
    Gradio-based search application.

    Provides:
    - Chat-style search interface
    - Configurable number of results
    - Database filtering
    - Source attribution
    """

    def __init__(
        self,
        retriever: SemanticRetriever,
        parent_fetcher: ParentDocumentFetcher | MockParentDocumentFetcher,
        config: SearchConfig,
        feedback_collector: FeedbackCollector | None = None,
        reranker: SearchReranker | None = None,
    ):
        """
        Initialize the search app.

        Args:
            retriever: Semantic retriever.
            parent_fetcher: Parent document fetcher.
            config: Search configuration.
            feedback_collector: Optional feedback collector for RLHF.
            reranker: Optional CrossEncoder reranker, applied after the
                parent-document fetch.
        """
        self.retriever = retriever
        self.parent_fetcher = parent_fetcher
        self.config = config
        self.feedback_collector = feedback_collector
        self.reranker = reranker
        self._app: gr.Blocks | None = None

    def _recover_chunk_text(self, result: SearchResultWithDocument) -> str:
        """
        Recover the matched chunk's text by slicing the parent document at
        the char offsets stored during ingestion.

        Falls back to a window around char_start (or the document head) when
        the offsets no longer fit the document — e.g. the source record
        changed after ingestion.
        """
        sr = result.search_result
        content = result.parent_document.content
        char_start = sr.metadata.get("char_start")
        char_end = sr.metadata.get("char_end")

        if (
            isinstance(char_start, int)
            and isinstance(char_end, int)
            and 0 <= char_start < char_end <= len(content)
            and (char_end - char_start) <= _MAX_PLAUSIBLE_CHUNK
        ):
            return content[char_start:char_end]

        logger.warning(
            "stale_chunk_offsets",
            chunk_id=sr.chunk_id,
            char_start=char_start,
            char_end=char_end,
            doc_length=len(content),
        )
        if isinstance(char_start, int) and 0 <= char_start < len(content):
            return content[char_start : char_start + _FALLBACK_WINDOW]
        return content[:_FALLBACK_WINDOW]

    async def search_async(
        self,
        query: str,
        num_results: int,
        db_filter: str,
        session_id: str | None = None,
        feedback_id: str | None = None,
    ) -> tuple[str, str | None, str | None]:
        """
        Async search handler.

        Args:
            query: Search query.
            num_results: Number of results to return.
            db_filter: Database filter ("All" for no filter).
            session_id: Per-browser-session feedback session id (gr.State).
            feedback_id: Feedback id of the previous search (gr.State).

        Returns:
            (formatted results, session_id, feedback_id) — the ids flow back
            into gr.State so concurrent users don't share feedback state.
        """
        if not query.strip():
            return "Please enter a search query.", session_id, feedback_id

        # Apply filter
        source_filter = None if db_filter == "All" else db_filter
        k = int(num_results)

        # Over-fetch candidates: reranking and dedup both need slack
        multiplier = (
            self.config.reranking.candidate_multiplier
            if self.reranker
            else _DEDUP_CANDIDATE_MULTIPLIER
        )
        candidates = self.retriever.search_candidates(
            query=query,
            n_results=k * multiplier,
            source_db_filter=source_filter,
        )

        if not candidates:
            return "No results found for your query.", session_id, feedback_id

        # Fetch parent documents (parallel, per-fetch error isolation)
        fetched = await self.parent_fetcher.fetch_documents(candidates)
        found = [r for r in fetched if r.parent_document]
        if len(found) < len(fetched):
            logger.warning(
                "parent_fetch_failures",
                failed=len(fetched) - len(found),
                total=len(fetched),
            )
        if not found:
            return (
                "No results found: matching documents could not be retrieved "
                "from the source databases.",
                session_id,
                feedback_id,
            )

        # Rerank against the recovered chunk texts
        if self.reranker:
            chunk_texts = [self._recover_chunk_text(r) for r in found]
            items = [{"index": i} for i in range(len(found))]
            reranked = self.reranker.rerank(
                query=query,
                results=items,
                documents=chunk_texts,
                top_k=len(found),
            )
            ordered = []
            for item in reranked:
                result = found[item["index"]]
                result.search_result.metadata["rerank_score"] = item["rerank_score"]
                ordered.append(result)
            found = ordered

        # Dedup by parent document (post-rerank), keep top-k
        seen_docs = set()
        results_with_docs = []
        for result in found:
            sr = result.search_result
            doc_key = (sr.source_db, sr.parent_doc_id)
            if doc_key in seen_docs:
                continue
            seen_docs.add(doc_key)
            results_with_docs.append(result)
            if len(results_with_docs) >= k:
                break

        # Record search for feedback
        if self.feedback_collector:
            if session_id is None:
                session_id = self.feedback_collector.create_session()
            result_dicts = [
                {
                    "chunk_id": r.search_result.chunk_id,
                    "similarity_score": r.search_result.similarity_score,
                    "rerank_score": r.search_result.metadata.get("rerank_score"),
                    "parent_doc_id": r.search_result.parent_doc_id,
                    "source_db": r.search_result.source_db,
                    "source_table": r.search_result.source_table,
                }
                for r in results_with_docs
            ]
            feedback_id = self.feedback_collector.record_search(
                session_id=session_id,
                query=query,
                results=result_dicts,
            )

        # Format output
        output = f"## Search Results for: *{query}*\n\n"
        output += f"Found {len(results_with_docs)} relevant documents.\n\n"

        for i, result in enumerate(results_with_docs):
            output += format_result(result, i)

        return output, session_id, feedback_id

    def submit_thumbs_up(self, feedback_id: str | None) -> tuple[str, str | None]:
        """Handle thumbs up feedback."""
        if not self.feedback_collector or not feedback_id:
            return "No active search to provide feedback on.", feedback_id

        self.feedback_collector.submit_feedback(
            feedback_id=feedback_id,
            thumbs_up=True,
        )
        return "✅ Thank you for your positive feedback!", None

    def submit_thumbs_down(self, feedback_id: str | None) -> tuple[str, str | None]:
        """Handle thumbs down feedback."""
        if not self.feedback_collector or not feedback_id:
            return "No active search to provide feedback on.", feedback_id

        self.feedback_collector.submit_feedback(
            feedback_id=feedback_id,
            thumbs_up=False,
        )
        return "✅ Thank you for your feedback. We'll work on improving results!", None

    def submit_detailed_feedback(
        self, rating: float, comment: str, feedback_id: str | None
    ) -> tuple[str, str | None]:
        """Handle detailed feedback submission."""
        if not self.feedback_collector or not feedback_id:
            return "No active search to provide feedback on.", feedback_id

        self.feedback_collector.submit_feedback(
            feedback_id=feedback_id,
            rating=int(rating),
            comment=comment,
        )
        return "✅ Thank you for your detailed feedback!", None

    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface.

        Returns:
            Gradio Blocks interface.
        """
        available_databases = self.retriever.get_available_databases()

        with gr.Blocks(
            title=self.config.gradio.title,
            theme=gr.themes.Soft(),
        ) as app:
            gr.Markdown(f"# {self.config.gradio.title}")
            gr.Markdown(self.config.gradio.description)

            # Per-browser-session feedback state (instance attributes would
            # be shared — and clobbered — across concurrent users)
            session_state = gr.State(None)
            feedback_state = gr.State(None)

            with gr.Row():
                with gr.Column(scale=3):
                    query_input = gr.Textbox(
                        label="Search Query",
                        placeholder="Enter your search query...",
                        lines=2,
                    )

                with gr.Column(scale=1):
                    num_results = gr.Slider(
                        minimum=1,
                        maximum=self.config.max_k,
                        value=self.config.default_k,
                        step=1,
                        label="Number of Results",
                    )

                    db_filter = gr.Dropdown(
                        choices=["All"] + available_databases,
                        value="All",
                        label="Filter by Database",
                    )

            search_btn = gr.Button("Search", variant="primary")

            results_output = gr.Markdown(
                label="Results",
                value="Enter a query and click Search to find relevant documents.",
            )

            # Feedback UI (only if feedback collector is enabled)
            if self.feedback_collector and self.config.feedback.enabled:
                with gr.Group():
                    gr.Markdown("### Was this search helpful?")
                    with gr.Row():
                        thumbs_up_btn = gr.Button("👍 Yes", variant="secondary", size="sm")
                        thumbs_down_btn = gr.Button("👎 No", variant="secondary", size="sm")

                    with gr.Accordion("Optional: Detailed Feedback", open=False):
                        rating_slider = gr.Slider(
                            minimum=1,
                            maximum=5,
                            value=3,
                            step=1,
                            label="Rating (1-5)",
                        )
                        feedback_text = gr.Textbox(
                            label="Comments",
                            placeholder="What could we improve?",
                            lines=2,
                        )
                        submit_feedback_btn = gr.Button("Submit Detailed Feedback", variant="primary")

                    feedback_status = gr.Markdown("")

                    # Connect feedback handlers
                    thumbs_up_btn.click(
                        fn=self.submit_thumbs_up,
                        inputs=[feedback_state],
                        outputs=[feedback_status, feedback_state],
                    )
                    thumbs_down_btn.click(
                        fn=self.submit_thumbs_down,
                        inputs=[feedback_state],
                        outputs=[feedback_status, feedback_state],
                    )
                    submit_feedback_btn.click(
                        fn=self.submit_detailed_feedback,
                        inputs=[rating_slider, feedback_text, feedback_state],
                        outputs=[feedback_status, feedback_state],
                    )

            # Connect handlers (Gradio supports async fns directly)
            search_inputs = [query_input, num_results, db_filter, session_state, feedback_state]
            search_outputs = [results_output, session_state, feedback_state]
            search_btn.click(
                fn=self.search_async,
                inputs=search_inputs,
                outputs=search_outputs,
            )

            # Also search on Enter
            query_input.submit(
                fn=self.search_async,
                inputs=search_inputs,
                outputs=search_outputs,
            )

            gr.Markdown(
                """
                ---
                **About:** This search interface uses semantic embeddings to find
                relevant documents across your enterprise databases. Results are
                ranked by similarity to your query.
                """
            )

        self._app = app
        return app

    def launch(
        self,
        host: str | None = None,
        port: int | None = None,
        share: bool | None = None,
    ) -> None:
        """
        Launch the Gradio app.

        Args:
            host: Server host (uses config default if None).
            port: Server port (uses config default if None).
            share: Whether to create public link (uses config default if None).
        """
        if self._app is None:
            self.create_interface()

        if self._app is None:
            raise RuntimeError("Failed to create Gradio interface")
        self._app.launch(
            server_name=host or self.config.gradio.host,
            server_port=port or self.config.gradio.port,
            share=share if share is not None else self.config.gradio.share,
        )


def _warn_on_model_version_mismatch(
    chromadb_client: ChromaDBClient,
    embedding_manager: EmbeddingModelManager,
) -> None:
    """Warn if indexed chunks were embedded with a different model.

    Query vectors from a different model than the index are meaningless —
    the collection must be re-ingested after a model retrain.
    """
    try:
        results = chromadb_client.collection.get(limit=100, include=["metadatas"])
        indexed_versions = {
            m["embedding_model_version"]
            for m in (results.get("metadatas") or [])
            if m and m.get("embedding_model_version")
        }
        loaded = embedding_manager.model_version
        stale = indexed_versions - {loaded}
        if stale:
            logger.warning(
                "embedding_model_version_mismatch",
                indexed_with=sorted(stale),
                loaded=loaded,
                hint="re-run program3 ingestion to re-embed with the current model",
            )
    except Exception as e:
        logger.warning("model_version_check_failed", error=str(e))


def create_search_app(
    settings: Settings,
    use_mock_fetcher: bool = False,
    test_mode: bool = False,
    chromadb_client: ChromaDBClient | None = None,
) -> SearchApp:
    """
    Create a search app from settings.

    Args:
        settings: Application settings.
        use_mock_fetcher: If True, use mock parent document fetcher.
        test_mode: If True, use test mode for feedback collector.
        chromadb_client: Optional already-connected client to reuse.

    Returns:
        Configured SearchApp instance.
    """
    # Initialize components
    embedding_manager = EmbeddingModelManager(settings.embedding)
    embedding_manager.load_model()

    if chromadb_client is None:
        chromadb_client = ChromaDBClient(settings.chromadb)
        chromadb_client.connect()
    chromadb_client.get_or_create_collection()

    _warn_on_model_version_mismatch(chromadb_client, embedding_manager)

    retriever = SemanticRetriever(
        embedding_manager=embedding_manager,
        chromadb_client=chromadb_client,
    )

    if use_mock_fetcher:
        parent_fetcher: ParentDocumentFetcher | MockParentDocumentFetcher = (
            MockParentDocumentFetcher()
        )
    else:
        # Connection pools initialize lazily on the first fetch
        db_manager = DatabaseConnectionManager(settings.databases)
        parent_fetcher = ParentDocumentFetcher(db_manager=db_manager, settings=settings)

    # Reranker runs after the parent-document fetch (the index stores no text)
    reranker = None
    reranking = settings.search.reranking
    if reranking.enabled and reranking.model:
        reranker = SearchReranker(reranking.model)
        logger.info("reranking_enabled", model=reranking.model)

    # Initialize feedback collector if enabled
    feedback_collector = None
    if settings.search.feedback.enabled:
        feedback_collector = FeedbackCollector(
            feedback_dir=settings.search.feedback.feedback_dir,
            test_mode=test_mode,
        )

    return SearchApp(
        retriever=retriever,
        parent_fetcher=parent_fetcher,
        config=settings.search,
        feedback_collector=feedback_collector,
        reranker=reranker,
    )
