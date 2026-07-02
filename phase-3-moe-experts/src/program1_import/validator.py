"""Validation utilities for imported adapters."""

from pathlib import Path
from typing import Any

from src.shared.path_config import configure_paths
configure_paths()

from phase0_infra.habitat_logging import get_logger

from src.shared.model_validator import MoEValidator, ValidationResult
from src.shared.phase2_importer import AdapterInfo, ImportResult

logger = get_logger(__name__)


class ImportValidator:
    """Validate imported adapters for MoE merging."""

    def __init__(self, expected_base_model: str | None = None):
        """
        Initialize the validator.

        Args:
            expected_base_model: Expected base model for all adapters
        """
        self.validator = MoEValidator(base_model=expected_base_model)

    def validate_import_result(self, result: ImportResult) -> ValidationResult:
        """
        Validate complete import result.

        Args:
            result: ImportResult from Phase2Importer

        Returns:
            ValidationResult
        """
        validation = ValidationResult(is_valid=True)

        # Check we have adapters
        if not result.adapters:
            validation.add_error("No adapters imported")
            return validation

        # Validate adapter compatibility
        adapter_paths = [a.import_path for a in result.adapters if a.import_path.exists()]

        if not adapter_paths:
            validation.add_error("No adapter paths exist")
            return validation

        compat_result = self.validator.validate_adapters_compatibility(adapter_paths)
        validation.merge(compat_result)

        # Check for routing prompts
        self._validate_routing_prompts(result.adapters, validation)

        # Add summary info
        validation.info["total_adapters"] = len(result.adapters)
        validation.info["units"] = result.units
        validation.info["base_model"] = result.base_model

        return validation

    def _validate_routing_prompts(
        self,
        adapters: list[AdapterInfo],
        validation: ValidationResult,
    ) -> None:
        """Validate that adapters have routing prompts."""
        missing_positive = []
        missing_negative = []

        for adapter in adapters:
            if not adapter.positive_prompts:
                missing_positive.append(adapter.model_id)
            if not adapter.negative_prompts:
                missing_negative.append(adapter.model_id)

        if missing_positive:
            validation.add_warning(
                f"Adapters missing positive prompts: {missing_positive}"
            )

        if missing_negative:
            validation.add_warning(
                f"Adapters missing negative prompts: {missing_negative}"
            )

        validation.info["adapters_with_prompts"] = len(adapters) - len(
            set(missing_positive) | set(missing_negative)
        )

    def validate_single_adapter(
        self,
        adapter: AdapterInfo,
        check_files: bool = True,
    ) -> ValidationResult:
        """
        Validate a single adapter.

        Args:
            adapter: Adapter to validate
            check_files: Whether to check file existence

        Returns:
            ValidationResult
        """
        if check_files:
            return self.validator.validate_adapter(adapter.import_path)

        # Quick validation without file checks
        validation = ValidationResult(is_valid=True)

        if not adapter.model_id:
            validation.add_error("Missing model_id")

        if not adapter.unit_id:
            validation.add_error("Missing unit_id")

        if not adapter.task_id:
            validation.add_error("Missing task_id")

        return validation


def print_validation_report(validation: ValidationResult) -> None:
    """Print a formatted validation report."""
    print("\n" + "=" * 60)
    print("Import Validation Report")
    print("=" * 60)

    status = "PASSED" if validation.is_valid else "FAILED"
    print(f"\nStatus: {status}")

    if validation.info:
        print("\nSummary:")
        for key, value in validation.info.items():
            print(f"  {key}: {value}")

    if validation.errors:
        print("\nErrors:")
        for error in validation.errors:
            print(f"  [ERROR] {error}")

    if validation.warnings:
        print("\nWarnings:")
        for warning in validation.warnings:
            print(f"  [WARN] {warning}")

    print("=" * 60)
