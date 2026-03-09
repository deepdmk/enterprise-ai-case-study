"""
Gradio Search Interface.

Provides a chat-style interface for semantic document search
with parent document retrieval.
"""

import asyncio

import gradio as gr

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import SearchConfig, Settings
from habitat_logging import get_logger

from src.shared.chromadb_client import ChromaDBClient
from src.shared.embedding_model import EmbeddingModelManager

from .feedback import FeedbackCollector
from .parent_document_fetcher import (
    MockParentDocumentFetcher,
    ParentDocumentFetcher,
    SearchResultWithDocument,
)
from .retriever import SemanticRetriever

logger = get_logger(__name__)


def format_result(result: SearchResultWithDocument, index: int) -> str:
    """Format a single search result for display."""
    sr = result.search_result
    doc = result.parent_document

    output = f"### Result {index + 1}\n\n"
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
    ):
        """
        Initialize the search app.

        Args:
            retriever: Semantic retriever.
            parent_fetcher: Parent document fetcher.
            config: Search configuration.
            feedback_collector: Optional feedback collector for RLHF.
        """
        self.retriever = retriever
        self.parent_fetcher = parent_fetcher
        self.config = config
        self.feedback_collector = feedback_collector
        self._app: gr.Blocks | None = None

        # Feedback tracking
        self._current_feedback_id: str | None = None
        self._current_session_id: str | None = None
        if self.feedback_collector:
            self._current_session_id = self.feedback_collector.create_session()

    async def search_async(
        self,
        query: str,
        num_results: int,
        db_filter: str,
    ) -> str:
        """
        Async search handler.

        Args:
            query: Search query.
            num_results: Number of results to return.
            db_filter: Database filter ("All" for no filter).

        Returns:
            Formatted search results.
        """
        if not query.strip():
            return "Please enter a search query."

        # Apply filter
        source_filter = None if db_filter == "All" else db_filter

        # Search
        results = self.retriever.search_with_deduplication(
            query=query,
            k=num_results,
            source_db_filter=source_filter,
        )

        if not results:
            return "No results found for your query."

        # Fetch parent documents
        results_with_docs = await self.parent_fetcher.fetch_documents(results)

        # Record search for feedback
        if self.feedback_collector and self._current_session_id:
            # Convert results to dicts for storage
            result_dicts = [
                {
                    "chunk_id": r.chunk_id,
                    "similarity_score": r.similarity_score,
                    "parent_doc_id": r.parent_doc_id,
                    "source_db": r.source_db,
                    "source_table": r.source_table,
                }
                for r in results
            ]
            self._current_feedback_id = self.feedback_collector.record_search(
                session_id=self._current_session_id,
                query=query,
                results=result_dicts,
            )

        # Format output
        output = f"## Search Results for: *{query}*\n\n"
        output += f"Found {len(results_with_docs)} relevant documents.\n\n"

        for i, result in enumerate(results_with_docs):
            output += format_result(result, i)

        return output

    def search(
        self,
        query: str,
        num_results: int,
        db_filter: str,
    ) -> str:
        """
        Sync search handler for Gradio.

        Wraps the async search in an event loop.
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            self.search_async(query, num_results, db_filter)
        )

    def submit_thumbs_up(self) -> str:
        """Handle thumbs up feedback."""
        if not self.feedback_collector or not self._current_feedback_id:
            return "No active search to provide feedback on."

        self.feedback_collector.submit_feedback(
            feedback_id=self._current_feedback_id,
            thumbs_up=True,
        )
        self._current_feedback_id = None
        return "✅ Thank you for your positive feedback!"

    def submit_thumbs_down(self) -> str:
        """Handle thumbs down feedback."""
        if not self.feedback_collector or not self._current_feedback_id:
            return "No active search to provide feedback on."

        self.feedback_collector.submit_feedback(
            feedback_id=self._current_feedback_id,
            thumbs_up=False,
        )
        self._current_feedback_id = None
        return "✅ Thank you for your feedback. We'll work on improving results!"

    def submit_detailed_feedback(self, rating: float, comment: str) -> str:
        """Handle detailed feedback submission."""
        if not self.feedback_collector or not self._current_feedback_id:
            return "No active search to provide feedback on."

        self.feedback_collector.submit_feedback(
            feedback_id=self._current_feedback_id,
            rating=int(rating),
            comment=comment,
        )
        self._current_feedback_id = None
        return "✅ Thank you for your detailed feedback!"

    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface.

        Returns:
            Gradio Blocks interface.
        """
        with gr.Blocks(
            title=self.config.gradio.title,
            theme=gr.themes.Soft(),
        ) as app:
            gr.Markdown(f"# {self.config.gradio.title}")
            gr.Markdown(self.config.gradio.description)

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
                        choices=["All", "database_1", "database_2", "database_3"],
                        value="All",
                        label="Filter by Database",
                    )

            search_btn = gr.Button("Search", variant="primary")

            results_output = gr.Markdown(
                label="Results",
                value="Enter a query and click Search to find relevant documents.",
            )

            # Feedback UI (only if feedback collector is enabled)
            feedback_status = None
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
                        outputs=feedback_status,
                    )
                    thumbs_down_btn.click(
                        fn=self.submit_thumbs_down,
                        outputs=feedback_status,
                    )
                    submit_feedback_btn.click(
                        fn=self.submit_detailed_feedback,
                        inputs=[rating_slider, feedback_text],
                        outputs=feedback_status,
                    )

            # Connect handlers
            search_btn.click(
                fn=self.search,
                inputs=[query_input, num_results, db_filter],
                outputs=results_output,
            )

            # Also search on Enter
            query_input.submit(
                fn=self.search,
                inputs=[query_input, num_results, db_filter],
                outputs=results_output,
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

        assert self._app is not None, "Failed to create Gradio interface"
        self._app.launch(
            server_name=host or self.config.gradio.host,
            server_port=port or self.config.gradio.port,
            share=share if share is not None else self.config.gradio.share,
        )


def create_search_app(
    settings: Settings,
    use_mock_fetcher: bool = False,
    test_mode: bool = False,
) -> SearchApp:
    """
    Create a search app from settings.

    Args:
        settings: Application settings.
        use_mock_fetcher: If True, use mock parent document fetcher.
        test_mode: If True, use test mode for feedback collector.

    Returns:
        Configured SearchApp instance.
    """
    # Initialize components
    embedding_manager = EmbeddingModelManager(settings.embedding)
    embedding_manager.load_model()

    chromadb_client = ChromaDBClient(settings.chromadb)
    chromadb_client.connect()
    chromadb_client.get_or_create_collection()

    retriever = SemanticRetriever(
        embedding_manager=embedding_manager,
        chromadb_client=chromadb_client,
        reranking_config=settings.search.reranking,
    )

    if use_mock_fetcher:
        parent_fetcher = MockParentDocumentFetcher()
    else:
        # Would need to initialize db_manager
        # For now, use mock
        parent_fetcher = MockParentDocumentFetcher()

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
    )
