"""Tests for data validators."""

import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import validators using direct file import
import importlib.util
spec = importlib.util.spec_from_file_location(
    "quality",
    project_root / "src" / "program1_data_preparation" / "validators" / "quality.py"
)
validators_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validators_module)

DataValidator = validators_module.DataValidator
DuplicateDetector = validators_module.DuplicateDetector
ValidationResult = validators_module.ValidationResult
ValidationReport = validators_module.ValidationReport
validate_and_deduplicate = validators_module.validate_and_deduplicate


class TestDataValidator:
    """Tests for DataValidator."""

    @pytest.fixture
    def validator(self):
        """Create a default validator instance."""
        return DataValidator(
            min_input_length=10,
            max_input_length=1000,
            min_output_length=20,
            max_output_length=2000,
        )

    def test_validate_valid_example(self, validator, valid_examples):
        """Test validation of a valid example."""
        result = validator.validate_example(valid_examples[0])

        assert result.is_valid
        assert len(result.errors) == 0

    def test_validate_missing_input(self, validator):
        """Test validation fails for missing input."""
        example = {"input": "", "output": "Valid output content that is long enough."}
        result = validator.validate_example(example)

        assert not result.is_valid
        assert "missing_input" in result.errors

    def test_validate_missing_output(self, validator):
        """Test validation fails for missing output."""
        example = {"input": "Valid input content that is long enough.", "output": ""}
        result = validator.validate_example(example)

        assert not result.is_valid
        assert "missing_output" in result.errors

    def test_validate_input_too_short(self, validator):
        """Test validation fails for input that's too short."""
        example = {"input": "Short", "output": "Valid output content that meets minimum length."}
        result = validator.validate_example(example)

        assert not result.is_valid
        assert any("input_too_short" in e for e in result.errors)

    def test_validate_input_too_long(self, validator):
        """Test validation fails for input that's too long."""
        example = {
            "input": "x" * 1001,  # Exceeds max_input_length
            "output": "Valid output content that meets minimum length requirements."
        }
        result = validator.validate_example(example)

        assert not result.is_valid
        assert any("input_too_long" in e for e in result.errors)

    def test_validate_output_too_short(self, validator):
        """Test validation fails for output that's too short."""
        example = {"input": "Valid input content that is long enough.", "output": "Too short"}
        result = validator.validate_example(example)

        assert not result.is_valid
        assert any("output_too_short" in e for e in result.errors)

    def test_validate_output_very_long_warning(self):
        """Test validation warns for very long output."""
        validator = DataValidator(max_output_length=50)
        example = {
            "input": "Valid input content that is long enough.",
            "output": "This output is longer than the maximum configured length for testing warnings."
        }
        result = validator.validate_example(example)

        # Should be valid but with a warning
        assert result.is_valid
        assert any("output_very_long" in w for w in result.warnings)

    def test_validate_identical_input_output(self, validator):
        """Test validation fails when input equals output."""
        example = {
            "input": "This is the exact same content.",
            "output": "This is the exact same content."
        }
        result = validator.validate_example(example)

        assert not result.is_valid
        assert "input_equals_output" in result.errors

    def test_validate_required_sections(self):
        """Test validation checks for required output sections."""
        validator = DataValidator(
            required_output_sections=["## Summary", "## Analysis"]
        )
        example = {
            "input": "Analyze this data for me please.",
            "output": "## Summary\nHere is the summary.\n\n## Analysis\nHere is the analysis."
        }
        result = validator.validate_example(example)

        assert result.is_valid

    def test_validate_missing_required_sections(self):
        """Test validation warns about missing required sections."""
        validator = DataValidator(
            required_output_sections=["## Summary", "## Missing Section"]
        )
        example = {
            "input": "Analyze this data for me please.",
            "output": "## Summary\nHere is the summary without the required missing section."
        }
        result = validator.validate_example(example)

        # Still valid but with warnings
        assert result.is_valid
        assert any("missing_section" in w for w in result.warnings)

    def test_validate_banned_phrases(self):
        """Test validation fails for banned phrases."""
        validator = DataValidator(banned_phrases=["confidential", "secret"])
        example = {
            "input": "Tell me the confidential information.",
            "output": "Here is the confidential data that was requested by the user."
        }
        result = validator.validate_example(example)

        assert not result.is_valid
        assert any("banned_phrase" in e for e in result.errors)

    def test_validate_placeholder_warning(self, validator):
        """Test validation warns about placeholder patterns."""
        example = {
            "input": "Generate a report for me please.",
            "output": "Here is the report. [INSERT ADDITIONAL DATA HERE] for completion."
        }
        result = validator.validate_example(example)

        assert any("placeholder_found" in w for w in result.warnings)

    def test_validate_output_starts_with_input_warning(self, validator):
        """Test validation warns when output starts with input."""
        example = {
            "input": "What is the market analysis for renewable energy?",
            "output": "What is the market analysis for renewable energy? Here is my analysis..."
        }
        result = validator.validate_example(example)

        # Should warn but not fail
        assert any("output_starts_with_input" in w for w in result.warnings)

    def test_validate_case_insensitive_sections(self):
        """Test that section matching is case-insensitive."""
        validator = DataValidator(
            required_output_sections=["## Investment Thesis"]
        )
        example = {
            "input": "Analyze the investment opportunity.",
            "output": "## investment thesis\nThis is a good investment opportunity for growth."
        }
        result = validator.validate_example(example)

        # Should find the section despite case difference
        assert not any("missing_section:## Investment Thesis" in w for w in result.warnings)


