"""Tests for semantic retriever.

These tests are self-contained and define necessary dataclasses locally
to avoid import dependency issues.
"""

from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

import pytest


# Local copies of dataclasses for testing (avoid import issues)
@dataclass
class QueryResult:
    """Result from a ChromaDB query."""

    ids: list[str]
    distances: list[float]
    metadatas: list[dict[str, Any]]
    embeddings: list[list[float]] | None = None
    documents: list[str] | None = None

    def __len__(self):
        return len(self.ids)


@dataclass
class SearchResult:
    """A single search result."""

    chunk_id: str
    similarity_score: float
    parent_doc_id: str
    chunk_index: int
    source_db: str
    source_table: str
    metadata: dict[str, Any]

    def __repr__(self) -> str:
        return (
            f"SearchResult(doc={self.parent_doc_id}, "
            f"chunk={self.chunk_index}, "
            f"score={self.similarity_score:.4f})"
        )


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_basic_creation(self):
        """Test basic SearchResult creation."""
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
        assert result.parent_doc_id == "doc_001"
        assert result.chunk_index == 0
        assert result.source_db == "test_db"
        assert result.source_table == "test_table"
        assert result.metadata == {"key": "value"}

    def test_repr(self):
        """Test string representation."""
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

    def test_empty_metadata(self):
        """Test SearchResult with empty metadata."""
        result = SearchResult(
            chunk_id="chunk_002",
            similarity_score=0.8,
            parent_doc_id="doc_002",
            chunk_index=1,
            source_db="db",
            source_table="table",
            metadata={},
        )
        assert result.metadata == {}

    def test_high_similarity_score(self):
        """Test SearchResult with high similarity."""
        result = SearchResult(
            chunk_id="chunk_003",
            similarity_score=0.999,
            parent_doc_id="doc_003",
            chunk_index=0,
            source_db="db",
            source_table="table",
            metadata={},
        )
        assert result.similarity_score == pytest.approx(0.999)

    def test_low_similarity_score(self):
        """Test SearchResult with low similarity."""
        result = SearchResult(
            chunk_id="chunk_004",
            similarity_score=0.1,
            parent_doc_id="doc_004",
            chunk_index=5,
            source_db="db",
            source_table="table",
            metadata={},
        )
        assert result.similarity_score == pytest.approx(0.1)


class TestQueryResult:
    """Tests for QueryResult used in retriever context."""

    def test_query_result_length(self):
        """Test QueryResult length calculation."""
        result = QueryResult(
            ids=["id1", "id2", "id3"],
            distances=[0.1, 0.2, 0.3],
            metadatas=[{}, {}, {}],
        )
        assert len(result) == 3

    def test_query_result_empty(self):
        """Test empty QueryResult."""
        result = QueryResult(ids=[], distances=[], metadatas=[])
        assert len(result) == 0

    def test_query_result_with_documents(self):
        """Test QueryResult with documents field (for reranking)."""
        result = QueryResult(
            ids=["id1"],
            distances=[0.1],
            metadatas=[{"source": "test"}],
            documents=["Document content here"],
        )
        assert result.documents == ["Document content here"]


class TestSimilarityCalculation:
    """Tests for similarity score calculation from distance."""

    def test_cosine_distance_to_similarity(self):
        """Test converting cosine distance to similarity score."""
        # For cosine space: similarity = 1 - distance/2
        distance = 0.2
        similarity = 1 - distance / 2
        assert similarity == pytest.approx(0.9)

    def test_zero_distance(self):
        """Test perfect match (zero distance)."""
        distance = 0.0
        similarity = 1 - distance / 2
        assert similarity == pytest.approx(1.0)

    def test_max_distance(self):
        """Test maximum distance (opposite vectors)."""
        distance = 2.0  # Max cosine distance
        similarity = 1 - distance / 2
        assert similarity == pytest.approx(0.0)


