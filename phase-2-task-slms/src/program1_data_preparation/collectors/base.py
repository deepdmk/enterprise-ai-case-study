"""Base collector for loading training data from various sources."""

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from phase-0-infrastructure
from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


class DataCollector(ABC):
    """Abstract base class for data collectors."""

    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        """Collect data from the source."""
        pass


class CSVCollector(DataCollector):
    """Collect training data from CSV files."""

    def __init__(
        self,
        file_path: str | Path,
        input_column: str = "input",
        output_column: str = "output",
        delimiter: str = ",",
        encoding: str = "utf-8",
    ):
        """
        Initialize CSV collector.

        Args:
            file_path: Path to CSV file
            input_column: Column name for input text
            output_column: Column name for output text
            delimiter: CSV delimiter
            encoding: File encoding
        """
        self.file_path = Path(file_path)
        self.input_column = input_column
        self.output_column = output_column
        self.delimiter = delimiter
        self.encoding = encoding

    def collect(self) -> list[dict[str, Any]]:
        """Load data from CSV file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")

        examples = []
        with open(self.file_path, encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            for row in reader:
                if self.input_column in row and self.output_column in row:
                    examples.append(
                        {
                            "input": row[self.input_column],
                            "output": row[self.output_column],
                            "metadata": {
                                k: v
                                for k, v in row.items()
                                if k not in (self.input_column, self.output_column)
                            },
                        }
                    )

        logger.info("csv_collected", file=str(self.file_path), count=len(examples))
        return examples


class JSONCollector(DataCollector):
    """Collect training data from JSON files."""

    def __init__(
        self,
        file_path: str | Path,
        input_key: str = "input",
        output_key: str = "output",
        data_key: str | None = None,
    ):
        """
        Initialize JSON collector.

        Args:
            file_path: Path to JSON file
            input_key: Key for input text
            output_key: Key for output text
            data_key: Optional key if examples are nested (e.g., "data" or "examples")
        """
        self.file_path = Path(file_path)
        self.input_key = input_key
        self.output_key = output_key
        self.data_key = data_key

    def collect(self) -> list[dict[str, Any]]:
        """Load data from JSON file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.file_path}")

        with open(self.file_path) as f:
            data = json.load(f)

        # Handle nested data
        if self.data_key:
            data = data.get(self.data_key, [])

        # Ensure data is a list
        if isinstance(data, dict):
            data = [data]

        examples = []
        for item in data:
            if self.input_key in item and self.output_key in item:
                examples.append(
                    {
                        "input": item[self.input_key],
                        "output": item[self.output_key],
                        "metadata": {
                            k: v
                            for k, v in item.items()
                            if k not in (self.input_key, self.output_key)
                        },
                    }
                )

        logger.info("json_collected", file=str(self.file_path), count=len(examples))
        return examples


class JSONLCollector(DataCollector):
    """Collect training data from JSONL files."""

    def __init__(
        self,
        file_path: str | Path,
        input_key: str = "input",
        output_key: str = "output",
    ):
        """
        Initialize JSONL collector.

        Args:
            file_path: Path to JSONL file
            input_key: Key for input text
            output_key: Key for output text
        """
        self.file_path = Path(file_path)
        self.input_key = input_key
        self.output_key = output_key

    def collect(self) -> list[dict[str, Any]]:
        """Load data from JSONL file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSONL file not found: {self.file_path}")

        examples = []
        with open(self.file_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                if self.input_key in item and self.output_key in item:
                    examples.append(
                        {
                            "input": item[self.input_key],
                            "output": item[self.output_key],
                            "metadata": {
                                k: v
                                for k, v in item.items()
                                if k not in (self.input_key, self.output_key)
                            },
                        }
                    )

        logger.info("jsonl_collected", file=str(self.file_path), count=len(examples))
        return examples


class DirectoryCollector(DataCollector):
    """Collect training data from all files in a directory."""

    def __init__(
        self,
        directory: str | Path,
        pattern: str = "*.jsonl",
        input_key: str = "input",
        output_key: str = "output",
    ):
        """
        Initialize directory collector.

        Args:
            directory: Directory path
            pattern: Glob pattern for files
            input_key: Key for input text
            output_key: Key for output text
        """
        self.directory = Path(directory)
        self.pattern = pattern
        self.input_key = input_key
        self.output_key = output_key

    def collect(self) -> list[dict[str, Any]]:
        """Load data from all matching files in directory."""
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory not found: {self.directory}")

        all_examples: list[dict[str, Any]] = []
        for file_path in self.directory.glob(self.pattern):
            collector: DataCollector
            if file_path.suffix == ".jsonl":
                collector = JSONLCollector(
                    file_path, self.input_key, self.output_key
                )
            elif file_path.suffix == ".json":
                collector = JSONCollector(
                    file_path, self.input_key, self.output_key
                )
            elif file_path.suffix == ".csv":
                collector = CSVCollector(
                    file_path, self.input_key, self.output_key
                )
            else:
                continue

            all_examples.extend(collector.collect())

        logger.info(
            "directory_collected",
            directory=str(self.directory),
            pattern=self.pattern,
            count=len(all_examples),
        )
        return all_examples


class ShareGPTCollector(DataCollector):
    """Collect training data in ShareGPT format."""

    def __init__(self, file_path: str | Path):
        """
        Initialize ShareGPT collector.

        Args:
            file_path: Path to ShareGPT format JSON/JSONL file
        """
        self.file_path = Path(file_path)

    def collect(self) -> list[dict[str, Any]]:
        """Load data from ShareGPT format file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        # Load data
        if self.file_path.suffix == ".jsonl":
            data = []
            with open(self.file_path) as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
        else:
            with open(self.file_path) as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]

        # Convert ShareGPT format
        examples = []
        for item in data:
            conversations = item.get("conversations", [])
            if len(conversations) >= 2:
                human_turn = next(
                    (c for c in conversations if c.get("from") == "human"), None
                )
                gpt_turn = next(
                    (c for c in conversations if c.get("from") == "gpt"), None
                )
                if human_turn and gpt_turn:
                    examples.append(
                        {
                            "input": human_turn.get("value", ""),
                            "output": gpt_turn.get("value", ""),
                            "metadata": {
                                "format": "sharegpt",
                                "num_turns": len(conversations),
                            },
                        }
                    )

        logger.info("sharegpt_collected", file=str(self.file_path), count=len(examples))
        return examples
