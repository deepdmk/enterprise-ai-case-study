"""Tests for token_utils module."""

import pytest
from unittest.mock import MagicMock

# Skip all tests if datasets is not available
datasets = pytest.importorskip("datasets", reason="datasets library not installed")
Dataset = datasets.Dataset

from src.program2_fine_tuning.token_utils import (
    calculate_token_lengths,
    _split_input_output_tokens,
    get_token_stats,
)


@pytest.fixture
def mock_tokenizer():
    """Create a mock tokenizer that returns predictable token counts."""
    tokenizer = MagicMock()
    # Simple mock: each word becomes one token
    tokenizer.encode = lambda text, add_special_tokens=False: text.split()
    return tokenizer


@pytest.fixture
def sample_dataset():
    """Create a sample dataset for testing."""
    return Dataset.from_list([
        {"text": "User: Hello world <|start_header_id|>assistant<|end_header_id|> Hi there how are you"},
        {"text": "User: Test input <|start_header_id|>assistant<|end_header_id|> Test output response"},
        {"text": "Question here <|start_header_id|>assistant<|end_header_id|> Answer here"},
    ])


class TestCalculateTokenLengths:
    """Tests for calculate_token_lengths function."""

    def test_empty_dataset(self, mock_tokenizer):
        """Test with empty dataset."""
        dataset = Dataset.from_list([])
        avg_in, avg_out, avg_total = calculate_token_lengths(dataset, mock_tokenizer)
        assert avg_in == 0.0
        assert avg_out == 0.0
        assert avg_total == 0.0

    def test_basic_calculation(self, mock_tokenizer, sample_dataset):
        """Test basic token length calculation."""
        avg_in, avg_out, avg_total = calculate_token_lengths(
            sample_dataset, mock_tokenizer
        )
        # With our mock tokenizer, each word is a token
        assert avg_in > 0
        assert avg_out > 0
        assert avg_total > 0
        assert avg_total >= avg_in  # Total should be >= input

    def test_max_samples_limit(self, mock_tokenizer):
        """Test that max_samples limits processing."""
        # Create a larger dataset
        data = [{"text": f"Input {i} <|start_header_id|>assistant<|end_header_id|> Output {i}"} for i in range(100)]
        dataset = Dataset.from_list(data)

        # Should work with limit
        avg_in, avg_out, avg_total = calculate_token_lengths(
            dataset, mock_tokenizer, max_samples=10
        )
        assert avg_in > 0
        assert avg_out > 0

    def test_missing_text_field(self, mock_tokenizer):
        """Test handling of missing text field."""
        dataset = Dataset.from_list([{"other_field": "value"}])
        avg_in, avg_out, avg_total = calculate_token_lengths(dataset, mock_tokenizer)
        assert avg_in == 0.0
        assert avg_out == 0.0


class TestSplitInputOutputTokens:
    """Tests for _split_input_output_tokens function."""

    def test_chatml_marker(self, mock_tokenizer):
        """Test splitting with ChatML assistant marker."""
        text = "User input here <|start_header_id|>assistant<|end_header_id|> Assistant response"
        tokens = text.split()  # Mock tokenization

        input_count, output_count = _split_input_output_tokens(text, tokens, mock_tokenizer)
        assert input_count > 0
        assert output_count > 0
        assert input_count + output_count == len(tokens)

    def test_response_marker(self, mock_tokenizer):
        """Test splitting with ### Response: marker."""
        text = "User input here ### Response: Assistant response here"
        tokens = text.split()

        input_count, output_count = _split_input_output_tokens(text, tokens, mock_tokenizer)
        assert input_count > 0
        assert output_count > 0

    def test_no_marker_fallback(self, mock_tokenizer):
        """Test fallback when no marker found."""
        text = "Some text without any markers at all"
        tokens = text.split()

        input_count, output_count = _split_input_output_tokens(text, tokens, mock_tokenizer)
        # Should fall back to 50/50 split
        assert input_count + output_count == len(tokens)
        assert abs(input_count - output_count) <= 1  # Roughly equal


class TestGetTokenStats:
    """Tests for get_token_stats function."""

    def test_returns_dict(self, mock_tokenizer, sample_dataset):
        """Test that get_token_stats returns expected dict structure."""
        stats = get_token_stats(sample_dataset, mock_tokenizer)

        assert "num_samples" in stats
        assert "avg_input_tokens" in stats
        assert "avg_output_tokens" in stats
        assert "avg_total_tokens" in stats
        assert stats["num_samples"] == 3

    def test_empty_dataset(self, mock_tokenizer):
        """Test with empty dataset."""
        dataset = Dataset.from_list([])
        stats = get_token_stats(dataset, mock_tokenizer)

        assert stats["num_samples"] == 0
        assert stats["avg_input_tokens"] == 0.0
