"""
Phase 0 Infrastructure Integration

Integrates Phase 5 with Phase 0's DataRegistry, ModelRegistry, and ExperimentTracker.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import sys

# Add phase-0 to path
phase0_path = Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"
if phase0_path.exists():
    sys.path.insert(0, str(phase0_path))

try:
    from registries.data_registry import DataRegistry
    from registries.model_registry import ModelRegistry
    from registries.experiment_tracker import ExperimentTracker
    from registries.schemas import (
        RegisteredDataset,
        RegisteredModel,
        Phase,
        DataType,
        ModelType,
        DatasetStatus,
        ModelStatus
    )
    PHASE0_AVAILABLE = True
except ImportError:
    PHASE0_AVAILABLE = False
    DataRegistry = None
    ModelRegistry = None
    ExperimentTracker = None

import structlog

logger = structlog.get_logger()


class Phase5DataRegistry:
    """
    Phase 5 integration with Phase 0 DataRegistry.

    Registers:
    - Converted Phase 4 training data
    - Augmented datasets
    - Train/val/test splits
    """

    def __init__(self, data_dir: Path, test_mode: bool = False):
        """
        Initialize Phase 5 data registry.

        Args:
            data_dir: Data directory
            test_mode: If True, use test mode registry
        """
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component="phase5_data_registry")

        if PHASE0_AVAILABLE:
            self.registry = DataRegistry(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_data_registry_initialized")
        else:
            self.registry = None
            self.logger.warning(
                "phase0_not_available",
                message="Phase 0 infrastructure not found. Install from ../phase-0-infrastructure"
            )

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
        tags: Optional[list] = None
    ) -> bool:
        """
        Register converted training dataset.

        Args:
            dataset_id: Dataset ID (e.g., "phase-5/orchestrator/converted/v1")
            train_path: Training data path
            val_path: Validation data path
            test_path: Test data path
            train_samples: Number of training samples
            val_samples: Number of validation samples
            test_samples: Number of test samples
            source_description: Description of source data
            tags: Optional tags

        Returns:
            True if registered successfully
        """
        if not self.registry:
            self.logger.warning("phase0_unavailable", action="register_dataset")
            return False

        try:
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
                status=DatasetStatus.CREATED
            )

            self.registry.register(dataset)
            self.logger.info(
                "dataset_registered",
                dataset_id=dataset_id,
                total_samples=train_samples + val_samples + test_samples
            )
            return True

        except Exception as e:
            self.logger.error("dataset_registration_failed", dataset_id=dataset_id, error=str(e))
            return False


class Phase5ModelRegistry:
    """
    Phase 5 integration with Phase 0 ModelRegistry.

    Registers:
    - Fine-tuned orchestrator models
    - LoRA adapters
    - Model checkpoints
    """

    def __init__(self, data_dir: Path, test_mode: bool = False):
        """
        Initialize Phase 5 model registry.

        Args:
            data_dir: Data directory
            test_mode: If True, use test mode registry
        """
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component="phase5_model_registry")

        if PHASE0_AVAILABLE:
            self.registry = ModelRegistry(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_model_registry_initialized")
        else:
            self.registry = None
            self.logger.warning("phase0_not_available")

    def register_orchestrator_model(
        self,
        model_id: str,
        model_path: Path,
        base_model: str,
        source_dataset_id: str,
        lora_config: Dict[str, Any],
        tags: Optional[list] = None
    ) -> bool:
        """
        Register fine-tuned orchestrator model.

        Args:
            model_id: Model ID (e.g., "phase-5/orchestrator/qwen2.5-7b/v1")
            model_path: Path to model
            base_model: Base model name (e.g., "Qwen/Qwen2.5-7B")
            source_dataset_id: Source dataset ID
            lora_config: LoRA configuration
            tags: Optional tags

        Returns:
            True if registered successfully
        """
        if not self.registry:
            self.logger.warning("phase0_unavailable", action="register_model")
            return False

        try:
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
                    "adapter_type": "orchestrator_routing"
                },
                tags=tags or ["orchestrator", "routing", "lora"],
                status=ModelStatus.CREATED
            )

            self.registry.register(model)
            self.logger.info("model_registered", model_id=model_id, base_model=base_model)
            return True

        except Exception as e:
            self.logger.error("model_registration_failed", model_id=model_id, error=str(e))
            return False


class Phase5ExperimentTracker:
    """
    Phase 5 integration with Phase 0 ExperimentTracker.

    Tracks:
    - Fine-tuning experiments
    - Evaluation runs
    - Hyperparameter configurations
    """

    def __init__(self, data_dir: Path, test_mode: bool = False):
        """
        Initialize Phase 5 experiment tracker.

        Args:
            data_dir: Data directory
            test_mode: If True, use test mode tracker
        """
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component="phase5_experiment_tracker")

        if PHASE0_AVAILABLE:
            self.tracker = ExperimentTracker(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_experiment_tracker_initialized")
        else:
            self.tracker = None
            self.logger.warning("phase0_not_available")

    def log_finetuning_experiment(
        self,
        experiment_id: str,
        config: Dict[str, Any],
        metrics: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Log fine-tuning experiment.

        Args:
            experiment_id: Experiment ID
            config: Training configuration
            metrics: Training metrics

        Returns:
            True if logged successfully
        """
        if not self.tracker:
            self.logger.warning("phase0_unavailable", action="log_experiment")
            return False

        try:
            self.tracker.start_experiment(
                experiment_id=experiment_id,
                phase="phase-5",
                unit="orchestrator",
                task="fine-tuning",
                config=config
            )

            if metrics:
                for metric_name, metric_value in metrics.items():
                    self.tracker.log_metric(experiment_id, metric_name, metric_value)

            self.logger.info("experiment_logged", experiment_id=experiment_id)
            return True

        except Exception as e:
            self.logger.error("experiment_logging_failed", experiment_id=experiment_id, error=str(e))
            return False

    def complete_experiment(
        self,
        experiment_id: str,
        final_metrics: Dict[str, Any]
    ) -> bool:
        """
        Mark experiment as complete.

        Args:
            experiment_id: Experiment ID
            final_metrics: Final evaluation metrics

        Returns:
            True if completed successfully
        """
        if not self.tracker:
            return False

        try:
            for metric_name, metric_value in final_metrics.items():
                self.tracker.log_metric(experiment_id, metric_name, metric_value)

            self.tracker.complete_experiment(experiment_id, status="completed")
            self.logger.info("experiment_completed", experiment_id=experiment_id)
            return True

        except Exception as e:
            self.logger.error("experiment_completion_failed", experiment_id=experiment_id, error=str(e))
            return False


def get_phase0_integration(data_dir: Path, test_mode: bool = False) -> Dict[str, Any]:
    """
    Get Phase 0 integration components.

    Args:
        data_dir: Data directory
        test_mode: If True, use test mode

    Returns:
        Dictionary with data_registry, model_registry, experiment_tracker
    """
    return {
        "data_registry": Phase5DataRegistry(data_dir, test_mode),
        "model_registry": Phase5ModelRegistry(data_dir, test_mode),
        "experiment_tracker": Phase5ExperimentTracker(data_dir, test_mode),
        "available": PHASE0_AVAILABLE
    }
