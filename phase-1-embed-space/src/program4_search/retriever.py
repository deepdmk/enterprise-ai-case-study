"""
Semantic Retriever.

Core retrieval logic using fine-tuned embeddings and ChromaDB.
"""

from dataclasses import dataclass
from typing import Any

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger

from config.settings import RerankingConfig
from src.shared.chromadb_client import ChromaDBClient
from src.shared.embedding_model import EmbeddingModelManager

from .reranker import SearchReranker

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
        reranking_config: RerankingConfig | None = None,
    ):
        """
        Initialize the retriever.

        Args:
            embedding_manager: Embedding model manager.
            chromadb_client: ChromaDB client.
            reranking_config: Optional reranking configuration.
        """
        self.embedding_manager = embedding_manager
        self.chromadb_client = chromadb_client
        self.reranking_config = reranking_config

        # Initialize reranker if enabled
        self.reranker: SearchReranker | None = None
        if reranking_config and reranking_config.enabled and reranking_config.model:
            self.reranker = SearchReranker(reranking_config.model)
            logger.info("reranking_enabled", model=reranking_config.model)

    def search(
        self,
        query: str,
        k: int = 5,
        source_db_filter: str | None = None,
    ) -> list[SearchResult]:
        """
        Search for relevant chunks.

        Args:
            query: Search query text.
            k: Number of results to return.
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

        # Determine how many candidates to retrieve
        n_candidates = k
        if self.reranker and self.reranking_config:
            n_candidates = k * self.reranking_config.candidate_multiplier

        # Query ChromaDB (include documents if reranking)
        include_list = ["metadatas", "distances"]
        if self.reranker:
            include_list.append("documents")

        results = self.chromadb_client.query(
            query_embeddings=[query_embedding],
            n_results=n_candidates,
            where=where_filter,
            include=include_list,
        )

        # Convert to SearchResult objects
        search_results = []
        for i in range(len(results.ids)):
            metadata = results.metadatas[i]
            # Convert distance to similarity (ChromaDB uses L2/cosine distance)
            # For cosine, distance is 2*(1-similarity), so similarity = 1 - distance/2
            distance = results.distances[i]
            similarity = 1 - distance / 2  # Assumes cosine space

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

        # Rerank if enabled
        if self.reranker and results.documents:
            # Convert SearchResults to dicts for reranker
            result_dicts = [
                {
                    "chunk_id": r.chunk_id,
                    "similarity_score": r.similarity_score,
                    "parent_doc_id": r.parent_doc_id,
                    "chunk_index": r.chunk_index,
                    "source_db": r.source_db,
                    "source_table": r.source_table,
                    "metadata": r.metadata,
                    "distance": results.distances[i],
                }
                for i, r in enumerate(search_results)
            ]

            # Rerank
            reranked_dicts = self.reranker.rerank(
                query=query,
                results=result_dicts,
                documents=results.documents,
                top_k=k,
            )

            # Convert back to SearchResult objects
            search_results = [
                SearchResult(
                    chunk_id=r["chunk_id"],
                    similarity_score=r.get("rerank_score", r["similarity_score"]),
                    parent_doc_id=r["parent_doc_id"],
                    chunk_index=r["chunk_index"],
                    source_db=r["source_db"],
                    source_table=r["source_table"],
                    metadata=r["metadata"],
                )
                for r in reranked_dicts
            ]

        logger.debug(
            "search_complete",
            query=query[:50],
            results=len(search_results),
            top_score=search_results[0].similarity_score if search_results else 0,
            reranked=self.reranker is not None,
        )

        return search_results

    def search_with_deduplication(
        self,
        query: str,
        k: int = 5,
        source_db_filter: str | None = None,
    ) -> list[SearchResult]:
        """
        Search with deduplication by parent document.

        Returns at most one chunk per parent document.

        Args:
            query: Search query text.
            k: Number of unique documents to return.
            source_db_filter: Optional filter by source database.

        Returns:
            List of SearchResult objects (one per unique document).
        """
        # Get more results than needed for deduplication
        results = self.search(query, k=k * 3, source_db_filter=source_db_filter)

        # Deduplicate by parent document, keeping highest scoring chunk
        seen_docs = set()
        deduplicated = []

        for result in results:
            doc_key = f"{result.source_db}_{result.parent_doc_id}"
            if doc_key not in seen_docs:
                seen_docs.add(doc_key)
                deduplicated.append(result)
                if len(deduplicated) >= k:
                    break

        return deduplicated

    def get_available_databases(self) -> list[str]:
        """
        Get list of source databases in the collection.

        Returns:
            List of unique source database names.
        """
        try:
            results = self.chroma_client.collection.get(
                limit=1000,
                include=["metadatas"],
            )
            databases = set()
            for metadata in (results.get("metadatas") or []):
                if metadata and "source_database" in metadata:
                    databases.add(metadata["source_database"])
            return sorted(databases)
        except Exception as e:
            logger.warning("failed_to_get_databases", error=str(e))
            return []
