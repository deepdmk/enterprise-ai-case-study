"""Tests for data formatters."""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import formatters using direct file import
import importlib.util
spec = importlib.util.spec_from_file_location(
    "data_formatter",
    project_root / "src" / "shared" / "data_formatter.py"
)
formatter_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(formatter_module)

format_chatml = formatter_module.format_chatml
format_conversation = formatter_module.format_conversation
format_for_training = formatter_module.format_for_training
DataFormatter = formatter_module.DataFormatter
load_jsonl = formatter_module.load_jsonl
save_jsonl = formatter_module.save_jsonl
split_dataset = formatter_module.split_dataset
validate_example = formatter_module.validate_example
convert_sharegpt_format = formatter_module.convert_sharegpt_format
convert_alpaca_format = formatter_module.convert_alpaca_format


class TestFormatChatML:
    """Tests for format_chatml function."""

    def test_basic_formatting(self):
        """Test basic ChatML formatting."""
        result = format_chatml(
            system_prompt="You are a helpful assistant.",
            user_message="What is the weather?",
            assistant_response="I can help with that."
        )

        assert "<|begin_of_text|>" in result
        assert "<|start_header_id|>system<|end_header_id|>" in result
        assert "<|start_header_id|>user<|end_header_id|>" in result
        assert "<|start_header_id|>assistant<|end_header_id|>" in result
        assert "<|eot_id|>" in result
        assert "You are a helpful assistant." in result
        assert "What is the weather?" in result
        assert "I can help with that." in result

    def test_whitespace_stripping(self):
        """Test that whitespace is stripped from inputs."""
        result = format_chatml(
            system_prompt="  System prompt with spaces  ",
            user_message="\nUser message with newlines\n",
            assistant_response="  Response  "
        )

        assert "  System prompt with spaces  " not in result
        assert "System prompt with spaces" in result

    def test_empty_strings(self):
        """Test handling of empty strings."""
        result = format_chatml(
            system_prompt="",
            user_message="User message",
            assistant_response="Response"
        )

        assert "<|begin_of_text|>" in result


class TestFormatConversation:
    """Tests for format_conversation function."""

    def test_multi_turn_conversation(self):
        """Test formatting multi-turn conversations."""
        conversations = [
            {"from": "human", "value": "Hello"},
            {"from": "gpt", "value": "Hi there!"},
            {"from": "human", "value": "How are you?"},
            {"from": "gpt", "value": "I'm doing well!"},
        ]

        result = format_conversation(conversations)

        assert result.count("<|start_header_id|>user<|end_header_id|>") == 2
        assert result.count("<|start_header_id|>assistant<|end_header_id|>") == 2

    def test_with_system_prompt(self):
        """Test formatting with system prompt."""
        conversations = [
            {"from": "human", "value": "Hello"},
            {"from": "gpt", "value": "Hi!"},
        ]

        result = format_conversation(conversations, system_prompt="Be helpful.")

        assert "<|start_header_id|>system<|end_header_id|>" in result
        assert "Be helpful." in result

    def test_alternative_role_names(self):
        """Test handling of alternative role names (user/assistant)."""
        conversations = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"},
        ]

        result = format_conversation(conversations)

        assert "Hello" in result
        assert "Hi!" in result


class TestFormatForTraining:
    """Tests for format_for_training function."""

    def test_basic_formatting(self):
        """Test basic training data formatting."""
        examples = [
            {"input": "Question 1", "output": "Answer 1"},
            {"input": "Question 2", "output": "Answer 2"},
        ]

        result = format_for_training(examples, system_prompt="You are helpful.")

        assert len(result) == 2
        assert all("text" in ex for ex in result)
        assert "You are helpful." in result[0]["text"]
        assert "Question 1" in result[0]["text"]

    def test_custom_keys(self):
        """Test formatting with custom input/output keys."""
        examples = [
            {"question": "What is AI?", "answer": "AI is artificial intelligence."},
        ]

        result = format_for_training(
            examples,
            system_prompt="Expert",
            input_key="question",
            output_key="answer"
        )

        assert "What is AI?" in result[0]["text"]
        assert "AI is artificial intelligence." in result[0]["text"]


class TestDataFormatterClass:
    """Tests for DataFormatter class."""

    @pytest.fixture
    def formatter(self):
        """Create a formatter instance."""
        return DataFormatter(system_prompt="You are a test assistant.")

    def test_format_example(self, formatter):
        """Test formatting a single example."""
        result = formatter.format_example(
            input_text="Test input",
            output_text="Test output"
        )

        assert "You are a test assistant." in result
        assert "Test input" in result
        assert "Test output" in result

    def test_format_example_override_system_prompt(self, formatter):
        """Test overriding system prompt for single example."""
        result = formatter.format_example(
            input_text="Test input",
            output_text="Test output",
            system_prompt="Override prompt"
        )

        assert "Override prompt" in result
        assert "You are a test assistant." not in result

    def test_format_batch(self, formatter):
        """Test formatting a batch of examples."""
        examples = [
            {"input": "Input 1", "output": "Output 1"},
            {"input": "Input 2", "output": "Output 2"},
        ]

        result = formatter.format_batch(examples)

        assert len(result) == 2
        assert all("text" in ex for ex in result)


