"""
Phase 0 Infrastructure Integration

Integrates Phase 5 with Phase 0's DataRegistry, ModelRegistry, and ExperimentTracker.
Uses base classes from Phase 0's registries.phase_integration module.
"""

from pathlib import Path
from typing import Any

from src.shared.path_config import configure_paths
configure_paths()

try:
    from registries.phase_integration import (
        BasePhaseDataRegistry,
        BasePhaseExperimentTracker,
        BasePhaseModelRegistry,
        PHASE0_AVAILABLE,
    )
    from registries.schemas import (
        DatasetStatus,
        DataType,
        ModelStatus,
        ModelType,
        Phase,
        RegisteredDataset,
        RegisteredModel,
    )
except ImportError:
    PHASE0_AVAILABLE = False
    BasePhaseDataRegistry = object  # type: ignore[assignment, misc]
    BasePhaseModelRegistry = object  # type: ignore[assignment, misc]
    BasePhaseExperimentTracker = object  # type: ignore[assignment, misc]

from habitat_logging import get_logger

logger = get_logger(__name__)


class Phase5DataRegistry(BasePhaseDataRegistry):
    """Phase 5 integration with Phase 0 DataRegistry."""

    def __init__(self, data_dir: Path, test_mode: bool = False):
        super().__init__(data_dir, test_mode, component="phase5_data_registry")

    def register_converted_dataset(
        self,
        dataset_id: str,
        train_path: Path,
        val_path: Path,
        test_path: Path,
        train_samples: int,
        val_samples: int,
        test_samples: int,
        source_description: str = "Phase 4 discovery logs",
        tags: list | None = None,
    ) -> bool:
        """Register converted training dataset."""
        if not PHASE0_AVAILABLE or not self.registry:
            self.logger.warning("phase0_unavailable", action="register_dataset")
            return False

        dataset = RegisteredDataset(
            dataset_id=dataset_id,
            phase=Phase.PHASE_5,
            unit="orchestrator",
            task="converted",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_path),
            val_path=str(val_path),
            test_path=str(test_path),
            train_samples=train_samples,
            val_samples=val_samples,
            test_samples=test_samples,
            source_description=source_description,
            tags=tags or ["orchestrator", "routing", "fine-tuning"],
            status=DatasetStatus.CREATED,
        )
        return self._register_dataset(dataset)


class Phase5ModelRegistry(BasePhaseModelRegistry):
    """Phase 5 integration with Phase 0 ModelRegistry."""

    def __init__(self, data_dir: Path, test_mode: bool = False):
        super().__init__(data_dir, test_mode, component="phase5_model_registry")

    def register_orchestrator_model(
        self,
        model_id: str,
        model_path: Path,
        base_model: str,
        source_dataset_id: str,
        lora_config: dict[str, Any],
        tags: list | None = None,
    ) -> bool:
        """Register fine-tuned orchestrator model."""
        if not PHASE0_AVAILABLE or not self.registry:
            self.logger.warning("phase0_unavailable", action="register_model")
            return False

        model = RegisteredModel(
            model_id=model_id,
            phase=Phase.PHASE_5,
            unit="orchestrator",
            task="routing",
            model_type=ModelType.LORA_ADAPTER,
            model_path=str(model_path),
            base_model=base_model,
            source_dataset_id=source_dataset_id,
            metadata={
                "lora_rank": lora_config.get("r", 16),
                "lora_alpha": lora_config.get("lora_alpha", 32),
                "target_modules": lora_config.get("target_modules", []),
                "lora_dropout": lora_config.get("lora_dropout", 0.05),
                "adapter_type": "orchestrator_routing",
            },
            tags=tags or ["orchestrator", "routing", "lora"],
            status=ModelStatus.CREATED,
        )
        return self._register_model(model)


class Phase5ExperimentTracker(BasePhaseExperimentTracker):
    """Phase 5 integration with Phase 0 ExperimentTracker."""

    def __init__(self, data_dir: Path, test_mode: bool = False):
        super().__init__(data_dir, test_mode, component="phase5_experiment_tracker")

    def log_finetuning_experiment(
        self,
        experiment_id: str,
        config: dict[str, Any],
        metrics: dict[str, Any] | None = None,
    ) -> bool:
        """Log fine-tuning experiment."""
        if not self.tracker:
            self.logger.warning("phase0_unavailable", action="log_experiment")
            return False

        try:
            self.tracker.start_experiment(
                experiment_id=experiment_id,
                phase="phase-5",
                unit="orchestrator",
                task="fine-tuning",
                config=config,
            )

            if metrics:
                for metric_name, metric_value in metrics.items():
                    self.tracker.log_metric(experiment_id, metric_name, metric_value)

            self.logger.info("experiment_logged", experiment_id=experiment_id)
            return True
        except Exception as e:
            self.logger.error(
                "experiment_logging_failed", experiment_id=experiment_id, error=str(e)
            )
            return False

    def complete_experiment(
        self,
        experiment_id: str,
        final_metrics: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> bool:
        """Mark experiment as complete with final metrics."""
        if not self.tracker:
            return False

        try:
            if final_metrics:
                for metric_name, metric_value in final_metrics.items():
                    self.tracker.log_metric(experiment_id, metric_name, metric_value)

            self.tracker.complete_experiment(experiment_id, status="completed")
            self.logger.info("experiment_completed", experiment_id=experiment_id)
            return True
        except Exception as e:
            self.logger.error(
                "experiment_completion_failed", experiment_id=experiment_id, error=str(e)
            )
            return False


def get_phase0_integration(data_dir: Path, test_mode: bool = False) -> dict[str, Any]:
    """Get Phase 0 integration components."""
    return {
        "data_registry": Phase5DataRegistry(data_dir, test_mode),
        "model_registry": Phase5ModelRegistry(data_dir, test_mode),
        "experiment_tracker": Phase5ExperimentTracker(data_dir, test_mode),
        "available": PHASE0_AVAILABLE,
    }
