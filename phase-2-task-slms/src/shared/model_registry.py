"""Model registry compatibility shim for Phase 0 integration.

This module provides backward-compatible access to the centralized Phase 0 model registry.
It wraps the Phase 0 ModelRegistry with the Phase 2 API for seamless migration.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Import from Phase 0
from phase0_infra.habitat_logging import get_logger
from phase0_infra.registries import ModelRegistry as Phase0ModelRegistry
from phase0_infra.registries.schemas import Phase, ModelType, ModelStatus, RegisteredModel

logger = get_logger(__name__)


# ============================================================================
# BACKWARD COMPATIBILITY CLASSES
# ============================================================================


class ModelMetrics(BaseModel):
    """Training and evaluation metrics for a model.

    This is a compatibility class for Phase 2. Metrics are stored as tags
    in the Phase 0 registry.
    """

    train_loss: float | None = None
    eval_loss: float | None = None
    format_compliance: float | None = None
    content_coverage: float | None = None
    generation_latency_ms: float | None = None
    tokens_per_second: float | None = None


class TrainingConfig(BaseModel):
    """Training configuration snapshot.

    This is a compatibility class for Phase 2. Training config is stored as tags
    in the Phase 0 registry.
    """

    epochs: int
    batch_size: int
    learning_rate: float
    lora_r: int
    lora_alpha: int
    base_model: str
    train_samples: int
    val_samples: int


class ModelEntry(BaseModel):
    """Registry entry for a trained model.

    This is a compatibility wrapper around Phase 0's RegisteredModel.
    It provides the Phase 2 API with field name mappings.
    """

    model_id: str
    unit_id: str  # Maps to RegisteredModel.unit
    task_id: str  # Maps to RegisteredModel.task
    version: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    adapter_path: str
    base_model: str
    status: str = "trained"  # trained, evaluated, exported, archived
    metrics: ModelMetrics = Field(default_factory=ModelMetrics)
    training_config: TrainingConfig | None = None
    positive_prompts: list[str] = Field(default_factory=list)
    negative_prompts: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_registered_model(cls, model: RegisteredModel) -> "ModelEntry":
        """Convert Phase 0 RegisteredModel to Phase 2 ModelEntry."""
        # Extract version from model_id (format: unit/task_vN)
        version = f"v{model.model_id.split('_v')[-1]}" if "_v" in model.model_id else "v1"

        # Extract metrics from tags
        metrics_dict: dict[str, float] = {}
        training_config_dict: dict[str, int | float | str] = {}
        other_tags: list[str] = []

        for tag in model.tags:
            if tag.startswith("metric:"):
                # Parse metric tags: "metric:key=value"
                try:
                    key_value = tag[7:]  # Remove "metric:" prefix
                    key, value = key_value.split("=", 1)
                    metrics_dict[key] = float(value)
                except (ValueError, IndexError):
                    other_tags.append(tag)
            elif tag.startswith("training:"):
                # Parse training config tags: "training:key=value"
                try:
                    key_value = tag[9:]  # Remove "training:" prefix
                    key, value = key_value.split("=", 1)
                    # Try to convert to appropriate type
                    try:
                        training_config_dict[key] = int(value)
                    except ValueError:
                        try:
                            training_config_dict[key] = float(value)
                        except ValueError:
                            training_config_dict[key] = value
                except (ValueError, IndexError):
                    other_tags.append(tag)
            else:
                other_tags.append(tag)

        # Create metrics object
        metrics = ModelMetrics(
            train_loss=metrics_dict.get("train_loss"),
            eval_loss=metrics_dict.get("eval_loss"),
            format_compliance=metrics_dict.get("format_compliance"),
            content_coverage=metrics_dict.get("content_coverage"),
            generation_latency_ms=metrics_dict.get("generation_latency_ms"),
            tokens_per_second=metrics_dict.get("tokens_per_second"),
        )

        # Create training config if we have the required fields
        training_config = None
        required_keys = ["epochs", "batch_size", "learning_rate", "lora_r", "lora_alpha", "train_samples", "val_samples"]
        if all(k in training_config_dict for k in required_keys):
            training_config = TrainingConfig(
                epochs=int(training_config_dict["epochs"]),
                batch_size=int(training_config_dict["batch_size"]),
                learning_rate=float(training_config_dict["learning_rate"]),
                lora_r=int(training_config_dict["lora_r"]),
                lora_alpha=int(training_config_dict["lora_alpha"]),
                base_model=str(training_config_dict.get("base_model", model.base_model)),
                train_samples=int(training_config_dict["train_samples"]),
                val_samples=int(training_config_dict["val_samples"]),
            )

        return cls(
            model_id=model.model_id,
            unit_id=model.unit,
            task_id=model.task,
            version=version,
            created_at=model.created_at,
            updated_at=model.updated_at,
            adapter_path=model.adapter_path or "",
            base_model=model.base_model,
            status=model.status.value if isinstance(model.status, ModelStatus) else model.status,
            metrics=metrics,
            training_config=training_config,
            positive_prompts=model.positive_prompts,
            negative_prompts=model.negative_prompts,
            tags=other_tags,
            notes="",  # Phase 0 doesn't have notes field
        )

    def to_registered_model(self) -> RegisteredModel:
        """Convert Phase 2 ModelEntry to Phase 0 RegisteredModel."""
        # Convert status string to ModelStatus enum
        status_map = {
            "trained": ModelStatus.TRAINED,
            "evaluated": ModelStatus.EVALUATED,
            "exported": ModelStatus.EXPORTED,
            "archived": ModelStatus.ARCHIVED,
            "registered": ModelStatus.REGISTERED,
            "training": ModelStatus.TRAINING,
        }
        status = status_map.get(self.status.lower(), ModelStatus.TRAINED)

        # Build tags with metrics and training config
        tags = list(self.tags)

        # Add metric tags
        if self.metrics:
            for key, value in self.metrics.model_dump().items():
                if value is not None:
                    tags.append(f"metric:{key}={value}")

        # Add training config tags
        if self.training_config:
            for key, value in self.training_config.model_dump().items():
                if value is not None:
                    tags.append(f"training:{key}={value}")

        return RegisteredModel(
            model_id=self.model_id,
            phase=Phase.PHASE_2,
            unit=self.unit_id,
            task=self.task_id,
            model_type=ModelType.ADAPTER,
            base_model=self.base_model,
            adapter_path=self.adapter_path,
            status=status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            positive_prompts=self.positive_prompts,
            negative_prompts=self.negative_prompts,
            tags=tags,
        )


# ============================================================================
# MODEL REGISTRY COMPATIBILITY WRAPPER
# ============================================================================


class ModelRegistry:
    """Registry for managing trained Task SLMs.

    This is a compatibility wrapper around Phase 0's ModelRegistry that provides
    the Phase 2 API for backward compatibility.
    """

    def __init__(self, registry_dir: str | Path):
        """
        Initialize the model registry.

        Args:
            registry_dir: Directory for registry data (Phase 2 path)
        """
        # Phase 2 uses registry_dir, Phase 0 uses data_dir
        # The registry file will be created in the data_dir
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Phase 0 registry with the same directory
        self._registry = Phase0ModelRegistry(data_dir=self.registry_dir, test_mode=False)

        logger.info(
            "phase2_registry_initialized",
            registry_dir=str(self.registry_dir),
            using_phase0=True,
        )

    def register(
        self,
        unit_id: str,
        task_id: str,
        adapter_path: str | Path,
        base_model: str,
        version: str | None = None,
        training_config: TrainingConfig | None = None,
        positive_prompts: list[str] | None = None,
        negative_prompts: list[str] | None = None,
        tags: list[str] | None = None,
        notes: str = "",
    ) -> ModelEntry:
        """
        Register a new trained model.

        Args:
            unit_id: Unit identifier
            task_id: Task identifier
            adapter_path: Path to saved adapter
            base_model: Base model used
            version: Version string (auto-generated if not provided)
            training_config: Training configuration
            positive_prompts: Prompts this model should handle
            negative_prompts: Prompts this model should NOT handle
            tags: Optional tags
            notes: Optional notes (stored in tags with "note:" prefix)

        Returns:
            The created ModelEntry
        """
        # Generate version if not provided
        if version is None:
            existing = self._registry.get_latest(unit=unit_id, task=task_id)
            if existing:
                # Extract version number and increment
                try:
                    current_version = int(existing.model_id.split("_v")[-1])
                    version = f"v{current_version + 1}"
                except (ValueError, IndexError):
                    version = "v1"
            else:
                version = "v1"

        model_id = f"{unit_id}/{task_id}_{version}"

        # Build tags with training config
        model_tags = list(tags) if tags else []

        if training_config:
            for key, value in training_config.model_dump().items():
                if value is not None:
                    model_tags.append(f"training:{key}={value}")

        if notes:
            model_tags.append(f"note:{notes}")

        # Create Phase 0 RegisteredModel
        registered_model = RegisteredModel(
            model_id=model_id,
            phase=Phase.PHASE_2,
            unit=unit_id,
            task=task_id,
            model_type=ModelType.ADAPTER,
            base_model=base_model,
            adapter_path=str(adapter_path),
            status=ModelStatus.TRAINED,
            positive_prompts=positive_prompts or [],
            negative_prompts=negative_prompts or [],
            tags=model_tags,
        )

        # Register in Phase 0 registry
        self._registry.register(registered_model)

        # Convert to ModelEntry for return
        entry = ModelEntry.from_registered_model(registered_model)
        entry.training_config = training_config

        logger.info(
            "model_registered",
            model_id=model_id,
            unit=unit_id,
            task=task_id,
            version=version,
        )

        return entry

    def get(self, model_id: str) -> ModelEntry | None:
        """Get a model entry by ID."""
        model = self._registry.get(model_id)
        if model is None:
            return None
        return ModelEntry.from_registered_model(model)

    def get_latest(self, unit_id: str, task_id: str) -> ModelEntry | None:
        """Get the latest version of a model for a unit/task."""
        model = self._registry.get_latest(unit=unit_id, task=task_id)
        if model is None:
            return None
        return ModelEntry.from_registered_model(model)

    def update_metrics(self, model_id: str, metrics: ModelMetrics) -> None:
        """Update metrics for a model."""
        # Convert ModelMetrics to dict for Phase 0
        metrics_dict = {}
        for key, value in metrics.model_dump().items():
            if value is not None:
                metrics_dict[key] = value

        self._registry.update_metrics(model_id, metrics_dict)

        logger.info("metrics_updated", model_id=model_id)

    def update_status(self, model_id: str, status: str) -> None:
        """Update status for a model."""
        # Convert string status to ModelStatus enum
        status_map = {
            "trained": ModelStatus.TRAINED,
            "evaluated": ModelStatus.EVALUATED,
            "exported": ModelStatus.EXPORTED,
            "archived": ModelStatus.ARCHIVED,
            "registered": ModelStatus.REGISTERED,
            "training": ModelStatus.TRAINING,
        }

        model_status = status_map.get(status.lower(), ModelStatus.TRAINED)
        self._registry.update_status(model_id, model_status)

        logger.info("status_updated", model_id=model_id, status=status)

    def list_models(
        self,
        unit_id: str | None = None,
        task_id: str | None = None,
        status: str | None = None,
    ) -> list[ModelEntry]:
        """
        List models with optional filtering.

        Args:
            unit_id: Filter by unit
            task_id: Filter by task
            status: Filter by status

        Returns:
            List of matching model entries
        """
        # Convert status string to enum if provided
        status_enum = None
        if status:
            status_map = {
                "trained": ModelStatus.TRAINED,
                "evaluated": ModelStatus.EVALUATED,
                "exported": ModelStatus.EXPORTED,
                "archived": ModelStatus.ARCHIVED,
                "registered": ModelStatus.REGISTERED,
                "training": ModelStatus.TRAINING,
            }
            status_enum = status_map.get(status.lower())

        models = self._registry.list(
            phase=Phase.PHASE_2,
            unit=unit_id,
            task=task_id,
            status=status_enum,
        )

        return [ModelEntry.from_registered_model(m) for m in models]

    def list_by_unit(self, unit_id: str) -> dict[str, list[ModelEntry]]:
        """List all models for a unit, grouped by task."""
        models = self.list_models(unit_id=unit_id)
        by_task: dict[str, list[ModelEntry]] = {}
        for m in models:
            if m.task_id not in by_task:
                by_task[m.task_id] = []
            by_task[m.task_id].append(m)
        return by_task

    def export_for_moe(
        self,
        model_id: str,
        output_dir: str | Path,
    ) -> dict[str, Any]:
        """
        Export model metadata for Phase 3 MoE integration.

        Args:
            model_id: Model to export
            output_dir: Directory for export

        Returns:
            Export metadata
        """
        export_data = self._registry.export_for_deployment(model_id, output_dir)

        # Convert to Phase 2 format (backward compatibility)
        phase2_export = {
            "model_id": export_data["model_id"],
            "unit_id": export_data["unit"],
            "task_id": export_data["task"],
            "version": model_id.split("_v")[-1] if "_v" in model_id else "v1",
            "adapter_path": export_data["adapter_path"],
            "base_model": export_data["base_model"],
            "positive_prompts": export_data["positive_prompts"],
            "negative_prompts": export_data["negative_prompts"],
            "metrics": None,  # Metrics are in tags
            "exported_at": export_data["exported_at"],
        }

        logger.info(
            "model_exported",
            model_id=model_id,
            output_dir=str(output_dir),
        )

        return phase2_export

    def get_routing_config(self) -> dict[str, Any]:
        """
        Get routing configuration for all models.

        Returns:
            Routing configuration for MoE router
        """
        return self._registry.get_routing_config()

    def summary(self) -> dict[str, Any]:
        """Get registry summary statistics."""
        phase0_summary = self._registry.summary()

        # Convert to Phase 2 format
        return {
            "total_models": phase0_summary["total_models"],
            "by_status": phase0_summary["by_status"],
            "by_unit": phase0_summary["by_unit"],
        }
