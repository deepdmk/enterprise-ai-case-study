"""
Infrastructure registries for tracking datasets, models, and experiments.

This module provides centralized tracking and management of:
- Datasets across all pipeline phases
- Models and their lineage
- Experiment results and hyperparameter tuning

The registries use JSON file storage with file locking for thread-safe operations.

Basic usage:
    >>> from phase_0_infrastructure.registries import DataRegistry, ModelRegistry
    >>>
    >>> # Initialize registries
    >>> data_registry = DataRegistry(data_dir="./data")
    >>> model_registry = ModelRegistry(data_dir="./data")
    >>>
    >>> # Register a dataset
    >>> from phase_0_infrastructure.registries import RegisteredDataset, Phase, DataType
    >>> dataset = RegisteredDataset(
    ...     dataset_id="train_001",
    ...     phase=Phase.PHASE_2,
    ...     unit="program1",
    ...     task="format-alpaca",
    ...     data_type=DataType.TASK_EXAMPLES,
    ...     train_path="/data/train.jsonl",
    ...     train_samples=1000,
    ...     source_description="Training data from Alpaca dataset",
    ... )
    >>> data_registry.register(dataset)
"""

# Schema exports
# Registry exports
from .data_registry import DataRegistry
from .experiment_tracker import ExperimentTracker
from .model_registry import ModelRegistry
from .schemas import (
    DataCharacteristics,
    DatasetStatus,
    DataType,
    DeploymentInfo,
    ExperimentResult,
    ExperimentStatus,
    HyperparameterConfig,
    ModelStatus,
    ModelType,
    Phase,
    RegisteredDataset,
    RegisteredModel,
    TrainingMetrics,
    ValidationResult,
)

# Storage exports
from .storage import JSONStorage

__all__ = [
    # Enums
    "Phase",
    "DataType",
    "ModelType",
    "ModelStatus",
    "DatasetStatus",
    "ExperimentStatus",
    # Dataset models
    "RegisteredDataset",
    # Model models
    "RegisteredModel",
    "DeploymentInfo",
    # Experiment models
    "DataCharacteristics",
    "HyperparameterConfig",
    "TrainingMetrics",
    "ExperimentResult",
    # Validation
    "ValidationResult",
    # Storage
    "JSONStorage",
    # Registries
    "DataRegistry",
    "ModelRegistry",
    "ExperimentTracker",
]
