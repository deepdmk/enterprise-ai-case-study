"""Tests for the semantic retriever (candidate flow, no reranking)."""

from unittest.mock import MagicMock

import pytest

from src.program4_search.retriever import SearchResult, SemanticRetriever
from src.shared.chromadb_client import QueryResult


def make_retriever(query_result: QueryResult | None = None) -> SemanticRetriever:
    """Build a retriever with mocked embedding manager and chromadb client."""
    embedding_manager = MagicMock()
    embedding_manager.encode_single.return_value = [0.1, 0.2, 0.3]

    chromadb_client = MagicMock()
    if query_result is not None:
        chromadb_client.query.return_value = query_result

    return SemanticRetriever(
        embedding_manager=embedding_manager,
        chromadb_client=chromadb_client,
    )


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_basic_creation(self):
        result = SearchResult(
            chunk_id="chunk_001",
            similarity_score=0.95,
            parent_doc_id="doc_001",
            chunk_index=0,
            source_db="test_db",
            source_table="test_table",
            metadata={"key": "value"},
        )
        assert result.chunk_id == "chunk_001"
        assert result.similarity_score == 0.95
        assert result.metadata == {"key": "value"}

    def test_repr(self):
        result = SearchResult(
            chunk_id="chunk_001",
            similarity_score=0.9512,
            parent_doc_id="doc_001",
            chunk_index=2,
            source_db="db",
            source_table="table",
            metadata={},
        )
        repr_str = repr(result)
        assert "doc_001" in repr_str
        assert "chunk=2" in repr_str
        assert "0.9512" in repr_str


class TestSearchCandidates:
    """Tests for the raw candidate search."""

    def test_similarity_is_one_minus_distance(self):
        """ChromaDB cosine distance is 1 - cos_sim, so similarity = 1 - distance."""
        retriever = make_retriever(
            QueryResult(
                ids=["c1", "c2", "c3"],
                distances=[0.0, 0.2, 1.0],
                metadatas=[{}, {}, {}],
            )
        )

        results = retriever.search_candidates("query", n_results=3)

        assert results[0].similarity_score == pytest.approx(1.0)
        assert results[1].similarity_score == pytest.approx(0.8)
        assert results[2].similarity_score == pytest.approx(0.0)

    def test_metadata_passthrough(self):
        retriever = make_retriever(
            QueryResult(
                ids=["c1"],
                distances=[0.1],
                metadatas=[
                    {
                        "parent_doc_id": "doc_001",
                        "chunk_index": 3,
                        "source_db": "db_a",
                        "source_table": "projects",
                        "char_start": 10,
                        "char_end": 200,
                    }
                ],
            )
        )

        results = retriever.search_candidates("query", n_results=1)

        assert len(results) == 1
        r = results[0]
        assert r.parent_doc_id == "doc_001"
        assert r.chunk_index == 3
        assert r.source_db == "db_a"
        assert r.source_table == "projects"
        assert r.metadata["char_start"] == 10
        assert r.metadata["char_end"] == 200

    def test_source_db_filter_builds_where(self):
        retriever = make_retriever(QueryResult(ids=[], distances=[], metadatas=[]))

        retriever.search_candidates("query", n_results=5, source_db_filter="db_a")

        _, kwargs = retriever.chromadb_client.query.call_args
        assert kwargs["where"] == {"source_db": "db_a"}
        assert kwargs["n_results"] == 5

    def test_no_filter_passes_none(self):
        retriever = make_retriever(QueryResult(ids=[], distances=[], metadatas=[]))

        retriever.search_candidates("query", n_results=5)

        _, kwargs = retriever.chromadb_client.query.call_args
        assert kwargs["where"] is None

    def test_no_documents_requested(self):
        """The index is metadata-only; the retriever must never ask for documents."""
        retriever = make_retriever(QueryResult(ids=[], distances=[], metadatas=[]))

        retriever.search_candidates("query", n_results=5)

        _, kwargs = retriever.chromadb_client.query.call_args
        assert "documents" not in kwargs["include"]

    def test_search_wrapper_matches_candidates(self):
        retriever = make_retriever(
            QueryResult(ids=["c1"], distances=[0.4], metadatas=[{}])
        )

        results = retriever.search("query", k=1)

        assert len(results) == 1
        assert results[0].similarity_score == pytest.approx(0.6)


class TestGetAvailableDatabases:
    """Tests for source-database discovery (feeds the UI dropdown)."""

    def test_reads_source_db_metadata(self):
        retriever = make_retriever()
        retriever.chromadb_client.iter_metadata.return_value = iter(
            [
                ("c1", {"source_db": "db_b"}),
                ("c2", {"source_db": "db_a"}),
                ("c3", {"source_db": "db_a"}),
            ]
        )

        assert retriever.get_available_databases() == ["db_a", "db_b"]

    def test_returns_empty_on_error(self):
        retriever = make_retriever()
        retriever.chromadb_client.iter_metadata.side_effect = RuntimeError("down")

        assert retriever.get_available_databases() == []

    def test_ignores_missing_metadata(self):
        retriever = make_retriever()
        retriever.chromadb_client.iter_metadata.return_value = iter(
            [("c1", None), ("c2", {"other_key": "x"})]
        )

        assert retriever.get_available_databases() == []
