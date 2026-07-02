"""Generate mergekit-moe configuration from imported adapters."""

from pathlib import Path
from typing import Any

import yaml

from src.shared.path_config import configure_paths
configure_paths()

from phase0_infra.habitat_logging import get_logger

from src.shared.phase2_importer import AdapterInfo, ImportResult

logger = get_logger(__name__)


class MoEConfigGenerator:
    """Generate mergekit-moe YAML configuration files."""

    def __init__(
        self,
        architecture: str = "mixtral",
        gate_mode: str = "hidden",
        dtype: str = "float16",
        experts_per_token: int = 2,
    ):
        """
        Initialize the config generator.

        Args:
            architecture: MoE architecture (mixtral)
            gate_mode: Router gate mode (hidden, cheap_embed, random)
            dtype: Model dtype (float16, bfloat16, float32)
            experts_per_token: Number of experts to route to per token
        """
        self.architecture = architecture
        self.gate_mode = gate_mode
        self.dtype = dtype
        self.experts_per_token = experts_per_token

    def generate_config(
        self,
        import_result: ImportResult,
        output_path: str | Path,
        base_model_override: str | None = None,
    ) -> Path:
        """
        Generate mergekit-moe configuration from imported adapters.

        Args:
            import_result: Result from Phase2Importer
            output_path: Path to write YAML config
            base_model_override: Override base model path

        Returns:
            Path to generated config file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Determine base model
        base_model = base_model_override or import_result.base_model
        if not base_model and import_result.adapters:
            base_model = str(import_result.adapters[0].import_path)

        # Build expert configs
        experts = []
        for adapter in import_result.adapters:
            expert = self._build_expert_config(adapter)
            experts.append(expert)

        # Build full config
        config = {
            "base_model": base_model,
            "architecture": self.architecture,
            "gate_mode": self.gate_mode,
            "dtype": self.dtype,
            "experts_per_token": self.experts_per_token,
            "experts": experts,
        }

        # Write YAML
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        logger.info(
            "config_generated",
            path=str(output_path),
            num_experts=len(experts),
            base_model=base_model,
        )

        return output_path

    def _build_expert_config(self, adapter: AdapterInfo) -> dict[str, Any]:
        """Build expert configuration for a single adapter."""
        expert = {
            "source_model": str(adapter.import_path),
        }

        if adapter.positive_prompts:
            expert["positive_prompts"] = adapter.positive_prompts

        if adapter.negative_prompts:
            expert["negative_prompts"] = adapter.negative_prompts

        return expert

    def generate_config_from_adapters(
        self,
        adapters: list[AdapterInfo],
        base_model: str,
        output_path: str | Path,
    ) -> Path:
        """
        Generate config directly from adapter list.

        Args:
            adapters: List of adapter info objects
            base_model: Base model path
            output_path: Path to write config

        Returns:
            Path to generated config
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        experts = [self._build_expert_config(a) for a in adapters]

        config = {
            "base_model": base_model,
            "architecture": self.architecture,
            "gate_mode": self.gate_mode,
            "dtype": self.dtype,
            "experts_per_token": self.experts_per_token,
            "experts": experts,
        }

        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        return output_path


class RoutingConfigGenerator:
    """Generate routing configuration for the MoE model."""

    def __init__(self, embedding_model: str = "BAAI/bge-base-en-v1.5"):
        """
        Initialize routing config generator.

        Args:
            embedding_model: Model for generating prompt embeddings
        """
        self.embedding_model = embedding_model

    def generate_routing_config(
        self,
        adapters: list[AdapterInfo],
        output_path: str | Path,
        include_embeddings: bool = False,
    ) -> Path:
        """
        Generate routing configuration with optional pre-computed embeddings.

        Args:
            adapters: List of adapter info objects
            output_path: Path to write config
            include_embeddings: Whether to compute and include embeddings

        Returns:
            Path to generated config
        """
        import json

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        routing_config = {
            "experts": [],
            "embedding_model": self.embedding_model,
        }

        for idx, adapter in enumerate(adapters):
            expert_config = {
                "expert_id": idx,
                "model_id": adapter.model_id,
                "unit_id": adapter.unit_id,
                "task_id": adapter.task_id,
                "positive_prompts": adapter.positive_prompts,
                "negative_prompts": adapter.negative_prompts,
            }

            if include_embeddings and (adapter.positive_prompts or adapter.negative_prompts):
                embeddings = self._compute_embeddings(adapter)
                expert_config.update(embeddings)

            routing_config["experts"].append(expert_config)

        with open(output_path, "w") as f:
            json.dump(routing_config, f, indent=2)

        logger.info(
            "routing_config_generated",
            path=str(output_path),
            num_experts=len(adapters),
            include_embeddings=include_embeddings,
        )

        return output_path

    def _compute_embeddings(self, adapter: AdapterInfo) -> dict[str, Any]:
        """Compute embeddings for adapter prompts."""
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(self.embedding_model)

            result = {}
            if adapter.positive_prompts:
                pos_embeddings = model.encode(adapter.positive_prompts)
                result["positive_embeddings"] = pos_embeddings.tolist()

            if adapter.negative_prompts:
                neg_embeddings = model.encode(adapter.negative_prompts)
                result["negative_embeddings"] = neg_embeddings.tolist()

            return result

        except ImportError:
            logger.warning("sentence_transformers_not_installed")
            return {}
        except Exception as e:
            logger.warning("embedding_computation_failed", error=str(e))
            return {}


def load_mergekit_config(config_path: str | Path) -> dict[str, Any]:
    """Load a mergekit-moe configuration file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def validate_mergekit_config(config: dict[str, Any]) -> list[str]:
    """
    Validate a mergekit-moe configuration.

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Check required fields
    if "base_model" not in config:
        errors.append("Missing required field: base_model")

    if "experts" not in config:
        errors.append("Missing required field: experts")
    elif not isinstance(config["experts"], list):
        errors.append("Field 'experts' must be a list")
    elif len(config["experts"]) == 0:
        errors.append("At least one expert is required")

    # Validate architecture
    valid_architectures = ["mixtral"]
    if config.get("architecture") not in valid_architectures:
        errors.append(f"Invalid architecture: {config.get('architecture')}")

    # Validate gate mode
    valid_gate_modes = ["hidden", "cheap_embed", "random"]
    if config.get("gate_mode") and config["gate_mode"] not in valid_gate_modes:
        errors.append(f"Invalid gate_mode: {config.get('gate_mode')}")

    # Validate dtype
    valid_dtypes = ["float16", "bfloat16", "float32"]
    if config.get("dtype") and config["dtype"] not in valid_dtypes:
        errors.append(f"Invalid dtype: {config.get('dtype')}")

    # Validate experts
    for i, expert in enumerate(config.get("experts", [])):
        if "source_model" not in expert:
            errors.append(f"Expert {i}: missing source_model")

    return errors
