"""
Text Chunking Utilities.

Provides various strategies for splitting text into chunks suitable for embedding.
Preserves metadata and tracks chunk positions within parent documents.
"""

from dataclasses import dataclass, field
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.shared.path_config import configure_paths
configure_paths()

from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class ChunkResult:
    """Result of chunking a piece of text."""

    text: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def length(self) -> int:
        """Get the length of the chunk text."""
        return len(self.text)


@dataclass
class DocumentChunks:
    """All chunks from a single document."""

    doc_id: str
    source_db: str
    source_table: str
    chunks: list[ChunkResult]
    total_chunks: int
    original_length: int

    def __iter__(self):
        return iter(self.chunks)

    def __len__(self):
        return len(self.chunks)


class TextChunker:
    """
    Text chunking with multiple strategy support.

    Strategies:
    - recursive: RecursiveCharacterTextSplitter (default, best for most text)
    - sentence: Split on sentence boundaries
    - fixed: Fixed-size chunks with overlap
    """

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        strategy: str = "recursive",
        min_chunk_length: int = 50,
    ):
        """
        Initialize the text chunker.

        Args:
            chunk_size: Target size for each chunk in characters.
            chunk_overlap: Number of overlapping characters between chunks.
            strategy: Chunking strategy ('recursive', 'sentence', 'fixed').
            min_chunk_length: Minimum length for a chunk to be included.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy
        self.min_chunk_length = min_chunk_length

        # Initialize the splitter based on strategy
        if strategy == "recursive":
            self._splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
        elif strategy == "sentence":
            self._splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
            )
        elif strategy == "fixed":
            self._splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=[""],  # No separators = fixed size
            )
        else:
            raise ValueError(f"Unknown chunking strategy: {strategy}")

    def chunk_text(self, text: str, metadata: dict[str, Any] | None = None) -> list[ChunkResult]:
        """
        Split text into chunks.

        Args:
            text: The text to chunk.
            metadata: Optional metadata to attach to each chunk.

        Returns:
            List of ChunkResult objects.
        """
        if not text or len(text.strip()) < self.min_chunk_length:
            return []

        metadata = metadata or {}

        # Use langchain splitter
        chunks = self._splitter.split_text(text)

        results: list[ChunkResult] = []
        current_pos = 0

        for i, chunk_text in enumerate(chunks):
            # Skip chunks that are too short
            if len(chunk_text.strip()) < self.min_chunk_length:
                continue

            # Find the start position of this chunk in original text
            start_pos = text.find(chunk_text, current_pos)
            if start_pos == -1:
                # The splitter may normalize whitespace; retry from the top of
                # the document before giving up and approximating
                start_pos = text.find(chunk_text)
            if start_pos == -1:
                start_pos = current_pos
                logger.warning(
                    "chunk_offset_approximate",
                    chunk_index=len(results),
                    approximate_start=start_pos,
                )

            end_pos = start_pos + len(chunk_text)

            results.append(
                ChunkResult(
                    text=chunk_text,
                    chunk_index=len(results),  # Use actual index after filtering
                    start_char=start_pos,
                    end_char=end_pos,
                    metadata=metadata.copy(),
                )
            )

            # Update position for next search (accounting for overlap)
            current_pos = max(start_pos + 1, end_pos - self.chunk_overlap)

        return results

    def chunk_document(
        self,
        doc_id: str,
        text: str,
        source_db: str,
        source_table: str,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentChunks:
        """
        Chunk a document and return structured result.

        Args:
            doc_id: Unique identifier for the document.
            text: The document text to chunk.
            source_db: Name of the source database.
            source_table: Name of the source table.
            metadata: Optional additional metadata.

        Returns:
            DocumentChunks object containing all chunks.
        """
        # Add document-level metadata
        chunk_metadata = {
            "doc_id": doc_id,
            "source_db": source_db,
            "source_table": source_table,
            **(metadata or {}),
        }

        chunks = self.chunk_text(text, chunk_metadata)

        return DocumentChunks(
            doc_id=doc_id,
            source_db=source_db,
            source_table=source_table,
            chunks=chunks,
            total_chunks=len(chunks),
            original_length=len(text),
        )


def create_chunker_from_config(config: dict[str, Any]) -> TextChunker:
    """
    Create a TextChunker from configuration dictionary.

    Args:
        config: Configuration dict with chunk_size, chunk_overlap, strategy.

    Returns:
        Configured TextChunker instance.
    """
    return TextChunker(
        chunk_size=config.get("chunk_size", 512),
        chunk_overlap=config.get("chunk_overlap", 50),
        strategy=config.get("strategy", "recursive"),
        min_chunk_length=config.get("min_chunk_length", 50),
    )
