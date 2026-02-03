"""Experiment tracker for ML experiments and hyperparameter tuning."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, UTC
from typing import Any
import uuid
import structlog

from .storage import JSONStorage
from .schemas import (
    ExperimentResult,
    ExperimentStatus,
    Phase,
    DataCharacteristics,
    HyperparameterConfig,
    TrainingMetrics,
)

logger = structlog.get_logger(__name__)


class ExperimentTracker:
    """Tracker for ML experiments and hyperparameter tuning."""

    def __init__(self, data_dir: str | Path = "./data", test_mode: bool = False):
        """
        Initialize experiment tracker.

        Args:
            data_dir: Directory for registry storage
            test_mode: If True, use isolated test storage
        """
        self.data_dir = Path(data_dir)
        self.test_mode = test_mode

        # Choose filename based on test mode
        filename = "experiments_test.json" if test_mode else "experiments.json"
        storage_path = self.data_dir / filename

        # Initialize JSONStorage
        self.storage = JSONStorage(storage_path, auto_create=True)

        logger.info(
            "initialized_experiment_tracker",
            data_dir=str(self.data_dir),
            test_mode=test_mode,
            storage_path=str(storage_path),
        )

    def start_experiment(
        self,
        phase: Phase,
        unit: str,
        task: str,
        experiment_id: str | None = None,
        notes: str = "",
    ) -> ExperimentResult:
        """
        Start a new experiment.

        Args:
            phase: Pipeline phase
            unit: Unit identifier
            task: Task identifier
            experiment_id: Optional experiment ID (auto-generated if None)
            notes: Experiment notes

        Returns:
            ExperimentResult with RUNNING status
        """
        # Auto-generate experiment_id if not provided
        if experiment_id is None:
            experiment_id = str(uuid.uuid4())

        # Check if experiment already exists
        if self.storage.exists(experiment_id):
            logger.error(
                "experiment_already_exists",
                experiment_id=experiment_id,
            )
            raise ValueError(f"Experiment {experiment_id} already exists")

        # Create experiment record
        experiment = ExperimentResult(
            experiment_id=experiment_id,
            phase=phase,
            unit=unit,
            task=task,
            started_at=datetime.now(UTC).isoformat(),
            status=ExperimentStatus.RUNNING,
            notes=notes,
        )

        # Save to storage
        self.storage.update(experiment_id, experiment.model_dump())

        logger.info(
            "started_experiment",
            experiment_id=experiment_id,
            phase=phase.value,
            unit=unit,
            task=task,
        )

        return experiment

    def log_data_characteristics(
        self,
        experiment_id: str,
        characteristics: DataCharacteristics,
    ) -> None:
        """
        Log data characteristics for experiment.

        Args:
            experiment_id: Experiment identifier
            characteristics: Data characteristics to log
        """
        # Get existing experiment
        experiment_data = self.storage.get(experiment_id)
        if experiment_data is None:
            logger.error(
                "experiment_not_found",
                experiment_id=experiment_id,
            )
            raise ValueError(f"Experiment {experiment_id} not found")

        # Update with data characteristics
        experiment_data["data_characteristics"] = characteristics.model_dump()
        self.storage.update(experiment_id, experiment_data)

        logger.info(
            "logged_data_characteristics",
            experiment_id=experiment_id,
            num_samples=characteristics.num_samples,
        )

    def log_hyperparameters(
        self,
        experiment_id: str,
        hyperparameters: HyperparameterConfig,
    ) -> None:
        """
        Log hyperparameters for experiment.

        Args:
            experiment_id: Experiment identifier
            hyperparameters: Hyperparameter configuration to log
        """
        # Get existing experiment
        experiment_data = self.storage.get(experiment_id)
        if experiment_data is None:
            logger.error(
                "experiment_not_found",
                experiment_id=experiment_id,
            )
            raise ValueError(f"Experiment {experiment_id} not found")

        # Update with hyperparameters
        experiment_data["hyperparameters"] = hyperparameters.model_dump()
        self.storage.update(experiment_id, experiment_data)

        logger.info(
            "logged_hyperparameters",
            experiment_id=experiment_id,
            learning_rate=hyperparameters.learning_rate,
            batch_size=hyperparameters.batch_size,
            epochs=hyperparameters.epochs,
        )

    def log_training_metrics(
        self,
        experiment_id: str,
        metrics: TrainingMetrics,
    ) -> None:
        """
        Log training metrics for experiment.

        Args:
            experiment_id: Experiment identifier
            metrics: Training metrics to log
        """
        # Get existing experiment
        experiment_data = self.storage.get(experiment_id)
        if experiment_data is None:
            logger.error(
                "experiment_not_found",
                experiment_id=experiment_id,
            )
            raise ValueError(f"Experiment {experiment_id} not found")

        # Update with training metrics
        experiment_data["metrics"] = metrics.model_dump()
        self.storage.update(experiment_id, experiment_data)

        logger.info(
            "logged_training_metrics",
            experiment_id=experiment_id,
            train_loss=metrics.train_loss,
            eval_loss=metrics.eval_loss,
        )

    def complete_experiment(
        self,
        experiment_id: str,
        model_id: str | None = None,
    ) -> ExperimentResult:
        """
        Mark experiment as COMPLETED.

        Args:
            experiment_id: Experiment identifier
            model_id: Optional model ID to link to experiment

        Returns:
            Updated ExperimentResult
        """
        # Get existing experiment
        experiment_data = self.storage.get(experiment_id)
        if experiment_data is None:
            logger.error(
                "experiment_not_found",
                experiment_id=experiment_id,
            )
            raise ValueError(f"Experiment {experiment_id} not found")

        # Update status and completion time
        experiment_data["status"] = ExperimentStatus.COMPLETED.value
        experiment_data["completed_at"] = datetime.now(UTC).isoformat()
        if model_id is not None:
            experiment_data["model_id"] = model_id

        self.storage.update(experiment_id, experiment_data)

        logger.info(
            "completed_experiment",
            experiment_id=experiment_id,
            model_id=model_id,
        )

        return ExperimentResult(**experiment_data)

    def fail_experiment(
        self,
        experiment_id: str,
        error_message: str,
    ) -> ExperimentResult:
        """
        Mark experiment as FAILED with error in notes.

        Args:
            experiment_id: Experiment identifier
            error_message: Error message to append to notes

        Returns:
            Updated ExperimentResult
        """
        # Get existing experiment
        experiment_data = self.storage.get(experiment_id)
        if experiment_data is None:
            logger.error(
                "experiment_not_found",
                experiment_id=experiment_id,
            )
            raise ValueError(f"Experiment {experiment_id} not found")

        # Update status, completion time, and notes
        experiment_data["status"] = ExperimentStatus.FAILED.value
        experiment_data["completed_at"] = datetime.now(UTC).isoformat()

        # Append error to notes
        existing_notes = experiment_data.get("notes", "")
        if existing_notes:
            experiment_data["notes"] = f"{existing_notes}\n\nERROR: {error_message}"
        else:
            experiment_data["notes"] = f"ERROR: {error_message}"

        self.storage.update(experiment_id, experiment_data)

        logger.error(
            "failed_experiment",
            experiment_id=experiment_id,
            error_message=error_message,
        )

        return ExperimentResult(**experiment_data)

    def get(self, experiment_id: str) -> ExperimentResult | None:
        """
        Get experiment by ID.

        Args:
            experiment_id: Experiment identifier

        Returns:
            ExperimentResult if found, None otherwise
        """
        experiment_data = self.storage.get(experiment_id)
        if experiment_data is None:
            logger.debug(
                "experiment_not_found",
                experiment_id=experiment_id,
            )
            return None

        return ExperimentResult(**experiment_data)

    def list(
        self,
        phase: Phase | None = None,
        unit: str | None = None,
        task: str | None = None,
        status: ExperimentStatus | None = None,
    ) -> list[ExperimentResult]:
        """
        List experiments with optional filters.

        Args:
            phase: Filter by phase
            unit: Filter by unit
            task: Filter by task
            status: Filter by status

        Returns:
            List of matching ExperimentResults
        """
        all_data = self.storage.load()
        results = []

        for experiment_data in all_data.values():
            # Apply filters
            if phase is not None and experiment_data.get("phase") != phase.value:
                continue
            if unit is not None and experiment_data.get("unit") != unit:
                continue
            if task is not None and experiment_data.get("task") != task:
                continue
            if status is not None and experiment_data.get("status") != status.value:
                continue

            results.append(ExperimentResult(**experiment_data))

        logger.debug(
            "listed_experiments",
            total_count=len(all_data),
            filtered_count=len(results),
            phase=phase.value if phase else None,
            unit=unit,
            task=task,
            status=status.value if status else None,
        )

        return results

    def find_best_config(
        self,
        unit: str,
        task: str,
        metric: str = "eval_loss",
        minimize: bool = True,
    ) -> ExperimentResult | None:
        """
        Find experiment with best metric value for unit/task.

        Args:
            unit: Unit identifier
            task: Task identifier
            metric: Metric field name in TrainingMetrics (e.g., "eval_loss", "train_loss")
            minimize: If True, find minimum value; if False, find maximum value

        Returns:
            ExperimentResult with best metric, or None if no experiments found
        """
        # Get all completed experiments for this unit/task
        experiments = self.list(
            unit=unit,
            task=task,
            status=ExperimentStatus.COMPLETED,
        )

        if not experiments:
            logger.warning(
                "no_completed_experiments_found",
                unit=unit,
                task=task,
            )
            return None

        # Filter experiments that have the requested metric
        valid_experiments = []
        for exp in experiments:
            if exp.metrics is not None:
                metric_value = getattr(exp.metrics, metric, None)
                if metric_value is not None:
                    valid_experiments.append((exp, metric_value))

        if not valid_experiments:
            logger.warning(
                "no_experiments_with_metric",
                unit=unit,
                task=task,
                metric=metric,
            )
            return None

        # Find best experiment
        if minimize:
            best_exp, best_value = min(valid_experiments, key=lambda x: x[1])
        else:
            best_exp, best_value = max(valid_experiments, key=lambda x: x[1])

        logger.info(
            "found_best_config",
            experiment_id=best_exp.experiment_id,
            unit=unit,
            task=task,
            metric=metric,
            best_value=best_value,
            minimize=minimize,
        )

        return best_exp

    def summary(self) -> dict[str, Any]:
        """
        Get tracker summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        all_data = self.storage.load()
        experiments = [ExperimentResult(**data) for data in all_data.values()]

        # Count by status
        status_counts = {
            ExperimentStatus.RUNNING.value: 0,
            ExperimentStatus.COMPLETED.value: 0,
            ExperimentStatus.FAILED.value: 0,
        }
        for exp in experiments:
            # exp.status is already a string due to use_enum_values = True
            status_counts[exp.status] += 1

        # Count by phase
        phase_counts = {}
        for exp in experiments:
            # exp.phase is already a string due to use_enum_values = True
            phase_counts[exp.phase] = phase_counts.get(exp.phase, 0) + 1

        # Count by unit
        unit_counts = {}
        for exp in experiments:
            unit_counts[exp.unit] = unit_counts.get(exp.unit, 0) + 1

        # Count by task
        task_counts = {}
        for exp in experiments:
            task_counts[exp.task] = task_counts.get(exp.task, 0) + 1

        summary = {
            "total_experiments": len(experiments),
            "by_status": status_counts,
            "by_phase": phase_counts,
            "by_unit": unit_counts,
            "by_task": task_counts,
        }

        logger.info(
            "generated_summary",
            total_experiments=len(experiments),
            completed=status_counts[ExperimentStatus.COMPLETED.value],
            running=status_counts[ExperimentStatus.RUNNING.value],
            failed=status_counts[ExperimentStatus.FAILED.value],
        )

        return summary
