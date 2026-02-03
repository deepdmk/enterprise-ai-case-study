# Phase 0 Infrastructure Migration

This document describes the migration of Phase 2's model registry to use the centralized Phase 0 infrastructure.

## Overview

Phase 2 now uses a **compatibility shim** that wraps the Phase 0 `ModelRegistry` while maintaining the original Phase 2 API. This ensures:

1. **Centralized registry** - All models are tracked in Phase 0's unified infrastructure
2. **Backward compatibility** - Existing Phase 2 code continues to work without changes
3. **Cross-phase lineage** - Models can be tracked across pipeline phases
4. **Consistent schemas** - All phases use the same data models

## Changes Made

### 1. Model Registry Compatibility Shim

**File**: `/src/shared/model_registry.py`

The original standalone registry has been replaced with a compatibility wrapper that:

- Imports `ModelRegistry` from `phase-0-infrastructure/registries`
- Wraps it with the Phase 2 API (method names, parameters, return types)
- Handles field name mappings:
  - `unit_id` (Phase 2) → `unit` (Phase 0)
  - `task_id` (Phase 2) → `task` (Phase 0)
- Automatically sets Phase 2-specific metadata:
  - `phase = Phase.PHASE_2`
  - `model_type = ModelType.ADAPTER`
- Stores metrics and training config as tags in Phase 0 format

### 2. Backward Compatibility Classes

The shim maintains Phase 2's original classes:

- `ModelMetrics` - Training and evaluation metrics
- `TrainingConfig` - Training configuration snapshot
- `ModelEntry` - Registry entry for a trained model

These classes are preserved for API compatibility but internally convert to/from Phase 0's `RegisteredModel` schema.

### 3. Field Mappings

| Phase 2 Field      | Phase 0 Field        | Notes                                    |
|--------------------|----------------------|------------------------------------------|
| `unit_id`          | `unit`               | Unit identifier                          |
| `task_id`          | `task`               | Task identifier                          |
| `metrics`          | `tags` (with prefix) | Stored as `metric:key=value` tags        |
| `training_config`  | `tags` (with prefix) | Stored as `training:key=value` tags      |
| `notes`            | `tags` (with prefix) | Stored as `note:text` tag                |
| `status` (string)  | `status` (enum)      | Converted to `ModelStatus` enum          |
| N/A                | `phase`              | Automatically set to `Phase.PHASE_2`     |
| N/A                | `model_type`         | Automatically set to `ModelType.ADAPTER` |

### 4. Status Mapping

Phase 2 status strings are mapped to Phase 0 enums:

```python
{
    "trained": ModelStatus.TRAINED,
    "evaluated": ModelStatus.EVALUATED,
    "exported": ModelStatus.EXPORTED,
    "archived": ModelStatus.ARCHIVED,
    "registered": ModelStatus.REGISTERED,
    "training": ModelStatus.TRAINING,
}
```

## API Compatibility

### No Changes Required

The following Phase 2 code patterns continue to work **without modification**:

```python
from src.shared.model_registry import ModelRegistry, ModelEntry, ModelMetrics, TrainingConfig

# Initialize registry
registry = ModelRegistry(registry_dir)

# Register a model
entry = registry.register(
    unit_id="fundraising",
    task_id="portfolio_analysis",
    adapter_path="/path/to/adapter",
    base_model="unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    training_config=training_config,
    positive_prompts=["analyze portfolio"],
    negative_prompts=["unrelated query"]
)

# Retrieve models
model = registry.get(model_id)
latest = registry.get_latest(unit_id, task_id)
models = registry.list_models(unit_id="unit1", status="evaluated")

# Update status and metrics
registry.update_status(model_id, "evaluated")
registry.update_metrics(model_id, metrics)

# Export for MoE
export_data = registry.export_for_moe(model_id, output_dir)
routing_config = registry.get_routing_config()
```

### Files Using Model Registry

The following files import and use the model registry (no changes needed):

1. `src/program4_model_registry/main.py` - Registry management CLI
2. `src/program4_model_registry/exporter.py` - Model export for Phase 3
3. `src/shared/__init__.py` - Module exports

## Testing

A comprehensive test suite is provided in `test_model_registry_migration.py`:

```bash
cd phase-2-task-slms
python test_model_registry_migration.py
```

This validates:
- Basic CRUD operations (create, read, update, delete)
- Metrics and status updates
- Automatic version increment
- Summary statistics
- Routing configuration export
- Field name mappings
- Phase 0 backend integration

