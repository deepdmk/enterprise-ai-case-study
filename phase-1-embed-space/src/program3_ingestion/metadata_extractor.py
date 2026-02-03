"""
Metadata Extractor.

Extracts and structures metadata for each chunk to enable parent document retrieval.
"""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.shared.chunking import ChunkResult


@dataclass
class ChunkMetadata:
    """Structured metadata for a chunk stored in ChromaDB."""

    chunk_id: str  # Unique identifier for the chunk
    parent_doc_id: str  # ID of the source document
    chunk_index: int  # Position within parent document
    total_chunks: int  # Total chunks in parent document
    source_db: str  # Database identifier
    source_table: str  # Source table name
    created_at: str  # ISO format timestamp
    char_start: int  # Start position in original text
    char_end: int  # End position in original text
    additional: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for ChromaDB storage."""
        result = {
            "chunk_id": self.chunk_id,
            "parent_doc_id": self.parent_doc_id,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "source_db": self.source_db,
            "source_table": self.source_table,
            "created_at": self.created_at,
            "char_start": self.char_start,
            "char_end": self.char_end,
        }
        # Add additional metadata (flatten nested dict)
        for key, value in self.additional.items():
            if value is not None:
                result[f"meta_{key}"] = str(value) if not isinstance(value, (str, int, float, bool)) else value
        return result


class MetadataExtractor:
    """
    Extracts metadata from records and chunks.

    Creates structured metadata that enables:
    - Parent document retrieval from source databases
    - Chunk position tracking within documents
    - Source attribution and traceability
    """

    def __init__(self, include_text_hash: bool = False):
        """
        Initialize the metadata extractor.

        Args:
            include_text_hash: Whether to include a hash of chunk text for deduplication.
        """
        self.include_text_hash = include_text_hash

    def generate_chunk_id(
        self,
        doc_id: str,
        source_db: str,
        chunk_index: int,
    ) -> str:
        """
        Generate a unique chunk ID.

        Format: {source_db}_{doc_id}_chunk_{index}

        Args:
            doc_id: Parent document ID.
            source_db: Source database name.
            chunk_index: Index of chunk within document.

        Returns:
            Unique chunk ID string.
        """
        # Sanitize doc_id (remove special characters)
        safe_doc_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(doc_id))
        return f"{source_db}_{safe_doc_id}_chunk_{chunk_index}"

    def extract_metadata(
        self,
        chunk: ChunkResult,
        doc_id: str,
        source_db: str,
        source_table: str,
        total_chunks: int,
        additional_metadata: dict[str, Any] | None = None,
    ) -> ChunkMetadata:
        """
        Extract metadata for a single chunk.

        Args:
            chunk: The chunk result.
            doc_id: Parent document ID.
            source_db: Source database name.
            source_table: Source table name.
            total_chunks: Total number of chunks in the document.
            additional_metadata: Extra metadata from the source record.

        Returns:
            ChunkMetadata with all extracted information.
        """
        chunk_id = self.generate_chunk_id(doc_id, source_db, chunk.chunk_index)

        additional = additional_metadata.copy() if additional_metadata else {}

        # Optionally add text hash for deduplication
        if self.include_text_hash:
            text_hash = hashlib.md5(chunk.text.encode()).hexdigest()[:12]
            additional["text_hash"] = text_hash

        return ChunkMetadata(
            chunk_id=chunk_id,
            parent_doc_id=str(doc_id),
            chunk_index=chunk.chunk_index,
            total_chunks=total_chunks,
            source_db=source_db,
            source_table=source_table,
            created_at=datetime.utcnow().isoformat(),
            char_start=chunk.start_char,
            char_end=chunk.end_char,
            additional=additional,
        )

    def extract_from_document_chunks(
        self,
        chunks: list[ChunkResult],
        doc_id: str,
        source_db: str,
        source_table: str,
        additional_metadata: dict[str, Any] | None = None,
    ) -> list[ChunkMetadata]:
        """
        Extract metadata for all chunks from a document.

        Args:
            chunks: List of chunks from the document.
            doc_id: Parent document ID.
            source_db: Source database name.
            source_table: Source table name.
            additional_metadata: Extra metadata from the source record.

        Returns:
            List of ChunkMetadata for all chunks.
        """
        total_chunks = len(chunks)
        return [
            self.extract_metadata(
                chunk=chunk,
                doc_id=doc_id,
                source_db=source_db,
                source_table=source_table,
                total_chunks=total_chunks,
                additional_metadata=additional_metadata,
            )
            for chunk in chunks
        ]
