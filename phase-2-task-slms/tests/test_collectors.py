"""Tests for data collectors."""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import collectors using direct file import to avoid __init__.py dependencies
import importlib.util
spec = importlib.util.spec_from_file_location(
    "base",
    project_root / "src" / "program1_data_preparation" / "collectors" / "base.py"
)
collectors_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collectors_module)

CSVCollector = collectors_module.CSVCollector
JSONCollector = collectors_module.JSONCollector
JSONLCollector = collectors_module.JSONLCollector
DirectoryCollector = collectors_module.DirectoryCollector
ShareGPTCollector = collectors_module.ShareGPTCollector


class TestCSVCollector:
    """Tests for CSVCollector."""

    def test_collect_valid_csv(self, sample_csv_file):
        """Test collecting data from a valid CSV file."""
        collector = CSVCollector(sample_csv_file)
        examples = collector.collect()

        assert len(examples) == 3
        assert all("input" in ex for ex in examples)
        assert all("output" in ex for ex in examples)
        assert examples[0]["input"] == "What is investor A's portfolio?"

    def test_collect_with_metadata(self, sample_csv_file):
        """Test that extra columns are captured as metadata."""
        collector = CSVCollector(sample_csv_file)
        examples = collector.collect()

        assert all("metadata" in ex for ex in examples)
        assert examples[0]["metadata"]["category"] == "energy"

    def test_collect_custom_columns(self, temp_dir):
        """Test collecting with custom column names."""
        csv_content = 'question,answer\n"Custom input","Custom output"'
        csv_path = temp_dir / "custom.csv"
        csv_path.write_text(csv_content)

        collector = CSVCollector(
            csv_path,
            input_column="question",
            output_column="answer"
        )
        examples = collector.collect()

        assert len(examples) == 1
        assert examples[0]["input"] == "Custom input"
        assert examples[0]["output"] == "Custom output"

    def test_collect_nonexistent_file(self, temp_dir):
        """Test error handling for nonexistent file."""
        collector = CSVCollector(temp_dir / "nonexistent.csv")

        with pytest.raises(FileNotFoundError):
            collector.collect()

    def test_collect_missing_columns(self, temp_dir):
        """Test handling of CSV with missing required columns."""
        csv_content = 'other_col,another_col\n"value1","value2"'
        csv_path = temp_dir / "missing_cols.csv"
        csv_path.write_text(csv_content)

        collector = CSVCollector(csv_path)
        examples = collector.collect()

        # Should return empty list when required columns are missing
        assert len(examples) == 0


class TestJSONCollector:
    """Tests for JSONCollector."""

    def test_collect_valid_json(self, sample_json_file):
        """Test collecting data from a valid JSON file."""
        collector = JSONCollector(sample_json_file)
        examples = collector.collect()

        assert len(examples) == 2
        assert all("input" in ex for ex in examples)
        assert all("output" in ex for ex in examples)

    def test_collect_with_metadata(self, sample_json_file):
        """Test that extra fields are captured as metadata."""
        collector = JSONCollector(sample_json_file)
        examples = collector.collect()

        assert examples[0]["metadata"]["source"] == "manual"

    def test_collect_nested_data(self, temp_dir):
        """Test collecting from nested JSON structure."""
        nested_data = {
            "data": [
                {"input": "Nested input content for testing", "output": "Nested output content for testing"}
            ],
            "metadata": {"version": "1.0"}
        }
        json_path = temp_dir / "nested.json"
        json_path.write_text(json.dumps(nested_data))

        collector = JSONCollector(json_path, data_key="data")
        examples = collector.collect()

        assert len(examples) == 1
        assert examples[0]["input"] == "Nested input content for testing"

    def test_collect_single_object(self, temp_dir):
        """Test collecting from a single JSON object (not array)."""
        single_data = {"input": "Single object input", "output": "Single object output"}
        json_path = temp_dir / "single.json"
        json_path.write_text(json.dumps(single_data))

        collector = JSONCollector(json_path)
        examples = collector.collect()

        assert len(examples) == 1

    def test_collect_nonexistent_file(self, temp_dir):
        """Test error handling for nonexistent file."""
        collector = JSONCollector(temp_dir / "nonexistent.json")

        with pytest.raises(FileNotFoundError):
            collector.collect()


