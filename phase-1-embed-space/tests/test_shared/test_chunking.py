"""Tests for text chunking utilities.

Runs against the real langchain splitter so offset tracking (start_char /
end_char) is exercised against actual splitting behavior.
"""

from unittest.mock import MagicMock

import pytest

from src.shared.chunking import ChunkResult, DocumentChunks, TextChunker, create_chunker_from_config


class TestChunkResult:
    """Tests for ChunkResult dataclass."""

    def test_length_property(self):
        """Test that length property returns correct text length."""
        chunk = ChunkResult(text="Hello world", chunk_index=0, start_char=0, end_char=11)
        assert chunk.length == 11

    def test_metadata_default(self):
        """Test that metadata defaults to empty dict."""
        chunk = ChunkResult(text="test", chunk_index=0, start_char=0, end_char=4)
        assert chunk.metadata == {}

    def test_chunk_with_metadata(self):
        """Test ChunkResult with custom metadata."""
        metadata = {"source": "test", "key": "value"}
        chunk = ChunkResult(
            text="test content",
            chunk_index=1,
            start_char=10,
            end_char=22,
            metadata=metadata,
        )
        assert chunk.metadata == metadata
        assert chunk.chunk_index == 1
        assert chunk.start_char == 10
        assert chunk.end_char == 22


class TestDocumentChunks:
    """Tests for DocumentChunks dataclass."""

    def test_iteration(self):
        """Test that DocumentChunks is iterable."""
        chunks = [
            ChunkResult(text="chunk1", chunk_index=0, start_char=0, end_char=6),
            ChunkResult(text="chunk2", chunk_index=1, start_char=7, end_char=13),
        ]
        doc_chunks = DocumentChunks(
            doc_id="doc1",
            source_db="db1",
            source_table="table1",
            chunks=chunks,
            total_chunks=2,
            original_length=13,
        )
        assert list(doc_chunks) == chunks
        assert len(doc_chunks) == 2

    def test_empty_chunks(self):
        """Test DocumentChunks with no chunks."""
        doc_chunks = DocumentChunks(
            doc_id="doc1",
            source_db="db1",
            source_table="table1",
            chunks=[],
            total_chunks=0,
            original_length=0,
        )
        assert len(doc_chunks) == 0
        assert list(doc_chunks) == []


