"""Data quality validators for training examples."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from phase-0-infrastructure
from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationResult:
    """Result of validating a training example."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Aggregate validation report for a dataset."""

    total_examples: int = 0
    valid_examples: int = 0
    invalid_examples: int = 0
    error_counts: dict[str, int] = field(default_factory=dict)
    warning_counts: dict[str, int] = field(default_factory=dict)

    @property
    def validation_rate(self) -> float:
        """Get validation success rate."""
        if self.total_examples == 0:
            return 0.0
        return self.valid_examples / self.total_examples


class DataValidator:
    """Validator for training data quality."""

    def __init__(
        self,
        min_input_length: int = 10,
        max_input_length: int = 4000,
        min_output_length: int = 20,
        max_output_length: int = 8000,
        required_output_sections: list[str] | None = None,
        banned_phrases: list[str] | None = None,
    ):
        """
        Initialize the validator.

        Args:
            min_input_length: Minimum input character length
            max_input_length: Maximum input character length
            min_output_length: Minimum output character length
            max_output_length: Maximum output character length
            required_output_sections: Sections that must appear in output
            banned_phrases: Phrases that should not appear
        """
        self.min_input_length = min_input_length
        self.max_input_length = max_input_length
        self.min_output_length = min_output_length
        self.max_output_length = max_output_length
        self.required_output_sections = required_output_sections or []
        self.banned_phrases = banned_phrases or []

    def validate_example(self, example: dict[str, Any]) -> ValidationResult:
        """
        Validate a single training example.

        Args:
            example: Example with 'input' and 'output' keys

        Returns:
            ValidationResult with errors and warnings
        """
        errors: list[str] = []
        warnings: list[str] = []

        input_text = example.get("input", "")
        output_text = example.get("output", "")

        # Check for missing fields
        if not input_text:
            errors.append("missing_input")
        if not output_text:
            errors.append("missing_output")

        if errors:
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # Check input length
        input_len = len(input_text)
        if input_len < self.min_input_length:
            errors.append(f"input_too_short:{input_len}")
        elif input_len > self.max_input_length:
            errors.append(f"input_too_long:{input_len}")

        # Check output length
        output_len = len(output_text)
        if output_len < self.min_output_length:
            errors.append(f"output_too_short:{output_len}")
        elif output_len > self.max_output_length:
            warnings.append(f"output_very_long:{output_len}")

        # Check required sections
        for section in self.required_output_sections:
            if section.lower() not in output_text.lower():
                warnings.append(f"missing_section:{section}")

        # Check banned phrases
        combined_text = (input_text + output_text).lower()
        for phrase in self.banned_phrases:
            if phrase.lower() in combined_text:
                errors.append(f"banned_phrase:{phrase}")

        # Check for quality issues
        if input_text == output_text:
            errors.append("input_equals_output")

        if output_text.strip().startswith(input_text.strip()[:50]):
            warnings.append("output_starts_with_input")

        # Check for placeholder patterns
        placeholder_patterns = ["[INSERT", "{TODO", "PLACEHOLDER", "XXX", "###"]
        for pattern in placeholder_patterns:
            if pattern in output_text.upper():
                warnings.append(f"placeholder_found:{pattern}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def validate_dataset(
        self,
        examples: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], ValidationReport]:
        """
        Validate a full dataset and return valid examples.

        Args:
            examples: List of training examples

        Returns:
            Tuple of (valid_examples, validation_report)
        """
        valid_examples = []
        report = ValidationReport(total_examples=len(examples))

        for example in examples:
            result = self.validate_example(example)

            if result.is_valid:
                report.valid_examples += 1
                valid_examples.append(example)
            else:
                report.invalid_examples += 1

            # Count errors
            for error in result.errors:
                error_type = error.split(":")[0]
                report.error_counts[error_type] = (
                    report.error_counts.get(error_type, 0) + 1
                )

            # Count warnings
            for warning in result.warnings:
                warning_type = warning.split(":")[0]
                report.warning_counts[warning_type] = (
                    report.warning_counts.get(warning_type, 0) + 1
                )

        logger.info(
            "dataset_validated",
            total=report.total_examples,
            valid=report.valid_examples,
            invalid=report.invalid_examples,
            validation_rate=f"{report.validation_rate:.1%}",
        )

        return valid_examples, report


class DuplicateDetector:
    """Detect and remove duplicate examples.

    Currently implements exact hash-based deduplication. The similarity_threshold
    parameter is reserved for future fuzzy/near-duplicate detection using techniques
    like MinHash, SimHash, or embedding similarity.
    """

    def __init__(self, similarity_threshold: float = 0.95):
        """
        Initialize duplicate detector.

        Args:
            similarity_threshold: Threshold for considering examples duplicates.
                Currently unused - only exact matching is implemented.
                Reserved for future fuzzy matching implementation.
        """
        # Note: similarity_threshold is stored for API compatibility but currently unused.
        # Only exact hash-based deduplication is implemented.
        self._similarity_threshold = similarity_threshold
        self._seen_hashes: set[int] = set()

    def _hash_example(self, example: dict[str, Any]) -> int:
        """Create a hash for an example."""
        text = f"{example.get('input', '')}|||{example.get('output', '')}"
        return hash(text)

    def is_duplicate(self, example: dict[str, Any]) -> bool:
        """Check if an example is a duplicate."""
        h = self._hash_example(example)
        if h in self._seen_hashes:
            return True
        self._seen_hashes.add(h)
        return False

    def deduplicate(
        self,
        examples: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], int]:
        """
        Remove duplicates from a dataset.

        Args:
            examples: List of training examples

        Returns:
            Tuple of (deduplicated_examples, num_duplicates_removed)
        """
        self._seen_hashes.clear()
        deduplicated = []
        duplicates = 0

        for example in examples:
            if not self.is_duplicate(example):
                deduplicated.append(example)
            else:
                duplicates += 1

        logger.info(
            "deduplication_complete",
            original=len(examples),
            deduplicated=len(deduplicated),
            duplicates_removed=duplicates,
        )

        return deduplicated, duplicates


def validate_and_deduplicate(
    examples: list[dict[str, Any]],
    validator: DataValidator | None = None,
    deduplicate: bool = True,
) -> tuple[list[dict[str, Any]], ValidationReport, int]:
    """
    Validate and optionally deduplicate a dataset.

    Args:
        examples: List of training examples
        validator: DataValidator instance (creates default if not provided)
        deduplicate: Whether to remove duplicates

    Returns:
        Tuple of (clean_examples, validation_report, duplicates_removed)
    """
    validator = validator or DataValidator()

    # Validate
    valid_examples, report = validator.validate_dataset(examples)

    # Deduplicate
    duplicates_removed = 0
    if deduplicate:
        detector = DuplicateDetector()
        valid_examples, duplicates_removed = detector.deduplicate(valid_examples)

    return valid_examples, report, duplicates_removed