class TestJSONLCollector:
    """Tests for JSONLCollector."""

    def test_collect_valid_jsonl(self, sample_jsonl_file):
        """Test collecting data from a valid JSONL file."""
        collector = JSONLCollector(sample_jsonl_file)
        examples = collector.collect()

        assert len(examples) == 3
        assert all("input" in ex for ex in examples)
        assert all("output" in ex for ex in examples)

    def test_collect_with_blank_lines(self, temp_dir):
        """Test handling of JSONL with blank lines."""
        jsonl_path = temp_dir / "with_blanks.jsonl"
        with open(jsonl_path, "w") as f:
            f.write('{"input": "First line input content", "output": "First line output"}\n')
            f.write('\n')  # Blank line
            f.write('{"input": "Second line input content", "output": "Second line output"}\n')
            f.write('   \n')  # Whitespace-only line

        collector = JSONLCollector(jsonl_path)
        examples = collector.collect()

        assert len(examples) == 2

    def test_collect_nonexistent_file(self, temp_dir):
        """Test error handling for nonexistent file."""
        collector = JSONLCollector(temp_dir / "nonexistent.jsonl")

        with pytest.raises(FileNotFoundError):
            collector.collect()

    def test_collect_custom_keys(self, temp_dir):
        """Test collecting with custom key names."""
        jsonl_path = temp_dir / "custom_keys.jsonl"
        with open(jsonl_path, "w") as f:
            f.write('{"question": "Custom key input", "answer": "Custom key output"}\n')

        collector = JSONLCollector(
            jsonl_path,
            input_key="question",
            output_key="answer"
        )
        examples = collector.collect()

        assert len(examples) == 1
        assert examples[0]["input"] == "Custom key input"


class TestDirectoryCollector:
    """Tests for DirectoryCollector."""

    def test_collect_multiple_files(self, temp_dir, sample_jsonl_file, sample_json_file):
        """Test collecting from multiple files in a directory."""
        # Copy files to temp_dir
        import shutil
        shutil.copy(sample_jsonl_file, temp_dir / "data1.jsonl")

        collector = DirectoryCollector(temp_dir, pattern="*.jsonl")
        examples = collector.collect()

        assert len(examples) >= 3  # At least from the JSONL file

    def test_collect_mixed_formats(self, temp_dir):
        """Test collecting from mixed file formats."""
        # Create a JSONL file
        jsonl_path = temp_dir / "data.jsonl"
        with open(jsonl_path, "w") as f:
            f.write('{"input": "JSONL input with enough content", "output": "JSONL output with enough content"}\n')

        # Create a JSON file
        json_path = temp_dir / "data.json"
        json_data = [{"input": "JSON input with enough content", "output": "JSON output with enough content"}]
        json_path.write_text(json.dumps(json_data))

        # Create a CSV file
        csv_path = temp_dir / "data.csv"
        csv_path.write_text("input,output\n\"CSV input with enough content\",\"CSV output with enough content\"")

        collector = DirectoryCollector(temp_dir, pattern="*.*")
        examples = collector.collect()

        assert len(examples) == 3  # One from each file

    def test_collect_nonexistent_directory(self, temp_dir):
        """Test error handling for nonexistent directory."""
        collector = DirectoryCollector(temp_dir / "nonexistent")

        with pytest.raises(FileNotFoundError):
            collector.collect()

    def test_collect_empty_directory(self, temp_dir):
        """Test collecting from an empty directory."""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()

        collector = DirectoryCollector(empty_dir)
        examples = collector.collect()

        assert len(examples) == 0


class TestShareGPTCollector:
    """Tests for ShareGPTCollector."""

    def test_collect_valid_sharegpt(self, sample_sharegpt_file):
        """Test collecting data from valid ShareGPT format."""
        collector = ShareGPTCollector(sample_sharegpt_file)
        examples = collector.collect()

        assert len(examples) == 2
        assert all("input" in ex for ex in examples)
        assert all("output" in ex for ex in examples)
        assert examples[0]["metadata"]["format"] == "sharegpt"

    def test_collect_sharegpt_jsonl(self, temp_dir):
        """Test collecting from ShareGPT JSONL format."""
        jsonl_path = temp_dir / "sharegpt.jsonl"
        with open(jsonl_path, "w") as f:
            f.write(json.dumps({
                "conversations": [
                    {"from": "human", "value": "JSONL ShareGPT input"},
                    {"from": "gpt", "value": "JSONL ShareGPT output"}
                ]
            }) + "\n")

        collector = ShareGPTCollector(jsonl_path)
        examples = collector.collect()

        assert len(examples) == 1

    def test_collect_incomplete_conversation(self, temp_dir):
        """Test handling of incomplete conversations."""
        data = [
            {"conversations": [{"from": "human", "value": "Only human turn"}]},  # Missing gpt
            {"conversations": []},  # Empty conversations
        ]
        file_path = temp_dir / "incomplete.json"
        file_path.write_text(json.dumps(data))

        collector = ShareGPTCollector(file_path)
        examples = collector.collect()

        # Should skip incomplete conversations
        assert len(examples) == 0

    def test_collect_nonexistent_file(self, temp_dir):
        """Test error handling for nonexistent file."""
        collector = ShareGPTCollector(temp_dir / "nonexistent.json")

        with pytest.raises(FileNotFoundError):
            collector.collect()