class TestDataValidatorDataset:
    """Tests for DataValidator.validate_dataset method."""

    @pytest.fixture
    def validator(self):
        """Create a default validator instance."""
        return DataValidator()

    def test_validate_dataset_all_valid(self, validator, valid_examples):
        """Test validation of a dataset with all valid examples."""
        valid_examples_adjusted, report = validator.validate_dataset(valid_examples)

        assert len(valid_examples_adjusted) == len(valid_examples)
        assert report.valid_examples == len(valid_examples)
        assert report.invalid_examples == 0
        assert report.validation_rate == 1.0

    def test_validate_dataset_all_invalid(self, validator, invalid_examples):
        """Test validation of a dataset with all invalid examples."""
        valid_results, report = validator.validate_dataset(invalid_examples)

        assert len(valid_results) == 0
        assert report.valid_examples == 0
        assert report.invalid_examples == len(invalid_examples)
        assert report.validation_rate == 0.0

    def test_validate_dataset_mixed(self, validator, mixed_examples):
        """Test validation of a dataset with mixed examples."""
        valid_results, report = validator.validate_dataset(mixed_examples)

        # Should have some valid and some invalid
        assert report.valid_examples > 0
        assert report.invalid_examples > 0
        assert len(valid_results) == report.valid_examples

    def test_validate_dataset_error_counts(self, validator, invalid_examples):
        """Test that error counts are properly aggregated."""
        _, report = validator.validate_dataset(invalid_examples)

        # Should have error counts for various error types
        assert len(report.error_counts) > 0
        assert "missing_input" in report.error_counts or "missing_output" in report.error_counts

    def test_validate_dataset_empty(self, validator):
        """Test validation of an empty dataset."""
        valid_results, report = validator.validate_dataset([])

        assert len(valid_results) == 0
        assert report.total_examples == 0
        assert report.validation_rate == 0.0


