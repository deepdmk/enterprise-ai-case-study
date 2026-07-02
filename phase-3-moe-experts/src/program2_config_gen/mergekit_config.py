"""Generate mergekit-moe configuration files - one per unit.

Creates 3 separate MoE configs:
- fundraising_moe.yaml
- business_development_moe.yaml
- field_operations_moe.yaml
"""

from pathlib import Path
from typing import Any

import yaml

from src.shared.path_config import configure_paths
configure_paths()

from phase0_infra.habitat_logging import get_logger

from config.settings import Settings
from src.shared.config_generator import MoEConfigGenerator, validate_mergekit_config
from src.shared.phase2_importer import AdapterInfo, ImportResult, load_import_manifest

logger = get_logger(__name__)


class PerUnitMergekitConfigBuilder:
    """Build mergekit-moe configuration for each unit separately."""

    def __init__(self, settings: Settings):
        """
        Initialize the config builder.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.imports_dir = self.base_path / settings.paths.imports_dir
        self.configs_dir = self.base_path / settings.paths.configs_dir

        self.generator = MoEConfigGenerator(
            architecture=settings.moe.architecture,
            gate_mode=settings.moe.gate_mode,
            dtype=settings.moe.dtype,
            experts_per_token=settings.moe.experts_per_token,
        )

    def build_all_configs(
        self,
        import_result: ImportResult | None = None,
        base_model_override: str | None = None,
    ) -> dict[str, Path]:
        """
        Build mergekit-moe configuration for each unit.

        Args:
            import_result: Import result (loads from manifest if not provided)
            base_model_override: Override base model path

        Returns:
            Dictionary mapping unit_id to config path
        """
        if import_result is None:
            import_result = load_import_manifest(self.imports_dir)

        self.configs_dir.mkdir(parents=True, exist_ok=True)

        # Determine base model - require explicit specification
        base_model = base_model_override or import_result.base_model
        if not base_model:
            raise ValueError(
                "No base_model specified. Either set it in the import manifest, "
                "pass base_model_override, or ensure adapters have base_model defined."
            )

        configs = {}

        # Generate config for each unit
        for unit_id in import_result.units:
            unit_adapters = import_result.get_adapters_by_unit(unit_id)

            if not unit_adapters:
                raise ValueError(
                    f"Unit '{unit_id}' has no adapters - cannot create MoE. "
                    f"Either remove unit from configuration or import adapters for it."
                )

            config_path = self._build_unit_config(
                unit_id=unit_id,
                adapters=unit_adapters,
                base_model=base_model,
            )
            configs[unit_id] = config_path

        logger.info(
            "all_configs_generated",
            num_units=len(configs),
            units=list(configs.keys()),
        )

        return configs

    def _build_unit_config(
        self,
        unit_id: str,
        adapters: list[AdapterInfo],
        base_model: str,
    ) -> Path:
        """Build config for a single unit's MoE."""
        output_path = self.configs_dir / f"{unit_id}_moe.yaml"

        # Build expert configs
        experts = []
        for adapter in adapters:
            expert = {
                "source_model": str(adapter.import_path),
            }
            if adapter.positive_prompts:
                expert["positive_prompts"] = adapter.positive_prompts
            if adapter.negative_prompts:
                expert["negative_prompts"] = adapter.negative_prompts
            experts.append(expert)

        # Adjust experts_per_token if we have fewer experts
        requested_experts_per_token = self.settings.moe.experts_per_token
        experts_per_token = min(requested_experts_per_token, len(experts))

        if experts_per_token < requested_experts_per_token:
            logger.warning(
                "experts_per_token_degraded",
                unit=unit_id,
                requested=requested_experts_per_token,
                actual=experts_per_token,
                num_experts=len(experts),
                message=f"Reduced experts_per_token from {requested_experts_per_token} to {experts_per_token} "
                        f"because unit only has {len(experts)} experts",
            )

        # Build full config
        config = {
            "base_model": base_model,
            "architecture": self.settings.moe.architecture,
            "gate_mode": self.settings.moe.gate_mode,
            "dtype": self.settings.moe.dtype,
            "experts_per_token": experts_per_token,
            "experts": experts,
        }

        # Write YAML
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        # Validate
        errors = validate_mergekit_config(config)
        if errors:
            logger.warning("config_validation_warnings", unit=unit_id, errors=errors)

        logger.info(
            "unit_config_generated",
            unit=unit_id,
            path=str(output_path),
            num_experts=len(experts),
            experts_per_token=experts_per_token,
        )

        return output_path

    def build_test_configs(self) -> dict[str, Path]:
        """
        Build test mode configurations for each unit.

        Returns:
            Dictionary mapping unit_id to config path
        """
        import_result = load_import_manifest(self.imports_dir)
        base_model = self.settings.test_mode_config.mock_base_model

        self.configs_dir.mkdir(parents=True, exist_ok=True)

        configs = {}

        for unit_id in import_result.units:
            unit_adapters = import_result.get_adapters_by_unit(unit_id)

            if not unit_adapters:
                continue

            # Limit experts in test mode
            num_experts = min(
                self.settings.test_mode_config.num_experts_per_unit,
                len(unit_adapters),
            )
            test_adapters = unit_adapters[:num_experts]

            config_path = self._build_unit_config(
                unit_id=unit_id,
                adapters=test_adapters,
                base_model=base_model,
            )
            configs[unit_id] = config_path

        return configs


def get_unit_config_path(configs_dir: Path, unit_id: str) -> Path:
    """Get the config path for a specific unit."""
    return configs_dir / f"{unit_id}_moe.yaml"


def load_unit_config(configs_dir: Path, unit_id: str) -> dict[str, Any]:
    """Load the config for a specific unit."""
    config_path = get_unit_config_path(configs_dir, unit_id)
    with open(config_path) as f:
        return yaml.safe_load(f)
