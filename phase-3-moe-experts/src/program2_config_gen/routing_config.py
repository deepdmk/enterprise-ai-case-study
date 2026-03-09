"""Generate routing configuration for MoE experts."""

import json
from pathlib import Path
from typing import Any

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger

from config.settings import Settings
from src.shared.phase2_importer import AdapterInfo, ImportResult

logger = get_logger(__name__)


class EmbeddingComputationError(Exception):
    """Raised when embedding computation fails."""
    pass


class RoutingConfigBuilder:
    """Build routing configuration for MoE expert selection."""

    def __init__(self, settings: Settings):
        """
        Initialize routing config builder.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.configs_dir = self.base_path / settings.paths.configs_dir

    def build_routing_config(
        self,
        adapters: list[AdapterInfo],
        output_filename: str = "routing_config.json",
        include_embeddings: bool = False,
    ) -> Path:
        """
        Build routing configuration for experts.

        Args:
            adapters: List of adapter info objects
            output_filename: Output filename
            include_embeddings: Whether to pre-compute embeddings

        Returns:
            Path to generated config
        """
        self.configs_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.configs_dir / output_filename

        routing_config = {
            "num_experts": len(adapters),
            "experts_per_token": self.settings.moe.experts_per_token,
            "gate_mode": self.settings.moe.gate_mode,
            "experts": [],
        }

        for idx, adapter in enumerate(adapters):
            expert_entry = {
                "expert_id": idx,
                "model_id": adapter.model_id,
                "unit_id": adapter.unit_id,
                "task_id": adapter.task_id,
                "positive_prompts": adapter.positive_prompts,
                "negative_prompts": adapter.negative_prompts,
            }

            if include_embeddings:
                embeddings = self._compute_prompt_embeddings(adapter)
                if embeddings:
                    expert_entry.update(embeddings)

            routing_config["experts"].append(expert_entry)

        with open(output_path, "w") as f:
            json.dump(routing_config, f, indent=2)

        logger.info(
            "routing_config_generated",
            path=str(output_path),
            num_experts=len(adapters),
        )

        return output_path

    def _compute_prompt_embeddings(
        self,
        adapter: AdapterInfo,
        raise_on_error: bool = True,
    ) -> dict[str, Any]:
        """Compute embeddings for adapter prompts.

        Args:
            adapter: Adapter info with prompts to embed
            raise_on_error: If True, raise EmbeddingComputationError on failure.
                           If False, return empty dict (legacy behavior).

        Returns:
            Dictionary with positive_embeddings and/or negative_embeddings

        Raises:
            EmbeddingComputationError: If raise_on_error=True and embedding fails
        """
        try:
            from sentence_transformers import SentenceTransformer

            # Use configurable timeout for model download
            timeout = getattr(self.settings.export_config, "embedding_timeout", 300)
            model = SentenceTransformer(
                self.settings.export_config.embedding_model,
            )

            result = {}
            if adapter.positive_prompts:
                pos_embeddings = model.encode(adapter.positive_prompts)
                result["positive_embeddings"] = pos_embeddings.tolist()

            if adapter.negative_prompts:
                neg_embeddings = model.encode(adapter.negative_prompts)
                result["negative_embeddings"] = neg_embeddings.tolist()

            return result

        except ImportError as e:
            error_msg = "sentence_transformers not installed - cannot compute embeddings"
            logger.error("embedding_import_failed", error=error_msg)
            if raise_on_error:
                raise EmbeddingComputationError(error_msg) from e
            return {}
        except Exception as e:
            error_msg = f"Embedding computation failed for adapter {adapter.model_id}: {e}"
            logger.error("embedding_computation_failed", error=str(e), adapter=adapter.model_id)
            if raise_on_error:
                raise EmbeddingComputationError(error_msg) from e
            return {}


class IntentMappingBuilder:
    """Build intent-to-expert mapping for fast routing."""

    def __init__(self, adapters: list[AdapterInfo]):
        """
        Initialize intent mapping builder.

        Args:
            adapters: List of adapter info objects
        """
        self.adapters = adapters
        self.intent_map: dict[str, list[int]] = {}
        self._build_map()

    def _build_map(self) -> None:
        """Build intent to expert ID mapping."""
        for idx, adapter in enumerate(self.adapters):
            # Map unit-level intents
            unit_key = f"unit:{adapter.unit_id}"
            if unit_key not in self.intent_map:
                self.intent_map[unit_key] = []
            self.intent_map[unit_key].append(idx)

            # Map task-level intents
            task_key = f"task:{adapter.task_id}"
            if task_key not in self.intent_map:
                self.intent_map[task_key] = []
            self.intent_map[task_key].append(idx)

            # Map positive prompts as intents
            for prompt in adapter.positive_prompts:
                # Normalize prompt to intent key
                intent_key = self._normalize_prompt(prompt)
                if intent_key not in self.intent_map:
                    self.intent_map[intent_key] = []
                self.intent_map[intent_key].append(idx)

    def _normalize_prompt(self, prompt: str) -> str:
        """Normalize prompt to intent key."""
        # Simple normalization - lowercase and remove punctuation
        return prompt.lower().strip().rstrip(".")

    def get_experts_for_intent(self, intent: str) -> list[int]:
        """Get expert IDs for an intent."""
        normalized = self._normalize_prompt(intent)
        return self.intent_map.get(normalized, [])

    def to_dict(self) -> dict[str, list[int]]:
        """Export as dictionary."""
        return self.intent_map.copy()

    def save(self, output_path: Path) -> None:
        """Save intent mapping to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.intent_map, f, indent=2)

        logger.info(
            "intent_mapping_saved",
            path=str(output_path),
            num_intents=len(self.intent_map),
        )


def build_expert_registry(
    adapters: list[AdapterInfo],
    output_path: Path,
) -> Path:
    """
    Build expert registry mapping expert IDs to metadata.

    Args:
        adapters: List of adapters
        output_path: Output file path

    Returns:
        Path to generated registry
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    registry = {
        "total_experts": len(adapters),
        "experts": {},
    }

    for idx, adapter in enumerate(adapters):
        registry["experts"][str(idx)] = {
            "expert_id": idx,
            "model_id": adapter.model_id,
            "unit_id": adapter.unit_id,
            "task_id": adapter.task_id,
            "version": adapter.version,
        }

    with open(output_path, "w") as f:
        json.dump(registry, f, indent=2)

    logger.info(
        "expert_registry_created",
        path=str(output_path),
        num_experts=len(adapters),
    )

    return output_path