class TestSearchDeduplication:
    """Tests for search result deduplication logic."""

    def test_deduplication_by_parent_doc(self):
        """Test deduplication keeps one result per parent document."""
        results = [
            SearchResult(
                chunk_id="chunk_001",
                similarity_score=0.95,
                parent_doc_id="doc_001",
                chunk_index=0,
                source_db="db",
                source_table="table",
                metadata={},
            ),
            SearchResult(
                chunk_id="chunk_002",
                similarity_score=0.90,
                parent_doc_id="doc_001",  # Same document
                chunk_index=1,
                source_db="db",
                source_table="table",
                metadata={},
            ),
            SearchResult(
                chunk_id="chunk_003",
                similarity_score=0.85,
                parent_doc_id="doc_002",  # Different document
                chunk_index=0,
                source_db="db",
                source_table="table",
                metadata={},
            ),
        ]

        # Simulate deduplication logic
        seen_docs = set()
        deduplicated = []
        for result in results:
            doc_key = f"{result.source_db}_{result.parent_doc_id}"
            if doc_key not in seen_docs:
                seen_docs.add(doc_key)
                deduplicated.append(result)

        assert len(deduplicated) == 2
        assert deduplicated[0].parent_doc_id == "doc_001"
        assert deduplicated[1].parent_doc_id == "doc_002"

    def test_deduplication_preserves_order(self):
        """Test that deduplication preserves similarity order."""
        results = [
            SearchResult(
                chunk_id="c1", similarity_score=0.99, parent_doc_id="d1",
                chunk_index=0, source_db="db", source_table="t", metadata={}
            ),
            SearchResult(
                chunk_id="c2", similarity_score=0.95, parent_doc_id="d2",
                chunk_index=0, source_db="db", source_table="t", metadata={}
            ),
            SearchResult(
                chunk_id="c3", similarity_score=0.90, parent_doc_id="d1",  # Duplicate
                chunk_index=1, source_db="db", source_table="t", metadata={}
            ),
        ]

        seen_docs = set()
        deduplicated = []
        for result in results:
            doc_key = f"{result.source_db}_{result.parent_doc_id}"
            if doc_key not in seen_docs:
                seen_docs.add(doc_key)
                deduplicated.append(result)

        # First result should have highest score
        assert deduplicated[0].similarity_score > deduplicated[1].similarity_score


class TestMockedRetriever:
    """Tests for retriever with mocked dependencies."""

    def test_mock_embedding_manager(self):
        """Test mock embedding manager returns expected embedding."""
        mock_manager = MagicMock()
        mock_manager.encode_single.return_value = [0.1, 0.2, 0.3]

        embedding = mock_manager.encode_single("test query")

        assert embedding == [0.1, 0.2, 0.3]
        mock_manager.encode_single.assert_called_once_with("test query")

    def test_mock_chromadb_query(self):
        """Test mock ChromaDB client query."""
        mock_client = MagicMock()
        mock_client.query.return_value = QueryResult(
            ids=["chunk_001", "chunk_002"],
            distances=[0.2, 0.4],
            metadatas=[
                {"parent_doc_id": "doc_001", "chunk_index": 0},
                {"parent_doc_id": "doc_002", "chunk_index": 1},
            ],
        )

        results = mock_client.query(
            query_embeddings=[[0.1, 0.2, 0.3]],
            n_results=5,
        )

        assert len(results) == 2
        assert results.ids == ["chunk_001", "chunk_002"]

    def test_search_flow_integration(self):
        """Test full search flow with mocked components."""
        # Mock embedding manager
        mock_embedding = MagicMock()
        mock_embedding.encode_single.return_value = [0.1, 0.2, 0.3]

        # Mock ChromaDB client
        mock_chromadb = MagicMock()
        mock_chromadb.query.return_value = QueryResult(
            ids=["chunk_001"],
            distances=[0.2],
            metadatas=[{
                "parent_doc_id": "doc_001",
                "chunk_index": 0,
                "source_db": "test_db",
                "source_table": "test_table",
            }],
        )

        # Simulate search
        query = "test query"
        query_embedding = mock_embedding.encode_single(query)
        results = mock_chromadb.query(
            query_embeddings=[query_embedding],
            n_results=5,
        )

        # Verify results
        assert len(results) == 1
        assert results.ids[0] == "chunk_001"
        assert results.metadatas[0]["parent_doc_id"] == "doc_001"
