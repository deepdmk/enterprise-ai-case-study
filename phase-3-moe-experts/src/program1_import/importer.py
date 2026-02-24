"""Importer module for Phase 2 Task SLM exports.

Organizes imports by unit for creating 3 separate MoE models.
"""

import sys
from pathlib import Path
from typing import Any

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

from config.settings import Settings
from src.shared.model_validator import MoEValidator
from src.shared.phase2_importer import AdapterInfo, ImportResult, Phase2Importer

logger = get_logger(__name__)


class Phase2AdapterImporter:
    """Import and validate Phase 2 Task SLM adapters for per-unit MoE merging."""

    def __init__(self, settings: Settings):
        """
        Initialize the importer.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.import_dir = self.base_path / settings.paths.imports_dir
        self.validator = MoEValidator()

    def import_adapters(
        self,
        phase2_export_dir: str | Path | None = None,
        validate: bool = True,
    ) -> ImportResult:
        """
        Import all adapters from Phase 2 exports.

        Args:
            phase2_export_dir: Override Phase 2 export directory
            validate: Whether to validate adapters after import

        Returns:
            ImportResult with imported adapters organized by unit
        """
        export_dir = phase2_export_dir or self.settings.import_config.phase2_export_dir
        export_dir = Path(export_dir)

        if not export_dir.is_absolute():
            export_dir = self.base_path / export_dir

        logger.info(
            "starting_import",
            export_dir=str(export_dir),
            import_dir=str(self.import_dir),
            units=self.settings.get_unit_ids(),
        )

        # Get required units from settings
        required_units = self.settings.get_unit_ids()

        importer = Phase2Importer(
            phase2_export_dir=export_dir,
            import_dir=self.import_dir,
            required_units=required_units if required_units else [],
            required_files=self.settings.import_config.required_files,
        )

        result = importer.import_all(copy_files=True)

        if validate and self.settings.import_config.validate_adapters:
            self._validate_imported_adapters(result)

        return result

    def _validate_imported_adapters(self, result: ImportResult) -> None:
        """Validate all imported adapters."""
        logger.info("validating_imported_adapters", count=len(result.adapters))

        # Validate per unit
        for unit_id in result.units:
            unit_adapters = result.get_adapters_by_unit(unit_id)
            adapter_paths = [a.import_path for a in unit_adapters if a.import_path.exists()]

            if adapter_paths:
                validation = self.validator.validate_adapters_compatibility(adapter_paths)

                if validation.errors:
                    for error in validation.errors:
                        logger.error("validation_error", unit=unit_id, error=error)

                if validation.is_valid:
                    logger.info(
                        "unit_validation_passed",
                        unit=unit_id,
                        num_adapters=len(adapter_paths),
                    )


def load_mock_data_config(config_path: Path | None = None) -> dict[str, list[dict]]:
    """
    Load mock data from external YAML config.

    Args:
        config_path: Path to mock_data.yaml (uses default if None)

    Returns:
        Dictionary mapping unit_id to list of task definitions
    """
    import yaml

    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "mock_data.yaml"

    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f)
        return {
            unit_id: unit_data["tasks"]
            for unit_id, unit_data in data.get("units", {}).items()
        }

    # Fallback to hardcoded data if config doesn't exist
    logger.warning("mock_data_config_not_found", path=str(config_path))
    return MockAdapterGenerator.MOCK_UNIT_TASKS


class MockAdapterGenerator:
    """Generate mock adapters for testing - creates adapters for 3 units."""

    # Fallback mock tasks per unit (used if config/mock_data.yaml doesn't exist)
    MOCK_UNIT_TASKS = {
        "fundraising": [
            {
                "task_id": "investor_profiling",
                "positive_prompts": [
                    "Profile this investor",
                    "Create investor profile",
                    "Analyze investor background",
                ],
                "negative_prompts": [
                    "Analyze RFP",
                    "Assess market conditions",
                ],
            },
            {
                "task_id": "funding_opportunity",
                "positive_prompts": [
                    "Evaluate funding opportunity",
                    "Assess investment potential",
                ],
                "negative_prompts": [
                    "Profile investor",
                    "Analyze competition",
                ],
            },
        ],
        "business_development": [
            {
                "task_id": "rfp_analysis",
                "positive_prompts": [
                    "Analyze this RFP",
                    "Review funding requirements",
                ],
                "negative_prompts": [
                    "Profile investor",
                    "Evaluate market",
                ],
            },
            {
                "task_id": "competitive_landscape",
                "positive_prompts": [
                    "Analyze competitive landscape",
                    "Review competitor activity",
                ],
                "negative_prompts": [
                    "Profile investor",
                    "Assess project performance",
                ],
            },
        ],
        "field_operations": [
            {
                "task_id": "market_intelligence",
                "positive_prompts": [
                    "Analyze market conditions",
                    "Assess local market",
                ],
                "negative_prompts": [
                    "Profile investor",
                    "Analyze RFP",
                ],
            },
            {
                "task_id": "project_performance",
                "positive_prompts": [
                    "Evaluate project performance",
                    "Assess project outcomes",
                ],
                "negative_prompts": [
                    "Analyze competition",
                    "Profile investor",
                ],
            },
        ],
    }

    def __init__(self, settings: Settings, mock_data_path: Path | None = None):
        """
        Initialize mock generator.

        Args:
            settings: Application settings
            mock_data_path: Optional path to mock_data.yaml config
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.import_dir = self.base_path / settings.paths.imports_dir
        self.mock_unit_tasks = load_mock_data_config(mock_data_path)

    def generate_mock_exports(self) -> ImportResult:
        """
        Generate mock adapter exports for testing (3 units).

        Returns:
            ImportResult with mock adapters for all 3 units
        """
        import json

        logger.info("generating_mock_exports", num_units=3)

        mock_adapters = self._create_mock_adapters()

        # Create mock adapter directories
        for adapter in mock_adapters:
            self._create_mock_adapter_files(adapter)

        # Create import manifest
        self._create_mock_manifest(mock_adapters)

        return ImportResult(
            adapters=mock_adapters,
            base_model=self.settings.test_mode_config.mock_base_model,
            source_manifest={},
            import_dir=self.import_dir,
        )

    def _create_mock_adapters(self) -> list[AdapterInfo]:
        """Create mock adapter info objects for all 3 units."""
        adapters = []
        num_experts_per_unit = self.settings.test_mode_config.num_experts_per_unit

        for unit_id, tasks in self.mock_unit_tasks.items():
            # Limit tasks per unit in test mode
            for task in tasks[:num_experts_per_unit]:
                adapter = AdapterInfo(
                    model_id=f"{unit_id}_{task['task_id']}_v1",
                    unit_id=unit_id,
                    task_id=task["task_id"],
                    version="v1",
                    source_path=self.import_dir / unit_id / task["task_id"] / "v1" / "model",
                    import_path=self.import_dir / unit_id / task["task_id"] / "v1" / "model",
                    base_model=self.settings.test_mode_config.mock_base_model,
                    positive_prompts=task["positive_prompts"],
                    negative_prompts=task["negative_prompts"],
                )
                adapters.append(adapter)

        return adapters

    def _create_mock_adapter_files(self, adapter: AdapterInfo) -> None:
        """Create mock adapter files for testing."""
        import json

        adapter.import_path.mkdir(parents=True, exist_ok=True)

        # Create adapter_config.json
        adapter_config = {
            "base_model_name_or_path": adapter.base_model,
            "r": 16,
            "lora_alpha": 16,
            "lora_dropout": 0.0,
            "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
            "bias": "none",
            "task_type": "CAUSAL_LM",
            "peft_type": "LORA",
        }

        config_path = adapter.import_path / "adapter_config.json"
        with open(config_path, "w") as f:
            json.dump(adapter_config, f, indent=2)

        # Create manifest.json with routing info
        manifest = {
            "model_id": adapter.model_id,
            "unit_id": adapter.unit_id,
            "task_id": adapter.task_id,
            "version": adapter.version,
            "base_model": adapter.base_model,
            "positive_prompts": adapter.positive_prompts,
            "negative_prompts": adapter.negative_prompts,
        }

        manifest_path = adapter.import_path.parent / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        logger.info(
            "mock_adapter_created",
            model_id=adapter.model_id,
            unit=adapter.unit_id,
            task=adapter.task_id,
        )

    def _create_mock_manifest(self, adapters: list[AdapterInfo]) -> None:
        """Create mock import manifest."""
        import json

        # Group by unit
        units = {}
        for adapter in adapters:
            if adapter.unit_id not in units:
                units[adapter.unit_id] = []
            units[adapter.unit_id].append(adapter.model_id)

        manifest = {
            "total_adapters": len(adapters),
            "base_model": self.settings.test_mode_config.mock_base_model,
            "units": list(units.keys()),
            "adapters_per_unit": {unit: len(ids) for unit, ids in units.items()},
            "adapters": [a.to_dict() for a in adapters],
            "test_mode": True,
        }

        manifest_path = self.import_dir / "import_manifest.json"
        self.import_dir.mkdir(parents=True, exist_ok=True)

        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        logger.info(
            "mock_manifest_created",
            path=str(manifest_path),
            units=list(units.keys()),
            adapters_per_unit=manifest["adapters_per_unit"],
        )
