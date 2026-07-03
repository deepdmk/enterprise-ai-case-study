"""
Semantic Retriever.

Core retrieval logic using fine-tuned embeddings and ChromaDB.
"""

from dataclasses import dataclass
from typing import Any

from src.shared.path_config import configure_paths
configure_paths()

from phase0_infra.habitat_logging import get_logger

from src.shared.chromadb_client import ChromaDBClient
from src.shared.embedding_model import EmbeddingModelManager

logger = get_logger(__name__)


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


class SemanticRetriever:
    """
    Retrieves relevant chunks using semantic similarity search.

    Uses:
    - Fine-tuned embedding model to encode queries
    - ChromaDB for vector similarity search
    - Metadata for filtering and source attribution
    """

    def __init__(
        self,
        embedding_manager: EmbeddingModelManager,
        chromadb_client: ChromaDBClient,
    ):
        """
        Initialize the retriever.

        Args:
            embedding_manager: Embedding model manager.
            chromadb_client: ChromaDB client.
        """
        self.embedding_manager = embedding_manager
        self.chromadb_client = chromadb_client

    def search_candidates(
        self,
        query: str,
        n_results: int,
        source_db_filter: str | None = None,
    ) -> list[SearchResult]:
        """
        Vector search returning raw candidates, ordered by similarity.

        The index is metadata-only (no chunk text), so reranking and
        deduplication happen downstream in the search app, after the parent
        documents have been fetched from the source databases.

        Args:
            query: Search query text.
            n_results: Number of candidates to retrieve.
            source_db_filter: Optional filter by source database.

        Returns:
            List of SearchResult objects.
        """
        # Encode query
        query_embedding = self.embedding_manager.encode_single(query)

        # Build filter
        where_filter = None
        if source_db_filter:
            where_filter = {"source_db": source_db_filter}

        results = self.chromadb_client.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter,
            include=["metadatas", "distances"],
        )

        # Convert to SearchResult objects
        search_results = []
        for i in range(len(results.ids)):
            metadata = results.metadatas[i]
            # ChromaDB cosine distance is 1 - cosine_similarity
            distance = results.distances[i]
            similarity = 1 - distance

            search_results.append(
                SearchResult(
                    chunk_id=results.ids[i],
                    similarity_score=similarity,
                    parent_doc_id=metadata.get("parent_doc_id", ""),
                    chunk_index=metadata.get("chunk_index", 0),
                    source_db=metadata.get("source_db", ""),
                    source_table=metadata.get("source_table", ""),
                    metadata=metadata,
                )
            )

        logger.debug(
            "search_candidates_complete",
            query=query[:50],
            results=len(search_results),
            top_score=search_results[0].similarity_score if search_results else 0,
        )

        return search_results

    def search(
        self,
        query: str,
        k: int = 5,
        source_db_filter: str | None = None,
    ) -> list[SearchResult]:
        """
        Search for the k most relevant chunks (no reranking).

        Args:
            query: Search query text.
            k: Number of results to return.
            source_db_filter: Optional filter by source database.

        Returns:
            List of SearchResult objects.
        """
        return self.search_candidates(query, n_results=k, source_db_filter=source_db_filter)

    def get_available_databases(self) -> list[str]:
        """
        Get list of source databases in the collection.

        Returns:
            List of unique source database names.
        """
        try:
            databases = {
                metadata["source_db"]
                for _, metadata in self.chromadb_client.iter_metadata()
                if metadata and "source_db" in metadata
            }
            return sorted(databases)
        except Exception as e:
            logger.warning("failed_to_get_databases", error=str(e))
            return []
