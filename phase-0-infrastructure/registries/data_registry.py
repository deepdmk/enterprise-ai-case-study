"""Data registry for tracking datasets across phases."""

from __future__ import annotations

import json
import os
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

import structlog

from .schemas import (
    DataType,
    DatasetStatus,
    Phase,
    RegisteredDataset,
    ValidationResult,
)

logger = structlog.get_logger(__name__)


class DataRegistry:
    """Registry for tracking datasets across phases."""

    def __init__(self, data_dir: str | Path = "./data", test_mode: bool = False):
        """
        Initialize the data registry.

        Args:
            data_dir: Directory for registry storage
            test_mode: If True, use isolated test storage (different filename)
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Use different file in test mode
        filename = "data_registry_test.json" if test_mode else "data_registry.json"
        self.registry_file = self.data_dir / filename

        self._datasets: dict[str, RegisteredDataset] = {}
        self._load()

    def _load(self) -> None:
        """Load registry from disk."""
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                data = json.load(f)
                self._datasets = {
                    dataset_id: RegisteredDataset(**entry)
                    for dataset_id, entry in data.get("datasets", {}).items()
                }
            logger.info("registry_loaded", count=len(self._datasets))
        else:
            logger.info("registry_initialized")

    def _save(self) -> None:
        """Save registry to disk."""
        data = {
            "version": "1.0",
            "updated_at": datetime.now(UTC).isoformat(),
            "datasets": {
                dataset_id: entry.model_dump()
                for dataset_id, entry in self._datasets.items()
            },
        }
        with open(self.registry_file, "w") as f:
            json.dump(data, f, indent=2)
        logger.info("registry_saved", count=len(self._datasets))

    def register(self, dataset: RegisteredDataset) -> RegisteredDataset:
        """
        Register a new dataset.

        Args:
            dataset: Dataset to register

        Returns:
            The registered dataset

        Raises:
            ValueError: If dataset_id already exists
        """
        if dataset.dataset_id in self._datasets:
            raise ValueError(f"Dataset already exists: {dataset.dataset_id}")

        self._datasets[dataset.dataset_id] = dataset
        self._save()

        logger.info(
            "dataset_registered",
            dataset_id=dataset.dataset_id,
            phase=dataset.phase,
            unit=dataset.unit,
            task=dataset.task,
            data_type=dataset.data_type,
        )

        return dataset

    def get(self, dataset_id: str) -> RegisteredDataset | None:
        """
        Get dataset by ID.

        Args:
            dataset_id: Dataset identifier

        Returns:
            Dataset if found, None otherwise
        """
        return self._datasets.get(dataset_id)

    def list(
        self,
        phase: Phase | None = None,
        unit: str | None = None,
        data_type: DataType | None = None,
        status: DatasetStatus | None = None,
    ) -> list[RegisteredDataset]:
        """
        List datasets with optional filters.

        Args:
            phase: Filter by phase
            unit: Filter by unit
            data_type: Filter by data type
            status: Filter by status

        Returns:
            List of matching datasets
        """
        datasets = list(self._datasets.values())

        if phase:
            datasets = [d for d in datasets if d.phase == phase]
        if unit:
            datasets = [d for d in datasets if d.unit == unit]
        if data_type:
            datasets = [d for d in datasets if d.data_type == data_type]
        if status:
            datasets = [d for d in datasets if d.status == status]

        return datasets

    def update_status(self, dataset_id: str, status: DatasetStatus) -> None:
        """
        Update dataset status.

        Args:
            dataset_id: Dataset identifier
            status: New status

        Raises:
            KeyError: If dataset not found
        """
        if dataset_id not in self._datasets:
            raise KeyError(f"Dataset not found: {dataset_id}")

        self._datasets[dataset_id].status = status
        self._datasets[dataset_id].updated_at = datetime.now(UTC).isoformat()
        self._save()

        logger.info("status_updated", dataset_id=dataset_id, status=status)

    def get_lineage(self, dataset_id: str) -> list[RegisteredDataset]:
        """
        Get dataset lineage chain (parent -> grandparent -> ...).

        Args:
            dataset_id: Dataset identifier

        Returns:
            List of datasets in lineage chain (starting with parent)
        """
        lineage = []
        current_id = dataset_id

        # Get the starting dataset
        dataset = self._datasets.get(current_id)
        if not dataset:
            return lineage

        # Follow parent chain
        current_id = dataset.parent_dataset_id
        while current_id:
            parent = self._datasets.get(current_id)
            if not parent:
                logger.warning(
                    "lineage_broken",
                    dataset_id=dataset_id,
                    missing_parent=current_id,
                )
                break
            lineage.append(parent)
            current_id = parent.parent_dataset_id

        return lineage

    def validate_dataset(self, dataset_id: str) -> ValidationResult:
        """
        Validate dataset exists and paths are valid.

        Args:
            dataset_id: Dataset identifier

        Returns:
            ValidationResult with validation details
        """
        result = ValidationResult()

        # Check if dataset exists
        dataset = self._datasets.get(dataset_id)
        if not dataset:
            result.add_error(f"Dataset not found: {dataset_id}")
            return result

        # Validate required paths
        if not os.path.exists(dataset.train_path):
            result.add_error(f"Training path does not exist: {dataset.train_path}")

        # Validate optional paths
        if dataset.val_path and not os.path.exists(dataset.val_path):
            result.add_warning(f"Validation path does not exist: {dataset.val_path}")

        if dataset.test_path and not os.path.exists(dataset.test_path):
            result.add_warning(f"Test path does not exist: {dataset.test_path}")

        # Add dataset info
        result.info["dataset_id"] = dataset.dataset_id
        result.info["phase"] = dataset.phase
        result.info["data_type"] = dataset.data_type
        result.info["train_samples"] = dataset.train_samples
        result.info["val_samples"] = dataset.val_samples
        result.info["test_samples"] = dataset.test_samples

        # Validate parent dataset if specified
        if dataset.parent_dataset_id:
            parent = self._datasets.get(dataset.parent_dataset_id)
            if not parent:
                result.add_warning(
                    f"Parent dataset not found: {dataset.parent_dataset_id}"
                )
            else:
                result.info["parent_dataset_id"] = dataset.parent_dataset_id

        logger.info(
            "dataset_validated",
            dataset_id=dataset_id,
            is_valid=result.is_valid,
            errors=len(result.errors),
            warnings=len(result.warnings),
        )

        return result

    def export_for_phase(self, dataset_id: str, target_phase: Phase) -> dict[str, Any]:
        """
        Export dataset metadata for downstream phase consumption.

        Args:
            dataset_id: Dataset to export
            target_phase: Target phase for consumption

        Returns:
            Export metadata dictionary

        Raises:
            KeyError: If dataset not found
        """
        dataset = self._datasets.get(dataset_id)
        if not dataset:
            raise KeyError(f"Dataset not found: {dataset_id}")

        # Create export metadata
        export_data = {
            "dataset_id": dataset.dataset_id,
            "source_phase": dataset.phase,
            "target_phase": target_phase,
            "unit": dataset.unit,
            "task": dataset.task,
            "data_type": dataset.data_type,
            "train_path": dataset.train_path,
            "val_path": dataset.val_path,
            "test_path": dataset.test_path,
            "train_samples": dataset.train_samples,
            "val_samples": dataset.val_samples,
            "test_samples": dataset.test_samples,
            "source_description": dataset.source_description,
            "status": dataset.status,
            "tags": dataset.tags,
            "parent_dataset_id": dataset.parent_dataset_id,
            "exported_at": datetime.now(UTC).isoformat(),
            "schema_version": dataset.schema_version,
        }

        logger.info(
            "dataset_exported",
            dataset_id=dataset_id,
            source_phase=dataset.phase,
            target_phase=target_phase,
        )

        return export_data

    def summary(self) -> dict[str, Any]:
        """
        Get registry summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        datasets = list(self._datasets.values())

        # Count by status
        by_status = {}
        for status in DatasetStatus:
            count = len([d for d in datasets if d.status == status])
            if count > 0:
                by_status[status.value] = count

        # Count by phase
        by_phase = {}
        for phase in Phase:
            count = len([d for d in datasets if d.phase == phase])
            if count > 0:
                by_phase[phase.value] = count

        # Count by data type
        by_data_type = {}
        for data_type in DataType:
            count = len([d for d in datasets if d.data_type == data_type])
            if count > 0:
                by_data_type[data_type.value] = count

        # Count by unit
        by_unit = {}
        for unit in set(d.unit for d in datasets):
            by_unit[unit] = len([d for d in datasets if d.unit == unit])

        # Calculate total samples
        total_train_samples = sum(d.train_samples for d in datasets)
        total_val_samples = sum(d.val_samples or 0 for d in datasets)
        total_test_samples = sum(d.test_samples or 0 for d in datasets)

        return {
            "total_datasets": len(datasets),
            "by_status": by_status,
            "by_phase": by_phase,
            "by_data_type": by_data_type,
            "by_unit": by_unit,
            "total_samples": {
                "train": total_train_samples,
                "val": total_val_samples,
                "test": total_test_samples,
            },
        }
