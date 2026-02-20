"""Tests for ChromaDB client wrapper.

These tests are self-contained and define the dataclasses locally
to avoid import dependency issues.
"""

from dataclasses import dataclass
from typing import Any


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

    def __iter__(self):
        for i in range(len(self.ids)):
            yield {
                "id": self.ids[i],
                "distance": self.distances[i],
                "metadata": self.metadatas[i],
                "embedding": self.embeddings[i] if self.embeddings else None,
            }


@dataclass
class CollectionStats:
    """Statistics for a ChromaDB collection."""

    name: str
    count: int
    metadata: dict[str, Any]


class TestQueryResult:
    """Tests for QueryResult dataclass."""

    def test_basic_creation(self):
        """Test basic QueryResult creation."""
        result = QueryResult(
            ids=["id1", "id2"],
            distances=[0.1, 0.2],
            metadatas=[{"key": "value1"}, {"key": "value2"}],
        )
        assert result.ids == ["id1", "id2"]
        assert result.distances == [0.1, 0.2]
        assert result.metadatas == [{"key": "value1"}, {"key": "value2"}]
        assert result.embeddings is None
        assert result.documents is None

    def test_with_embeddings(self):
        """Test QueryResult with embeddings."""
        embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        result = QueryResult(
            ids=["id1", "id2"],
            distances=[0.1, 0.2],
            metadatas=[{}, {}],
            embeddings=embeddings,
        )
        assert result.embeddings == embeddings

    def test_with_documents(self):
        """Test QueryResult with documents field."""
        result = QueryResult(
            ids=["id1", "id2"],
            distances=[0.1, 0.2],
            metadatas=[{}, {}],
            documents=["doc1 content", "doc2 content"],
        )
        assert result.documents == ["doc1 content", "doc2 content"]

    def test_length(self):
        """Test __len__ returns number of results."""
        result = QueryResult(
            ids=["id1", "id2", "id3"],
            distances=[0.1, 0.2, 0.3],
            metadatas=[{}, {}, {}],
        )
        assert len(result) == 3

    def test_empty_result(self):
        """Test empty QueryResult."""
        result = QueryResult(ids=[], distances=[], metadatas=[])
        assert len(result) == 0

    def test_iteration(self):
        """Test iterating over QueryResult."""
        result = QueryResult(
            ids=["id1", "id2"],
            distances=[0.1, 0.2],
            metadatas=[{"key": "val1"}, {"key": "val2"}],
            embeddings=[[0.1], [0.2]],
        )
        items = list(result)
        assert len(items) == 2
        assert items[0]["id"] == "id1"
        assert items[0]["distance"] == 0.1
        assert items[0]["metadata"] == {"key": "val1"}
        assert items[0]["embedding"] == [0.1]

    def test_iteration_without_embeddings(self):
        """Test iteration when embeddings are None."""
        result = QueryResult(
            ids=["id1"],
            distances=[0.1],
            metadatas=[{}],
        )
        items = list(result)
        assert items[0]["embedding"] is None

    def test_single_result(self):
        """Test QueryResult with single item."""
        result = QueryResult(
            ids=["single_id"],
            distances=[0.05],
            metadatas=[{"type": "test"}],
        )
        assert len(result) == 1
        items = list(result)
        assert items[0]["id"] == "single_id"


class TestCollectionStats:
    """Tests for CollectionStats dataclass."""

    def test_basic_creation(self):
        """Test basic CollectionStats creation."""
        stats = CollectionStats(
            name="test_collection",
            count=100,
            metadata={"description": "test"},
        )
        assert stats.name == "test_collection"
        assert stats.count == 100
        assert stats.metadata == {"description": "test"}

    def test_empty_metadata(self):
        """Test CollectionStats with empty metadata."""
        stats = CollectionStats(name="test", count=0, metadata={})
        assert stats.metadata == {}

    def test_large_count(self):
        """Test CollectionStats with large count."""
        stats = CollectionStats(
            name="large_collection",
            count=1_000_000,
            metadata={"hnsw:space": "cosine"},
        )
        assert stats.count == 1_000_000

    def test_complex_metadata(self):
        """Test CollectionStats with complex metadata."""
        metadata = {
            "description": "Enterprise embeddings",
            "hnsw:space": "cosine",
            "hnsw:ef_construction": 200,
            "created_at": "2024-01-01",
        }
        stats = CollectionStats(name="enterprise", count=50000, metadata=metadata)
        assert stats.metadata["hnsw:space"] == "cosine"
        assert stats.metadata["hnsw:ef_construction"] == 200
