# Phase 0: Infrastructure

Foundational infrastructure for Enterprise AI Habitat phases 1-5

## Overview

Phase 0 provides the core infrastructure that all downstream phases (1-5) depend on. It establishes a unified approach to data tracking, model versioning, experiment logging, and system configuration across the entire Enterprise AI Habitat ecosystem.

**Purpose**: This infrastructure layer centralizes critical capabilities:
- **Registries**: Track datasets and models with full lineage across all phases
- **Experiment Tracking**: Log hyperparameters, metrics, and results for reproducibility
- **Logging**: Structured logging with both human-readable console and machine-parseable JSON formats
- **Configuration**: Pydantic-based settings management with environment variable support
- **Evaluation Schemas**: Standardized metrics for token usage, costs, performance, and quality

**Design Principles**:
- JSON file storage with file locking for thread-safe concurrent access
- Pydantic schemas for type safety and validation
- Test mode support for isolated testing without affecting production registries
- Shared schemas and conventions across all phases (ID format: `{phase}/{unit}/{task}/{version}`)
- Automatic lineage tracking for datasets (parent relationships) and models (source datasets)

**Usage Pattern**: Other phases import via `sys.path.insert` to access registries and schemas without package installation complexity:

```python
import sys
sys.path.insert(0, "../phase-0-infrastructure")
from registries import DataRegistry, ModelRegistry, ExperimentTracker
```

## Quick Start

### Installation

```bash
cd phase-0-infrastructure
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Test basic imports
python -c "from registries.data_registry import DataRegistry; from registries.model_registry import ModelRegistry; print('OK')"

# Check logging configuration
python -c "from logging.config import configure_logging; configure_logging(); print('Logging configured')"
```

### Environment Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

## Usage Examples

### DataRegistry: Track Datasets Across Phases

```python
from registries.data_registry import DataRegistry
from registries.schemas import RegisteredDataset, Phase, DataType, DatasetStatus

# Initialize registry
registry = DataRegistry(data_dir="./data", test_mode=False)

# Register a new dataset
dataset = RegisteredDataset(
    dataset_id="phase-2/fundraising/format-alpaca/v1",
    phase=Phase.PHASE_2,
    unit="fundraising",
    task="format-alpaca",
    data_type=DataType.TASK_EXAMPLES,
    train_path="./data/phase-2/fundraising/train.jsonl",
    val_path="./data/phase-2/fundraising/val.jsonl",
    train_samples=500,
    val_samples=100,
    source_description="Fundraising portfolio analysis training data",
    tags=["fine-tuning", "instruction"],
)
registry.register(dataset)

# Retrieve dataset
dataset = registry.get("phase-2/fundraising/format-alpaca/v1")

# List datasets by phase/unit/type
phase2_datasets = registry.list(phase=Phase.PHASE_2, unit="fundraising")

# Update status
registry.update_status("phase-2/fundraising/format-alpaca/v1", DatasetStatus.VALIDATED)

# Validate dataset (checks paths exist)
result = registry.validate_dataset("phase-2/fundraising/format-alpaca/v1")
if not result.is_valid:
    print(f"Validation errors: {result.errors}")

# Get lineage (parent chain)
lineage = registry.get_lineage("phase-2/fundraising/format-alpaca/v1")

# Export for downstream phase
export_data = registry.export_for_phase(
    dataset_id="phase-2/fundraising/format-alpaca/v1",
    target_phase=Phase.PHASE_3
)

# Get summary statistics
summary = registry.summary()
print(f"Total datasets: {summary['total_datasets']}")
print(f"By phase: {summary['by_phase']}")
```

### ModelRegistry: Track Models and Versions

