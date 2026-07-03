"""Tests for the SearchApp orchestration (rerank-after-fetch flow)."""

from unittest.mock import AsyncMock, MagicMock

from src.program4_search.gradio_app import SearchApp, _FALLBACK_WINDOW
from src.program4_search.parent_document_fetcher import (
    ParentDocument,
    SearchResultWithDocument,
)
from src.program4_search.retriever import SearchResult


def make_result(
    doc_id: str,
    content: str,
    similarity: float = 0.9,
    **metadata,
) -> SearchResultWithDocument:
    sr = SearchResult(
        chunk_id=f"db_a_{doc_id}_chunk_0",
        similarity_score=similarity,
        parent_doc_id=doc_id,
        chunk_index=0,
        source_db="db_a",
        source_table="projects",
        metadata=metadata,
    )
    doc = ParentDocument(
        doc_id=doc_id,
        content=content,
        source_db="db_a",
        source_table="projects",
        metadata={},
        matched_chunk_index=0,
        similarity_score=similarity,
    )
    return SearchResultWithDocument(search_result=sr, parent_document=doc)


def make_app(candidates=None, fetched=None, reranker=None) -> SearchApp:
    retriever = MagicMock()
    retriever.search_candidates.return_value = candidates or []

    parent_fetcher = MagicMock()
    parent_fetcher.fetch_documents = AsyncMock(return_value=fetched or [])

    config = MagicMock()
    config.reranking.candidate_multiplier = 3

    return SearchApp(
        retriever=retriever,
        parent_fetcher=parent_fetcher,
        config=config,
        feedback_collector=None,
        reranker=reranker,
    )


class TestRecoverChunkText:
    """Tests for chunk-text recovery via stored char offsets."""

    def test_valid_offsets_slice_exactly(self):
        app = make_app()
        content = "0123456789" * 20
        result = make_result("d1", content, char_start=10, char_end=30)

        assert app._recover_chunk_text(result) == content[10:30]

    def test_out_of_bounds_end_falls_back_to_window(self):
        """Stale offsets (document shrank) -> window from char_start."""
        app = make_app()
        content = "short document content"
        result = make_result("d1", content, char_start=6, char_end=5000)

        recovered = app._recover_chunk_text(result)

        assert recovered == content[6 : 6 + _FALLBACK_WINDOW]

    def test_missing_offsets_fall_back_to_head(self):
        app = make_app()
        content = "x" * 3000
        result = make_result("d1", content)  # no char_start/char_end

        assert app._recover_chunk_text(result) == content[:_FALLBACK_WINDOW]

    def test_start_beyond_document_falls_back_to_head(self):
        app = make_app()
        content = "tiny"
        result = make_result("d1", content, char_start=500, char_end=600)

        assert app._recover_chunk_text(result) == content


class TestSearchAsync:
    """Tests for the end-to-end search orchestration."""

    async def test_dedups_by_parent_doc_and_truncates_to_k(self):
        sr_list = [MagicMock()] * 4  # candidates (content unused by mock fetcher)
        fetched = [
            make_result("d1", "doc one content", similarity=0.9),
            make_result("d1", "doc one content", similarity=0.85),  # dup parent
            make_result("d2", "doc two content", similarity=0.8),
            make_result("d3", "doc three content", similarity=0.7),
        ]
        app = make_app(candidates=sr_list, fetched=fetched)

        output, _, _ = await app.search_async("query", num_results=2, db_filter="All")

        assert "Found 2 relevant documents" in output
        assert "`d1`" in output
        assert "`d2`" in output
        assert "`d3`" not in output

    async def test_over_fetches_candidates(self):
        app = make_app(candidates=[], fetched=[])

        output, _, _ = await app.search_async("query", num_results=5, db_filter="All")

        _, kwargs = app.retriever.search_candidates.call_args
        assert kwargs["n_results"] == 15  # k * dedup multiplier
        assert "No results" in output

    async def test_reranker_reorders_results(self):
        fetched = [
            make_result("d1", "irrelevant text", similarity=0.9, char_start=0, char_end=15),
            make_result("d2", "highly relevant", similarity=0.8, char_start=0, char_end=15),
        ]
        reranker = MagicMock()

        def rerank(query, results, documents, top_k):
            # Score the second candidate higher
            results[0]["rerank_score"] = 0.1
            results[1]["rerank_score"] = 0.9
            return sorted(results, key=lambda r: r["rerank_score"], reverse=True)

        reranker.rerank.side_effect = rerank
        app = make_app(candidates=[MagicMock()] * 2, fetched=fetched, reranker=reranker)

        output, _, _ = await app.search_async("query", num_results=2, db_filter="All")

        # d2 must now rank first
        assert output.index("`d2`") < output.index("`d1`")

    async def test_failed_fetches_dropped(self):
        good = make_result("d1", "content here")
        bad = SearchResultWithDocument(
            search_result=good.search_result,
            parent_document=None,
            error="Document not found",
        )
        app = make_app(candidates=[MagicMock()] * 2, fetched=[bad, good])

        output, _, _ = await app.search_async("query", num_results=5, db_filter="All")

        assert "Found 1 relevant documents" in output

    async def test_empty_query_short_circuits(self):
        app = make_app()

        output, _, _ = await app.search_async("   ", num_results=5, db_filter="All")

        assert output == "Please enter a search query."
        app.retriever.search_candidates.assert_not_called()

    async def test_feedback_session_created_lazily_per_state(self):
        fetched = [make_result("d1", "content")]
        app = make_app(candidates=[MagicMock()], fetched=fetched)
        app.feedback_collector = MagicMock()
        app.feedback_collector.create_session.return_value = "session-1"
        app.feedback_collector.record_search.return_value = "feedback-1"

        _, session_id, feedback_id = await app.search_async(
            "query", num_results=1, db_filter="All", session_id=None, feedback_id=None
        )

        assert session_id == "session-1"
        assert feedback_id == "feedback-1"

        # Existing session is reused, not recreated
        _, session_id2, _ = await app.search_async(
            "query", num_results=1, db_filter="All", session_id="session-1"
        )
        assert session_id2 == "session-1"
        app.feedback_collector.create_session.assert_called_once()
