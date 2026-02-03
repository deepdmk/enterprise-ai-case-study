"""
Phase 0 Infrastructure Integration

Integrates Phase 4 with Phase 0's DataRegistry, ModelRegistry, and ExperimentTracker.
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


class Phase4DataRegistry:
    """
    Phase 4 integration with Phase 0 DataRegistry.

    Registers:
    - A2A training datasets
    - Discovery logs
    - Phase 5 export datasets
    """

    def __init__(self, data_dir: Path, test_mode: bool = False):
        """
        Initialize Phase 4 data registry.

        Args:
            data_dir: Data directory
            test_mode: If True, use test mode registry
        """
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component="phase4_data_registry")

        if PHASE0_AVAILABLE:
            self.registry = DataRegistry(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_data_registry_initialized")
        else:
            self.registry = None
            self.logger.warning(
                "phase0_not_available",
                message="Phase 0 infrastructure not found. Install from ../phase-0-infrastructure"
            )

    def register_a2a_training_dataset(
        self,
        dataset_id: str,
        unit_name: str,
        train_path: Path,
        num_examples: int,
        category_distribution: Dict[str, float],
        tags: Optional[list] = None
    ) -> bool:
        """
        Register A2A training dataset.

        Args:
            dataset_id: Dataset ID (e.g., "phase-4/fundraising/a2a-training/v1")
            unit_name: Unit name (fundraising, business_development, field_operations)
            train_path: Path to training data
            num_examples: Number of training examples
            category_distribution: Distribution of example categories
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
                phase=Phase.PHASE_4,
                unit=unit_name,
                task="a2a-training",
                data_type=DataType.TASK_EXAMPLES,
                train_path=str(train_path),
                train_samples=num_examples,
                source_description=f"A2A protocol training data for {unit_name}",
                metadata={
                    "category_distribution": category_distribution,
                    "format": "chatml"
                },
                tags=tags or ["a2a", "protocol", "fine-tuning"],
                status=DatasetStatus.REGISTERED
            )

            self.registry.register(dataset)
            self.logger.info(
                "dataset_registered",
                dataset_id=dataset_id,
                total_samples=num_examples
            )
            return True

        except Exception as e:
            self.logger.error("dataset_registration_failed", dataset_id=dataset_id, error=str(e))
            return False

    def register_discovery_logs(
        self,
        dataset_id: str,
        logs_path: Path,
        discovery_phase: int,
        max_depth: int,
        total_calls: int,
        success_rate: float,
        tags: Optional[list] = None
    ) -> bool:
        """
        Register discovery logs as dataset.

        Args:
            dataset_id: Dataset ID (e.g., "phase-4/discovery/phase1-logs/v1")
            logs_path: Path to discovery logs
            discovery_phase: Discovery phase number (1-7)
            max_depth: Maximum depth for this phase
            total_calls: Total A2A calls made
            success_rate: Success rate (0.0-1.0)
            tags: Optional tags

        Returns:
            True if registered successfully
        """
        if not self.registry:
            self.logger.warning("phase0_unavailable", action="register_discovery_logs")
            return False

        try:
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
                    "success_rate": success_rate
                },
                tags=tags or ["discovery", "a2a-calls", "logs"],
                status=DatasetStatus.REGISTERED
            )

            self.registry.register(dataset)
            self.logger.info(
                "discovery_logs_registered",
                dataset_id=dataset_id,
                phase=discovery_phase,
                calls=total_calls
            )
            return True

        except Exception as e:
            self.logger.error("discovery_logs_registration_failed", dataset_id=dataset_id, error=str(e))
            return False

    def register_phase5_export(
        self,
        dataset_id: str,
        train_path: Path,
        chat_path: Path,
        num_examples: int,
        optimal_depths: Dict[str, int],
        tags: Optional[list] = None
    ) -> bool:
        """
        Register Phase 5 orchestrator training export.

        Args:
            dataset_id: Dataset ID (e.g., "phase-4/discovery/orchestrator-export/v1")
            train_path: Path to training examples
            chat_path: Path to chat format data
            num_examples: Number of examples
            optimal_depths: Optimal depths per workflow
            tags: Optional tags

        Returns:
            True if registered successfully
        """
        if not self.registry:
            self.logger.warning("phase0_unavailable", action="register_phase5_export")
            return False

        try:
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
                    "target_phase": "phase-5"
                },
                tags=tags or ["orchestrator", "phase5-export", "routing"],
                status=DatasetStatus.REGISTERED
            )

            self.registry.register(dataset)
            self.logger.info(
                "phase5_export_registered",
                dataset_id=dataset_id,
                examples=num_examples
            )
            return True

        except Exception as e:
            self.logger.error("phase5_export_registration_failed", dataset_id=dataset_id, error=str(e))
            return False