```python
from registries.model_registry import ModelRegistry
from registries.schemas import RegisteredModel, Phase, ModelType, ModelStatus

# Initialize registry
registry = ModelRegistry(data_dir="./data", test_mode=False)

# Register a fine-tuned model
model = RegisteredModel(
    model_id="phase-2/fundraising/portfolio-analysis_v1",
    phase=Phase.PHASE_2,
    unit="fundraising",
    task="portfolio-analysis",
    model_type=ModelType.FINE_TUNED,
    base_model="unsloth/llama-3.1-8b-bnb-4bit",
    adapter_path="./models/phase-2/fundraising/portfolio-analysis-v1",
    source_dataset_id="phase-2/fundraising/format-alpaca/v1",
    positive_prompts=[
        "Analyze this investor's portfolio for emerging tech startups",
        "What are the key investment themes in this portfolio?"
    ],
    negative_prompts=[
        "Tell me about the weather",
        "What is 2+2?"
    ],
    tags=["lora", "instruction-tuned"],
)
registry.register(model)

# Get latest version for a task
latest = registry.get_latest(unit="fundraising", task="portfolio-analysis")

# List models with filters
phase2_models = registry.list(
    phase=Phase.PHASE_2,
    unit="fundraising",
    status=ModelStatus.EVALUATED
)

# Update status
registry.update_status("phase-2/fundraising/portfolio-analysis_v1", ModelStatus.TRAINED)

# Update metrics (stored as tags)
registry.update_metrics(
    model_id="phase-2/fundraising/portfolio-analysis_v1",
    metrics={"eval_loss": 0.42, "format_compliance": 0.95}
)

# Get lineage (source dataset info)
lineage = registry.get_lineage("phase-2/fundraising/portfolio-analysis_v1")

# Get routing config for MoE (Phase 3)
routing_config = registry.get_routing_config()  # Only EVALUATED/EXPORTED models

# Export for deployment
export_data = registry.export_for_deployment(
    model_id="phase-2/fundraising/portfolio-analysis_v1",
    output_dir="./exports/phase-2"
)

# Get summary
summary = registry.summary()
print(f"Total models: {summary['total_models']}")
print(f"By status: {summary['by_status']}")
```

### ExperimentTracker: Log Training Experiments

```python
from registries.experiment_tracker import ExperimentTracker
from registries.schemas import (
    Phase,
    DataCharacteristics,
    HyperparameterConfig,
    TrainingMetrics,
    ExperimentStatus
)

# Initialize tracker
tracker = ExperimentTracker(data_dir="./data", test_mode=False)

# Start experiment
experiment = tracker.start_experiment(
    phase=Phase.PHASE_2,
    unit="fundraising",
    task="portfolio-analysis",
    notes="Testing LoRA with increased rank"
)

# Log data characteristics
tracker.log_data_characteristics(
    experiment_id=experiment.experiment_id,
    characteristics=DataCharacteristics(
        num_samples=500,
        avg_input_length=128.5,
        avg_output_length=256.3,
        vocab_size=32000,
        unique_tasks=5
    )
)

# Log hyperparameters
tracker.log_hyperparameters(
    experiment_id=experiment.experiment_id,
    hyperparameters=HyperparameterConfig(
        epochs=3,
        batch_size=4,
        learning_rate=2e-4,
        lora_r=16,
        lora_alpha=32,
        warmup_steps=100,
        weight_decay=0.01,
        extra={"gradient_accumulation_steps": 4}
    )
)

# Log training metrics
tracker.log_training_metrics(
    experiment_id=experiment.experiment_id,
    metrics=TrainingMetrics(
        train_loss=0.42,
        eval_loss=0.38,
        format_compliance=0.95,
        content_coverage=0.88,
        tokens_per_second=450.5,
        training_time_seconds=3600.0
    )
)

# Complete experiment
tracker.complete_experiment(
    experiment_id=experiment.experiment_id,
    model_id="phase-2/fundraising/portfolio-analysis_v1"
)

# Or mark as failed
# tracker.fail_experiment(
#     experiment_id=experiment.experiment_id,
#     error_message="Out of memory error during training"
# )

# List experiments with filters
completed = tracker.list(
    phase=Phase.PHASE_2,
    unit="fundraising",
    status=ExperimentStatus.COMPLETED
)

# Find best configuration for a task
best = tracker.find_best_config(
    unit="fundraising",
    task="portfolio-analysis",
    metric="eval_loss",
    minimize=True
)
if best:
    print(f"Best config: {best.hyperparameters}")
    print(f"Best eval_loss: {best.metrics.eval_loss}")

# Get summary
summary = tracker.summary()
print(f"Total experiments: {summary['total_experiments']}")
print(f"By status: {summary['by_status']}")
```

## Import from Other Phases

All downstream phases (1-5) should import Phase 0 infrastructure using this pattern:

