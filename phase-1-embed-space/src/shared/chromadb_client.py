"""
ChromaDB Client Wrapper.

Provides a clean interface for ChromaDB operations in persistent server mode.
Handles collection management, embedding storage, and querying.
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

# Import local config BEFORE adding phase-0 to path
from config.settings import ChromaDBConfig

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class QueryResult:
    """Result from a ChromaDB query."""

    ids: list[str]
    distances: list[float]
    metadatas: list[dict[str, Any]]
    embeddings: list[list[float]] | None = None

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


class ChromaDBClient:
    """
    Wrapper for ChromaDB operations.

    Supports both HTTP server mode and local persistent mode.
    Falls back to local mode if server connection fails.
    """

    def __init__(self, config: ChromaDBConfig, persist_directory: str = "data/chromadb"):
        """
        Initialize the ChromaDB client.

        Args:
            config: ChromaDB configuration with host, port, collection name.
            persist_directory: Directory for local persistent storage (fallback).
        """
        self.config = config
        self.persist_directory = persist_directory
        self._client: chromadb.HttpClient | chromadb.PersistentClient | None = None
        self._collection: chromadb.Collection | None = None
        self._using_local = False

    def connect(self) -> None:
        """Connect to ChromaDB (HTTP server or local persistent)."""
        # Try HTTP server first
        try:
            self._client = chromadb.HttpClient(
                host=self.config.host,
                port=int(self.config.port),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            # Test connection
            self._client.heartbeat()
            self._using_local = False
            logger.info(
                "chromadb_connected", host=self.config.host, port=self.config.port, mode="http"
            )
        except Exception as e:
            # Fall back to local persistent client
            logger.warning(
                "chromadb_http_failed_using_local",
                host=self.config.host,
                port=self.config.port,
                error=str(e),
            )
            import os
            os.makedirs(self.persist_directory, exist_ok=True)
            self._client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            self._using_local = True
            logger.info(
                "chromadb_connected", path=self.persist_directory, mode="local_persistent"
            )

    def get_or_create_collection(
        self, name: str | None = None, metadata: dict[str, Any] | None = None
    ) -> chromadb.Collection:
        """
        Get or create a collection.

        Args:
            name: Collection name (uses config default if not specified).
            metadata: Optional metadata for the collection.

        Returns:
            ChromaDB Collection object.
        """
        if self._client is None:
            self.connect()

        name = name or self.config.collection_name
        metadata = metadata or {
            "description": "Enterprise unified embedding space",
            "hnsw:space": self.config.hnsw.get("space", "cosine"),
        }

        self._collection = self._client.get_or_create_collection(
            name=name,
            metadata=metadata,
        )

        logger.info("chromadb_collection_ready", name=name, count=self._collection.count())
        return self._collection

    @property
    def collection(self) -> chromadb.Collection:
        """Get the current collection, creating if necessary."""
        if self._collection is None:
            self.get_or_create_collection()
        return self._collection

    def upsert_embeddings(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """
        Upsert embeddings with their metadata.

        Note: We intentionally do NOT store document text in ChromaDB.
        Only embeddings and metadata are stored. Parent documents are
        retrieved from source databases at query time.

        Args:
            ids: Unique identifiers for each embedding.
            embeddings: List of embedding vectors.
            metadatas: List of metadata dicts for each embedding.
        """
        if len(ids) != len(embeddings) or len(ids) != len(metadatas):
            raise ValueError("ids, embeddings, and metadatas must have the same length")

        if not ids:
            return

        # Ensure metadata values are serializable
        clean_metadatas = []
        for meta in metadatas:
            clean_meta = {}
            for k, v in meta.items():
                if v is not None:
                    if isinstance(v, (str, int, float, bool)):
                        clean_meta[k] = v
                    else:
                        clean_meta[k] = str(v)
            clean_metadatas.append(clean_meta)

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=clean_metadatas,
        )

        logger.debug("chromadb_upserted", count=len(ids))

    def query(
        self,
        query_embeddings: list[list[float]],
        n_results: int = 5,
        where: dict[str, Any] | None = None,
        include_embeddings: bool = False,
    ) -> QueryResult:
        """
        Query the collection for similar embeddings.

        Args:
            query_embeddings: List of query embedding vectors.
            n_results: Number of results per query.
            where: Optional metadata filter.
            include_embeddings: Whether to include embeddings in results.

        Returns:
            QueryResult with matching IDs, distances, and metadata.
        """
        include = ["metadatas", "distances"]
        if include_embeddings:
            include.append("embeddings")

        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where,
            include=include,
        )

        # Extract first query results (we typically query one at a time)
        return QueryResult(
            ids=results["ids"][0] if results["ids"] else [],
            distances=results["distances"][0] if results["distances"] else [],
            metadatas=results["metadatas"][0] if results["metadatas"] else [],
            embeddings=results["embeddings"][0] if results.get("embeddings") else None,
        )

    def delete_by_ids(self, ids: list[str]) -> None:
        """
        Delete embeddings by their IDs.

        Args:
            ids: List of IDs to delete.
        """
        if not ids:
            return

        self.collection.delete(ids=ids)
        logger.debug("chromadb_deleted", count=len(ids))

    def delete_by_metadata(self, where: dict[str, Any]) -> int:
        """
        Delete embeddings matching metadata filter.

        Args:
            where: Metadata filter for deletion.

        Returns:
            Number of items deleted.
        """
        # Get IDs matching the filter
        results = self.collection.get(where=where, include=[])
        ids = results["ids"]

        if ids:
            self.collection.delete(ids=ids)
            logger.info("chromadb_deleted_by_metadata", count=len(ids), filter=where)

        return len(ids)

    def get_by_ids(
        self, ids: list[str], include_embeddings: bool = False
    ) -> list[dict[str, Any]]:
        """
        Get embeddings and metadata by IDs.

        Args:
            ids: List of IDs to retrieve.
            include_embeddings: Whether to include embeddings.

        Returns:
            List of records with id, metadata, and optionally embedding.
        """
        include = ["metadatas"]
        if include_embeddings:
            include.append("embeddings")

        results = self.collection.get(ids=ids, include=include)

        records = []
        for i, id_ in enumerate(results["ids"]):
            record = {
                "id": id_,
                "metadata": results["metadatas"][i] if results["metadatas"] else {},
            }
            if include_embeddings and results.get("embeddings"):
                record["embedding"] = results["embeddings"][i]
            records.append(record)

        return records

    def get_collection_stats(self) -> CollectionStats:
        """
        Get statistics for the current collection.

        Returns:
            CollectionStats with count and metadata.
        """
        return CollectionStats(
            name=self.collection.name,
            count=self.collection.count(),
            metadata=self.collection.metadata or {},
        )

    def list_collections(self) -> list[str]:
        """
        List all collections in the database.

        Returns:
            List of collection names.
        """
        if self._client is None:
            self.connect()
        collections = self._client.list_collections()
        return [c.name for c in collections]

    def delete_collection(self, name: str | None = None) -> None:
        """
        Delete a collection.

        Args:
            name: Collection name (uses config default if not specified).
        """
        if self._client is None:
            self.connect()

        name = name or self.config.collection_name
        self._client.delete_collection(name=name)
        if self._collection and self._collection.name == name:
            self._collection = None

        logger.info("chromadb_collection_deleted", name=name)


def create_client_from_config(config: ChromaDBConfig) -> ChromaDBClient:
    """
    Create a ChromaDB client from configuration.

    Args:
        config: ChromaDB configuration.

    Returns:
        Configured ChromaDBClient instance.
    """
    client = ChromaDBClient(config)
    client.connect()
    return client
