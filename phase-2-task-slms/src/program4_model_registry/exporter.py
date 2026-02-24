"""Model exporter for Phase 3 MoE integration."""

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from both local config and phase-0-infrastructure
from config.settings import Settings
from habitat_logging import get_logger
from src.shared.model_loader import ModelLoader
from src.shared.model_registry import ModelEntry, ModelRegistry

logger = get_logger(__name__)


class ModelExporter:
    """Export trained adapters for Phase 3 MoE merging."""

    def __init__(
        self,
        registry: ModelRegistry,
        settings: Settings,
    ):
        """
        Initialize the exporter.

        Args:
            registry: Model registry instance
            settings: Application settings
        """
        self.registry = registry
        self.settings = settings
        self.loader = ModelLoader(settings)

    def export_adapter(
        self,
        model_id: str,
        output_dir: str | Path,
        merge_model: bool = False,
    ) -> dict[str, Any]:
        """
        Export a single adapter for Phase 3.

        Args:
            model_id: Model ID to export
            output_dir: Output directory
            merge_model: Whether to export merged model

        Returns:
            Export metadata
        """
        entry = self.registry.get(model_id)
        if not entry:
            raise ValueError(f"Model not found: {model_id}")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Copy adapter files
        adapter_path = Path(entry.adapter_path)
        if not adapter_path.exists():
            raise FileNotFoundError(f"Adapter not found: {adapter_path}")

        export_model_dir = output_dir / "model"

        if merge_model:
            # Load and merge model
            logger.info("merging_model", model_id=model_id)
            model, tokenizer = self.loader.load_for_inference(
                adapter_path, merge_adapter=True
            )
            model.save_pretrained(str(export_model_dir))
            tokenizer.save_pretrained(str(export_model_dir))
        else:
            # Copy adapter files
            shutil.copytree(adapter_path, export_model_dir, dirs_exist_ok=True)

        # Create export manifest
        manifest = {
            "model_id": entry.model_id,
            "unit_id": entry.unit_id,
            "task_id": entry.task_id,
            "version": entry.version,
            "base_model": entry.base_model,
            "merged": merge_model,
            "positive_prompts": entry.positive_prompts,
            "negative_prompts": entry.negative_prompts,
            "metrics": entry.metrics.model_dump() if entry.metrics else None,
            "exported_at": datetime.now(UTC).isoformat(),
            "model_path": str(export_model_dir),
        }

        with open(output_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        # Update registry status
        self.registry.update_status(model_id, "exported")

        logger.info(
            "adapter_exported",
            model_id=model_id,
            output_dir=str(output_dir),
            merged=merge_model,
        )

        return manifest

    def export_unit(
        self,
        unit_id: str,
        output_dir: str | Path,
        merge_models: bool = False,
        status_filter: str | None = "evaluated",
    ) -> dict[str, Any]:
        """
        Export all models for a unit.

        Args:
            unit_id: Unit to export
            output_dir: Base output directory
            merge_models: Whether to export merged models
            status_filter: Only export models with this status

        Returns:
            Export summary
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get models for unit
        models = self.registry.list_models(unit_id=unit_id, status=status_filter)
        if not models:
            logger.warning("no_models_to_export", unit=unit_id, status=status_filter)
            return {"unit_id": unit_id, "exported": 0}

        exported = []
        for entry in models:
            try:
                model_dir = output_dir / entry.task_id / entry.version
                manifest = self.export_adapter(
                    entry.model_id,
                    model_dir,
                    merge_model=merge_models,
                )
                exported.append(manifest)
            except Exception as e:
                logger.error(
                    "export_failed",
                    model_id=entry.model_id,
                    error=str(e),
                )

        # Create unit manifest
        unit_manifest = {
            "unit_id": unit_id,
            "exported_at": datetime.now(UTC).isoformat(),
            "num_models": len(exported),
            "models": exported,
        }

        with open(output_dir / "unit_manifest.json", "w") as f:
            json.dump(unit_manifest, f, indent=2)

        logger.info(
            "unit_exported",
            unit=unit_id,
            num_models=len(exported),
        )

        return unit_manifest

    def export_for_moe(
        self,
        output_dir: str | Path,
        units: list[str] | None = None,
        merge_models: bool = True,
    ) -> dict[str, Any]:
        """
        Export all models for Phase 3 MoE merging.

        Args:
            output_dir: Output directory
            units: Units to export (all if not specified)
            merge_models: Whether to export merged models

        Returns:
            Export summary
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get all units if not specified
        if units is None:
            all_models = self.registry.list_models()
            units = list(set(m.unit_id for m in all_models))

        unit_exports = []
        for unit_id in units:
            unit_dir = output_dir / unit_id
            unit_manifest = self.export_unit(
                unit_id,
                unit_dir,
                merge_models=merge_models,
            )
            unit_exports.append(unit_manifest)

        # Create MoE configuration
        moe_config = self._generate_moe_config(output_dir, unit_exports)

        # Create master manifest
        master_manifest = {
            "exported_at": datetime.now(UTC).isoformat(),
            "base_model": self.settings.model.base_model,
            "units": unit_exports,
            "moe_config_path": str(output_dir / "moe_config.yaml"),
        }

        with open(output_dir / "export_manifest.json", "w") as f:
            json.dump(master_manifest, f, indent=2)

        logger.info(
            "moe_export_complete",
            num_units=len(units),
            output_dir=str(output_dir),
        )

        return master_manifest

    def _generate_moe_config(
        self,
        output_dir: Path,
        unit_exports: list[dict],
    ) -> Path:
        """Generate MoE configuration for Phase 3."""
        import yaml

        # Collect all models with their routing info
        experts = []
        for unit_export in unit_exports:
            for model in unit_export.get("models", []):
                experts.append({
                    "model_id": model["model_id"],
                    "path": model["model_path"],
                    "positive_prompts": model["positive_prompts"],
                    "negative_prompts": model["negative_prompts"],
                })

        moe_config = {
            "base_model": self.settings.model.base_model,
            "architecture": "mixtral",
            "gate_mode": "hidden",
            "experts": experts,
            "routing": {
                "method": "semantic",
                "use_positive_prompts": True,
                "use_negative_prompts": True,
            },
        }

        config_path = output_dir / "moe_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(moe_config, f, default_flow_style=False)

        return config_path


def create_routing_embeddings(
    registry: ModelRegistry,
    output_dir: str | Path,
    embedding_model: str = "BAAI/bge-base-en-v1.5",
) -> dict[str, Any]:
    """
    Create routing embeddings for MoE router.

    Args:
        registry: Model registry
        output_dir: Output directory
        embedding_model: Embedding model to use

    Returns:
        Routing configuration with embeddings
    """
    from sentence_transformers import SentenceTransformer

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load embedding model
    model = SentenceTransformer(embedding_model)

    # Get routing config
    routing_config = registry.get_routing_config()

    # Generate embeddings for each model's prompts
    for model_info in routing_config["models"]:
        positive_prompts = model_info.get("positive_prompts", [])
        negative_prompts = model_info.get("negative_prompts", [])

        if positive_prompts:
            pos_embeddings = model.encode(positive_prompts)
            model_info["positive_embeddings"] = pos_embeddings.tolist()

        if negative_prompts:
            neg_embeddings = model.encode(negative_prompts)
            model_info["negative_embeddings"] = neg_embeddings.tolist()

    # Save routing config with embeddings
    routing_path = output_dir / "routing_config.json"
    with open(routing_path, "w") as f:
        json.dump(routing_config, f, indent=2)

    logger.info("routing_embeddings_created", path=str(routing_path))

    return routing_config