class Phase4ModelRegistry:
    """
    Phase 4 integration with Phase 0 ModelRegistry.

    Registers:
    - A2A adapters (LoRA)
    - Fine-tuned A2A models
    """

    def __init__(self, data_dir: Path, test_mode: bool = False):
        """
        Initialize Phase 4 model registry.

        Args:
            data_dir: Data directory
            test_mode: If True, use test mode registry
        """
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component="phase4_model_registry")

        if PHASE0_AVAILABLE:
            self.registry = ModelRegistry(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_model_registry_initialized")
        else:
            self.registry = None
            self.logger.warning("phase0_not_available")

    def register_a2a_adapter(
        self,
        model_id: str,
        unit_name: str,
        adapter_path: Path,
        base_model: str,
        source_dataset_id: str,
        lora_config: Dict[str, Any],
        tags: Optional[list] = None
    ) -> bool:
        """
        Register A2A adapter model.

        Args:
            model_id: Model ID (e.g., "phase-4/fundraising/a2a-adapter/v1")
            unit_name: Unit name
            adapter_path: Path to adapter
            base_model: Base model name (e.g., "fundraising_moe")
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
                phase=Phase.PHASE_4,
                unit=unit_name,
                task="a2a-adapter",
                model_type=ModelType.ADAPTER,
                adapter_path=str(adapter_path),
                base_model=base_model,
                source_dataset_id=source_dataset_id,
                tags=tags or ["a2a", "protocol", "lora"],
                status=ModelStatus.REGISTERED
            )

            self.registry.register(model)
            self.logger.info("model_registered", model_id=model_id, unit=unit_name)
            return True

        except Exception as e:
            self.logger.error("model_registration_failed", model_id=model_id, error=str(e))
            return False


class Phase4ExperimentTracker:
    """
    Phase 4 integration with Phase 0 ExperimentTracker.

    Tracks:
    - A2A fine-tuning experiments
    - Discovery experiments
    """

    def __init__(self, data_dir: Path, test_mode: bool = False):
        """
        Initialize Phase 4 experiment tracker.

        Args:
            data_dir: Data directory
            test_mode: If True, use test mode tracker
        """
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode
        self.logger = logger.bind(component="phase4_experiment_tracker")

        if PHASE0_AVAILABLE:
            self.tracker = ExperimentTracker(data_dir=data_dir, test_mode=test_mode)
            self.logger.info("phase0_experiment_tracker_initialized")
        else:
            self.tracker = None
            self.logger.warning("phase0_not_available")

    def log_a2a_finetuning_experiment(
        self,
        experiment_id: str,
        unit_name: str,
        config: Dict[str, Any],
        notes: str = ""
    ) -> bool:
        """
        Log A2A fine-tuning experiment.

        Args:
            experiment_id: Experiment ID
            unit_name: Unit name
            config: Training configuration (stored in notes)
            notes: Additional notes

        Returns:
            True if logged successfully
        """
        if not self.tracker:
            self.logger.warning("phase0_unavailable", action="log_experiment")
            return False

        try:
            import json
            config_notes = json.dumps(config, indent=2)
            full_notes = f"{notes}\n\nConfig:\n{config_notes}" if notes else f"Config:\n{config_notes}"

            self.tracker.start_experiment(
                experiment_id=experiment_id,
                phase=Phase.PHASE_4,
                unit=unit_name,
                task="a2a-finetuning",
                notes=full_notes
            )

            self.logger.info("experiment_logged", experiment_id=experiment_id, unit=unit_name)
            return True

        except Exception as e:
            self.logger.error("experiment_logging_failed", experiment_id=experiment_id, error=str(e))
            return False

    def complete_experiment(
        self,
        experiment_id: str,
        model_id: Optional[str] = None
    ) -> bool:
        """
        Mark experiment as complete.

        Args:
            experiment_id: Experiment ID
            model_id: Optional model ID to link to experiment

        Returns:
            True if completed successfully
        """
        if not self.tracker:
            return False

        try:
            self.tracker.complete_experiment(experiment_id, model_id=model_id)
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
        "data_registry": Phase4DataRegistry(data_dir, test_mode),
        "model_registry": Phase4ModelRegistry(data_dir, test_mode),
        "experiment_tracker": Phase4ExperimentTracker(data_dir, test_mode),
        "available": PHASE0_AVAILABLE
    }