class TestTextChunkerInit:
    """Tests for TextChunker initialization."""

    def test_recursive_strategy_init(self):
        """Test recursive chunking strategy initialization."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=10, strategy="recursive")
        assert chunker.chunk_size == 100
        assert chunker.chunk_overlap == 10
        assert chunker.strategy == "recursive"

    def test_sentence_strategy_init(self):
        """Test sentence-based chunking strategy initialization."""
        chunker = TextChunker(chunk_size=200, chunk_overlap=20, strategy="sentence")
        assert chunker.strategy == "sentence"

    def test_fixed_strategy_init(self):
        """Test fixed-size chunking strategy initialization."""
        chunker = TextChunker(chunk_size=50, chunk_overlap=5, strategy="fixed")
        assert chunker.strategy == "fixed"

    def test_invalid_strategy(self):
        """Test that invalid strategy raises ValueError."""
        with pytest.raises(ValueError, match="Unknown chunking strategy"):
            TextChunker(strategy="invalid_strategy")

    def test_default_values(self):
        """Test default initialization values."""
        chunker = TextChunker()
        assert chunker.chunk_size == 512
        assert chunker.chunk_overlap == 50
        assert chunker.strategy == "recursive"
        assert chunker.min_chunk_length == 50


class TestTextChunkerChunking:
    """Tests for TextChunker chunking methods."""

    def test_empty_text(self):
        """Test handling of empty text."""
        chunker = TextChunker()
        chunks = chunker.chunk_text("")
        assert chunks == []

    def test_whitespace_only_text(self):
        """Test handling of whitespace-only text."""
        chunker = TextChunker(min_chunk_length=10)
        chunks = chunker.chunk_text("     ")
        assert chunks == []

    def test_text_shorter_than_min_length(self):
        """Test text shorter than minimum chunk length."""
        chunker = TextChunker(min_chunk_length=100)
        chunks = chunker.chunk_text("Short text")
        assert chunks == []

    def test_chunk_text_with_mock_splitter(self):
        """Test chunk_text with mocked splitter."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=10, min_chunk_length=10)
        # Mock the internal splitter
        chunker._splitter = MagicMock()
        chunker._splitter.split_text.return_value = [
            "First chunk of text here",
            "Second chunk of text here",
        ]

        text = "First chunk of text here Second chunk of text here"
        chunks = chunker.chunk_text(text)

        assert len(chunks) == 2
        assert chunks[0].text == "First chunk of text here"
        assert chunks[1].text == "Second chunk of text here"
        assert chunks[0].chunk_index == 0
        assert chunks[1].chunk_index == 1

    def test_chunk_document(self):
        """Test document chunking with full metadata."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=10, min_chunk_length=10)
        chunker._splitter = MagicMock()
        chunker._splitter.split_text.return_value = ["Test chunk content"]

        text = "Test chunk content"
        doc_chunks = chunker.chunk_document(
            doc_id="doc123",
            text=text,
            source_db="test_db",
            source_table="test_table",
            metadata={"custom": "value"},
        )

        assert doc_chunks.doc_id == "doc123"
        assert doc_chunks.source_db == "test_db"
        assert doc_chunks.source_table == "test_table"
        assert doc_chunks.original_length == len(text)
        assert len(doc_chunks.chunks) == 1


class TestRealSplitting:
    """Tests exercising the real langchain splitter (no mocks)."""

    def test_offsets_slice_back_to_chunk_text(self):
        """Every chunk's stored offsets must slice the original text exactly.

        Parent-document retrieval reconstructs chunk text with
        content[char_start:char_end], so this invariant is load-bearing.
        """
        chunker = TextChunker(chunk_size=120, chunk_overlap=20, min_chunk_length=20)
        text = (
            "Funding strategy overview for the northern region. "
            "The programme targets water infrastructure across twelve districts. "
            "Donor interest has grown steadily since the last review cycle. "
            "Local partners report improved delivery timelines this quarter. "
            "The next proposal round opens in September with expanded criteria."
        )
        chunks = chunker.chunk_text(text)

        assert len(chunks) > 1
        for chunk in chunks:
            assert text[chunk.start_char : chunk.end_char] == chunk.text

    def test_chunk_indices_are_sequential(self):
        """Chunk indices count filtered (kept) chunks sequentially."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=10, min_chunk_length=20)
        text = "A meaningful sentence about enterprise data pipelines. " * 10
        chunks = chunker.chunk_text(text)

        assert [c.chunk_index for c in chunks] == list(range(len(chunks)))

    def test_offset_fallback_retries_from_document_start(self):
        """A chunk located before the search cursor is still found exactly."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=10, min_chunk_length=5)
        chunker._splitter = MagicMock()
        # Splitter returns chunks out of order: the second chunk appears
        # before the first in the original text
        chunker._splitter.split_text.return_value = [
            "second part of the text",
            "first part here",
        ]
        text = "first part here and then the second part of the text"

        chunks = chunker.chunk_text(text)

        assert len(chunks) == 2
        # Retry-from-start must find the true position, not approximate
        assert chunks[1].start_char == text.find("first part here")
        assert text[chunks[1].start_char : chunks[1].end_char] == "first part here"


class TestCreateChunkerFromConfig:
    """Tests for create_chunker_from_config function."""

    def test_default_config(self):
        """Test creation with default config."""
        config = {}
        chunker = create_chunker_from_config(config)
        assert chunker.chunk_size == 512
        assert chunker.chunk_overlap == 50
        assert chunker.strategy == "recursive"

    def test_custom_config(self):
        """Test creation with custom config."""
        config = {
            "chunk_size": 256,
            "chunk_overlap": 25,
            "strategy": "sentence",
            "min_chunk_length": 100,
        }
        chunker = create_chunker_from_config(config)
        assert chunker.chunk_size == 256
        assert chunker.chunk_overlap == 25
        assert chunker.strategy == "sentence"
        assert chunker.min_chunk_length == 100

    def test_partial_config(self):
        """Test creation with partial config."""
        config = {"chunk_size": 1024}
        chunker = create_chunker_from_config(config)
        assert chunker.chunk_size == 1024
        assert chunker.chunk_overlap == 50  # default
        assert chunker.strategy == "recursive"  # default
