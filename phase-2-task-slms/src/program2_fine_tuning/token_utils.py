"""Token counting utilities for accurate metrics."""

from typing import Any

from datasets import Dataset

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

from habitat_logging import get_logger
from src.shared.data_formatter import (
    CHAT_TEMPLATES,
    get_default_template,
)

logger = get_logger(__name__)


def _get_assistant_markers() -> list[str]:
    """Get all known assistant start markers from configured templates."""
    markers = []
    for template in CHAT_TEMPLATES.values():
        if template.assistant_start and template.assistant_start not in markers:
            markers.append(template.assistant_start)
    return markers


def calculate_token_lengths(
    dataset: Dataset,
    tokenizer: Any,
    text_field: str = "text",
    max_samples: int | None = None,
) -> tuple[float, float, float]:
    """
    Calculate average token lengths using the actual tokenizer.

    Args:
        dataset: HuggingFace Dataset with text field
        tokenizer: The tokenizer to use for counting
        text_field: Name of the text field in the dataset
        max_samples: Maximum samples to process (None for all)

    Returns:
        Tuple of (avg_input_tokens, avg_output_tokens, avg_total_tokens)
    """
    if len(dataset) == 0:
        return 0.0, 0.0, 0.0

    total_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    count = 0

    # Limit samples if specified (for performance on large datasets)
    samples_to_process = dataset
    if max_samples and len(dataset) > max_samples:
        samples_to_process = dataset.select(range(max_samples))
        logger.info(
            "token_counting_sampled",
            total_samples=len(dataset),
            sampled=max_samples,
        )

    for example in samples_to_process:
        text = example.get(text_field, "")
        if not text:
            continue

        # Tokenize the full text
        tokens = tokenizer.encode(text, add_special_tokens=False)
        total_tokens += len(tokens)

        # Find the assistant response boundary
        input_tokens, output_tokens = _split_input_output_tokens(
            text, tokens, tokenizer
        )
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        count += 1

    if count == 0:
        return 0.0, 0.0, 0.0

    avg_input = total_input_tokens / count
    avg_output = total_output_tokens / count
    avg_total = total_tokens / count

    logger.info(
        "token_lengths_calculated",
        samples=count,
        avg_input_tokens=round(avg_input, 1),
        avg_output_tokens=round(avg_output, 1),
        avg_total_tokens=round(avg_total, 1),
    )

    return avg_input, avg_output, avg_total


def _split_input_output_tokens(
    text: str,
    tokens: list[int],
    tokenizer: Any,
) -> tuple[int, int]:
    """
    Split token count into input and output portions.

    Looks for ChatML assistant markers to find the boundary.
    Falls back to 50/50 split if no marker found.

    Args:
        text: The full text
        tokens: Pre-tokenized token IDs
        tokenizer: The tokenizer

    Returns:
        Tuple of (input_token_count, output_token_count)
    """
    total = len(tokens)

    # Try to find assistant response marker in text using template markers
    assistant_start = -1
    assistant_markers = _get_assistant_markers()

    for marker in assistant_markers:
        pos = text.find(marker)
        if pos != -1:
            assistant_start = pos + len(marker)
            break

    if assistant_start == -1:
        # Fallback markers for other formats not in templates
        for marker in ["### Response:", "### Output:", "ASSISTANT:"]:
            pos = text.find(marker)
            if pos != -1:
                assistant_start = pos + len(marker)
                break

    if assistant_start != -1:
        # Tokenize just the input portion to get accurate count
        input_text = text[:assistant_start]
        input_tokens = tokenizer.encode(input_text, add_special_tokens=False)
        input_count = len(input_tokens)
        output_count = total - input_count
        return input_count, max(0, output_count)

    # Fallback: assume roughly 50/50 split
    # This is still better than word-based approximation
    mid = total // 2
    return mid, total - mid


def get_token_stats(
    dataset: Dataset,
    tokenizer: Any,
    text_field: str = "text",
) -> dict[str, Any]:
    """
    Get comprehensive token statistics for a dataset.

    Args:
        dataset: HuggingFace Dataset
        tokenizer: The tokenizer to use
        text_field: Name of the text field

    Returns:
        Dictionary with token statistics
    """
    avg_input, avg_output, avg_total = calculate_token_lengths(
        dataset, tokenizer, text_field
    )

    return {
        "num_samples": len(dataset),
        "avg_input_tokens": round(avg_input, 1),
        "avg_output_tokens": round(avg_output, 1),
        "avg_total_tokens": round(avg_total, 1),
    }