## Registry Storage

### Phase 2 Location

Registry data is stored at:
```
phase-2-task-slms/data/registry/model_registry.json
```

### Phase 0 Format

The registry file uses Phase 0's schema:

```json
{
  "version": "1.0",
  "updated_at": "2026-01-17T12:00:00.000000",
  "models": {
    "fundraising/portfolio_analysis_v1": {
      "model_id": "fundraising/portfolio_analysis_v1",
      "phase": "2",
      "unit": "fundraising",
      "task": "portfolio_analysis",
      "model_type": "adapter",
      "base_model": "unsloth/Meta-Llama-3.1-8B-bnb-4bit",
      "adapter_path": "/path/to/adapter",
      "status": "trained",
      "positive_prompts": ["analyze portfolio"],
      "negative_prompts": ["unrelated query"],
      "tags": [
        "metric:train_loss=0.5",
        "metric:eval_loss=0.6",
        "training:epochs=3",
        "training:batch_size=4",
        "training:learning_rate=0.0003"
      ],
      "created_at": "2026-01-17T12:00:00.000000",
      "updated_at": "2026-01-17T12:00:00.000000",
      "schema_version": "1.0"
    }
  }
}
```

## Benefits

### 1. Centralized Tracking

All models across all phases are now tracked in a single, consistent format. This enables:

- Cross-phase lineage tracking (dataset → model → MoE → deployment)
- Unified querying and reporting
- Easier experiment management

### 2. Standardized Schemas

Using Phase 0's Pydantic schemas ensures:

- Type safety and validation
- Consistent field names and types
- Better IDE support and autocomplete

### 3. Future-Proof

As Phase 0 infrastructure evolves, Phase 2 automatically benefits from:

- Enhanced metadata tracking
- Improved storage backends (SQLite, PostgreSQL)
- Advanced querying capabilities
- Better lineage visualization

### 4. Zero Migration Cost

The compatibility shim means:

- No code changes in existing Phase 2 programs
- No data migration required
- Immediate integration with Phase 0

## Implementation Details

### Version Generation

The shim automatically generates version numbers:

```python
# First registration
entry = registry.register(unit_id="unit1", task_id="task1", ...)
# entry.version = "v1"

# Second registration (same unit/task)
entry = registry.register(unit_id="unit1", task_id="task1", ...)
# entry.version = "v2"
```

Version numbers are extracted from the latest model's `model_id` format: `{unit}/{task}_v{N}`

### Metrics Storage

Metrics are stored as tags with the `metric:` prefix:

```python
metrics = ModelMetrics(
    train_loss=0.5,
    eval_loss=0.6,
    format_compliance=0.95
)
registry.update_metrics(model_id, metrics)

# Stored as tags:
# ["metric:train_loss=0.5", "metric:eval_loss=0.6", "metric:format_compliance=0.95"]
```

When retrieving a model, these tags are automatically parsed back into a `ModelMetrics` object.

### Training Config Storage

Similar to metrics, training config is stored as tags:

```python
training_config = TrainingConfig(
    epochs=3,
    batch_size=4,
    learning_rate=3e-4,
    lora_r=16,
    lora_alpha=16,
    base_model="test-model",
    train_samples=100,
    val_samples=20
)

# Stored as tags:
# ["training:epochs=3", "training:batch_size=4", ...]
```

## Troubleshooting

### Import Errors

If you see import errors related to `phase-0-infrastructure`, ensure:

1. Phase 0 infrastructure exists at: `../phase-0-infrastructure/`
2. The path is correct in `model_registry.py` line 15

### Missing Fields

If you're accessing fields that don't exist on `ModelEntry`:

- Check the field mapping table above
- Use `entry.unit_id` instead of `entry.unit`
- Use `entry.task_id` instead of `entry.task`

### Status Conversion

If status updates fail, ensure you're using Phase 2 status strings:

- `"trained"`, `"evaluated"`, `"exported"`, `"archived"`
- Not Phase 0 enums: `ModelStatus.TRAINED`

## Next Steps

With Phase 2 now integrated with Phase 0 infrastructure, the next migrations are:

1. **Phase 3 (MoE)** - Use Phase 0 registry for merged models
2. **Phase 1 (Embeddings)** - Migrate dataset tracking to Phase 0 DataRegistry
3. **Phase 4 (Agentic)** - Track experiments in Phase 0 ExperimentTracker

This creates a fully unified infrastructure with end-to-end lineage tracking across all pipeline phases.