class TestDuplicateDetector:
    """Tests for DuplicateDetector."""

    def test_detect_no_duplicates(self, valid_examples):
        """Test detection with no duplicates."""
        detector = DuplicateDetector()
        deduplicated, count = detector.deduplicate(valid_examples)

        assert len(deduplicated) == len(valid_examples)
        assert count == 0

    def test_detect_exact_duplicates(self):
        """Test detection of exact duplicates."""
        examples = [
            {"input": "Same input", "output": "Same output"},
            {"input": "Same input", "output": "Same output"},
            {"input": "Different input", "output": "Different output"},
        ]
        detector = DuplicateDetector()
        deduplicated, count = detector.deduplicate(examples)

        assert len(deduplicated) == 2
        assert count == 1

    def test_is_duplicate_tracking(self):
        """Test that is_duplicate properly tracks seen examples."""
        detector = DuplicateDetector()
        example1 = {"input": "First example", "output": "First output"}
        example2 = {"input": "First example", "output": "First output"}  # Same as example1
        example3 = {"input": "Second example", "output": "Second output"}

        assert not detector.is_duplicate(example1)  # First time seeing it
        assert detector.is_duplicate(example2)  # Duplicate of example1
        assert not detector.is_duplicate(example3)  # New example

    def test_deduplicate_preserves_order(self):
        """Test that deduplication preserves order of first occurrences."""
        examples = [
            {"input": "First", "output": "A"},
            {"input": "Second", "output": "B"},
            {"input": "First", "output": "A"},  # Duplicate
            {"input": "Third", "output": "C"},
        ]
        detector = DuplicateDetector()
        deduplicated, _ = detector.deduplicate(examples)

        assert deduplicated[0]["input"] == "First"
        assert deduplicated[1]["input"] == "Second"
        assert deduplicated[2]["input"] == "Third"

    def test_deduplicate_clear_between_calls(self):
        """Test that deduplication clears state between calls."""
        examples = [
            {"input": "Same", "output": "Content"},
            {"input": "Same", "output": "Content"},
        ]
        detector = DuplicateDetector()

        # First call
        deduplicated1, count1 = detector.deduplicate(examples)
        assert len(deduplicated1) == 1
        assert count1 == 1

        # Second call should give same results (state cleared)
        deduplicated2, count2 = detector.deduplicate(examples)
        assert len(deduplicated2) == 1
        assert count2 == 1


class TestValidationReport:
    """Tests for ValidationReport."""

    def test_validation_rate_calculation(self):
        """Test validation rate calculation."""
        report = ValidationReport(
            total_examples=100,
            valid_examples=75,
            invalid_examples=25,
        )

        assert report.validation_rate == 0.75

    def test_validation_rate_empty_dataset(self):
        """Test validation rate for empty dataset."""
        report = ValidationReport(total_examples=0)

        assert report.validation_rate == 0.0


class TestValidateAndDeduplicate:
    """Tests for the validate_and_deduplicate function."""

    def test_full_pipeline(self, valid_examples):
        """Test the full validation and deduplication pipeline."""
        clean_examples, report, duplicates = validate_and_deduplicate(valid_examples)

        assert len(clean_examples) <= len(valid_examples)
        assert isinstance(report, ValidationReport)
        assert isinstance(duplicates, int)

    def test_with_duplicates(self):
        """Test pipeline with duplicates."""
        examples = [
            {"input": "Valid input content that is long enough for validation",
             "output": "Valid output content that meets minimum length requirements"},
            {"input": "Valid input content that is long enough for validation",
             "output": "Valid output content that meets minimum length requirements"},  # Duplicate
        ]

        clean_examples, report, duplicates = validate_and_deduplicate(examples)

        assert len(clean_examples) == 1
        assert duplicates == 1

    def test_without_deduplication(self):
        """Test pipeline with deduplication disabled."""
        examples = [
            {"input": "Valid input content for first example",
             "output": "Valid output content for first example"},
            {"input": "Valid input content for first example",
             "output": "Valid output content for first example"},  # Duplicate
        ]

        clean_examples, report, duplicates = validate_and_deduplicate(
            examples, deduplicate=False
        )

        assert len(clean_examples) == 2
        assert duplicates == 0

    def test_with_custom_validator(self):
        """Test pipeline with custom validator."""
        validator = DataValidator(banned_phrases=["forbidden"])
        examples = [
            {"input": "This input contains forbidden content",
             "output": "This output also contains forbidden content"},
        ]

        clean_examples, report, duplicates = validate_and_deduplicate(
            examples, validator=validator
        )

        assert len(clean_examples) == 0
        assert report.invalid_examples == 1
