"""Tests for parent document fetching and combined-text reconstruction."""

from unittest.mock import AsyncMock, MagicMock

from config.settings import DatabaseConfig, Settings, TableConfig
from src.program4_search.parent_document_fetcher import ParentDocumentFetcher
from src.program4_search.retriever import SearchResult

TABLE = TableConfig(
    name="projects",
    text_columns=["title", "summary", "body"],
    id_column="id",
    timestamp_column="updated_at",
    additional_metadata=["region"],
)


def make_fetcher(record: dict | None) -> ParentDocumentFetcher:
    """Fetcher with a mocked db manager returning the given record."""
    settings = Settings()
    settings.databases = {"db_a": DatabaseConfig(name="db_a", tables=[TABLE])}

    db_manager = MagicMock()
    db_manager.initialize = AsyncMock()
    db_manager.get_record_by_id = AsyncMock(return_value=record)

    return ParentDocumentFetcher(db_manager=db_manager, settings=settings)


def make_search_result(**metadata) -> SearchResult:
    return SearchResult(
        chunk_id="db_a_1_chunk_0",
        similarity_score=0.9,
        parent_doc_id="1",
        chunk_index=0,
        source_db="db_a",
        source_table="projects",
        metadata=metadata,
    )


class TestCombinedTextReconstruction:
    """The Python reconstruction must mirror ingestion's SQL expression:
    COALESCE(col::text, '') for every column, joined with single spaces.
    Otherwise the stored char offsets drift."""

    async def test_null_column_still_contributes_separator(self):
        record = {"id": 1, "title": "Hello", "summary": None, "body": "World"}
        fetcher = make_fetcher(record)

        doc = await fetcher.fetch_document(make_search_result())

        # SQL: 'Hello' || ' ' || '' || ' ' || 'World' -> double space
        assert doc.content == "Hello  World"

    async def test_all_columns_present(self):
        record = {"id": 1, "title": "A", "summary": "B", "body": "C"}
        fetcher = make_fetcher(record)

        doc = await fetcher.fetch_document(make_search_result())

        assert doc.content == "A B C"

    async def test_offsets_computed_on_sql_text_slice_correctly(self):
        """End-to-end offset invariant: slicing the reconstructed content at
        offsets computed from the SQL-style combined text recovers the chunk."""
        record = {"id": 1, "title": "Header text", "summary": None, "body": "Body text here"}
        sql_combined = " ".join(
            "" if record[col] is None else str(record[col]) for col in TABLE.text_columns
        )
        char_start = sql_combined.find("Body")
        char_end = char_start + len("Body text")

        fetcher = make_fetcher(record)
        doc = await fetcher.fetch_document(make_search_result())

        assert doc.content[char_start:char_end] == "Body text"


class TestFetchDocuments:
    """Tests for the parallel multi-fetch."""

    async def test_missing_document_reported_not_raised(self):
        fetcher = make_fetcher(None)

        results = await fetcher.fetch_documents([make_search_result()])

        assert len(results) == 1
        assert results[0].parent_document is None
        assert results[0].error == "Document not found"

    async def test_fetch_error_isolated_per_document(self):
        record = {"id": 1, "title": "OK", "summary": "fine", "body": "good"}
        fetcher = make_fetcher(record)
        fetcher.db_manager.get_record_by_id = AsyncMock(
            side_effect=[RuntimeError("connection lost"), record]
        )

        results = await fetcher.fetch_documents(
            [make_search_result(), make_search_result()]
        )

        assert results[0].parent_document is None
        assert results[1].parent_document is not None

    async def test_initializes_db_manager_lazily(self):
        fetcher = make_fetcher(None)

        await fetcher.fetch_documents([make_search_result()])

        fetcher.db_manager.initialize.assert_awaited_once()
