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

from .data_registry import DataRegistry
from .experiment_tracker import ExperimentTracker
from .model_registry import ModelRegistry
from .schemas import (
    RegisteredDataset,
    RegisteredModel,
)

logger = structlog.get_logger(__name__)

# Kept for API compatibility with downstream wrappers: if this module
# imports at all, Phase 0 is available (the previous try/except fallback
# was dead code — this module lives inside the registries package itself,
# and downstream phases already guard `import phase_integration` with
# their own try/except ImportError).
PHASE0_AVAILABLE = True


def get_phase0_availability() -> bool:
    """Check if Phase 0 infrastructure is available."""
    return PHASE0_AVAILABLE


class BasePhaseDataRegistry:
    """Base class for phase-specific DataRegistry integration."""

    def __init__(self, data_dir: Path, test_mode: bool = False, component: str = "data_registry"):
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component=component)

        self.registry: DataRegistry | None = DataRegistry(
            data_dir=data_dir, test_mode=test_mode
        )
        self.logger.info("phase0_data_registry_initialized")

    def _register_dataset(self, dataset: RegisteredDataset) -> bool:
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

        self.registry: ModelRegistry | None = ModelRegistry(
            data_dir=data_dir, test_mode=test_mode
        )
        self.logger.info("phase0_model_registry_initialized")

    def _register_model(self, model: RegisteredModel) -> bool:
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

        self.tracker: ExperimentTracker | None = ExperimentTracker(
            data_dir=data_dir, test_mode=test_mode
        )
        self.logger.info("phase0_experiment_tracker_initialized")

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
