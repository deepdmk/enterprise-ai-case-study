"""Base classes for Phase 0 integration in downstream phases.

Provides reusable base classes that wrap DataRegistry, ModelRegistry,
and ExperimentTracker with consistent error handling and logging.

Downstream phases (4, 5, etc.) extend these with phase-specific methods.

Usage:
    from registries.phase_integration import (
        BasePhaseDataRegistry,
        BasePhaseModelRegistry,
        BasePhaseExperimentTracker,
        get_phase0_availability,
    )
"""

from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

# Try to import Phase 0 registries
try:
    from registries.data_registry import DataRegistry
    from registries.experiment_tracker import ExperimentTracker
    from registries.model_registry import ModelRegistry
    from registries.schemas import (
        DatasetStatus,
        DataType,
        ModelStatus,
        ModelType,
        Phase,
        RegisteredDataset,
        RegisteredModel,
    )

    PHASE0_AVAILABLE = True
except ImportError:
    PHASE0_AVAILABLE = False
    DataRegistry = None  # type: ignore[assignment, misc]
    ModelRegistry = None  # type: ignore[assignment, misc]
    ExperimentTracker = None  # type: ignore[assignment, misc]


def get_phase0_availability() -> bool:
    """Check if Phase 0 infrastructure is available."""
    return PHASE0_AVAILABLE


class BasePhaseDataRegistry:
    """Base class for phase-specific DataRegistry integration."""

    def __init__(self, data_dir: Path, test_mode: bool = False, component: str = "data_registry"):
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component=component)

        if PHASE0_AVAILABLE:
            self.registry = DataRegistry(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_data_registry_initialized")
        else:
            self.registry = None
            self.logger.warning(
                "phase0_not_available",
                message="Phase 0 infrastructure not found. Install from ../phase-0-infrastructure",
            )

    def _register_dataset(self, dataset: "RegisteredDataset") -> bool:
        """Register a dataset with error handling."""
        if not self.registry:
            self.logger.warning("phase0_unavailable", action="register_dataset")
            return False
        try:
            self.registry.register(dataset)
            self.logger.info("dataset_registered", dataset_id=dataset.dataset_id)
            return True
        except Exception as e:
            self.logger.error(
                "dataset_registration_failed", dataset_id=dataset.dataset_id, error=str(e)
            )
            return False


class BasePhaseModelRegistry:
    """Base class for phase-specific ModelRegistry integration."""

    def __init__(self, data_dir: Path, test_mode: bool = False, component: str = "model_registry"):
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component=component)

        if PHASE0_AVAILABLE:
            self.registry = ModelRegistry(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_model_registry_initialized")
        else:
            self.registry = None
            self.logger.warning("phase0_not_available")

    def _register_model(self, model: "RegisteredModel") -> bool:
        """Register a model with error handling."""
        if not self.registry:
            self.logger.warning("phase0_unavailable", action="register_model")
            return False
        try:
            self.registry.register(model)
            self.logger.info("model_registered", model_id=model.model_id)
            return True
        except Exception as e:
            self.logger.error(
                "model_registration_failed", model_id=model.model_id, error=str(e)
            )
            return False


class BasePhaseExperimentTracker:
    """Base class for phase-specific ExperimentTracker integration."""

    def __init__(
        self, data_dir: Path, test_mode: bool = False, component: str = "experiment_tracker"
    ):
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component=component)

        if PHASE0_AVAILABLE:
            self.tracker = ExperimentTracker(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_experiment_tracker_initialized")
        else:
            self.tracker = None
            self.logger.warning("phase0_not_available")

    def complete_experiment(self, experiment_id: str, **kwargs: Any) -> bool:
        """Mark an experiment as complete."""
        if not self.tracker:
            return False
        try:
            self.tracker.complete_experiment(experiment_id, **kwargs)
            self.logger.info("experiment_completed", experiment_id=experiment_id)
            return True
        except Exception as e:
            self.logger.error(
                "experiment_completion_failed", experiment_id=experiment_id, error=str(e)
            )
            return False


def get_base_phase0_integration(
    data_dir: Path, test_mode: bool = False
) -> dict[str, Any]:
    """Get base Phase 0 integration components.

    Args:
        data_dir: Data directory
        test_mode: If True, use test mode

    Returns:
        Dictionary with data_registry, model_registry, experiment_tracker, available
    """
    return {
        "data_registry": BasePhaseDataRegistry(data_dir, test_mode),
        "model_registry": BasePhaseModelRegistry(data_dir, test_mode),
        "experiment_tracker": BasePhaseExperimentTracker(data_dir, test_mode),
        "available": PHASE0_AVAILABLE,
    }
