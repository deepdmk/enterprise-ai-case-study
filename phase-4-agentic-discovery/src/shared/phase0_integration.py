"""
Phase 0 Infrastructure Integration

Integrates Phase 4 with Phase 0's DataRegistry, ModelRegistry, and ExperimentTracker.
Uses base classes from Phase 0's registries.phase_integration module.
"""

import json
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


class Phase4DataRegistry(BasePhaseDataRegistry):
    """Phase 4 integration with Phase 0 DataRegistry."""

    def __init__(self, data_dir: Path, test_mode: bool = False):
        super().__init__(data_dir, test_mode, component="phase4_data_registry")

    def register_a2a_training_dataset(
        self,
        dataset_id: str,
        unit_name: str,
        train_path: Path,
        num_examples: int,
        category_distribution: dict[str, float],
        tags: list | None = None,
    ) -> bool:
        """Register A2A training dataset."""
        if not PHASE0_AVAILABLE or not self.registry:
            self.logger.warning("phase0_unavailable", action="register_dataset")
            return False

        dataset = RegisteredDataset(
            dataset_id=dataset_id,
            phase=Phase.PHASE_4,
            unit=unit_name,
            task="a2a-training",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_path),
            train_samples=num_examples,
            source_description=f"A2A protocol training data for {unit_name}",
            metadata={"category_distribution": category_distribution, "format": "chatml"},
            tags=tags or ["a2a", "protocol", "fine-tuning"],
            status=DatasetStatus.REGISTERED,
        )
        return self._register_dataset(dataset)

    def register_discovery_logs(
        self,
        dataset_id: str,
        logs_path: Path,
        discovery_phase: int,
        max_depth: int,
        total_calls: int,
        success_rate: float,
        tags: list | None = None,
    ) -> bool:
        """Register discovery logs as dataset."""
        if not PHASE0_AVAILABLE or not self.registry:
            self.logger.warning("phase0_unavailable", action="register_discovery_logs")
            return False

        dataset = RegisteredDataset(
            dataset_id=dataset_id,
            phase=Phase.PHASE_4,
            unit="discovery",
            task=f"phase{discovery_phase}-logs",
            data_type=DataType.RAW_DATA,
            train_path=str(logs_path),
            train_samples=total_calls,
            source_description=f"Discovery phase {discovery_phase} logs (depth={max_depth})",
            metadata={
                "discovery_phase": discovery_phase,
                "max_depth": max_depth,
                "success_rate": success_rate,
            },
            tags=tags or ["discovery", "a2a-calls", "logs"],
            status=DatasetStatus.REGISTERED,
        )
        return self._register_dataset(dataset)

    def register_phase5_export(
        self,
        dataset_id: str,
        train_path: Path,
        chat_path: Path,
        num_examples: int,
        optimal_depths: dict[str, int],
        tags: list | None = None,
    ) -> bool:
        """Register Phase 5 orchestrator training export."""
        if not PHASE0_AVAILABLE or not self.registry:
            self.logger.warning("phase0_unavailable", action="register_phase5_export")
            return False

        dataset = RegisteredDataset(
            dataset_id=dataset_id,
            phase=Phase.PHASE_4,
            unit="discovery",
            task="orchestrator-export",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_path),
            train_samples=num_examples,
            source_description="Phase 5 orchestrator training data from discovery logs",
            metadata={
                "optimal_depths": optimal_depths,
                "chat_format_path": str(chat_path),
                "target_phase": "phase-5",
            },
            tags=tags or ["orchestrator", "phase5-export", "routing"],
            status=DatasetStatus.REGISTERED,
        )
        return self._register_dataset(dataset)


class Phase4ModelRegistry(BasePhaseModelRegistry):
    """Phase 4 integration with Phase 0 ModelRegistry."""

    def __init__(self, data_dir: Path, test_mode: bool = False):
        super().__init__(data_dir, test_mode, component="phase4_model_registry")

    def register_a2a_adapter(
        self,
        model_id: str,
        unit_name: str,
        adapter_path: Path,
        base_model: str,
        source_dataset_id: str,
        lora_config: dict[str, Any],
        tags: list | None = None,
    ) -> bool:
        """Register A2A adapter model."""
        if not PHASE0_AVAILABLE or not self.registry:
            self.logger.warning("phase0_unavailable", action="register_model")
            return False

        model = RegisteredModel(
            model_id=model_id,
            phase=Phase.PHASE_4,
            unit=unit_name,
            task="a2a-adapter",
            model_type=ModelType.ADAPTER,
            adapter_path=str(adapter_path),
            base_model=base_model,
            source_dataset_id=source_dataset_id,
            tags=tags or ["a2a", "protocol", "lora"],
            status=ModelStatus.REGISTERED,
        )
        return self._register_model(model)


class Phase4ExperimentTracker(BasePhaseExperimentTracker):
    """Phase 4 integration with Phase 0 ExperimentTracker."""

    def __init__(self, data_dir: Path, test_mode: bool = False):
        super().__init__(data_dir, test_mode, component="phase4_experiment_tracker")

    def log_a2a_finetuning_experiment(
        self,
        experiment_id: str,
        unit_name: str,
        config: dict[str, Any],
        notes: str = "",
    ) -> bool:
        """Log A2A fine-tuning experiment."""
        if not self.tracker:
            self.logger.warning("phase0_unavailable", action="log_experiment")
            return False

        try:
            config_notes = json.dumps(config, indent=2)
            full_notes = f"{notes}\n\nConfig:\n{config_notes}" if notes else f"Config:\n{config_notes}"

            self.tracker.start_experiment(
                experiment_id=experiment_id,
                phase=Phase.PHASE_4,
                unit=unit_name,
                task="a2a-finetuning",
                notes=full_notes,
            )
            self.logger.info("experiment_logged", experiment_id=experiment_id, unit=unit_name)
            return True
        except Exception as e:
            self.logger.error(
                "experiment_logging_failed", experiment_id=experiment_id, error=str(e)
            )
            return False


def get_phase0_integration(data_dir: Path, test_mode: bool = False) -> dict[str, Any]:
    """Get Phase 0 integration components."""
    return {
        "data_registry": Phase4DataRegistry(data_dir, test_mode),
        "model_registry": Phase4ModelRegistry(data_dir, test_mode),
        "experiment_tracker": Phase4ExperimentTracker(data_dir, test_mode),
        "available": PHASE0_AVAILABLE,
    }
