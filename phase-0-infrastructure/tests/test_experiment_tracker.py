"""Tests for ExperimentTracker."""


import pytest

from phase0_infra.registries.experiment_tracker import ExperimentTracker
from phase0_infra.registries.schemas import (
    ExperimentStatus,
    Phase,
    TrainingMetrics,
)


class TestExperimentTracker:
    """Test ExperimentTracker class."""

    @pytest.fixture
    def tracker(self, temp_storage_dir):
        """Create an ExperimentTracker instance with test mode."""
        return ExperimentTracker(data_dir=temp_storage_dir, test_mode=True)

    def test_initialization(self, tracker, temp_storage_dir):
        """Test tracker initialization."""
        assert tracker.data_dir == temp_storage_dir
        assert tracker.test_mode is True
        assert tracker.storage is not None

    def test_start_experiment_with_auto_id(self, tracker):
        """Test starting experiment with auto-generated ID."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            notes="Test experiment",
        )

        assert experiment.experiment_id is not None
        assert experiment.phase == Phase.PHASE_2
        assert experiment.unit == "unit1"
        assert experiment.task == "task1"
        assert experiment.status == ExperimentStatus.RUNNING
        assert experiment.notes == "Test experiment"
        assert experiment.started_at is not None

    def test_start_experiment_with_custom_id(self, tracker):
        """Test starting experiment with custom ID."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            experiment_id="custom_exp_001",
        )

        assert experiment.experiment_id == "custom_exp_001"

    def test_start_experiment_duplicate_id_raises_error(self, tracker):
        """Test that starting experiment with duplicate ID raises ValueError."""
        tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            experiment_id="exp_001",
        )

        with pytest.raises(ValueError, match="Experiment .* already exists"):
            tracker.start_experiment(
                phase=Phase.PHASE_2,
                unit="unit1",
                task="task1",
                experiment_id="exp_001",
            )

    def test_log_data_characteristics(self, tracker, sample_data_characteristics):
        """Test logging data characteristics."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )

        tracker.log_data_characteristics(
            experiment.experiment_id,
            sample_data_characteristics,
        )

        retrieved = tracker.get(experiment.experiment_id)
        assert retrieved.data_characteristics is not None
        assert retrieved.data_characteristics.num_samples == sample_data_characteristics.num_samples
        assert retrieved.data_characteristics.avg_input_length == sample_data_characteristics.avg_input_length

    def test_log_data_characteristics_nonexistent_experiment_raises_error(self, tracker, sample_data_characteristics):
        """Test logging characteristics to nonexistent experiment raises ValueError."""
        with pytest.raises(ValueError, match="Experiment .* not found"):
            tracker.log_data_characteristics("nonexistent", sample_data_characteristics)

    def test_log_hyperparameters(self, tracker, sample_hyperparameters):
        """Test logging hyperparameters."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )

        tracker.log_hyperparameters(
            experiment.experiment_id,
            sample_hyperparameters,
        )

        retrieved = tracker.get(experiment.experiment_id)
        assert retrieved.hyperparameters is not None
        assert retrieved.hyperparameters.epochs == sample_hyperparameters.epochs
        assert retrieved.hyperparameters.batch_size == sample_hyperparameters.batch_size
        assert retrieved.hyperparameters.learning_rate == sample_hyperparameters.learning_rate

    def test_log_hyperparameters_nonexistent_experiment_raises_error(self, tracker, sample_hyperparameters):
        """Test logging hyperparameters to nonexistent experiment raises ValueError."""
        with pytest.raises(ValueError, match="Experiment .* not found"):
            tracker.log_hyperparameters("nonexistent", sample_hyperparameters)

    def test_log_training_metrics(self, tracker, sample_training_metrics):
        """Test logging training metrics."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )

        tracker.log_training_metrics(
            experiment.experiment_id,
            sample_training_metrics,
        )

        retrieved = tracker.get(experiment.experiment_id)
        assert retrieved.metrics is not None
        assert retrieved.metrics.train_loss == sample_training_metrics.train_loss
        assert retrieved.metrics.eval_loss == sample_training_metrics.eval_loss

    def test_log_training_metrics_nonexistent_experiment_raises_error(self, tracker, sample_training_metrics):
        """Test logging metrics to nonexistent experiment raises ValueError."""
        with pytest.raises(ValueError, match="Experiment .* not found"):
            tracker.log_training_metrics("nonexistent", sample_training_metrics)

    def test_complete_experiment_without_model(self, tracker):
        """Test completing experiment without model ID."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )

        completed = tracker.complete_experiment(experiment.experiment_id)

        assert completed.status == ExperimentStatus.COMPLETED
        assert completed.completed_at is not None
        assert completed.model_id is None

    def test_complete_experiment_with_model(self, tracker):
        """Test completing experiment with model ID."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )

        completed = tracker.complete_experiment(
            experiment.experiment_id,
            model_id="test_model_v1",
        )

        assert completed.status == ExperimentStatus.COMPLETED
        assert completed.completed_at is not None
        assert completed.model_id == "test_model_v1"

    def test_complete_experiment_nonexistent_raises_error(self, tracker):
        """Test completing nonexistent experiment raises ValueError."""
        with pytest.raises(ValueError, match="Experiment .* not found"):
            tracker.complete_experiment("nonexistent")

    def test_fail_experiment(self, tracker):
        """Test failing experiment with error message."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            notes="Initial notes",
        )

        failed = tracker.fail_experiment(
            experiment.experiment_id,
            error_message="Training failed due to OOM error",
        )

        assert failed.status == ExperimentStatus.FAILED
        assert failed.completed_at is not None
        assert "ERROR: Training failed due to OOM error" in failed.notes

    def test_fail_experiment_appends_to_existing_notes(self, tracker):
        """Test that failing experiment appends error to existing notes."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            notes="Initial notes",
        )

        failed = tracker.fail_experiment(
            experiment.experiment_id,
            error_message="Training failed",
        )

        assert "Initial notes" in failed.notes
        assert "ERROR: Training failed" in failed.notes

    def test_fail_experiment_nonexistent_raises_error(self, tracker):
        """Test failing nonexistent experiment raises ValueError."""
        with pytest.raises(ValueError, match="Experiment .* not found"):
            tracker.fail_experiment("nonexistent", "Error message")

    def test_get_existing_experiment(self, tracker):
        """Test getting an existing experiment."""
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )

        retrieved = tracker.get(experiment.experiment_id)

        assert retrieved is not None
        assert retrieved.experiment_id == experiment.experiment_id
        assert retrieved.phase == experiment.phase

    def test_get_nonexistent_experiment_returns_none(self, tracker):
        """Test getting nonexistent experiment returns None."""
        result = tracker.get("nonexistent")
        assert result is None

    def test_list_all_experiments(self, tracker):
        """Test listing all experiments."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")
        tracker.start_experiment(phase=Phase.PHASE_3, unit="unit2", task="task2")

        experiments = tracker.list()
        assert len(experiments) == 2

    def test_list_with_phase_filter(self, tracker):
        """Test listing experiments filtered by phase."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")
        tracker.start_experiment(phase=Phase.PHASE_3, unit="unit2", task="task2")

        experiments = tracker.list(phase=Phase.PHASE_2)
        assert len(experiments) == 1
        assert experiments[0].phase == Phase.PHASE_2

    def test_list_with_unit_filter(self, tracker):
        """Test listing experiments filtered by unit."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit2", task="task2")

        experiments = tracker.list(unit="unit1")
        assert len(experiments) == 1
        assert experiments[0].unit == "unit1"

    def test_list_with_task_filter(self, tracker):
        """Test listing experiments filtered by task."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task2")

        experiments = tracker.list(task="task1")
        assert len(experiments) == 1
        assert experiments[0].task == "task1"

    def test_list_with_status_filter(self, tracker):
        """Test listing experiments filtered by status."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")
        exp2 = tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task2")

        tracker.complete_experiment(exp2.experiment_id)

        experiments = tracker.list(status=ExperimentStatus.RUNNING)
        assert len(experiments) == 1
        assert experiments[0].status == ExperimentStatus.RUNNING

        experiments = tracker.list(status=ExperimentStatus.COMPLETED)
        assert len(experiments) == 1
        assert experiments[0].status == ExperimentStatus.COMPLETED

    def test_list_with_multiple_filters(self, tracker):
        """Test listing experiments with multiple filters."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit2", task="task1")
        tracker.start_experiment(phase=Phase.PHASE_3, unit="unit1", task="task1")

        experiments = tracker.list(phase=Phase.PHASE_2, unit="unit1", task="task1")
        assert len(experiments) == 1

    def test_find_best_config_minimize_metric(
        self,
        tracker,
        sample_hyperparameters,
        sample_data_characteristics,
    ):
        """Test finding best configuration by minimizing metric."""
        # Create experiments with different eval_loss values
        for i in range(3):
            exp = tracker.start_experiment(
                phase=Phase.PHASE_2,
                unit="unit1",
                task="task1",
            )
            tracker.log_hyperparameters(exp.experiment_id, sample_hyperparameters)
            tracker.log_data_characteristics(exp.experiment_id, sample_data_characteristics)

            # Different eval_loss values
            metrics = TrainingMetrics(
                train_loss=0.5,
                eval_loss=0.8 - (i * 0.1),  # 0.8, 0.7, 0.6
            )
            tracker.log_training_metrics(exp.experiment_id, metrics)
            tracker.complete_experiment(exp.experiment_id)

        best = tracker.find_best_config("unit1", "task1", metric="eval_loss", minimize=True)

        assert best is not None
        # Minimum value (with floating point tolerance)
        assert abs(best.metrics.eval_loss - 0.6) < 0.001

    def test_find_best_config_maximize_metric(
        self,
        tracker,
        sample_hyperparameters,
        sample_data_characteristics,
    ):
        """Test finding best configuration by maximizing metric."""
        # Create experiments with different format_compliance values
        for i in range(3):
            exp = tracker.start_experiment(
                phase=Phase.PHASE_2,
                unit="unit1",
                task="task1",
            )
            tracker.log_hyperparameters(exp.experiment_id, sample_hyperparameters)
            tracker.log_data_characteristics(exp.experiment_id, sample_data_characteristics)

            # Different format_compliance values
            metrics = TrainingMetrics(
                train_loss=0.5,
                format_compliance=0.8 + (i * 0.05),  # 0.8, 0.85, 0.9
            )
            tracker.log_training_metrics(exp.experiment_id, metrics)
            tracker.complete_experiment(exp.experiment_id)

        best = tracker.find_best_config(
            "unit1", "task1", metric="format_compliance", minimize=False
        )

        assert best is not None
        assert best.metrics.format_compliance == 0.9  # Maximum value

    def test_find_best_config_no_experiments(self, tracker):
        """Test finding best config when no experiments exist."""
        best = tracker.find_best_config("unit1", "task1")
        assert best is None

    def test_find_best_config_no_completed_experiments(self, tracker):
        """Test finding best config when no completed experiments exist."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")

        best = tracker.find_best_config("unit1", "task1")
        assert best is None

    def test_find_best_config_no_experiments_with_metric(self, tracker):
        """Test finding best config when experiments don't have requested metric."""
        exp = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )
        metrics = TrainingMetrics(train_loss=0.5)  # No eval_loss
        tracker.log_training_metrics(exp.experiment_id, metrics)
        tracker.complete_experiment(exp.experiment_id)

        best = tracker.find_best_config("unit1", "task1", metric="eval_loss")
        assert best is None

    def test_summary_empty_tracker(self, tracker):
        """Test summary for empty tracker."""
        summary = tracker.summary()

        assert summary["total_experiments"] == 0
        assert summary["by_status"]["running"] == 0
        assert summary["by_status"]["completed"] == 0
        assert summary["by_status"]["failed"] == 0

    def test_summary_with_experiments(self, tracker):
        """Test summary with multiple experiments."""
        tracker.start_experiment(phase=Phase.PHASE_2, unit="unit1", task="task1")
        exp2 = tracker.start_experiment(phase=Phase.PHASE_2, unit="unit2", task="task2")
        exp3 = tracker.start_experiment(phase=Phase.PHASE_3, unit="unit1", task="task3")

        tracker.complete_experiment(exp2.experiment_id)
        tracker.fail_experiment(exp3.experiment_id, "Error")

        summary = tracker.summary()

        assert summary["total_experiments"] == 3
        assert summary["by_status"]["running"] == 1
        assert summary["by_status"]["completed"] == 1
        assert summary["by_status"]["failed"] == 1
        assert summary["by_phase"]["2"] == 2
        assert summary["by_phase"]["3"] == 1
        assert summary["by_unit"]["unit1"] == 2
        assert summary["by_unit"]["unit2"] == 1

    def test_full_experiment_workflow(
        self,
        tracker,
        sample_data_characteristics,
        sample_hyperparameters,
        sample_training_metrics,
    ):
        """Test complete experiment workflow from start to completion."""
        # Start experiment
        experiment = tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            notes="Full workflow test",
        )
        assert experiment.status == ExperimentStatus.RUNNING

        # Log data characteristics
        tracker.log_data_characteristics(experiment.experiment_id, sample_data_characteristics)

        # Log hyperparameters
        tracker.log_hyperparameters(experiment.experiment_id, sample_hyperparameters)

        # Log metrics
        tracker.log_training_metrics(experiment.experiment_id, sample_training_metrics)

        # Complete with model
        completed = tracker.complete_experiment(
            experiment.experiment_id,
            model_id="test_model_v1",
        )

        assert completed.status == ExperimentStatus.COMPLETED
        assert completed.completed_at is not None
        assert completed.model_id == "test_model_v1"
        assert completed.data_characteristics is not None
        assert completed.hyperparameters is not None
        assert completed.metrics is not None

    def test_persistence_across_instances(self, temp_storage_dir):
        """Test that tracker persists across instances."""
        # Create first instance and start experiment
        tracker1 = ExperimentTracker(data_dir=temp_storage_dir, test_mode=True)
        tracker1.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            experiment_id="test_exp",
        )

        # Create second instance and verify data persists
        tracker2 = ExperimentTracker(data_dir=temp_storage_dir, test_mode=True)
        retrieved = tracker2.get("test_exp")

        assert retrieved is not None
        assert retrieved.experiment_id == "test_exp"
        assert retrieved.unit == "unit1"
