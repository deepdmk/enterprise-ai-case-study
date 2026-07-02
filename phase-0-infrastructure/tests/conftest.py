"""Pytest fixtures for phase-0-infrastructure tests."""


import pytest

from phase0_infra.registries.schemas import (
    DataCharacteristics,
    DatasetStatus,
    DataType,
    ExperimentResult,
    ExperimentStatus,
    HyperparameterConfig,
    ModelStatus,
    ModelType,
    Phase,
    RegisteredDataset,
    RegisteredModel,
    TrainingMetrics,
)


@pytest.fixture
def temp_storage_dir(tmp_path):
    """
    Temporary directory for test storage.

    Uses pytest's tmp_path fixture which provides a unique temp directory
    per test function.
    """
    storage_dir = tmp_path / "test_storage"
    storage_dir.mkdir(exist_ok=True)
    return storage_dir


@pytest.fixture
def sample_dataset():
    """Sample RegisteredDataset for testing."""
    return RegisteredDataset(
        dataset_id="test_dataset_v1",
        phase=Phase.PHASE_1,
        unit="test_unit",
        task="test_task",
        data_type=DataType.TASK_EXAMPLES,
        train_path="/path/to/train.jsonl",
        val_path="/path/to/val.jsonl",
        test_path="/path/to/test.jsonl",
        train_samples=1000,
        val_samples=200,
        test_samples=300,
        source_description="Test dataset for unit tests",
        status=DatasetStatus.REGISTERED,
        tags=["test", "unit_test"],
    )


@pytest.fixture
def sample_model():
    """Sample RegisteredModel for testing."""
    return RegisteredModel(
        model_id="test_model_v1",
        phase=Phase.PHASE_2,
        unit="test_unit",
        task="test_task",
        model_type=ModelType.FINE_TUNED,
        base_model="meta-llama/Llama-3.1-8B",
        adapter_path="/path/to/adapter",
        model_path="/path/to/model",
        status=ModelStatus.REGISTERED,
        source_dataset_id="test_dataset_v1",
        positive_prompts=["Good prompt example"],
        negative_prompts=["Bad prompt example"],
        tags=["test", "lora"],
    )


@pytest.fixture
def sample_experiment():
    """Sample ExperimentResult for testing."""
    return ExperimentResult(
        experiment_id="test_exp_001",
        phase=Phase.PHASE_2,
        unit="test_unit",
        task="test_task",
        status=ExperimentStatus.RUNNING,
        notes="Test experiment",
    )


@pytest.fixture
def sample_data_characteristics():
    """Sample DataCharacteristics for testing."""
    return DataCharacteristics(
        num_samples=1000,
        avg_input_length=128.5,
        avg_output_length=64.2,
        vocab_size=50000,
        unique_tasks=10,
    )


@pytest.fixture
def sample_hyperparameters():
    """Sample HyperparameterConfig for testing."""
    return HyperparameterConfig(
        epochs=3,
        batch_size=8,
        learning_rate=2e-4,
        lora_r=16,
        lora_alpha=32,
        warmup_steps=100,
        weight_decay=0.01,
        extra={"gradient_accumulation_steps": 4},
    )


@pytest.fixture
def sample_training_metrics():
    """Sample TrainingMetrics for testing."""
    return TrainingMetrics(
        train_loss=0.5,
        eval_loss=0.6,
        format_compliance=0.95,
        content_coverage=0.88,
        tokens_per_second=1500.0,
        training_time_seconds=3600.0,
    )
