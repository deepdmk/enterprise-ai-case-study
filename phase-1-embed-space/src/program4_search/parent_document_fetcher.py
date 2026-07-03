"""
Parent Document Fetcher.

Retrieves full parent documents from source PostgreSQL databases
based on chunk metadata from search results.
"""

import asyncio
from dataclasses import dataclass
from typing import Any

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import Settings
from phase0_infra.habitat_logging import get_logger

from src.shared.database import DatabaseConnectionManager

from .retriever import SearchResult

logger = get_logger(__name__)


@dataclass
class ParentDocument:
    """A full parent document retrieved from source database."""

    doc_id: str
    content: str
    source_db: str
    source_table: str
    metadata: dict[str, Any]
    matched_chunk_index: int
    similarity_score: float

    def get_excerpt(self, max_length: int = 500) -> str:
        """Get a truncated excerpt of the content."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


@dataclass
class SearchResultWithDocument:
    """Search result combined with its parent document."""

    search_result: SearchResult
    parent_document: ParentDocument | None
    error: str | None = None


class ParentDocumentFetcher:
    """
    Fetches full parent documents from source databases.

    Uses the metadata stored in ChromaDB to identify and retrieve
    the original documents from their source PostgreSQL databases.
    """

    def __init__(
        self,
        db_manager: DatabaseConnectionManager,
        settings: Settings,
    ):
        """
        Initialize the fetcher.

        Args:
            db_manager: Database connection manager.
            settings: Application settings with database configs.
        """
        self.db_manager = db_manager
        self.settings = settings

    def _get_table_config(self, source_db: str, source_table: str):
        """Get table configuration for a source."""
        db_config = self.settings.databases.get(source_db)
        if not db_config:
            return None

        for table_config in db_config.tables:
            if table_config.name == source_table:
                return table_config

        return None

    async def fetch_document(
        self,
        search_result: SearchResult,
    ) -> ParentDocument | None:
        """
        Fetch a single parent document.

        Args:
            search_result: Search result with metadata.

        Returns:
            ParentDocument or None if not found.
        """
        source_db = search_result.source_db
        source_table = search_result.source_table
        doc_id = search_result.parent_doc_id

        # Get table config
        table_config = self._get_table_config(source_db, source_table)
        if not table_config:
            logger.warning(
                "table_config_not_found",
                source_db=source_db,
                source_table=source_table,
            )
            return None

        try:
            # Fetch from database
            record = await self.db_manager.get_record_by_id(
                db_name=source_db,
                table_config=table_config,
                doc_id=doc_id,
            )

            if not record:
                logger.warning(
                    "document_not_found",
                    source_db=source_db,
                    source_table=source_table,
                    doc_id=doc_id,
                )
                return None

            # Combine text columns exactly like ingestion's SQL expression
            # (COALESCE(col::text, '') joined with ' '): every configured
            # column contributes, NULLs become empty strings. Anything else
            # drifts the stored char_start/char_end offsets.
            content = " ".join(
                "" if record.get(col) is None else str(record.get(col))
                for col in table_config.text_columns
            )

            # Extract additional metadata
            metadata = {}
            for col in table_config.additional_metadata:
                if col in record:
                    metadata[col] = record[col]

            return ParentDocument(
                doc_id=doc_id,
                content=content,
                source_db=source_db,
                source_table=source_table,
                metadata=metadata,
                matched_chunk_index=search_result.chunk_index,
                similarity_score=search_result.similarity_score,
            )

        except Exception as e:
            logger.error(
                "fetch_document_error",
                source_db=source_db,
                doc_id=doc_id,
                error=str(e),
            )
            return None

    async def fetch_documents(
        self,
        search_results: list[SearchResult],
    ) -> list[SearchResultWithDocument]:
        """
        Fetch parent documents for multiple search results.

        Args:
            search_results: List of search results.

        Returns:
            List of SearchResultWithDocument with fetched documents.
        """
        # Lazy pool init: no-op after the first call. Lets the app construct
        # the fetcher synchronously and connect on first search. The mock
        # fetcher has no db_manager.
        if self.db_manager is not None:
            await self.db_manager.initialize()

        # fetch_document isolates per-fetch errors (returns None), so a
        # failed fetch never cancels its siblings
        parent_docs = await asyncio.gather(
            *(self.fetch_document(sr) for sr in search_results)
        )

        return [
            SearchResultWithDocument(
                search_result=search_result,
                parent_document=parent_doc,
                error=None if parent_doc else "Document not found",
            )
            for search_result, parent_doc in zip(search_results, parent_docs)
        ]


class MockParentDocumentFetcher(ParentDocumentFetcher):
    """Mock fetcher for testing without database connections."""

    def __init__(self):
        """Initialize mock fetcher."""
        self.db_manager = None
        self._mock_documents: dict[str, str] = {}

    def add_mock_document(self, doc_id: str, content: str) -> None:
        """Add a mock document."""
        self._mock_documents[doc_id] = content

    async def fetch_document(
        self,
        search_result: SearchResult,
    ) -> ParentDocument | None:
        """Fetch mock document."""
        doc_id = search_result.parent_doc_id

        # Generate mock content if not explicitly set
        content = self._mock_documents.get(
            doc_id,
            f"This is the full content of document {doc_id} from "
            f"{search_result.source_db}.{search_result.source_table}. "
            f"It contains information relevant to your search query. "
            f"The matched section was chunk {search_result.chunk_index}.",
        )

        return ParentDocument(
            doc_id=doc_id,
            content=content,
            source_db=search_result.source_db,
            source_table=search_result.source_table,
            metadata=search_result.metadata,
            matched_chunk_index=search_result.chunk_index,
            similarity_score=search_result.similarity_score,
        )
