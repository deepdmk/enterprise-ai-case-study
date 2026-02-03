"""Tests for Pydantic schemas."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from registries.schemas import (
    Phase,
    DataType,
    ModelType,
    ModelStatus,
    DatasetStatus,
    ExperimentStatus,
    RegisteredDataset,
    RegisteredModel,
    ExperimentResult,
    DataCharacteristics,
    HyperparameterConfig,
    TrainingMetrics,
    ValidationResult,
)


class TestEnums:
    """Test enum values."""

    def test_phase_enum_values(self):
        """Test Phase enum has correct values."""
        assert Phase.PHASE_1.value == "1"
        assert Phase.PHASE_2.value == "2"
        assert Phase.PHASE_3.value == "3"
        assert Phase.PHASE_4.value == "4"
        assert Phase.PHASE_5.value == "5"

    def test_data_type_enum_values(self):
        """Test DataType enum has correct values."""
        assert DataType.TASK_EXAMPLES.value == "task_examples"
        assert DataType.PREFERENCE_PAIRS.value == "preference_pairs"
        assert DataType.EVALUATION_RESULTS.value == "evaluation_results"
        assert DataType.RAW_DOCUMENTS.value == "raw_documents"
        assert DataType.EMBEDDINGS.value == "embeddings"

    def test_model_type_enum_values(self):
        """Test ModelType enum has correct values."""
        assert ModelType.BASE.value == "base"
        assert ModelType.FINE_TUNED.value == "fine_tuned"
        assert ModelType.MOE.value == "moe"
        assert ModelType.ADAPTER.value == "adapter"

    def test_model_status_enum_values(self):
        """Test ModelStatus enum has correct values."""
        assert ModelStatus.REGISTERED.value == "registered"
        assert ModelStatus.TRAINING.value == "training"
        assert ModelStatus.TRAINED.value == "trained"
        assert ModelStatus.EVALUATED.value == "evaluated"
        assert ModelStatus.EXPORTED.value == "exported"
        assert ModelStatus.ARCHIVED.value == "archived"

    def test_dataset_status_enum_values(self):
        """Test DatasetStatus enum has correct values."""
        assert DatasetStatus.REGISTERED.value == "registered"
        assert DatasetStatus.VALIDATED.value == "validated"
        assert DatasetStatus.PROCESSED.value == "processed"
        assert DatasetStatus.EXPORTED.value == "exported"

    def test_experiment_status_enum_values(self):
        """Test ExperimentStatus enum has correct values."""
        assert ExperimentStatus.RUNNING.value == "running"
        assert ExperimentStatus.COMPLETED.value == "completed"
        assert ExperimentStatus.FAILED.value == "failed"


class TestRegisteredDataset:
    """Test RegisteredDataset model."""

    def test_create_with_valid_data(self, sample_dataset):
        """Test creating dataset with valid data."""
        assert sample_dataset.dataset_id == "test_dataset_v1"
        assert sample_dataset.phase == Phase.PHASE_1
        assert sample_dataset.unit == "test_unit"
        assert sample_dataset.task == "test_task"
        assert sample_dataset.data_type == DataType.TASK_EXAMPLES
        assert sample_dataset.train_samples == 1000
        assert sample_dataset.val_samples == 200
        assert sample_dataset.test_samples == 300
        assert sample_dataset.status == DatasetStatus.REGISTERED
        assert "test" in sample_dataset.tags

    def test_negative_samples_raises_error(self):
        """Test that negative sample counts raise validation error."""
        with pytest.raises(ValidationError):
            RegisteredDataset(
                dataset_id="test",
                phase=Phase.PHASE_1,
                unit="test_unit",
                task="test_task",
                data_type=DataType.TASK_EXAMPLES,
                train_path="/path/to/train.jsonl",
                train_samples=-100,  # Invalid negative value
                source_description="Test",
            )

    def test_missing_required_field_raises_error(self):
        """Test that missing required fields raise validation error."""
        with pytest.raises(ValidationError):
            RegisteredDataset(
                dataset_id="test",
                phase=Phase.PHASE_1,
                unit="test_unit",
                task="test_task",
                data_type=DataType.TASK_EXAMPLES,
                # Missing train_path
                train_samples=100,
                source_description="Test",
            )

    def test_optional_fields_can_be_none(self):
        """Test that optional fields can be None."""
        dataset = RegisteredDataset(
            dataset_id="test",
            phase=Phase.PHASE_1,
            unit="test_unit",
            task="test_task",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train.jsonl",
            train_samples=100,
            source_description="Test",
            val_path=None,  # Optional
            test_path=None,  # Optional
            val_samples=None,  # Optional
            test_samples=None,  # Optional
            parent_dataset_id=None,  # Optional
        )
        assert dataset.val_path is None
        assert dataset.test_path is None
        assert dataset.val_samples is None
        assert dataset.test_samples is None
        assert dataset.parent_dataset_id is None

    def test_default_values(self):
        """Test that default values are set correctly."""
        dataset = RegisteredDataset(
            dataset_id="test",
            phase=Phase.PHASE_1,
            unit="test_unit",
            task="test_task",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train.jsonl",
            train_samples=100,
            source_description="Test",
        )
        assert dataset.status == DatasetStatus.REGISTERED
        assert dataset.schema_version == "1.0"
        assert dataset.tags == []
        assert dataset.created_at is not None
        assert dataset.updated_at is not None


class TestRegisteredModel:
    """Test RegisteredModel model."""

    def test_create_with_valid_data(self, sample_model):
        """Test creating model with valid data."""
        assert sample_model.model_id == "test_model_v1"
        assert sample_model.phase == Phase.PHASE_2
        assert sample_model.unit == "test_unit"
        assert sample_model.task == "test_task"
        assert sample_model.model_type == ModelType.FINE_TUNED
        assert sample_model.base_model == "meta-llama/Llama-3.1-8B"
        assert sample_model.status == ModelStatus.REGISTERED
        assert sample_model.source_dataset_id == "test_dataset_v1"

    def test_missing_required_field_raises_error(self):
        """Test that missing required fields raise validation error."""
        with pytest.raises(ValidationError):
            RegisteredModel(
                model_id="test",
                phase=Phase.PHASE_2,
                unit="test_unit",
                task="test_task",
                model_type=ModelType.FINE_TUNED,
                # Missing base_model
            )

    def test_optional_fields_can_be_none(self):
        """Test that optional fields can be None."""
        model = RegisteredModel(
            model_id="test",
            phase=Phase.PHASE_2,
            unit="test_unit",
            task="test_task",
            model_type=ModelType.BASE,
            base_model="meta-llama/Llama-3.1-8B",
            adapter_path=None,  # Optional
            model_path=None,  # Optional
            source_dataset_id=None,  # Optional
        )
        assert model.adapter_path is None
        assert model.model_path is None
        assert model.source_dataset_id is None

    def test_default_values(self):
        """Test that default values are set correctly."""
        model = RegisteredModel(
            model_id="test",
            phase=Phase.PHASE_2,
            unit="test_unit",
            task="test_task",
            model_type=ModelType.BASE,
            base_model="meta-llama/Llama-3.1-8B",
        )
        assert model.status == ModelStatus.REGISTERED
        assert model.schema_version == "1.0"
        assert model.tags == []
        assert model.positive_prompts == []
        assert model.negative_prompts == []
        assert model.created_at is not None
        assert model.updated_at is not None


class TestDataCharacteristics:
    """Test DataCharacteristics model."""

    def test_create_with_valid_data(self, sample_data_characteristics):
        """Test creating with valid data."""
        assert sample_data_characteristics.num_samples == 1000
        assert sample_data_characteristics.avg_input_length == 128.5
        assert sample_data_characteristics.avg_output_length == 64.2
        assert sample_data_characteristics.vocab_size == 50000
        assert sample_data_characteristics.unique_tasks == 10

    def test_negative_values_raise_error(self):
        """Test that negative values raise validation error."""
        with pytest.raises(ValidationError):
            DataCharacteristics(
                num_samples=-100,  # Invalid
                avg_input_length=128.5,
                avg_output_length=64.2,
            )

    def test_optional_fields_can_be_none(self):
        """Test that optional fields can be None."""
        chars = DataCharacteristics(
            num_samples=1000,
            avg_input_length=128.5,
            avg_output_length=64.2,
            vocab_size=None,  # Optional
            unique_tasks=None,  # Optional
        )
        assert chars.vocab_size is None
        assert chars.unique_tasks is None


class TestHyperparameterConfig:
    """Test HyperparameterConfig model."""

    def test_create_with_valid_data(self, sample_hyperparameters):
        """Test creating with valid data."""
        assert sample_hyperparameters.epochs == 3
        assert sample_hyperparameters.batch_size == 8
        assert sample_hyperparameters.learning_rate == 2e-4
        assert sample_hyperparameters.lora_r == 16
        assert sample_hyperparameters.lora_alpha == 32
        assert sample_hyperparameters.warmup_steps == 100
        assert sample_hyperparameters.weight_decay == 0.01
        assert sample_hyperparameters.extra["gradient_accumulation_steps"] == 4

    def test_zero_or_negative_epochs_raise_error(self):
        """Test that invalid epochs raise validation error."""
        with pytest.raises(ValidationError):
            HyperparameterConfig(
                epochs=0,  # Invalid
                batch_size=8,
                learning_rate=2e-4,
            )

    def test_zero_or_negative_learning_rate_raises_error(self):
        """Test that invalid learning rate raises validation error."""
        with pytest.raises(ValidationError):
            HyperparameterConfig(
                epochs=3,
                batch_size=8,
                learning_rate=0,  # Invalid
            )

    def test_optional_fields_default_to_none(self):
        """Test that optional fields default to None."""
        config = HyperparameterConfig(
            epochs=3,
            batch_size=8,
            learning_rate=2e-4,
        )
        assert config.lora_r is None
        assert config.lora_alpha is None
        assert config.warmup_steps is None
        assert config.weight_decay is None
        assert config.extra == {}


class TestTrainingMetrics:
    """Test TrainingMetrics model."""

    def test_create_with_valid_data(self, sample_training_metrics):
        """Test creating with valid data."""
        assert sample_training_metrics.train_loss == 0.5
        assert sample_training_metrics.eval_loss == 0.6
        assert sample_training_metrics.format_compliance == 0.95
        assert sample_training_metrics.content_coverage == 0.88
        assert sample_training_metrics.tokens_per_second == 1500.0
        assert sample_training_metrics.training_time_seconds == 3600.0

    def test_scores_out_of_range_raise_error(self):
        """Test that scores outside [0, 1] range raise validation error."""
        with pytest.raises(ValidationError):
            TrainingMetrics(
                train_loss=0.5,
                format_compliance=1.5,  # Invalid - should be <= 1
            )

        with pytest.raises(ValidationError):
            TrainingMetrics(
                train_loss=0.5,
                content_coverage=-0.1,  # Invalid - should be >= 0
            )

    def test_negative_time_raises_error(self):
        """Test that negative time values raise validation error."""
        with pytest.raises(ValidationError):
            TrainingMetrics(
                train_loss=0.5,
                training_time_seconds=-100,  # Invalid
            )


class TestExperimentResult:
    """Test ExperimentResult model."""

    def test_create_with_valid_data(self, sample_experiment):
        """Test creating with valid data."""
        assert sample_experiment.experiment_id == "test_exp_001"
        assert sample_experiment.phase == Phase.PHASE_2
        assert sample_experiment.unit == "test_unit"
        assert sample_experiment.task == "test_task"
        assert sample_experiment.status == ExperimentStatus.RUNNING
        assert sample_experiment.notes == "Test experiment"

    def test_optional_fields_default_to_none(self):
        """Test that optional fields default to None."""
        exp = ExperimentResult(
            experiment_id="test",
            phase=Phase.PHASE_2,
            unit="test_unit",
            task="test_task",
        )
        assert exp.completed_at is None
        assert exp.data_characteristics is None
        assert exp.hyperparameters is None
        assert exp.metrics is None
        assert exp.model_id is None
        assert exp.notes == ""

    def test_default_values(self):
        """Test that default values are set correctly."""
        exp = ExperimentResult(
            experiment_id="test",
            phase=Phase.PHASE_2,
            unit="test_unit",
            task="test_task",
        )
        assert exp.status == ExperimentStatus.RUNNING
        assert exp.schema_version == "1.0"
        assert exp.started_at is not None


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_default_initialization(self):
        """Test default initialization."""
        result = ValidationResult()
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []
        assert result.info == {}

    def test_add_error_marks_invalid(self):
        """Test that add_error marks result as invalid."""
        result = ValidationResult()
        assert result.is_valid is True

        result.add_error("Test error")
        assert result.is_valid is False
        assert "Test error" in result.errors

        result.add_error("Another error")
        assert result.is_valid is False
        assert len(result.errors) == 2

    def test_add_warning_keeps_valid(self):
        """Test that add_warning doesn't affect validity."""
        result = ValidationResult()
        result.add_warning("Test warning")

        assert result.is_valid is True
        assert "Test warning" in result.warnings

    def test_merge_combines_results(self):
        """Test that merge combines two results correctly."""
        result1 = ValidationResult()
        result1.add_error("Error 1")
        result1.add_warning("Warning 1")
        result1.info["key1"] = "value1"

        result2 = ValidationResult()
        result2.add_error("Error 2")
        result2.add_warning("Warning 2")
        result2.info["key2"] = "value2"

        result1.merge(result2)

        assert result1.is_valid is False
        assert "Error 1" in result1.errors
        assert "Error 2" in result1.errors
        assert "Warning 1" in result1.warnings
        assert "Warning 2" in result1.warnings
        assert result1.info["key1"] == "value1"
        assert result1.info["key2"] == "value2"

    def test_merge_propagates_invalid_status(self):
        """Test that merge propagates invalid status."""
        result1 = ValidationResult()
        result1.add_warning("Warning only")
        assert result1.is_valid is True

        result2 = ValidationResult()
        result2.add_error("Error")
        assert result2.is_valid is False

        result1.merge(result2)
        assert result1.is_valid is False

    def test_merge_with_valid_result_keeps_status(self):
        """Test that merging valid result doesn't change invalid status."""
        result1 = ValidationResult()
        result1.add_error("Error")
        assert result1.is_valid is False

        result2 = ValidationResult()
        assert result2.is_valid is True

        result1.merge(result2)
        assert result1.is_valid is False