```python
# Add Phase 0 to path (relative from your phase directory)
import sys
from pathlib import Path

phase0_path = Path(__file__).parent.parent / "phase-0-infrastructure"
sys.path.insert(0, str(phase0_path))

# Now import registries and schemas
from registries.data_registry import DataRegistry
from registries.model_registry import ModelRegistry
from registries.experiment_tracker import ExperimentTracker
from registries.schemas import (
    Phase, DataType, ModelType, DatasetStatus, ModelStatus,
    RegisteredDataset, RegisteredModel, ExperimentResult
)

# Import configuration utilities
from config.base_settings import HabitatBaseSettings, PhaseSettings
from config.conventions import make_id, parse_id

# Import logging
from logging.config import configure_logging, get_logger

# Import evaluation schemas
from evaluation.metrics_schema import (
    TokenMetrics, CostMetrics, LoadMetrics,
    QualityMetrics, EvaluationReport
)
```

## Architecture

```
phase-0-infrastructure/
├── config/                    # Configuration management
│   ├── __init__.py
│   ├── base_settings.py      # Pydantic base settings classes
│   └── conventions.py        # ID format conventions and utilities
│
├── registries/               # Core registry implementations
│   ├── data_registry.py     # Dataset tracking and lineage
│   ├── model_registry.py    # Model versioning and routing
│   ├── experiment_tracker.py # Experiment logging
│   ├── schemas.py           # Pydantic schemas for all registries
│   └── storage.py           # Thread-safe JSON storage with file locking
│
├── logging/                 # Structured logging infrastructure
│   ├── __init__.py
│   ├── config.py           # Logging configuration (console/JSON)
│   ├── formatters.py       # Custom log formatters
│   └── USAGE.md           # Logging usage guide
│
├── evaluation/             # Evaluation metrics schemas
│   └── metrics_schema.py  # Token, cost, load, quality metrics
│
├── templates/              # Templates for new phases
│   ├── README_TEMPLATE.md
│   ├── gitignore_template
│   └── pyproject_template.toml
│
├── tests/                  # Unit tests
│
├── data/                   # Runtime data storage
│   ├── data_registry.json  # Dataset registry (auto-created)
│   ├── model_registry.json # Model registry (auto-created)
│   └── experiments.json    # Experiment tracker (auto-created)
│
├── .env.example           # Environment variable template
├── .gitignore
├── pyproject.toml         # Package configuration
└── README.md             # This file
```

## API Reference

### DataRegistry

**Core Methods**:
- `register(dataset: RegisteredDataset)` → Register new dataset
- `get(dataset_id: str)` → Get dataset by ID
- `list(phase, unit, data_type, status)` → List datasets with filters
- `update_status(dataset_id, status)` → Update dataset status
- `get_lineage(dataset_id)` → Get parent chain
- `validate_dataset(dataset_id)` → Validate paths and structure
- `export_for_phase(dataset_id, target_phase)` → Export metadata
- `summary()` → Get registry statistics

**Key Schemas**:
- `RegisteredDataset`: Dataset entry with lineage and metadata
- `DataType`: Enum (task_examples, preference_pairs, evaluation_results, raw_documents, embeddings)
- `DatasetStatus`: Enum (registered, validated, processed, exported)

### ModelRegistry

**Core Methods**:
- `register(model: RegisteredModel)` → Register new model
- `get(model_id: str)` → Get model by ID
- `get_latest(unit, task)` → Get latest version for task
- `list(phase, unit, task, model_type, status)` → List models with filters
- `update_status(model_id, status)` → Update model status
- `update_metrics(model_id, metrics)` → Store evaluation metrics
- `get_lineage(model_id)` → Get source dataset info
- `get_routing_config()` → Export MoE routing config (Phase 3)
- `export_for_deployment(model_id, output_dir)` → Export deployment package
- `summary()` → Get registry statistics

**Key Schemas**:
- `RegisteredModel`: Model entry with lineage and prompts
- `ModelType`: Enum (base, fine_tuned, moe, adapter)
- `ModelStatus`: Enum (registered, training, trained, evaluated, exported, archived)

### ExperimentTracker

