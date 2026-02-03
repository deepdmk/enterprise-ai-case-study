# Phase 0 Infrastructure Tests

Comprehensive test suite for the phase-0-infrastructure registries.

## Test Structure

```
tests/
├── conftest.py                    # Pytest fixtures
├── test_schemas.py                # Pydantic model tests
├── test_storage.py                # JSONStorage tests
├── test_data_registry.py          # DataRegistry tests
├── test_model_registry.py         # ModelRegistry tests
├── test_experiment_tracker.py     # ExperimentTracker tests
└── test_integration.py            # Cross-registry integration tests
```

## Running Tests

### Important: Logging Module Conflict

The `logging` directory in phase-0-infrastructure shadows Python's built-in `logging` module, which prevents pytest from running normally. There are two workarounds:

**Option 1: Temporarily rename the logging directory** (Recommended)

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
mv logging logging_backup
python -m pytest tests/ -v
mv logging_backup logging
```

**Option 2: Run individual test files directly with python**

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
python tests/test_schemas.py
```

### Run all tests

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
# Temporarily rename logging directory
mv logging logging_backup
python -m pytest tests/ -v
mv logging_backup logging
```

### Run specific test file

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
mv logging logging_backup
python -m pytest tests/test_schemas.py -v
mv logging_backup logging
```

### Run specific test class

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
mv logging logging_backup
python -m pytest tests/test_schemas.py::TestEnums -v
mv logging_backup logging
```

### Run specific test function

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
mv logging logging_backup
python -m pytest tests/test_schemas.py::TestEnums::test_phase_enum_values -v
mv logging_backup logging
```

### Run with coverage (if pytest-cov is installed)

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
mv logging logging_backup
python -m pytest tests/ --cov=registries --cov-report=html
mv logging_backup logging
```

### Helper Script

Use the provided `run_tests.sh` script which handles the logging directory renaming automatically:

```bash
cd /Users/shigoto/Projects/GitHub\ Repos/emergent-enterprise-ai/phase-0-infrastructure
./run_tests.sh                          # Run all tests
./run_tests.sh tests/test_schemas.py    # Run specific file
```

## Test Coverage

### test_schemas.py (Pydantic Models)
- ✅ Enum values validation
- ✅ Model creation with valid data
- ✅ Model validation with invalid data
- ✅ ValidationResult operations (add_error, add_warning, merge)
- ✅ Default values and optional fields

### test_storage.py (JSONStorage)
- ✅ Save/load roundtrip
- ✅ Update, delete, exists operations
- ✅ Clear storage
- ✅ File locking for concurrent access
- ✅ Legacy format compatibility
- ✅ Error handling

### test_data_registry.py (DataRegistry)
- ✅ Register, get, list datasets
- ✅ List with filters (phase, unit, data_type, status)
- ✅ Update status
- ✅ Get lineage (parent-child tracking)
- ✅ Validate dataset (path existence)
- ✅ Duplicate ID error handling
- ✅ Persistence across instances

### test_model_registry.py (ModelRegistry)
- ✅ Register, get, get_latest models
- ✅ List with filters (phase, unit, task, model_type, status)
- ✅ Update status and metrics
- ✅ Get lineage
- ✅ Get routing config (for MoE)
- ✅ Export for deployment
- ✅ Persistence across instances

### test_experiment_tracker.py (ExperimentTracker)
- ✅ Start experiment (with/without ID)
- ✅ Log data characteristics
- ✅ Log hyperparameters
- ✅ Log training metrics
- ✅ Complete/fail experiment
- ✅ Find best config
- ✅ List with filters
- ✅ Full workflow test

### test_integration.py (Cross-Registry Workflows)
- ✅ Dataset → Model lineage tracking
- ✅ Experiment → Model linkage
- ✅ Full pipeline workflow (Dataset → Experiment → Model)
- ✅ Multiple models from same dataset
- ✅ Dataset parent-child with models
- ✅ Experiment comparison workflow
- ✅ MoE deployment workflow
- ✅ Export and deployment workflow
- ✅ Validation workflow

## Fixtures

All fixtures are defined in `conftest.py`:

- `temp_storage_dir` - Temporary directory for test storage (uses pytest's tmp_path)
- `sample_dataset` - RegisteredDataset fixture
- `sample_model` - RegisteredModel fixture
- `sample_experiment` - ExperimentResult fixture
- `sample_data_characteristics` - DataCharacteristics fixture
- `sample_hyperparameters` - HyperparameterConfig fixture
- `sample_training_metrics` - TrainingMetrics fixture

## Notes

### Test Mode

All registries should use `test_mode=True` or temporary directories to avoid interfering with production data:

```python
registry = DataRegistry(data_dir=temp_storage_dir, test_mode=True)
```

### Temporary Files

Tests use pytest's `tmp_path` fixture to create isolated temporary directories that are automatically cleaned up after tests complete.

### Concurrent Testing

`test_storage.py` includes tests for file locking to ensure thread-safe operations.

## Troubleshooting

### ImportError or Circular Import

If you see errors related to the `logging` module, make sure you're running tests from the parent directory as shown above. The `logging` directory in phase-0-infrastructure shadows Python's built-in `logging` module when running from within the directory.

### Missing Dependencies

Install required dependencies:

```bash
pip install pytest pytest-cov pydantic structlog filelock
```
