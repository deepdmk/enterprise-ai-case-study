"""Data formatters for ChatML and instruction formats."""

import json
import sys
from pathlib import Path
from typing import Any

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

from datasets import Dataset

logger = get_logger(__name__)

# ChatML template for Llama 3.1
CHATML_TEMPLATE = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{assistant}<|eot_id|>"""

# Llama 3.1 specific tokens
LLAMA_SPECIAL_TOKENS = {
    "bos": "<|begin_of_text|>",
    "eos": "<|eot_id|>",
    "system_start": "<|start_header_id|>system<|end_header_id|>",
    "user_start": "<|start_header_id|>user<|end_header_id|>",
    "assistant_start": "<|start_header_id|>assistant<|end_header_id|>",
}


def format_chatml(
    system_prompt: str,
    user_message: str,
    assistant_response: str,
) -> str:
    """
    Format a single example in ChatML format for Llama 3.1.

    Args:
        system_prompt: The system prompt
        user_message: The user's input
        assistant_response: The expected assistant response

    Returns:
        Formatted ChatML string
    """
    return CHATML_TEMPLATE.format(
        system=system_prompt.strip(),
        user=user_message.strip(),
        assistant=assistant_response.strip(),
    )


def format_conversation(
    conversations: list[dict[str, str]],
    system_prompt: str | None = None,
) -> str:
    """
    Format a multi-turn conversation in ChatML format.

    Args:
        conversations: List of {"from": "human"|"gpt", "value": "..."}
        system_prompt: Optional system prompt

    Returns:
        Formatted ChatML string
    """
    parts = ["<|begin_of_text|>"]

    # Add system prompt if provided
    if system_prompt:
        parts.append(f"<|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>")

    for turn in conversations:
        role = turn.get("from", turn.get("role", ""))
        content = turn.get("value", turn.get("content", ""))

        if role in ("human", "user"):
            parts.append(f"<|start_header_id|>user<|end_header_id|>\n\n{content}<|eot_id|>")
        elif role in ("gpt", "assistant"):
            parts.append(f"<|start_header_id|>assistant<|end_header_id|>\n\n{content}<|eot_id|>")

    return "".join(parts)


def format_for_training(
    examples: list[dict[str, Any]],
    system_prompt: str,
    input_key: str = "input",
    output_key: str = "output",
) -> list[dict[str, str]]:
    """
    Format examples for SFTTrainer.

    Args:
        examples: List of training examples
        system_prompt: System prompt to use
        input_key: Key for input field
        output_key: Key for output field

    Returns:
        List of formatted examples with 'text' field
    """
    formatted = []
    for ex in examples:
        text = format_chatml(
            system_prompt=system_prompt,
            user_message=ex[input_key],
            assistant_response=ex[output_key],
        )
        formatted.append({"text": text})
    return formatted


def create_conversation_dataset(
    examples: list[dict[str, Any]],
    system_prompt: str,
    input_key: str = "input",
    output_key: str = "output",
) -> Dataset:
    """
    Create a HuggingFace Dataset from examples.

    Args:
        examples: List of training examples
        system_prompt: System prompt to use
        input_key: Key for input field
        output_key: Key for output field

    Returns:
        HuggingFace Dataset ready for training
    """
    formatted = format_for_training(examples, system_prompt, input_key, output_key)
    return Dataset.from_list(formatted)


def load_jsonl(file_path: str | Path) -> list[dict[str, Any]]:
    """Load examples from a JSONL file."""
    file_path = Path(file_path)
    examples = []

    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line:
                examples.append(json.loads(line))

    logger.info("loaded_jsonl", file=str(file_path), count=len(examples))
    return examples


def save_jsonl(examples: list[dict[str, Any]], file_path: str | Path) -> Path:
    """Save examples to a JSONL file."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")

    logger.info("saved_jsonl", file=str(file_path), count=len(examples))
    return file_path


def convert_sharegpt_format(
    examples: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """
    Convert ShareGPT format to our internal format.

    ShareGPT format: {"conversations": [{"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}]}

    Args:
        examples: List of ShareGPT format examples

    Returns:
        List of converted examples
    """
    converted = []
    for ex in examples:
        conversations = ex.get("conversations", [])
        if len(conversations) >= 2:
            # Extract first human/gpt pair
            human_turn = next((c for c in conversations if c["from"] == "human"), None)
            gpt_turn = next((c for c in conversations if c["from"] == "gpt"), None)

            if human_turn and gpt_turn:
                converted.append(
                    {
                        "input": human_turn["value"],
                        "output": gpt_turn["value"],
                    }
                )
    return converted


def convert_alpaca_format(
    examples: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """
    Convert Alpaca format to our internal format.

    Alpaca format: {"instruction": "...", "input": "...", "output": "..."}

    Args:
        examples: List of Alpaca format examples

    Returns:
        List of converted examples
    """
    converted = []
    for ex in examples:
        instruction = ex.get("instruction", "")
        input_text = ex.get("input", "")
        output = ex.get("output", "")

        # Combine instruction and input
        if input_text:
            full_input = f"{instruction}\n\n{input_text}"
        else:
            full_input = instruction

        converted.append(
            {
                "input": full_input,
                "output": output,
            }
        )
    return converted


def validate_example(example: dict[str, Any], required_keys: list[str]) -> bool:
    """
    Validate that an example has required keys with non-empty values.

    Args:
        example: The example to validate
        required_keys: List of required keys

    Returns:
        True if valid, False otherwise
    """
    for key in required_keys:
        if key not in example:
            return False
        value = example[key]
        if not value or (isinstance(value, str) and not value.strip()):
            return False
    return True


def split_dataset(
    examples: list[dict[str, Any]],
    train_ratio: float = 0.9,
    shuffle: bool = True,
    seed: int = 42,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Split examples into train and validation sets.

    Args:
        examples: List of examples
        train_ratio: Ratio for training set
        shuffle: Whether to shuffle before splitting
        seed: Random seed for reproducibility

    Returns:
        Tuple of (train_examples, val_examples)
    """
    import random

    if shuffle:
        rng = random.Random(seed)
        examples = examples.copy()
        rng.shuffle(examples)

    split_idx = int(len(examples) * train_ratio)
    train_examples = examples[:split_idx]
    val_examples = examples[split_idx:]

    logger.info(
        "split_dataset",
        total=len(examples),
        train=len(train_examples),
        val=len(val_examples),
    )

    return train_examples, val_examples


class DataFormatter:
    """Main class for formatting training data."""

    def __init__(self, system_prompt: str):
        """
        Initialize the formatter.

        Args:
            system_prompt: Default system prompt to use
        """
        self.system_prompt = system_prompt

    def format_example(
        self,
        input_text: str,
        output_text: str,
        system_prompt: str | None = None,
    ) -> str:
        """Format a single example."""
        return format_chatml(
            system_prompt=system_prompt or self.system_prompt,
            user_message=input_text,
            assistant_response=output_text,
        )

    def format_batch(
        self,
        examples: list[dict[str, Any]],
        input_key: str = "input",
        output_key: str = "output",
    ) -> list[dict[str, str]]:
        """Format a batch of examples."""
        return format_for_training(
            examples=examples,
            system_prompt=self.system_prompt,
            input_key=input_key,
            output_key=output_key,
        )

    def create_dataset(
        self,
        examples: list[dict[str, Any]],
        input_key: str = "input",
        output_key: str = "output",
    ) -> Dataset:
        """Create a HuggingFace Dataset from examples."""
        return create_conversation_dataset(
            examples=examples,
            system_prompt=self.system_prompt,
            input_key=input_key,
            output_key=output_key,
        )