class TestLoadSaveJsonl:
    """Tests for JSONL I/O functions."""

    def test_load_jsonl(self, temp_dir):
        """Test loading JSONL file."""
        jsonl_path = temp_dir / "test.jsonl"
        with open(jsonl_path, "w") as f:
            f.write('{"a": 1}\n')
            f.write('{"b": 2}\n')

        result = load_jsonl(jsonl_path)

        assert len(result) == 2
        assert result[0]["a"] == 1
        assert result[1]["b"] == 2

    def test_load_jsonl_with_blanks(self, temp_dir):
        """Test loading JSONL with blank lines."""
        jsonl_path = temp_dir / "test.jsonl"
        with open(jsonl_path, "w") as f:
            f.write('{"a": 1}\n')
            f.write('\n')
            f.write('{"b": 2}\n')
            f.write('   \n')

        result = load_jsonl(jsonl_path)

        assert len(result) == 2

    def test_save_jsonl(self, temp_dir):
        """Test saving JSONL file."""
        jsonl_path = temp_dir / "output.jsonl"
        examples = [{"a": 1}, {"b": 2}]

        save_jsonl(examples, jsonl_path)

        assert jsonl_path.exists()
        with open(jsonl_path) as f:
            lines = f.readlines()
        assert len(lines) == 2

    def test_save_jsonl_creates_parent_dirs(self, temp_dir):
        """Test that save_jsonl creates parent directories."""
        jsonl_path = temp_dir / "nested" / "dir" / "output.jsonl"

        save_jsonl([{"test": 1}], jsonl_path)

        assert jsonl_path.exists()

    def test_roundtrip(self, temp_dir):
        """Test save and load roundtrip."""
        jsonl_path = temp_dir / "roundtrip.jsonl"
        original = [
            {"input": "Test input 1", "output": "Test output 1"},
            {"input": "Test input 2", "output": "Test output 2"},
        ]

        save_jsonl(original, jsonl_path)
        loaded = load_jsonl(jsonl_path)

        assert loaded == original


class TestSplitDataset:
    """Tests for split_dataset function."""

    def test_basic_split(self):
        """Test basic dataset splitting."""
        examples = [{"id": i} for i in range(100)]

        train, val = split_dataset(examples, train_ratio=0.8)

        assert len(train) == 80
        assert len(val) == 20

    def test_deterministic_with_seed(self):
        """Test that splitting is deterministic with same seed."""
        examples = [{"id": i} for i in range(100)]

        train1, val1 = split_dataset(examples, seed=42)
        train2, val2 = split_dataset(examples, seed=42)

        assert train1 == train2
        assert val1 == val2

    def test_different_seeds(self):
        """Test that different seeds produce different results."""
        examples = [{"id": i} for i in range(100)]

        train1, _ = split_dataset(examples, seed=42)
        train2, _ = split_dataset(examples, seed=123)

        assert train1 != train2

    def test_no_shuffle(self):
        """Test splitting without shuffling."""
        examples = [{"id": i} for i in range(10)]

        train, val = split_dataset(examples, train_ratio=0.8, shuffle=False)

        # Should maintain order
        assert train[0]["id"] == 0
        assert val[0]["id"] == 8

    def test_edge_ratios(self):
        """Test edge case ratios."""
        examples = [{"id": i} for i in range(10)]

        # All train
        train, val = split_dataset(examples, train_ratio=1.0)
        assert len(train) == 10
        assert len(val) == 0

        # All val
        train, val = split_dataset(examples, train_ratio=0.0)
        assert len(train) == 0
        assert len(val) == 10


class TestValidateExample:
    """Tests for validate_example function."""

    def test_valid_example(self):
        """Test validation of valid example."""
        example = {"input": "Valid input", "output": "Valid output"}

        assert validate_example(example, ["input", "output"]) is True

    def test_missing_key(self):
        """Test validation with missing key."""
        example = {"input": "Only input"}

        assert validate_example(example, ["input", "output"]) is False

    def test_empty_value(self):
        """Test validation with empty value."""
        example = {"input": "", "output": "Valid output"}

        assert validate_example(example, ["input", "output"]) is False

    def test_whitespace_only_value(self):
        """Test validation with whitespace-only value."""
        example = {"input": "   ", "output": "Valid output"}

        assert validate_example(example, ["input", "output"]) is False


class TestConvertShareGPTFormat:
    """Tests for convert_sharegpt_format function."""

    def test_basic_conversion(self):
        """Test basic ShareGPT format conversion."""
        examples = [
            {
                "conversations": [
                    {"from": "human", "value": "Hello"},
                    {"from": "gpt", "value": "Hi there!"},
                ]
            }
        ]

        result = convert_sharegpt_format(examples)

        assert len(result) == 1
        assert result[0]["input"] == "Hello"
        assert result[0]["output"] == "Hi there!"

    def test_incomplete_conversation(self):
        """Test handling of incomplete conversations."""
        examples = [
            {"conversations": [{"from": "human", "value": "Hello"}]},  # Missing gpt
            {"conversations": []},  # Empty
        ]

        result = convert_sharegpt_format(examples)

        assert len(result) == 0


class TestConvertAlpacaFormat:
    """Tests for convert_alpaca_format function."""

    def test_basic_conversion(self):
        """Test basic Alpaca format conversion."""
        examples = [
            {
                "instruction": "Summarize this text.",
                "input": "Long text here.",
                "output": "Summary of the text."
            }
        ]

        result = convert_alpaca_format(examples)

        assert len(result) == 1
        assert "Summarize this text." in result[0]["input"]
        assert "Long text here." in result[0]["input"]
        assert result[0]["output"] == "Summary of the text."

    def test_instruction_only(self):
        """Test conversion with empty input field."""
        examples = [
            {
                "instruction": "What is the capital of France?",
                "input": "",
                "output": "Paris"
            }
        ]

        result = convert_alpaca_format(examples)

        assert result[0]["input"] == "What is the capital of France?"
        assert result[0]["output"] == "Paris"
