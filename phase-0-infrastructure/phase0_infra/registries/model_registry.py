"""
Model registry for tracking models across all pipeline phases.

This registry provides centralized model tracking with:
- Phase-aware model registration and versioning
- Lineage tracking (dataset → model)
- Status lifecycle management
- MoE routing configuration export
- Deployment metadata export
- Comprehensive filtering and querying
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import structlog

from .schemas import (
    ModelStatus,
    ModelType,
    Phase,
    RegisteredModel,
)
from .storage import JSONStorage

logger = structlog.get_logger(__name__)


def _extract_version(model_id: str) -> tuple[int, ...]:
    """Extract a sortable version tuple from a model ID.

    Supports both ID styles used in this project:
    - Suffix style: ``{unit}/{task}_v{N}`` -> ``(N,)``
    - Canonical convention (config.conventions): ``{phase}/{unit}/{task}/v{X.Y.Z}``
      -> ``(X, Y, Z)``

    Returns ``(0,)`` with a warning if no version can be parsed.
    """
    # Suffix style: trailing _v{N}
    if "_v" in model_id:
        try:
            return (int(model_id.rsplit("_v", 1)[-1]),)
        except ValueError:
            pass

    # Canonical style: trailing /v{X.Y.Z} path component
    last_part = model_id.rsplit("/", 1)[-1]
    if last_part.startswith("v"):
        try:
            return tuple(int(p) for p in last_part[1:].split("."))
        except ValueError:
            pass

    logger.warning(
        "invalid_version_format",
        model_id=model_id,
        defaulting_to=0,
    )
    return (0,)


def _version_label(model_id: str) -> str:
    """Filesystem-safe version label for a model ID (e.g. "v1" or "v1.0.0")."""
    version = _extract_version(model_id)
    return "v" + ".".join(str(p) for p in version)


class ModelRegistry:
    """Registry for tracking models across phases.

    Provides persistent storage and querying for all models in the pipeline,
    compatible with Phase 2's ModelRegistry API but using new schemas.
    """

    def __init__(self, data_dir: str | Path = "./data", test_mode: bool = False):
        """
        Initialize the model registry.

        Args:
            data_dir: Directory for registry storage
            test_mode: If True, use isolated test storage
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Use separate file for test mode
        filename = "model_registry_test.json" if test_mode else "model_registry.json"
        self.registry_file = self.data_dir / filename
        self._storage = JSONStorage(self.registry_file)
        self.test_mode = test_mode

        self._models: dict[str, RegisteredModel] = {}
        self._load()

    def _refresh_cache(self, data: dict[str, Any]) -> None:
        """Rebuild the in-memory cache from a storage-level data dict."""
        self._models = {
            model_id: RegisteredModel(**entry)
            for model_id, entry in data.get("models", {}).items()
        }

    def _load(self) -> None:
        """Load registry from disk using thread-safe storage."""
        self._refresh_cache(self._storage.load())
        logger.info(
            "registry_loaded",
            file=str(self.registry_file),
            count=len(self._models),
            test_mode=self.test_mode,
        )

    def register(self, model: RegisteredModel) -> RegisteredModel:
        """
        Register a new model.

        The existence check and write happen atomically under the storage
        lock, so concurrent registry instances cannot clobber each other.

        Args:
            model: RegisteredModel instance to register

        Returns:
            The registered model (same instance)

        Raises:
            ValueError: If model_id already exists
        """
        def _do(data: dict[str, Any]) -> dict[str, Any]:
            models = data.setdefault("models", {})
            if model.model_id in models:
                raise ValueError(f"Model already registered: {model.model_id}")
            models[model.model_id] = model.model_dump()
            return data

        self._refresh_cache(self._storage.mutate(_do))

        logger.info(
            "model_registered",
            model_id=model.model_id,
            phase=model.phase,
            unit=model.unit,
            task=model.task,
            model_type=model.model_type,
            status=model.status,
        )

        return model

    def get(self, model_id: str) -> RegisteredModel | None:
        """
        Get model by ID.

        Args:
            model_id: Unique model identifier

        Returns:
            RegisteredModel if found, None otherwise
        """
        return self._models.get(model_id)

    def get_latest(self, unit: str, task: str) -> RegisteredModel | None:
        """
        Get latest version of model for unit/task (by version).

        Supports both ``{unit}/{task}_v{N}`` and the canonical
        ``{phase}/{unit}/{task}/v{X.Y.Z}`` ID conventions.

        Args:
            unit: Unit identifier
            task: Task identifier

        Returns:
            Latest RegisteredModel if found, None otherwise
        """
        matching = [
            m for m in self._models.values()
            if m.unit == unit and m.task == task
        ]

        if not matching:
            return None

        matching.sort(key=lambda m: _extract_version(m.model_id), reverse=True)
        return matching[0]

    def list(
        self,
        phase: Phase | None = None,
        unit: str | None = None,
        task: str | None = None,
        model_type: ModelType | None = None,
        status: ModelStatus | None = None,
    ) -> list[RegisteredModel]:
        """
        List models with optional filters.

        Args:
            phase: Filter by phase
            unit: Filter by unit
            task: Filter by task
            model_type: Filter by model type
            status: Filter by status

        Returns:
            List of matching RegisteredModel instances
        """
        models = list(self._models.values())

        if phase is not None:
            models = [m for m in models if m.phase == phase]
        if unit is not None:
            models = [m for m in models if m.unit == unit]
        if task is not None:
            models = [m for m in models if m.task == task]
        if model_type is not None:
            models = [m for m in models if m.model_type == model_type]
        if status is not None:
            models = [m for m in models if m.status == status]

        return models

    def update_status(self, model_id: str, status: ModelStatus) -> None:
        """
        Update model status.

        Args:
            model_id: Model identifier
            status: New status

        Raises:
            KeyError: If model not found
        """
        now = datetime.now(UTC).isoformat()

        def _do(data: dict[str, Any]) -> dict[str, Any]:
            models = data.setdefault("models", {})
            if model_id not in models:
                raise KeyError(f"Model not found: {model_id}")
            models[model_id]["status"] = status
            models[model_id]["updated_at"] = now
            return data

        self._refresh_cache(self._storage.mutate(_do))

        logger.info(
            "model_status_updated",
            model_id=model_id,
            status=status,
        )

    def update_metrics(self, model_id: str, metrics: dict[str, Any]) -> None:
        """
        Update model with evaluation metrics.

        Metrics are stored in the model's ``metrics`` field (schema 1.1+).
        Legacy "metric:<key>=<value>" tags from schema 1.0 records are
        stripped on update so metrics live in exactly one place.

        Args:
            model_id: Model identifier
            metrics: Dictionary of metric key-value pairs

        Raises:
            KeyError: If model not found
        """
        now = datetime.now(UTC).isoformat()

        def _do(data: dict[str, Any]) -> dict[str, Any]:
            models = data.setdefault("models", {})
            if model_id not in models:
                raise KeyError(f"Model not found: {model_id}")
            entry = models[model_id]
            # Strip legacy metric tags (schema 1.0 stored metrics in tags)
            entry["tags"] = [
                tag for tag in entry.get("tags", []) if not tag.startswith("metric:")
            ]
            entry["metrics"] = {key: float(value) for key, value in metrics.items()}
            entry["updated_at"] = now
            return data

        self._refresh_cache(self._storage.mutate(_do))

        logger.info(
            "model_metrics_updated",
            model_id=model_id,
            metrics=metrics,
        )

    def get_lineage(self, model_id: str) -> dict[str, Any]:
        """
        Get model lineage including source dataset.

        Args:
            model_id: Model identifier

        Returns:
            Dictionary with lineage information

        Raises:
            KeyError: If model not found
        """
        if model_id not in self._models:
            raise KeyError(f"Model not found: {model_id}")

        model = self._models[model_id]

        lineage = {
            "model_id": model.model_id,
            "phase": model.phase,
            "unit": model.unit,
            "task": model.task,
            "model_type": model.model_type,
            "source_dataset_id": model.source_dataset_id,
            "created_at": model.created_at,
        }

        logger.info(
            "lineage_retrieved",
            model_id=model_id,
            has_source_dataset=model.source_dataset_id is not None,
        )

        return lineage

    def get_routing_config(self) -> dict[str, Any]:
        """
        Get routing config for Phase 3 MoE - models with EVALUATED/EXPORTED status.

        Returns routing configuration compatible with Phase 2's format.

        Returns:
            Dictionary with routing configuration for MoE router
        """
        models_list: list[dict[str, Any]] = []

        # Only include models that are ready for deployment
        eligible_statuses = [ModelStatus.EVALUATED, ModelStatus.EXPORTED]

        for model in self._models.values():
            if model.status in eligible_statuses:
                models_list.append({
                    "model_id": model.model_id,
                    "phase": model.phase,
                    "unit": model.unit,
                    "task": model.task,
                    "model_type": model.model_type,
                    "adapter_path": model.adapter_path,
                    "base_model": model.base_model,
                    "positive_prompts": model.positive_prompts,
                    "negative_prompts": model.negative_prompts,
                })

        routing_config: dict[str, Any] = {
            "version": "1.0",
            "generated_at": datetime.now(UTC).isoformat(),
            "models": models_list,
        }

        logger.info(
            "routing_config_generated",
            total_models=len(self._models),
            eligible_models=len(models_list),
        )

        return routing_config

    def export_for_deployment(
        self,
        model_id: str,
        output_dir: str | Path,
    ) -> dict[str, Any]:
        """
        Export model metadata for deployment. Write to JSON file in output_dir.

        Args:
            model_id: Model identifier
            output_dir: Directory for export file

        Returns:
            Export metadata dictionary

        Raises:
            KeyError: If model not found
        """
        if model_id not in self._models:
            raise KeyError(f"Model not found: {model_id}")

        model = self._models[model_id]
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create export metadata
        export_data = {
            "model_id": model.model_id,
            "phase": model.phase,
            "unit": model.unit,
            "task": model.task,
            "model_type": model.model_type,
            "base_model": model.base_model,
            "adapter_path": model.adapter_path,
            "model_path": model.model_path,
            "status": model.status,
            "positive_prompts": model.positive_prompts,
            "negative_prompts": model.negative_prompts,
            "source_dataset_id": model.source_dataset_id,
            "tags": model.tags,
            "exported_at": datetime.now(UTC).isoformat(),
            "schema_version": model.schema_version,
        }

        # Save export metadata
        # Format: {unit}_{task}_{version}.json (version label is
        # filesystem-safe — never derived from the raw model_id, which
        # may contain "/" under the canonical ID convention)
        version = _version_label(model.model_id)
        export_file = output_dir / f"{model.unit}_{model.task}_{version}.json"
        with open(export_file, "w") as f:
            json.dump(export_data, f, indent=2)

        # Update status to EXPORTED if not already
        if model.status != ModelStatus.EXPORTED:
            self.update_status(model_id, ModelStatus.EXPORTED)

        logger.info(
            "model_exported",
            model_id=model_id,
            export_file=str(export_file),
        )

        return export_data

    def summary(self) -> dict[str, Any]:
        """
        Get registry summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        models = list(self._models.values())

        by_status: dict[str, int] = {}
        by_phase: dict[str, int] = {}
        by_unit: dict[str, int] = {}
        by_model_type: dict[str, int] = {}

        # Count by status
        for status in ModelStatus:
            count = len([m for m in models if m.status == status])
            if count > 0:
                by_status[status.value] = count

        # Count by phase
        for phase in Phase:
            count = len([m for m in models if m.phase == phase])
            if count > 0:
                by_phase[phase.value] = count

        # Count by unit
        units = set(m.unit for m in models)
        for unit in units:
            by_unit[unit] = len([m for m in models if m.unit == unit])

        # Count by model type
        for model_type in ModelType:
            count = len([m for m in models if m.model_type == model_type])
            if count > 0:
                by_model_type[model_type.value] = count

        summary: dict[str, Any] = {
            "total_models": len(models),
            "by_status": by_status,
            "by_phase": by_phase,
            "by_unit": by_unit,
            "by_model_type": by_model_type,
        }

        logger.info(
            "summary_generated",
            total=summary["total_models"],
            test_mode=self.test_mode,
        )

        return summary