**Core Methods**:
- `start_experiment(phase, unit, task, notes)` → Start new experiment
- `log_data_characteristics(experiment_id, characteristics)` → Log dataset stats
- `log_hyperparameters(experiment_id, hyperparameters)` → Log training config
- `log_training_metrics(experiment_id, metrics)` → Log results
- `complete_experiment(experiment_id, model_id)` → Mark as completed
- `fail_experiment(experiment_id, error_message)` → Mark as failed
- `get(experiment_id)` → Get experiment by ID
- `list(phase, unit, task, status)` → List experiments with filters
- `find_best_config(unit, task, metric, minimize)` → Find optimal config
- `summary()` → Get tracker statistics

**Key Schemas**:
- `ExperimentResult`: Experiment record with full details
- `DataCharacteristics`: Dataset statistics
- `HyperparameterConfig`: Training hyperparameters
- `TrainingMetrics`: Loss, quality, and performance metrics
- `ExperimentStatus`: Enum (running, completed, failed)

### JSONStorage

**Core Methods**:
- `load()` → Load all data from file
- `save(data)` → Save all data to file
- `update(key, value)` → Update single key
- `delete(key)` → Delete key
- `get(key, default)` → Get single key
- `exists(key)` → Check if key exists
- `clear()` → Clear all data
- `keys()` → Get all keys

**Features**:
- Thread-safe file locking (10s timeout)
- Automatic parent directory creation
- Metadata wrapper (version, updated_at)
- Legacy format support

### Logging

**Core Functions**:
- `configure_logging(level, format)` → Set up structlog
  - `level`: DEBUG, INFO, WARNING, ERROR, CRITICAL
  - `format`: "console" (colored) or "json" (machine-parseable)
- `get_logger(name)` → Get configured logger instance

**Usage**:
```python
from logging.config import configure_logging, get_logger

configure_logging(level="INFO", format="console")
logger = get_logger(__name__)

logger.info("operation_completed", dataset_id="abc-123", samples=500)
logger.error("validation_failed", errors=["path not found"])
```

### Configuration

**HabitatBaseSettings**:
- Base class for all phase configurations
- Attributes: `test_mode`, `data_dir`, `log_level`, `log_format`
- Reads from environment variables and `.env` file

**PhaseSettings**:
- Extends HabitatBaseSettings
- Attributes: `phase`, `unit`, `registry_dir` (computed)
- Phase-specific configuration

**Conventions**:
- `make_id(phase, unit, task, version)` → Create standardized ID
- `parse_id(id_str)` → Parse ID into components
- ID Format: `{phase}/{unit}/{task}/{version}` (e.g., "2/program1/format-alpaca/v1.0.0")

### Evaluation Schemas

**EvaluationReport**:
- Comprehensive evaluation container
- Fields: `report_id`, `model_id`, `dataset_id`, `created_at`, metrics, `sample_outputs`, `notes`

**Metric Types**:
- `TokenMetrics`: input_tokens, output_tokens, total_tokens, tokens_per_second
- `CostMetrics`: input_cost, output_cost, total_cost, currency
- `LoadMetrics`: latency_ms, throughput_rps, memory_mb, gpu_utilization
- `QualityMetrics`: format_compliance, content_coverage, factual_accuracy, relevance_score, human_preference_score

## Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Test mode - set to "true" to use isolated test storage
PHASE0_TEST_MODE=false

# Logging configuration
LOG_LEVEL=INFO
LOG_FORMAT=console  # console or json

# Data directory for registry storage
DATA_DIR=./data
```

**Variable Details**:

- `PHASE0_TEST_MODE`: Enable test mode for isolated testing
  - `false` (default): Use production registry files
  - `true`: Use `*_test.json` files for isolation

- `LOG_LEVEL`: Control logging verbosity
  - `DEBUG`: Detailed debug information
  - `INFO`: General informational messages (default)
  - `WARNING`: Warning messages only
  - `ERROR`: Error messages only
  - `CRITICAL`: Critical errors only

- `LOG_FORMAT`: Log output format
  - `console`: Human-readable colored output (default)
  - `json`: Machine-parseable JSON format

- `DATA_DIR`: Root directory for data storage
  - Default: `./data`
  - All registries stored as JSON files in this directory

### Test Mode Behavior

When `test_mode=True` or `PHASE0_TEST_MODE=true`:
- DataRegistry uses `data_registry_test.json`
- ModelRegistry uses `model_registry_test.json`
- ExperimentTracker uses `experiments_test.json`
- Production registries remain untouched

This allows safe testing without affecting production data.

## Testing

### Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=registries --cov=logging --cov=config --cov=evaluation

# Run specific test file
pytest tests/test_data_registry.py -v

# Run with test mode
PHASE0_TEST_MODE=true pytest tests/ -v
```

