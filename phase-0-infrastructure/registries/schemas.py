"""
Pydantic schemas for infrastructure registries.

This module defines all data models used across the infrastructure:
- Enums for phases, data types, model types, and statuses
- Core registry models for datasets and models
- Experiment tracking models
- Validation result dataclass
"""

from datetime import datetime, UTC
from enum import Enum
from typing import Any, Optional
from dataclasses import dataclass, field

from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================


class Phase(str, Enum):
    """Training pipeline phases."""
    PHASE_1 = "1"
    PHASE_2 = "2"
    PHASE_3 = "3"
    PHASE_4 = "4"
    PHASE_5 = "5"


class DataType(str, Enum):
    """Types of datasets in the registry."""
    TASK_EXAMPLES = "task_examples"
    PREFERENCE_PAIRS = "preference_pairs"
    EVALUATION_RESULTS = "evaluation_results"
    RAW_DOCUMENTS = "raw_documents"
    EMBEDDINGS = "embeddings"


class ModelType(str, Enum):
    """Types of models in the registry."""
    BASE = "base"
    FINE_TUNED = "fine_tuned"
    MOE = "moe"
    ADAPTER = "adapter"


class ModelStatus(str, Enum):
    """Model lifecycle states."""
    REGISTERED = "registered"
    TRAINING = "training"
    TRAINED = "trained"
    EVALUATED = "evaluated"
    EXPORTED = "exported"
    ARCHIVED = "archived"


class DatasetStatus(str, Enum):
    """Dataset lifecycle states."""
    REGISTERED = "registered"
    VALIDATED = "validated"
    PROCESSED = "processed"
    EXPORTED = "exported"


class ExperimentStatus(str, Enum):
    """Experiment execution states."""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================================
# CORE MODELS
# ============================================================================


class RegisteredDataset(BaseModel):
    """Dataset registry entry with lineage tracking."""

    dataset_id: str = Field(..., description="Unique dataset identifier")
    phase: Phase = Field(..., description="Pipeline phase (1-5)")
    unit: str = Field(..., description="Unit identifier")
    task: str = Field(..., description="Task identifier")
    data_type: DataType = Field(..., description="Type of dataset")

    # File paths
    train_path: str = Field(..., description="Path to training data")
    val_path: Optional[str] = Field(None, description="Path to validation data")
    test_path: Optional[str] = Field(None, description="Path to test data")

    # Sample counts
    train_samples: int = Field(..., ge=0, description="Number of training samples")
    val_samples: Optional[int] = Field(None, ge=0, description="Number of validation samples")
    test_samples: Optional[int] = Field(None, ge=0, description="Number of test samples")

    # Metadata
    source_description: str = Field(..., description="Description of data source and collection method")
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="Creation timestamp")
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="Last update timestamp")
    status: DatasetStatus = Field(default=DatasetStatus.REGISTERED, description="Current dataset status")
    schema_version: str = Field(default="1.0", description="Schema version")
    tags: list[str] = Field(default_factory=list, description="Searchable tags")

    # Lineage
    parent_dataset_id: Optional[str] = Field(None, description="Parent dataset for lineage tracking")

    model_config = {"use_enum_values": True, "protected_namespaces": ()}


class RegisteredModel(BaseModel):
    """Model registry entry with lineage tracking."""

    model_id: str = Field(..., description="Unique model identifier")
    phase: Phase = Field(..., description="Pipeline phase (1-5)")
    unit: str = Field(..., description="Unit identifier")
    task: str = Field(..., description="Task identifier")
    model_type: ModelType = Field(..., description="Type of model")

    # Model artifacts
    base_model: str = Field(..., description="Base model name or path")
    adapter_path: Optional[str] = Field(None, description="Path to adapter weights (for LoRA/adapters)")
    model_path: Optional[str] = Field(None, description="Path to full model weights")

    # Metadata
    status: ModelStatus = Field(default=ModelStatus.REGISTERED, description="Current model status")
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="Creation timestamp")
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="Last update timestamp")
    schema_version: str = Field(default="1.0", description="Schema version")
    tags: list[str] = Field(default_factory=list, description="Searchable tags")

    # Lineage
    source_dataset_id: Optional[str] = Field(None, description="Source dataset for lineage tracking")

    # Prompts for generation/evaluation
    positive_prompts: list[str] = Field(default_factory=list, description="Example prompts that work well")
    negative_prompts: list[str] = Field(default_factory=list, description="Example prompts to avoid")

    model_config = {"use_enum_values": True, "protected_namespaces": ()}


