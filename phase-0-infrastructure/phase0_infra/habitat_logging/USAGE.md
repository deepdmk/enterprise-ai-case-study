# Logging Module Usage Guide

This guide demonstrates how to use the centralized logging infrastructure for phase-0-infrastructure.

## Installation

Ensure structlog is installed (already in pyproject.toml):

```bash
pip install -e .
```

## Quick Start

```python
from phase0_infra.habitat_logging import configure_logging, get_logger, LOG_EVENTS

# Configure logging (do this once at application startup)
configure_logging(level="INFO", format="console")

# Get a logger instance
logger = get_logger(__name__)

# Log an event
logger.info("registry_loaded", registry_type="dataset", path="/data/registry.json")
```

## Configuration

### Console Format (Human-Readable)

```python
configure_logging(level="INFO", format="console")
```

Output example:
```
2026-01-17T10:30:45.123456Z [info     ] registry_loaded    logger=my_module registry_type=dataset path=/data/registry.json
```

### JSON Format (Machine-Parseable)

```python
configure_logging(level="INFO", format="json")
```

Output example:
```json
{"event": "registry_loaded", "logger": "my_module", "level": "info", "timestamp": "2026-01-17T10:30:45.123456Z", "registry_type": "dataset", "path": "/data/registry.json"}
```

### Log Levels

Supported levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

```python
configure_logging(level="DEBUG", format="console")
```

## Standard Events

Use `LOG_EVENTS` to ensure consistency across the codebase:

```python
from phase0_infra.habitat_logging import LOG_EVENTS

# View all available events
print(LOG_EVENTS.keys())
```

Available events:
- **Registry Operations**: `registry_loaded`, `registry_saved`, `dataset_registered`, `dataset_updated`, `model_registered`, `model_updated`, `model_exported`
- **Experiment Tracking**: `experiment_started`, `experiment_completed`, `experiment_failed`
- **Validation**: `validation_passed`, `validation_failed`

## Usage Patterns

### Basic Logging

```python
logger = get_logger(__name__)

# Simple event
logger.info("registry_loaded", registry_type="dataset", path="/data/registry.json")

# With multiple context fields
logger.info(
    "dataset_registered",
    dataset_id="train_001",
    path="/data/datasets/train.jsonl",
    size_mb=150.5,
    num_samples=10000,
)
```

### Using Format Helpers

The module provides helper functions for common logging patterns:

#### Registry Events

```python
from phase0_infra.habitat_logging import format_registry_event

logger.info(**format_registry_event(
    "dataset_registered",
    registry_type="dataset",
    path="/data/datasets/train.jsonl",
    dataset_id="train_001",
    size_mb=150.5,
))
```

#### Validation Events

```python
from phase0_infra.habitat_logging import format_validation_event

logger.warning(**format_validation_event(
    "validation_failed",
    validator="DatasetValidator",
    passed=False,
    errors=["missing field: name", "invalid type: size"],
))

logger.info(**format_validation_event(
    "validation_passed",
    validator="ConfigValidator",
    passed=True,
    warnings=["deprecated field: old_param"],
))
```

#### Experiment Events

```python
from phase0_infra.habitat_logging import format_experiment_event

# Starting an experiment
logger.info(**format_experiment_event(
    "experiment_started",
    experiment_id="exp_001",
    model="llama-3.1-8b",
    dataset="train_001",
))

# Completing an experiment
logger.info(**format_experiment_event(
    "experiment_completed",
    experiment_id="exp_001",
    duration_sec=120.5,
    accuracy=0.95,
    loss=0.12,
))

# Failed experiment
logger.error(**format_experiment_event(
    "experiment_failed",
    experiment_id="exp_002",
    error="CUDA out of memory",
))
```

### Exception Logging

```python
try:
    # Some operation
    process_dataset()
except Exception as e:
    logger.exception(
        "dataset_processing_failed",
        dataset_id="train_001",
        error=str(e),
    )
```

### Structured Context

Add persistent context to all log messages:

```python
import structlog

# Bind context
logger = logger.bind(user_id="user_123", session_id="sess_456")

# All subsequent logs will include user_id and session_id
logger.info("registry_loaded", registry_type="dataset")
logger.info("dataset_registered", dataset_id="train_001")

# Clear context
structlog.contextvars.clear_contextvars()
```

## Best Practices

1. **Use Standard Events**: Always use events from `LOG_EVENTS` for consistency
2. **Structured Fields**: Add context as key-value pairs, not in the message string
3. **Consistent Names**: Use snake_case for field names
4. **Include IDs**: Always log relevant identifiers (dataset_id, model_id, experiment_id)
5. **Error Context**: When logging errors, include enough context to debug
6. **Configure Once**: Call `configure_logging()` once at application startup
7. **Module Loggers**: Use `get_logger(__name__)` for each module

## Integration Examples

### Registry Module

```python
from phase0_infra.habitat_logging import configure_logging, get_logger

class DatasetRegistry:
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def load(self, path: str):
        self.logger.info("registry_loaded", registry_type="dataset", path=path)
        # Load logic...
    
    def save(self, path: str):
        self.logger.info("registry_saved", registry_type="dataset", path=path)
        # Save logic...
    
    def register(self, dataset_id: str, metadata: dict):
        self.logger.info(
            "dataset_registered",
            dataset_id=dataset_id,
            path=metadata["path"],
            size_mb=metadata["size_mb"],
        )
        # Registration logic...
```

### Validation Module

```python
from phase0_infra.habitat_logging import get_logger, format_validation_event

class DatasetValidator:
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def validate(self, dataset: dict) -> bool:
        errors = []
        
        # Validation logic...
        if errors:
            self.logger.warning(**format_validation_event(
                "validation_failed",
                validator=self.__class__.__name__,
                passed=False,
                errors=errors,
            ))
            return False
        
        self.logger.info(**format_validation_event(
            "validation_passed",
            validator=self.__class__.__name__,
            passed=True,
        ))
        return True
```

### Experiment Tracking

```python
from phase0_infra.habitat_logging import get_logger, format_experiment_event
import time

class ExperimentRunner:
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def run(self, experiment_id: str, config: dict):
        self.logger.info(**format_experiment_event(
            "experiment_started",
            experiment_id=experiment_id,
            **config,
        ))
        
        start_time = time.time()
        
        try:
            # Run experiment...
            results = {"accuracy": 0.95, "loss": 0.12}
            
            self.logger.info(**format_experiment_event(
                "experiment_completed",
                experiment_id=experiment_id,
                duration_sec=time.time() - start_time,
                **results,
            ))
            
        except Exception as e:
            self.logger.exception(**format_experiment_event(
                "experiment_failed",
                experiment_id=experiment_id,
                duration_sec=time.time() - start_time,
                error=str(e),
            ))
            raise
```

## Advanced Usage

### Custom Events

While it's recommended to use `LOG_EVENTS`, you can log custom events:

```python
logger.info(
    "custom_event_name",
    field1="value1",
    field2=42,
    field3=True,
)
```

### Dynamic Log Levels

```python
import os

# Set log level from environment
log_level = os.getenv("LOG_LEVEL", "INFO")
configure_logging(level=log_level, format="console")
```

### Testing with JSON Output

For tests, use JSON format for easier parsing:

```python
import json
from io import StringIO

# Capture logs
log_output = StringIO()
configure_logging(level="DEBUG", format="json")

# Run code that logs...

# Parse logs
logs = [json.loads(line) for line in log_output.getvalue().split('\n') if line]
assert logs[0]["event"] == "registry_loaded"
```

## Migration from Standard Logging

If migrating from Python's standard logging:

**Before:**
```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Loaded registry from {path} with {count} items")
```

**After:**
```python
from phase0_infra.habitat_logging import get_logger
logger = get_logger(__name__)
logger.info("registry_loaded", path=path, count=count)
```

Key differences:
- Use structured fields instead of string formatting
- Use event names as the first argument
- Add context as keyword arguments