### Test Structure

```
tests/
├── test_data_registry.py      # DataRegistry tests
├── test_model_registry.py     # ModelRegistry tests
├── test_experiment_tracker.py # ExperimentTracker tests
├── test_storage.py            # JSONStorage tests
├── test_schemas.py            # Pydantic schema validation tests
├── test_logging.py            # Logging configuration tests
└── test_config.py             # Configuration and conventions tests
```

### Writing Tests

```python
import pytest
from registries.data_registry import DataRegistry
from registries.schemas import RegisteredDataset, Phase, DataType

def test_register_dataset():
    # Use test mode
    registry = DataRegistry(data_dir="./test_data", test_mode=True)

    dataset = RegisteredDataset(
        dataset_id="test/unit/task/v1",
        phase=Phase.PHASE_1,
        unit="test_unit",
        task="test_task",
        data_type=DataType.TASK_EXAMPLES,
        train_path="./test_data/train.jsonl",
        train_samples=100,
        source_description="Test dataset"
    )

    result = registry.register(dataset)
    assert result.dataset_id == "test/unit/task/v1"

    # Cleanup
    import shutil
    shutil.rmtree("./test_data")
```

## Dependencies

From `pyproject.toml`:

### Core Dependencies

```toml
dependencies = [
    "pydantic>=2.5.0",           # Data validation and settings
    "pydantic-settings>=2.1.0",  # Settings management
    "structlog>=24.1.0",         # Structured logging
    "filelock>=3.13.0",          # Thread-safe file locking
    "pyyaml>=6.0.1",            # YAML configuration support
]
```

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",            # Testing framework
    "pytest-asyncio>=0.23.0",   # Async test support
    "ruff>=0.3.0",              # Linting and formatting
    "mypy>=1.8.0",              # Static type checking
]
```

### Python Version

- Requires Python 3.11 or higher
- Tested on Python 3.11, 3.12, 3.13

## Schema Versioning

All schemas include a `schema_version` field (default: "1.0") to support backward compatibility:

- `RegisteredDataset.schema_version`
- `RegisteredModel.schema_version`
- `ExperimentResult.schema_version`
- `EvaluationReport.schema_version`

When schemas change:
1. Increment version number
2. Add migration logic in registry loaders
3. Document breaking changes

## Lineage Tracking

### Dataset Lineage

Track parent-child relationships:

```python
# Parent dataset
parent = RegisteredDataset(
    dataset_id="phase-1/raw/documents/v1",
    phase=Phase.PHASE_1,
    # ... other fields
)
registry.register(parent)

# Child dataset (derived from parent)
child = RegisteredDataset(
    dataset_id="phase-2/processed/task-examples/v1",
    phase=Phase.PHASE_2,
    parent_dataset_id="phase-1/raw/documents/v1",  # Link to parent
    # ... other fields
)
registry.register(child)

# Get full lineage chain
lineage = registry.get_lineage("phase-2/processed/task-examples/v1")
# Returns: [parent, grandparent, ...]
```

### Model Lineage

Track source datasets:

```python
# Register model with source dataset
model = RegisteredModel(
    model_id="phase-2/unit/task/v1",
    phase=Phase.PHASE_2,
    source_dataset_id="phase-2/processed/task-examples/v1",  # Link to dataset
    # ... other fields
)
registry.register(model)

# Get lineage
lineage = registry.get_lineage("phase-2/unit/task/v1")
# Returns: {model_id, phase, unit, task, source_dataset_id, ...}
```

## Best Practices

### 1. Always Use Test Mode for Testing

```python
# Testing code
registry = DataRegistry(test_mode=True)

# Production code
registry = DataRegistry(test_mode=False)
```

### 2. Use Structured Logging

```python
# Good: Structured key-value pairs
logger.info("dataset_registered", dataset_id="abc", samples=500)

