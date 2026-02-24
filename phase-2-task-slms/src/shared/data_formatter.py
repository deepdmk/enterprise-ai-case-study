"""Data formatters for ChatML and instruction formats."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TYPE_CHECKING

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from phase-0-infrastructure
from habitat_logging import get_logger

# Lazy import for Dataset to avoid heavy dependencies at module load time
if TYPE_CHECKING:
    from datasets import Dataset

logger = get_logger(__name__)


# ============================================================================
# CONFIGURABLE CHAT TEMPLATES
# ============================================================================


@dataclass
class ChatTemplate:
    """Configurable chat template for different model families.

    Attributes:
        name: Template name for identification
        bos: Beginning of sequence token
        eos: End of turn/sequence token
        system_start: Token(s) before system message
        system_end: Token(s) after system message (defaults to eos)
        user_start: Token(s) before user message
        user_end: Token(s) after user message (defaults to eos)
        assistant_start: Token(s) before assistant message
        assistant_end: Token(s) after assistant message (defaults to eos)
    """

    name: str
    bos: str
    eos: str
    system_start: str
    user_start: str
    assistant_start: str
    system_end: str | None = None
    user_end: str | None = None
    assistant_end: str | None = None

    def __post_init__(self) -> None:
        """Set defaults for end tokens."""
        if self.system_end is None:
            self.system_end = self.eos
        if self.user_end is None:
            self.user_end = self.eos
        if self.assistant_end is None:
            self.assistant_end = self.eos

    def format_turn(self, role: str, content: str) -> str:
        """Format a single conversation turn."""
        if role == "system":
            return f"{self.system_start}\n\n{content}{self.system_end}"
        elif role in ("user", "human"):
            return f"{self.user_start}\n\n{content}{self.user_end}"
        elif role in ("assistant", "gpt"):
            return f"{self.assistant_start}\n\n{content}{self.assistant_end}"
        else:
            raise ValueError(f"Unknown role: {role}")

    def format_example(
        self,
        system_prompt: str,
        user_message: str,
        assistant_response: str,
    ) -> str:
        """Format a complete example with system, user, and assistant."""
        parts = [self.bos]
        parts.append(self.format_turn("system", system_prompt.strip()))
        parts.append(self.format_turn("user", user_message.strip()))
        parts.append(self.format_turn("assistant", assistant_response.strip()))
        return "".join(parts)


# Pre-defined templates for common model families
LLAMA3_TEMPLATE = ChatTemplate(
    name="llama3",
    bos="<|begin_of_text|>",
    eos="<|eot_id|>",
    system_start="<|start_header_id|>system<|end_header_id|>",
    user_start="<|start_header_id|>user<|end_header_id|>",
    assistant_start="<|start_header_id|>assistant<|end_header_id|>",
)

CHATML_STANDARD_TEMPLATE = ChatTemplate(
    name="chatml",
    bos="",
    eos="<|im_end|>\n",
    system_start="<|im_start|>system\n",
    user_start="<|im_start|>user\n",
    assistant_start="<|im_start|>assistant\n",
)

MISTRAL_TEMPLATE = ChatTemplate(
    name="mistral",
    bos="<s>",
    eos="</s>",
    system_start="[INST] ",
    system_end=" ",
    user_start="",
    user_end=" [/INST]",
    assistant_start="",
)

QWEN_TEMPLATE = ChatTemplate(
    name="qwen",
    bos="",
    eos="<|im_end|>\n",
    system_start="<|im_start|>system\n",
    user_start="<|im_start|>user\n",
    assistant_start="<|im_start|>assistant\n",
)

# Template registry for easy lookup by name
CHAT_TEMPLATES: dict[str, ChatTemplate] = {
    "llama3": LLAMA3_TEMPLATE,
    "llama3.1": LLAMA3_TEMPLATE,  # Alias
    "chatml": CHATML_STANDARD_TEMPLATE,
    "mistral": MISTRAL_TEMPLATE,
    "qwen": QWEN_TEMPLATE,
    "qwen2": QWEN_TEMPLATE,  # Alias
    "qwen2.5": QWEN_TEMPLATE,  # Alias
}


def get_chat_template(name: str) -> ChatTemplate:
    """Get a chat template by name.

    Args:
        name: Template name (e.g., "llama3", "chatml", "mistral", "qwen")

    Returns:
        ChatTemplate instance

    Raises:
        ValueError: If template name is not found
    """
    name_lower = name.lower()
    if name_lower not in CHAT_TEMPLATES:
        available = ", ".join(CHAT_TEMPLATES.keys())
        raise ValueError(f"Unknown chat template: {name}. Available: {available}")
    return CHAT_TEMPLATES[name_lower]


# Default template - Llama 3.1 for this project
_default_template: ChatTemplate = LLAMA3_TEMPLATE


def set_default_template(template: ChatTemplate | str) -> None:
    """Set the default chat template for the module.

    Args:
        template: ChatTemplate instance or template name string
    """
    global _default_template
    if isinstance(template, str):
        template = get_chat_template(template)
    _default_template = template
    logger.info("default_template_set", template=template.name)


def get_default_template() -> ChatTemplate:
    """Get the current default chat template."""
    return _default_template


# ============================================================================
# BACKWARD COMPATIBILITY - Legacy constants
# ============================================================================

# ChatML template for Llama 3.1 (legacy format string)
CHATML_TEMPLATE = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{assistant}<|eot_id|>"""

# Llama 3.1 specific tokens (legacy dict format)
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
) -> "Dataset":
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
    from datasets import Dataset  # Lazy import to avoid heavy dependency at module load

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
    """Main class for formatting training data.

    Supports configurable chat templates for different model families.
    Defaults to Llama 3.1 template for backward compatibility.
    """

    def __init__(
        self,
        system_prompt: str,
        template: ChatTemplate | str | None = None,
    ):
        """
        Initialize the formatter.

        Args:
            system_prompt: Default system prompt to use
            template: Chat template to use. Can be:
                - ChatTemplate instance
                - Template name string (e.g., "llama3", "mistral", "qwen")
                - None to use the module default (Llama 3.1)
        """
        self.system_prompt = system_prompt

        if template is None:
            self.template = get_default_template()
        elif isinstance(template, str):
            self.template = get_chat_template(template)
        else:
            self.template = template

    def format_example(
        self,
        input_text: str,
        output_text: str,
        system_prompt: str | None = None,
    ) -> str:
        """Format a single example using the configured template."""
        return self.template.format_example(
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
        """Format a batch of examples using the configured template."""
        formatted = []
        for ex in examples:
            text = self.format_example(
                input_text=ex[input_key],
                output_text=ex[output_key],
            )
            formatted.append({"text": text})
        return formatted

    def create_dataset(
        self,
        examples: list[dict[str, Any]],
        input_key: str = "input",
        output_key: str = "output",
    ) -> "Dataset":
        """Create a HuggingFace Dataset from examples."""
        from datasets import Dataset  # Lazy import

        formatted = self.format_batch(examples, input_key, output_key)
        return Dataset.from_list(formatted)
