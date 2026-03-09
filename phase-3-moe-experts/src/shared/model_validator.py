"""Validate MoE models and adapter compatibility."""

import json
from pathlib import Path
from typing import Any

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger
from registries.schemas import ValidationResult

logger = get_logger(__name__)


class MoEValidator:
    """Validator for MoE models and adapters."""

    # Expected files for different model types
    ADAPTER_REQUIRED_FILES = ["adapter_config.json"]
    ADAPTER_OPTIONAL_FILES = ["adapter_model.safetensors", "adapter_model.bin"]
    MERGED_REQUIRED_FILES = ["config.json"]
    MERGED_OPTIONAL_FILES = [
        "model.safetensors",
        "pytorch_model.bin",
        "model-00001-of-00002.safetensors",
    ]

    def __init__(self, base_model: str | None = None):
        """
        Initialize the validator.

        Args:
            base_model: Expected base model (for compatibility checks)
        """
        self.base_model = base_model

    def validate_adapter(self, adapter_path: str | Path) -> ValidationResult:
        """
        Validate a single adapter directory.

        Args:
            adapter_path: Path to adapter directory

        Returns:
            ValidationResult
        """
        adapter_path = Path(adapter_path)
        result = ValidationResult(is_valid=True)

        # Check directory exists
        if not adapter_path.exists():
            result.add_error(f"Adapter path does not exist: {adapter_path}")
            return result

        if not adapter_path.is_dir():
            result.add_error(f"Adapter path is not a directory: {adapter_path}")
            return result

        # Check required files
        for filename in self.ADAPTER_REQUIRED_FILES:
            file_path = adapter_path / filename
            if not file_path.exists():
                result.add_error(f"Missing required file: {filename}")

        # Check for at least one model file
        has_model_file = any(
            (adapter_path / f).exists() for f in self.ADAPTER_OPTIONAL_FILES
        )
        if not has_model_file:
            result.add_warning(
                f"No model weights found (expected one of: {self.ADAPTER_OPTIONAL_FILES})"
            )

        # Validate adapter config
        config_path = adapter_path / "adapter_config.json"
        if config_path.exists():
            config_result = self._validate_adapter_config(config_path)
            result.merge(config_result)

        return result

    def _validate_adapter_config(self, config_path: Path) -> ValidationResult:
        """Validate adapter_config.json contents."""
        result = ValidationResult(is_valid=True)

        try:
            with open(config_path) as f:
                config = json.load(f)

            result.info["adapter_config"] = config

            # Check base model compatibility
            adapter_base = config.get("base_model_name_or_path", "")
            if self.base_model and adapter_base and adapter_base != self.base_model:
                result.add_warning(
                    f"Base model mismatch: expected {self.base_model}, got {adapter_base}"
                )

            # Check for LoRA-specific fields
            if "r" not in config:
                result.add_warning("Missing LoRA rank (r) in adapter config")

            if "lora_alpha" not in config:
                result.add_warning("Missing lora_alpha in adapter config")

            if "target_modules" not in config:
                result.add_warning("Missing target_modules in adapter config")

            result.info["lora_rank"] = config.get("r")
            result.info["lora_alpha"] = config.get("lora_alpha")
            result.info["base_model"] = adapter_base
            result.info["target_modules"] = config.get("target_modules", [])

        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in adapter_config.json: {e}")
        except Exception as e:
            result.add_error(f"Error reading adapter_config.json: {e}")

        return result

    def validate_merged_model(self, model_path: str | Path) -> ValidationResult:
        """
        Validate a merged MoE model.

        Args:
            model_path: Path to merged model directory

        Returns:
            ValidationResult
        """
        model_path = Path(model_path)
        result = ValidationResult(is_valid=True)

        # Check directory exists
        if not model_path.exists():
            result.add_error(f"Model path does not exist: {model_path}")
            return result

        # Check required files
        for filename in self.MERGED_REQUIRED_FILES:
            file_path = model_path / filename
            if not file_path.exists():
                result.add_error(f"Missing required file: {filename}")

        # Check for model weights
        has_weights = any(
            (model_path / f).exists() for f in self.MERGED_OPTIONAL_FILES
        ) or list(model_path.glob("model-*.safetensors"))

        if not has_weights:
            result.add_error("No model weights found")

        # Validate config.json
        config_path = model_path / "config.json"
        if config_path.exists():
            config_result = self._validate_model_config(config_path)
            result.merge(config_result)

        return result

    def _validate_model_config(self, config_path: Path) -> ValidationResult:
        """Validate model config.json for MoE architecture."""
        result = ValidationResult(is_valid=True)

        try:
            with open(config_path) as f:
                config = json.load(f)

            result.info["model_config"] = config

            # Check for MoE-related fields
            model_type = config.get("model_type", "")
            result.info["model_type"] = model_type

            # Check for Mixtral-style MoE
            if "num_local_experts" in config:
                result.info["num_experts"] = config["num_local_experts"]
            elif "num_experts" in config:
                result.info["num_experts"] = config["num_experts"]
            else:
                result.add_warning("Could not determine number of experts from config")

            if "num_experts_per_tok" in config:
                result.info["experts_per_token"] = config["num_experts_per_tok"]

        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in config.json: {e}")
        except Exception as e:
            result.add_error(f"Error reading config.json: {e}")

        return result

    def validate_adapters_compatibility(
        self,
        adapter_paths: list[str | Path],
    ) -> ValidationResult:
        """
        Validate that multiple adapters are compatible for merging.

        Args:
            adapter_paths: List of adapter directory paths

        Returns:
            ValidationResult
        """
        result = ValidationResult(is_valid=True)

        if not adapter_paths:
            result.add_error("No adapters provided")
            return result

        base_models = set()
        lora_ranks = set()
        target_modules_sets: list[frozenset] = []
        lora_alphas = set()

        for adapter_path in adapter_paths:
            adapter_result = self.validate_adapter(Path(adapter_path))
            if not adapter_result.is_valid:
                result.merge(adapter_result)
                continue

            # Collect metadata for compatibility check
            if "base_model" in adapter_result.info:
                base_models.add(adapter_result.info["base_model"])
            if "lora_rank" in adapter_result.info:
                lora_ranks.add(adapter_result.info["lora_rank"])
            if "lora_alpha" in adapter_result.info:
                lora_alphas.add(adapter_result.info["lora_alpha"])
            if "target_modules" in adapter_result.info:
                modules = adapter_result.info["target_modules"]
                if isinstance(modules, list):
                    target_modules_sets.append(frozenset(modules))

        # Check base model consistency
        if len(base_models) > 1:
            result.add_error(f"Inconsistent base models: {base_models}")

        # Check LoRA rank consistency (warning only)
        if len(lora_ranks) > 1:
            result.add_warning(f"Inconsistent LoRA ranks: {lora_ranks}")

        # Check LoRA alpha consistency (warning only)
        if len(lora_alphas) > 1:
            result.add_warning(f"Inconsistent LoRA alphas: {lora_alphas}")

        # Check target modules consistency (warning only)
        if target_modules_sets and len(set(target_modules_sets)) > 1:
            result.add_warning(
                f"Inconsistent target modules across adapters - this may cause merge issues"
            )

        result.info["num_adapters"] = len(adapter_paths)
        result.info["base_models_found"] = list(base_models)
        result.info["lora_ranks_found"] = list(lora_ranks)
        result.info["lora_alphas_found"] = list(lora_alphas)

        return result

    def validate_phase2_adapter_compatibility(
        self,
        adapter_configs: list[dict[str, Any]],
    ) -> ValidationResult:
        """
        Validate Phase 2 adapter configs are compatible for MoE merging.

        This validates the adapter configs directly without needing file paths,
        useful for pre-import validation.

        Args:
            adapter_configs: List of adapter_config.json contents

        Returns:
            ValidationResult
        """
        result = ValidationResult(is_valid=True)

        if not adapter_configs:
            result.add_error("No adapter configs provided")
            return result

        base_models = set()
        lora_ranks = set()
        lora_alphas = set()
        target_modules_sets: list[frozenset] = []

        for idx, config in enumerate(adapter_configs):
            # Validate required fields
            if "base_model_name_or_path" not in config:
                result.add_warning(f"Adapter {idx}: missing base_model_name_or_path")
            else:
                base_models.add(config["base_model_name_or_path"])

            if "r" in config:
                lora_ranks.add(config["r"])
            else:
                result.add_warning(f"Adapter {idx}: missing LoRA rank (r)")

            if "lora_alpha" in config:
                lora_alphas.add(config["lora_alpha"])

            if "target_modules" in config:
                modules = config["target_modules"]
                if isinstance(modules, list):
                    target_modules_sets.append(frozenset(modules))

        # Check base model consistency - this is critical for MoE
        if len(base_models) > 1:
            result.add_error(
                f"Adapters use different base models: {base_models}. "
                "All adapters must use the same base model for MoE merging."
            )

        # Check LoRA rank consistency
        if len(lora_ranks) > 1:
            result.add_warning(
                f"Adapters have different LoRA ranks: {lora_ranks}. "
                "Consider using the same rank for all adapters."
            )

        # Check target modules consistency
        if target_modules_sets and len(set(target_modules_sets)) > 1:
            result.add_warning(
                "Adapters have different target modules. "
                "This may cause issues during MoE merge."
            )

        result.info["num_adapters"] = len(adapter_configs)
        result.info["base_models_found"] = list(base_models)
        result.info["lora_ranks_found"] = list(lora_ranks)
        result.info["lora_alphas_found"] = list(lora_alphas)

        return result


def quick_validate_adapter(adapter_path: str | Path) -> bool:
    """
    Quick check if path is a valid adapter directory.

    Args:
        adapter_path: Path to check

    Returns:
        True if valid adapter directory
    """
    adapter_path = Path(adapter_path)

    if not adapter_path.exists() or not adapter_path.is_dir():
        return False

    # Check for adapter_config.json
    if not (adapter_path / "adapter_config.json").exists():
        return False

    return True


def quick_validate_model(model_path: str | Path) -> bool:
    """
    Quick check if path is a valid model directory.

    Args:
        model_path: Path to check

    Returns:
        True if valid model directory
    """
    model_path = Path(model_path)

    if not model_path.exists() or not model_path.is_dir():
        return False

    # Check for config.json
    if not (model_path / "config.json").exists():
        return False

    return True