# Bad: String formatting
logger.info(f"Registered dataset {dataset_id} with {samples} samples")
```

### 3. Validate Datasets After Registration

```python
dataset = registry.register(dataset)
result = registry.validate_dataset(dataset.dataset_id)
if not result.is_valid:
    logger.error("validation_failed", errors=result.errors)
```

### 4. Track Experiments for Reproducibility

```python
# Always log:
# 1. Data characteristics
# 2. Hyperparameters
# 3. Metrics
# 4. Link to resulting model

experiment = tracker.start_experiment(...)
tracker.log_data_characteristics(...)
tracker.log_hyperparameters(...)
tracker.log_training_metrics(...)
tracker.complete_experiment(experiment_id, model_id=model.model_id)
```

### 5. Use Consistent ID Conventions

```python
from config.conventions import make_id, parse_id

# Create IDs consistently
model_id = make_id(
    phase=2,
    unit="fundraising",
    task="portfolio-analysis",
    version="v1.0.0"
)
# Result: "2/fundraising/portfolio-analysis/v1.0.0"
```

### 6. Export Models for Downstream Phases

```python
# Update status before export
registry.update_status(model_id, ModelStatus.EVALUATED)

# Export deployment package
export_data = registry.export_for_deployment(
    model_id=model_id,
    output_dir="./exports/phase-2"
)
```

## Troubleshooting

### Issue: File Lock Timeout

**Error**: `Timeout acquiring file lock`

**Solution**:
- Check for zombie processes holding locks
- Increase timeout in `JSONStorage.LOCK_TIMEOUT`
- Ensure proper exception handling to release locks

### Issue: Validation Errors

**Error**: `Validation path does not exist`

**Solution**:
- Ensure file paths are absolute or relative to correct directory
- Create directories before registering datasets
- Use `Path.resolve()` for absolute paths

### Issue: Import Errors

**Error**: `ModuleNotFoundError: No module named 'registries'`

**Solution**:
```python
# Ensure proper sys.path setup
import sys
from pathlib import Path

phase0_path = Path(__file__).parent.parent / "phase-0-infrastructure"
sys.path.insert(0, str(phase0_path))
```

### Issue: Test Data Contamination

**Problem**: Test data mixing with production data

**Solution**:
- Always use `test_mode=True` in tests
- Set `PHASE0_TEST_MODE=true` environment variable
- Use separate data directories for testing

### Issue: Schema Version Mismatch

**Error**: Pydantic validation errors on load

**Solution**:
- Check `schema_version` field
- Implement migration logic for older versions
- Document schema changes in CHANGELOG

## Migration Guide

### From Phase 2 Legacy Registry

If migrating from Phase 2's inline registry:

```python
# Old Phase 2 approach (inline)
class ModelRegistry:
    def __init__(self):
        self.registry_file = Path("./data/model_registry.json")
        # ... implementation

# New Phase 0 approach (import)
import sys
sys.path.insert(0, "../phase-0-infrastructure")
from registries import ModelRegistry

registry = ModelRegistry(data_dir="./data")
```

**Steps**:
1. Remove inline registry implementation
2. Add Phase 0 import
3. Update schema to use Phase 0 schemas
4. Migrate existing JSON data to new format
5. Update tests to use test mode

## Roadmap

### Phase 0.2 (Planned)

- [ ] Add async support for registries
- [ ] PostgreSQL backend option for registries
- [ ] REST API for remote registry access
- [ ] Web UI for registry visualization
- [ ] Enhanced metrics aggregation

### Phase 0.3 (Future)

- [ ] Multi-user support with authentication
- [ ] Registry replication and backup
- [ ] Performance benchmarking tools
- [ ] Automated data quality checks
- [ ] Integration with MLflow/Weights & Biases

## Contributing

When adding new features to Phase 0:

1. **Maintain backward compatibility**: Never break existing schemas
2. **Add tests**: All new code requires tests
3. **Update schemas**: Use Pydantic for validation
4. **Document thoroughly**: Update this README
5. **Version appropriately**: Increment schema versions when needed

## License

Part of the Emergent Enterprise AI project. See repository root for license information.

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Review existing documentation in `/docs`
- Check test files for usage examples

---

**Phase 0 Infrastructure** | Version 0.1.0 | Enterprise AI Habitat Framework
