import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { CodeBlock } from "@/components/ui/CodeBlock";
import { PhaseNav } from "@/components/phases/PhaseNav";
import { PhaseNavTop } from "@/components/phases/PhaseNavTop";
import { PhaseTabs } from "@/components/phases/PhaseTabs";
import { Phase0ArchitectureDiagram } from "@/components/phases/Phase0ArchitectureDiagram";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Phase 0: Infrastructure Foundation",
  description:
    "Foundational registries, logging, and evaluation infrastructure enabling all subsequent phases",
};

export default function Phase0() {
  return (
    <>
      <PageHeader
        title="Phase 0: Infrastructure Foundation"
        subtitle="Foundational registries and staging infrastructure that enable model training, evaluation, and progressive capability building"
      >
        <div className="flex gap-4 mt-4">
          <div className="text-base">
            <span className="text-white/60">Cost:</span>
            <span className="ml-2 font-semibold">$0</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Time:</span>
            <span className="ml-2 font-semibold">~2 hours</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Risk:</span>
            <span className="ml-2 font-semibold">Zero</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Enables:</span>
            <span className="ml-2 font-semibold">Phases 1-5</span>
          </div>
        </div>
      </PageHeader>

      <PhaseNavTop currentPhase={0} />

      <section className="py-12">
        <Container>
          <PhaseTabs
            vision={
              <>
                <p className="text-xl text-gray-700 mb-6">
                  Phase 0 establishes zero-cost staging infrastructure that enables all subsequent AI development—tracking models, datasets, and experiments while maintaining complete independence from production systems.
                </p>

                <p className="text-lg text-gray-700 leading-relaxed mb-6">
                  Phase 0 creates the foundational infrastructure that enables Phases 1-5. This phase establishes three file-based registries—model registry, training data registry, and experiment tracking—that make every training run measurable and every phase capable of learning from previous work.
                </p>

                <h3 className="text-xl font-bold text-navy mb-3">Strategic Value</h3>
                <p className="text-gray-700 leading-relaxed mb-4">
                  Zero-cost foundation using lightweight file-based registries with structured logging. All AI experimentation happens in isolated staging environments that cannot impact production systems. Divisions maintain self-service control over their data and experiments, preserving decentralized culture while building shared infrastructure. No customer-facing changes—all work happens behind the scenes.
                </p>

                <h3 className="text-xl font-bold text-navy mb-3">What&apos;s Delivered</h3>
                <p className="text-gray-700 leading-relaxed">
                  Staged data infrastructure mirroring each division&apos;s workflows, model registries tracking all trained models across phases, experiment tracking capturing every training run, and standardized evaluation frameworks enabling systematic learning.
                </p>
              </>
            }
            approach={
              <>
                <Card className="bg-navy/5 border-navy/20 border-t-4 border-t-navy">
                  <p className="text-xl text-gray-700 mb-6">
                    Three registries working together to track models, data, and experiments—learning what works and building on it
                  </p>

                  <h3 className="text-2xl font-bold text-navy mb-4">The Three Registry Approach</h3>
                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 0&apos;s strategy centers on deploying three registries that work together to enable systematic learning:
                  </p>

                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-navy mb-2">Model Registry</h4>
                    <p className="text-gray-700 leading-relaxed">
                      tracks every model trained across all phases—what it does, how it performs, and where it&apos;s deployed. This becomes critical in Phase 3 when the MoE router needs to know which expert models exist and which tasks they handle.
                    </p>
                  </div>

                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-navy mb-2">Training Data Registry</h4>
                    <p className="text-gray-700 leading-relaxed">
                      tracks all datasets used for training—what data exists, how it&apos;s structured, and which models trained on it. When a model performs well, you can trace back to its training data. When you create new training data, you can see which existing models might benefit from retraining.
                    </p>
                  </div>

                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-navy mb-2">Training Run Registry</h4>
                    <p className="text-gray-700 leading-relaxed">
                      captures every training experiment—what hyperparameters were used, how long it took, what the results were. This enables systematic learning: when you find hyperparameters that work for fundraising data, you can try similar settings for business development.
                    </p>
                  </div>

                  <h3 className="text-xl font-bold text-navy mb-3">How They Connect</h3>
                  <p className="text-gray-700 leading-relaxed">
                    These three registries link together through shared IDs. A training run references a dataset ID and produces a model ID. When Phase 3 needs to configure its MoE router, it queries the model registry. When Phase 4 discovers that certain data patterns work well, it can look up which training approaches produced those patterns. Everything is traceable, nothing is lost.
                  </p>

                  <div className="mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-bold text-navy mb-2">
                      Ready to see AI capabilities in action?
                    </h3>
                    <p className="text-gray-700 mb-4">
                      The technical implementation details below are optional. If you want to see the practical AI applications enabled by this infrastructure, continue to Phase 1.
                    </p>
                    <a
                      href="/solution/phase-1"
                      className="inline-block px-6 py-3 bg-navy text-white font-medium rounded-md hover:bg-navy/90 transition-colors"
                    >
                      Skip to Phase 1 →
                    </a>
                  </div>
                </Card>
              </>
            }
            technical={
              <>
                <p className="text-xl text-gray-700 mb-8">
                  File-based registry system using JSON storage with thread-safe locking, Pydantic validation, and structured logging—production-ready with 151 passing tests.
                </p>

                {/* Architecture Diagram */}
                <div className="mb-12 bg-white rounded-lg border border-gray-200 shadow-sm">
                  <Phase0ArchitectureDiagram />
                </div>

                {/* Architecture Overview */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Architecture Overview</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Three-Registry System</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 0 implements three interconnected registries that provide the foundation for all subsequent phases:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>DataRegistry</strong> tracks training datasets with full lineage—what data exists, where it came from, and which models trained on it. Every dataset gets a unique ID following the <code className="bg-gray-100 px-2 py-1 rounded text-sm">{"{phase}/{unit}/{task}/{version}"}</code> convention.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>ModelRegistry</strong> versions all models with deployment metadata—base models, fine-tuned adapters, merged MoE models, and the final orchestrator. Tracks model status from registered through trained to deployed.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    <strong>ExperimentTracker</strong> logs training runs with hyperparameters, metrics, and timestamps. Links experiments to both source datasets and resulting models, enabling complete reproducibility.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Technology Stack</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Storage:</strong> JSON files with thread-safe file locking (filelock library)</li>
                    <li><strong>Validation:</strong> Pydantic schemas for type safety and serialization</li>
                    <li><strong>Logging:</strong> structlog for structured, queryable logs</li>
                    <li><strong>Testing:</strong> pytest with 151 passing tests covering concurrent access</li>
                    <li><strong>Configuration:</strong> Pydantic BaseSettings with environment variable support</li>
                  </ul>
                </div>

                {/* Part 1: Registry Architecture */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 1: Registry Architecture</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Design Philosophy</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 0 uses a file-based approach with JSON storage and thread-safe file locking. This eliminates database infrastructure costs, simplifies deployment, and provides production-ready reliability validated by 151 passing tests.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Why File-Based?</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    For registry infrastructure tracking models, datasets, and experiments across ~5 phases with 3-5 business units, a file-based approach offers compelling advantages:
                  </p>
                  <ul className="space-y-2 text-gray-700 mb-6 list-disc list-inside">
                    <li><strong>Zero infrastructure cost:</strong> No database servers, no connection pools, no maintenance overhead</li>
                    <li><strong>Instant setup:</strong> Works immediately on any machine with a file system</li>
                    <li><strong>Simple deployment:</strong> Copy files between environments, commit to version control if needed</li>
                    <li><strong>Transparent storage:</strong> JSON files are human-readable and easy to inspect/debug</li>
                    <li><strong>Proven reliability:</strong> 151 passing tests including concurrent access scenarios</li>
                  </ul>
                  <p className="text-gray-700 leading-relaxed mb-6">
                    The registries handle metadata and lineage tracking—not high-frequency transactional workloads. This makes file-based storage an ideal fit.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Core Components</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 0 implements three registries with a shared storage backend:
                  </p>
                  <ol className="space-y-2 text-gray-700 mb-6 list-decimal list-inside">
                    <li><strong>DataRegistry</strong> (358 lines) - Tracks training datasets with lineage</li>
                    <li><strong>ModelRegistry</strong> (477 lines) - Versions models with deployment metadata</li>
                    <li><strong>ExperimentTracker</strong> (~200 lines) - Logs training runs with hyperparameters and metrics</li>
                  </ol>
                  <p className="text-gray-700 leading-relaxed mb-6">
                    All three use <strong>JSONStorage</strong> - a custom thread-safe storage backend.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">JSONStorage Implementation</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    The storage layer provides thread-safe file operations using the <code className="bg-gray-100 px-2 py-1 rounded text-sm">filelock</code> library:
                  </p>

                  <CodeBlock
                    language="python"
                    code={`from filelock import FileLock
from pathlib import Path
import json
from datetime import datetime, UTC

class JSONStorage:
    """Thread-safe JSON file storage with file locking."""

    LOCK_TIMEOUT = 10  # seconds

    def __init__(self, file_path: str | Path, auto_create: bool = True):
        self.file_path = Path(file_path)
        self.lock_path = self.file_path.with_suffix(self.file_path.suffix + ".lock")

        # Create parent directories and initialize empty file
        if auto_create:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.file_path.exists():
                self._write_data({})

    def update(self, key: str, value: Any) -> None:
        """Update with file locking to ensure thread safety."""
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                data = self._read_data()
                data[key] = value
                self._write_data(data)
                logger.debug("updated_key", file_path=str(self.file_path), key=key)
        except Exception as e:
            logger.error("update_failed", error=str(e), key=key)
            raise

    def _write_data(self, data: dict[str, Any]) -> None:
        """Write data with metadata wrapper."""
        storage_data = {
            "version": "1.0",
            "updated_at": datetime.now(UTC).isoformat(),
            "data": data,
        }

        with open(self.file_path, "w") as f:
            json.dump(storage_data, f, indent=2, ensure_ascii=False)`}
                  />

                  <div className="mt-4 bg-gray-50 p-4 rounded-lg">
                    <h5 className="font-bold text-navy mb-2">Key Features:</h5>
                    <ul className="space-y-1 text-base text-gray-700 list-disc list-inside">
                      <li><strong>10-second lock timeout:</strong> Prevents deadlocks while allowing concurrent operations</li>
                      <li><strong>Metadata wrapper:</strong> Every file includes version and timestamp</li>
                      <li><strong>Automatic directory creation:</strong> No manual setup required</li>
                      <li><strong>Backward compatibility:</strong> Handles legacy format without metadata wrapper</li>
                      <li><strong>Structured logging:</strong> All operations logged for debugging</li>
                    </ul>
                  </div>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Storage Format</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Registry files use a consistent JSON structure:
                  </p>

                  <CodeBlock
                    language="json"
                    code={`{
  "version": "1.0",
  "updated_at": "2026-01-20T10:30:00Z",
  "data": {
    "dataset_id_1": {
      "dataset_id": "2/fundraising/portfolio-analysis/v1.0.0",
      "phase": "2",
      "unit": "fundraising",
      "task": "portfolio-analysis",
      "train_samples": 1500,
      "status": "validated"
    }
  }
}`}
                  />
                </div>

                {/* Part 2: Data Registry Implementation */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 2: Data Registry Implementation</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Purpose & Responsibility:</strong> DataRegistry tracks all training datasets across phases with full lineage tracking—what data exists, where it came from, which models trained on it, and its lifecycle status.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Pydantic Schema</h4>

                  <CodeBlock
                    language="python"
                    code={`from pydantic import BaseModel
from enum import Enum

class Phase(str, Enum):
    PHASE_1 = "1"
    PHASE_2 = "2"
    PHASE_3 = "3"
    PHASE_4 = "4"
    PHASE_5 = "5"

class DataType(str, Enum):
    TASK_EXAMPLES = "task_examples"
    PREFERENCE_PAIRS = "preference_pairs"
    EMBEDDING_DATA = "embedding_data"
    CONVERSATION_DATA = "conversation_data"

class DatasetStatus(str, Enum):
    REGISTERED = "registered"
    VALIDATED = "validated"
    PROCESSED = "processed"
    EXPORTED = "exported"

class RegisteredDataset(BaseModel):
    dataset_id: str  # Format: "2/fundraising/portfolio-analysis/v1.0.0"
    phase: Phase
    unit: str
    task: str
    data_type: DataType

    # File paths
    train_path: str
    val_path: Optional[str]
    test_path: Optional[str]

    # Sample counts
    train_samples: int
    val_samples: Optional[int]
    test_samples: Optional[int]

    # Metadata
    source_description: str
    created_at: str
    updated_at: str
    status: DatasetStatus
    schema_version: str = "1.0"
    tags: list[str] = []

    # Lineage tracking
    parent_dataset_id: Optional[str] = None`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Usage Example</h4>

                  <CodeBlock
                    language="python"
                    code={`from registries import DataRegistry, RegisteredDataset
from registries.schemas import Phase, DataType, DatasetStatus

# Initialize registry
registry = DataRegistry(data_dir="./data", test_mode=False)

# Register a new dataset
dataset = RegisteredDataset(
    dataset_id="2/fundraising/portfolio-analysis/v1.0.0",
    phase=Phase.PHASE_2,
    unit="fundraising",
    task="portfolio-analysis",
    data_type=DataType.TASK_EXAMPLES,
    train_path="./data/fundraising/train.jsonl",
    train_samples=1500,
    val_path="./data/fundraising/val.jsonl",
    val_samples=200,
    source_description="Portfolio analysis task examples from investor database",
    status=DatasetStatus.VALIDATED,
    tags=["finance", "investment", "portfolio"]
)

registry.register(dataset)

# Query datasets
datasets = registry.list(
    phase=Phase.PHASE_2,
    unit="fundraising",
    status=DatasetStatus.VALIDATED
)

# Get lineage chain
lineage = registry.get_lineage("2/fundraising/portfolio-analysis/v1.0.0")

# Get registry statistics
stats = registry.summary()
# Returns: {'total': 12, 'by_phase': {'2': 5, '3': 4, '4': 3}, ...}`}
                  />

                  <div className="mt-4 bg-gray-50 p-4 rounded-lg">
                    <h5 className="font-bold text-navy mb-2">Key Methods:</h5>
                    <ul className="space-y-1 text-base text-gray-700">
                      <li><code>register(dataset)</code> - Add new dataset to registry</li>
                      <li><code>get(dataset_id)</code> - Retrieve specific dataset</li>
                      <li><code>list(phase, unit, data_type, status)</code> - Query with filters</li>
                      <li><code>update_status(dataset_id, status)</code> - Update lifecycle</li>
                      <li><code>get_lineage(dataset_id)</code> - Get parent chain</li>
                      <li><code>validate_dataset(dataset_id)</code> - Verify file paths exist</li>
                      <li><code>export_for_phase(dataset_id, target_phase)</code> - Export metadata for other phases</li>
                      <li><code>summary()</code> - Get registry statistics</li>
                    </ul>
                  </div>
                </div>

                {/* Part 3: Model Registry Implementation */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 3: Model Registry Implementation</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Purpose & Responsibility:</strong> ModelRegistry tracks all trained models across phases with deployment metadata—what models exist, what they&apos;re trained on, where they&apos;re deployed, and their performance metrics.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Pydantic Schema</h4>

                  <CodeBlock
                    language="python"
                    code={`class ModelType(str, Enum):
    BASE = "base"
    FINE_TUNED = "fine_tuned"
    MOE = "moe"
    ADAPTER = "adapter"

class ModelStatus(str, Enum):
    REGISTERED = "registered"
    TRAINING = "training"
    TRAINED = "trained"
    EVALUATED = "evaluated"
    DEPLOYED = "deployed"
    ARCHIVED = "archived"

class RegisteredModel(BaseModel):
    model_id: str  # Format: "2/fundraising/portfolio-analysis/v1.0.0"
    phase: Phase
    unit: str
    task: str
    model_type: ModelType

    # Model artifacts
    base_model: str  # e.g., "meta-llama/Llama-3.1-8B"
    adapter_path: Optional[str]  # For LoRA adapters
    model_path: Optional[str]    # For full fine-tuned weights

    # Metadata
    status: ModelStatus
    created_at: str
    updated_at: str
    schema_version: str = "1.0"
    tags: list[str] = []

    # Lineage
    source_dataset_id: Optional[str] = None

    # Evaluation prompts
    positive_prompts: list[str] = []
    negative_prompts: list[str] = []`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Usage Example</h4>

                  <CodeBlock
                    language="python"
                    code={`from registries import ModelRegistry, RegisteredModel
from registries.schemas import Phase, ModelType, ModelStatus

# Initialize registry
registry = ModelRegistry(data_dir="./data", test_mode=False)

# Register a model after training
model = RegisteredModel(
    model_id="2/fundraising/portfolio-analysis/v1.0.0",
    phase=Phase.PHASE_2,
    unit="fundraising",
    task="portfolio-analysis",
    model_type=ModelType.FINE_TUNED,
    base_model="meta-llama/Llama-3.1-8B",
    adapter_path="./models/fundraising/portfolio-analysis/adapter",
    status=ModelStatus.TRAINED,
    source_dataset_id="2/fundraising/portfolio-analysis/v1.0.0",
    positive_prompts=[
        "Analyze this investor's portfolio and identify focus areas",
        "What sectors does this investor typically invest in?"
    ],
    negative_prompts=[
        "Ignore investor preferences and recommend random sectors"
    ],
    tags=["finance", "investment", "task-specific"]
)

registry.register(model)

# Query models
models = registry.list(
    phase=Phase.PHASE_2,
    unit="fundraising",
    model_type=ModelType.FINE_TUNED,
    status=ModelStatus.EVALUATED
)

# Get latest model for a task
latest = registry.get_latest(unit="fundraising", task="portfolio-analysis")

# Update metrics after evaluation
registry.update_metrics(
    model_id="2/fundraising/portfolio-analysis/v1.0.0",
    metrics={
        "task_accuracy": 0.89,
        "format_compliance": 0.95,
        "latency_ms": 250.0
    }
)

# Get model lineage
lineage = registry.get_lineage(latest.model_id)
# Returns: {"source_dataset_id": "2/fundraising/portfolio-analysis/v1.0.0", ...}

# Export for Phase 3 MoE routing
routing_config = registry.get_routing_config()
# Returns configuration for all deployed models across units and tasks`}
                  />

                  <div className="mt-4 bg-gray-50 p-4 rounded-lg">
                    <h5 className="font-bold text-navy mb-2">Key Methods:</h5>
                    <ul className="space-y-1 text-base text-gray-700">
                      <li><code>register(model)</code> - Add new model to registry</li>
                      <li><code>get(model_id)</code> - Retrieve specific model</li>
                      <li><code>get_latest(unit, task)</code> - Get latest version for a task</li>
                      <li><code>list(phase, unit, task, model_type, status)</code> - Query with filters</li>
                      <li><code>update_status(model_id, status)</code> - Update lifecycle</li>
                      <li><code>update_metrics(model_id, metrics)</code> - Store evaluation results</li>
                      <li><code>get_lineage(model_id)</code> - Get source dataset information</li>
                      <li><code>get_routing_config()</code> - Export for Phase 3 MoE routing</li>
                      <li><code>export_for_deployment(model_id, output_dir)</code> - Create deployment package</li>
                      <li><code>summary()</code> - Get registry statistics</li>
                    </ul>
                  </div>
                </div>

                {/* Part 4: Experiment Tracking Implementation */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 4: Experiment Tracking Implementation</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Purpose & Responsibility:</strong> ExperimentTracker logs all training runs with hyperparameters, data characteristics, and metrics—enabling systematic comparison and optimization across experiments.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Pydantic Schemas</h4>

                  <CodeBlock
                    language="python"
                    code={`class ExperimentStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class DataCharacteristics(BaseModel):
    num_samples: int
    avg_input_length: float
    avg_output_length: float
    vocab_size: Optional[int] = None
    unique_tasks: Optional[int] = None

class HyperparameterConfig(BaseModel):
    epochs: int
    batch_size: int
    learning_rate: float
    lora_r: Optional[int] = None
    lora_alpha: Optional[int] = None
    warmup_steps: Optional[int] = None
    weight_decay: Optional[float] = None
    extra: dict[str, Any] = {}

class TrainingMetrics(BaseModel):
    train_loss: float
    eval_loss: Optional[float] = None
    format_compliance: Optional[float] = None
    content_coverage: Optional[float] = None
    tokens_per_second: Optional[float] = None
    training_time_seconds: Optional[float] = None

class ExperimentResult(BaseModel):
    experiment_id: str
    phase: Phase
    unit: str
    task: str

    # Timing
    started_at: str
    completed_at: Optional[str] = None
    status: ExperimentStatus

    # Experiment details
    data_characteristics: Optional[DataCharacteristics] = None
    hyperparameters: Optional[HyperparameterConfig] = None
    metrics: Optional[TrainingMetrics] = None

    # Lineage
    model_id: Optional[str] = None

    notes: str
    schema_version: str = "1.0"`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Usage Example</h4>

                  <CodeBlock
                    language="python"
                    code={`from registries import ExperimentTracker
from registries.schemas import (
    Phase,
    DataCharacteristics,
    HyperparameterConfig,
    TrainingMetrics
)

# Initialize tracker
tracker = ExperimentTracker(data_dir="./data")

# Start experiment
experiment = tracker.start_experiment(
    phase=Phase.PHASE_2,
    unit="fundraising",
    task="portfolio-analysis",
    notes="Fine-tuning Llama 3.1 8B with LoRA for portfolio analysis"
)

# Log dataset characteristics
tracker.log_data_characteristics(
    experiment.experiment_id,
    DataCharacteristics(
        num_samples=1500,
        avg_input_length=256,
        avg_output_length=128,
        vocab_size=32000,
        unique_tasks=1
    )
)

# Log hyperparameters
tracker.log_hyperparameters(
    experiment.experiment_id,
    HyperparameterConfig(
        epochs=3,
        batch_size=4,
        learning_rate=2e-4,
        lora_r=16,
        lora_alpha=32,
        warmup_steps=100,
        extra={"gradient_checkpointing": True, "optim": "adamw_8bit"}
    )
)

# After training completes, log metrics
tracker.log_training_metrics(
    experiment.experiment_id,
    TrainingMetrics(
        train_loss=0.45,
        eval_loss=0.52,
        format_compliance=0.95,
        content_coverage=0.88,
        tokens_per_second=150.0,
        training_time_seconds=3600
    )
)

# Mark experiment complete
tracker.complete_experiment(
    experiment.experiment_id,
    model_id="2/fundraising/portfolio-analysis/v1.0.0"
)

# Find best configuration for a task
best_config = tracker.find_best_config(
    unit="fundraising",
    task="portfolio-analysis",
    metric="eval_loss",
    minimize=True  # Lower is better for loss
)
print(f"Best learning rate: {best_config.hyperparameters.learning_rate}")
print(f"Best batch size: {best_config.hyperparameters.batch_size}")`}
                  />

                  <div className="mt-4 bg-gray-50 p-4 rounded-lg">
                    <h5 className="font-bold text-navy mb-2">Key Methods:</h5>
                    <ul className="space-y-1 text-base text-gray-700">
                      <li><code>start_experiment(phase, unit, task, notes)</code> - Begin tracking new experiment</li>
                      <li><code>log_data_characteristics(experiment_id, characteristics)</code> - Log dataset statistics</li>
                      <li><code>log_hyperparameters(experiment_id, hyperparameters)</code> - Log training configuration</li>
                      <li><code>log_training_metrics(experiment_id, metrics)</code> - Log training results</li>
                      <li><code>complete_experiment(experiment_id, model_id)</code> - Mark experiment as successful</li>
                      <li><code>fail_experiment(experiment_id, error_message)</code> - Mark experiment as failed</li>
                      <li><code>find_best_config(unit, task, metric, minimize)</code> - Find optimal hyperparameters</li>
                      <li><code>get_experiment(experiment_id)</code> - Retrieve specific experiment</li>
                      <li><code>list_experiments(phase, unit, task, status)</code> - Query with filters</li>
                      <li><code>summary()</code> - Get experiment statistics</li>
                    </ul>
                  </div>
                </div>

                {/* Part 5: Structured Logging & Configuration */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 5: Structured Logging & Configuration</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Structured Logging with structlog</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 0 uses structlog for production-ready logging with both human-readable console output and machine-parseable JSON format.
                  </p>

                  <h5 className="font-semibold text-navy mb-2">Configuration</h5>

                  <CodeBlock
                    language="python"
                    code={`from habitat_logging import configure_logging, get_logger

# Configure logging (call once at application startup)
configure_logging(level="INFO", format="console")  # or "json" for production

# Get logger instance
logger = get_logger(__name__)

# Log events with structured data
logger.info(
    "dataset_registered",
    dataset_id="2/fundraising/portfolio-analysis/v1.0.0",
    phase="2",
    unit="fundraising",
    train_samples=1500
)`}
                  />

                  <p className="text-gray-700 leading-relaxed mt-4 mb-2"><strong>Console Output</strong> (development):</p>
                  <CodeBlock
                    language="bash"
                    code={`2026-01-20T10:30:00Z [info] dataset_registered dataset_id=2/fundraising/portfolio-analysis/v1.0.0 phase=2 unit=fundraising train_samples=1500`}
                  />

                  <p className="text-gray-700 leading-relaxed mt-4 mb-2"><strong>JSON Output</strong> (production):</p>
                  <CodeBlock
                    language="json"
                    code={`{
  "event": "dataset_registered",
  "level": "info",
  "timestamp": "2026-01-20T10:30:00Z",
  "logger": "registries.data_registry",
  "dataset_id": "2/fundraising/portfolio-analysis/v1.0.0",
  "phase": "2",
  "unit": "fundraising",
  "train_samples": 1500
}`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Environment Configuration</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Use Pydantic Settings for environment-based configuration:
                  </p>

                  <CodeBlock
                    language="python"
                    code={`from config.base_settings import HabitatBaseSettings, PhaseSettings

# Base settings (used by Phase 0)
settings = HabitatBaseSettings()
print(settings.data_dir)  # Path('./data')
print(settings.log_level)  # 'INFO'
print(settings.log_format)  # 'console'

# Phase-specific settings (used by Phases 1-5)
phase_settings = PhaseSettings(phase=2, unit="fundraising")
print(phase_settings.registry_dir)  # Path('./data/registry')`}
                  />

                  <p className="text-gray-700 leading-relaxed mt-4 mb-2"><strong>.env file:</strong></p>
                  <CodeBlock
                    language="bash"
                    code={`# Phase 0 configuration
PHASE0_TEST_MODE=false
LOG_LEVEL=INFO
LOG_FORMAT=console  # or 'json' for production
DATA_DIR=./data`}
                  />
                </div>

                {/* Part 6: Cross-Phase Integration Pattern */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 6: Cross-Phase Integration Pattern</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">How Other Phases Use Phase 0</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    All phases (1-5) use a consistent integration pattern to import and use Phase 0 registries.
                  </p>

                  <p className="text-gray-700 mb-2"><strong>Integration Module Example</strong> (<code className="bg-gray-100 px-2 py-1 rounded text-sm">phase-4-agentic-discovery/src/shared/phase0_integration.py</code>):</p>

                  <CodeBlock
                    language="python"
                    code={`from pathlib import Path
import sys
import structlog

# Add phase-0 to Python path
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
    )
    PHASE0_AVAILABLE = True
except ImportError:
    PHASE0_AVAILABLE = False
    DataRegistry = None
    ModelRegistry = None

logger = structlog.get_logger()

class Phase4DataRegistry:
    """Phase 4 integration with Phase 0 DataRegistry."""

    def __init__(self, data_dir: Path, test_mode: bool = False):
        if PHASE0_AVAILABLE:
            self.registry = DataRegistry(data_dir=data_dir, test_mode=test_mode)
            logger.info("phase0_data_registry_initialized")
        else:
            self.registry = None
            logger.warning("phase0_not_available")`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Integration Across Phases</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Phase 1:</strong> Registers embedding training datasets and trained embedding models</li>
                    <li><strong>Phase 2:</strong> Registers task-specific datasets and fine-tuned task SLMs</li>
                    <li><strong>Phase 3:</strong> Queries ModelRegistry to build MoE routing configuration</li>
                    <li><strong>Phase 4:</strong> Registers agentic discovery datasets and experiment runs</li>
                    <li><strong>Phase 5:</strong> Queries all registries to understand available models and performance</li>
                  </ul>

                  <h4 className="text-lg font-bold text-navy mb-3">Shared ID Convention</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    All phases use standardized IDs: <code className="bg-gray-100 px-2 py-1 rounded text-sm">{"{phase}/{unit}/{task}/{version}"}</code>
                  </p>

                  <CodeBlock
                    language="python"
                    code={`from config.conventions import make_id, parse_id

# Create ID
dataset_id = make_id(
    phase=2,
    unit="fundraising",
    task="portfolio-analysis",
    version="v1.0.0"
)
# Returns: "2/fundraising/portfolio-analysis/v1.0.0"

# Parse ID
components = parse_id(dataset_id)
# Returns: {"phase": "2", "unit": "fundraising", "task": "portfolio-analysis", "version": "v1.0.0"}`}
                  />
                </div>

                {/* Part 7: Production Considerations */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 7: Production Considerations</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">When File-Based Works</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    File-based registries are production-ready for:
                  </p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li>Small to medium scale (up to hundreds of models/datasets)</li>
                    <li>Single-machine or network file system deployments</li>
                    <li>Environments where simplicity and zero infrastructure cost are priorities</li>
                    <li>Development, testing, and proof-of-concept phases</li>
                  </ul>

                  <h4 className="text-lg font-bold text-navy mb-3">When to Consider Scaling</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    As your AI habitat grows, you might consider migrating to database-backed registries if:
                  </p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li>You have thousands of models/datasets requiring complex queries</li>
                    <li>Multiple teams need concurrent high-frequency access</li>
                    <li>You need transaction guarantees across registry operations</li>
                    <li>You want to integrate with existing enterprise data infrastructure</li>
                  </ul>

                  <h4 className="text-lg font-bold text-navy mb-3">Migration Path (Optional)</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 0 is designed to make future migration straightforward:
                  </p>
                  <ol className="space-y-2 text-gray-700 list-decimal list-inside mb-6">
                    <li>Keep the same Pydantic schemas (RegisteredDataset, RegisteredModel, ExperimentResult)</li>
                    <li>Keep the same public APIs (register(), get(), list(), etc.)</li>
                    <li>Replace JSONStorage backend with SQLAlchemy or similar</li>
                    <li>All downstream phases (1-5) continue working without changes</li>
                  </ol>

                  <h4 className="text-lg font-bold text-navy mb-3">Backup Strategy</h4>

                  <CodeBlock
                    language="bash"
                    code={`#!/bin/bash
# backup_registries.sh

# Backup all registry files
tar -czf backups/phase0_registries_$(date +%Y%m%d).tar.gz ./data/*.json

# Backup to cloud storage (optional)
aws s3 cp backups/ s3://ai-habitat-backups/phase0/ --recursive`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Testing</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    The 151 passing tests provide confidence for production use:
                  </p>

                  <CodeBlock
                    language="bash"
                    code={`# Run full test suite
cd phase-0-infrastructure
pytest tests/ -v

# Results:
# test_schemas.py ......................................... 46 passed
# test_storage.py ......................................... 20 passed
# test_data_registry.py ................................... 24 passed
# test_model_registry.py .................................. 27 passed
# test_experiment_tracker.py .............................. 25 passed
# test_integration.py ..................................... 9 passed
# ============================================== 151 passed in 2.34s ==============`}
                  />
                </div>
              </>
            }
          />

          {/* Next Steps CTA */}
          <div className="bg-navy text-white p-8 rounded-lg mt-12 mb-12">
            <h3 className="text-2xl font-bold mb-4">Next: Phase 1 - Shared Embedding Space</h3>
            <p className="text-white/90 mb-4">
              With Phase 0 infrastructure in place—data staged, registries configured, experiment tracking enabled—you&apos;re ready to begin building AI capabilities. Phase 1 creates the <strong>Unified Embedding Space</strong> that enables semantic search and cross-divisional pattern discovery without centralized orchestration.
            </p>
            <p className="text-white/90 mb-6">
              Phase 1 trains custom embedding and reranker models on your staged data, creating a shared semantic infrastructure where all three divisions can find relevant information across silos—the foundation for all subsequent AI capabilities.
            </p>
            <a
              href="/solution/phase-1"
              className="inline-block px-6 py-3 bg-teal text-white font-medium rounded-md hover:bg-teal/90 transition-colors"
            >
              Continue to Phase 1 →
            </a>
          </div>
        </Container>
      </section>

      <PhaseNav currentPhase={0} />
    </>
  );
}