class DeploymentInfo(BaseModel):
    """Model deployment information."""

    model_id: str = Field(..., description="Model identifier")
    deployed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="Deployment timestamp")
    endpoint_url: Optional[str] = Field(None, description="API endpoint URL")
    deployment_type: str = Field(..., description="Type of deployment (e.g., 'vllm', 'tgi', 'local')")
    config: dict[str, Any] = Field(default_factory=dict, description="Deployment configuration")

    model_config = {"use_enum_values": True, "protected_namespaces": ()}


# ============================================================================
# EXPERIMENT MODELS
# ============================================================================


class DataCharacteristics(BaseModel):
    """Statistical characteristics of a dataset."""

    num_samples: int = Field(..., ge=0, description="Total number of samples")
    avg_input_length: float = Field(..., ge=0, description="Average input length in tokens")
    avg_output_length: float = Field(..., ge=0, description="Average output length in tokens")
    vocab_size: Optional[int] = Field(None, ge=0, description="Vocabulary size")
    unique_tasks: Optional[int] = Field(None, ge=0, description="Number of unique tasks")

    model_config = {"use_enum_values": True, "protected_namespaces": ()}


class HyperparameterConfig(BaseModel):
    """Training hyperparameters."""

    # Core training params
    epochs: int = Field(..., ge=1, description="Number of training epochs")
    batch_size: int = Field(..., ge=1, description="Batch size")
    learning_rate: float = Field(..., gt=0, description="Learning rate")

    # LoRA/Adapter params
    lora_r: Optional[int] = Field(None, ge=1, description="LoRA rank")
    lora_alpha: Optional[int] = Field(None, ge=1, description="LoRA alpha")

    # Optimization params
    warmup_steps: Optional[int] = Field(None, ge=0, description="Number of warmup steps")
    weight_decay: Optional[float] = Field(None, ge=0, description="Weight decay")

    # Additional params
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional hyperparameters")

    model_config = {"use_enum_values": True, "protected_namespaces": ()}


class TrainingMetrics(BaseModel):
    """Training and evaluation metrics."""

    # Loss metrics
    train_loss: float = Field(..., description="Training loss")
    eval_loss: Optional[float] = Field(None, description="Evaluation loss")

    # Quality metrics
    format_compliance: Optional[float] = Field(None, ge=0, le=1, description="Format compliance score")
    content_coverage: Optional[float] = Field(None, ge=0, le=1, description="Content coverage score")

    # Performance metrics
    tokens_per_second: Optional[float] = Field(None, ge=0, description="Training throughput")
    training_time_seconds: Optional[float] = Field(None, ge=0, description="Total training time")

    model_config = {"use_enum_values": True, "protected_namespaces": ()}


class ExperimentResult(BaseModel):
    """Complete experiment tracking record."""

    experiment_id: str = Field(..., description="Unique experiment identifier")
    phase: Phase = Field(..., description="Pipeline phase (1-5)")
    unit: str = Field(..., description="Unit identifier")
    task: str = Field(..., description="Task identifier")

    # Timing
    started_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="Experiment start time")
    completed_at: Optional[str] = Field(None, description="Experiment completion time")
    status: ExperimentStatus = Field(default=ExperimentStatus.RUNNING, description="Current experiment status")

    # Experiment details
    data_characteristics: Optional[DataCharacteristics] = Field(None, description="Dataset characteristics")
    hyperparameters: Optional[HyperparameterConfig] = Field(None, description="Hyperparameter configuration")
    metrics: Optional[TrainingMetrics] = Field(None, description="Training metrics")

    # Lineage
    model_id: Optional[str] = Field(None, description="Resulting model ID")

    # Additional info
    notes: str = Field(default="", description="Experiment notes and observations")
    schema_version: str = Field(default="1.0", description="Schema version")

    model_config = {"use_enum_values": True, "protected_namespaces": ()}


# ============================================================================
# VALIDATION RESULT
# ============================================================================


@dataclass
class ValidationResult:
    """Result of a validation operation.

    This follows the Phase 3 pattern for validation results.
    """

    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: dict[str, Any] = field(default_factory=dict)

    def add_error(self, message: str) -> None:
        """Add an error message and mark result as invalid."""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def merge(self, other: "ValidationResult") -> None:
        """Merge another validation result into this one."""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.update(other.info)
        if not other.is_valid:
            self.is_valid = False
