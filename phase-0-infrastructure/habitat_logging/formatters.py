"""Log event constants and custom formatters.

This module defines standard log events used across phase-0-infrastructure
to ensure consistency in logging patterns and make log analysis easier.
"""

from typing import Any, Final

# Standard log events with descriptions
# Use these event names as the first argument to logger methods for consistency
LOG_EVENTS: Final[dict[str, str]] = {
    # Registry operations
    "registry_loaded": "Registry file loaded from disk",
    "registry_saved": "Registry file saved to disk",
    "dataset_registered": "New dataset added to registry",
    "dataset_updated": "Existing dataset metadata updated",
    "model_registered": "New model added to registry",
    "model_updated": "Existing model metadata updated",
    "model_exported": "Model exported to destination path",

    # Experiment tracking
    "experiment_started": "New experiment initiated",
    "experiment_completed": "Experiment finished successfully",
    "experiment_failed": "Experiment terminated with error",

    # Validation events
    "validation_passed": "Data or configuration validation succeeded",
    "validation_failed": "Data or configuration validation failed",
}


def get_event_description(event: str) -> str:
    """Get human-readable description for a log event.

    Args:
        event: Event name from LOG_EVENTS

    Returns:
        Event description, or the event name itself if not found

    Example:
        >>> get_event_description("registry_loaded")
        'Registry file loaded from disk'
    """
    return LOG_EVENTS.get(event, event)


def format_registry_event(
    event: str,
    registry_type: str,
    path: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Format a registry-related log event with standard fields.

    Args:
        event: Event name (e.g., "registry_loaded", "dataset_registered")
        registry_type: Type of registry (e.g., "dataset", "model", "experiment")
        path: File path to registry
        **kwargs: Additional context fields

    Returns:
        Dictionary of structured log fields

    Example:
        >>> format_registry_event(
        ...     "registry_loaded", "dataset", "/data/registry.json", count=42
        ... )
        {'event': 'registry_loaded', 'registry_type': 'dataset', ...}
    """
    return {
        "event": event,
        "registry_type": registry_type,
        "path": path,
        **kwargs,
    }


def format_validation_event(
    event: str,
    validator: str,
    passed: bool,
    **kwargs: Any,
) -> dict[str, Any]:
    """Format a validation-related log event with standard fields.

    Args:
        event: Event name (e.g., "validation_passed", "validation_failed")
        validator: Name of validator class or function
        passed: Whether validation passed
        **kwargs: Additional context fields (e.g., errors, warnings)

    Returns:
        Dictionary of structured log fields

    Example:
        >>> format_validation_event(
        ...     "validation_failed", "DatasetValidator", False,
        ...     errors=["missing field: name"]
        ... )
        {'event': 'validation_failed', 'validator': 'DatasetValidator', ...}
    """
    return {
        "event": event,
        "validator": validator,
        "passed": passed,
        **kwargs,
    }


def format_experiment_event(
    event: str,
    experiment_id: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Format an experiment-related log event with standard fields.

    Args:
        event: Event name (e.g., "experiment_started", "experiment_completed")
        experiment_id: Unique experiment identifier
        **kwargs: Additional context fields (e.g., metrics, duration, error)

    Returns:
        Dictionary of structured log fields

    Example:
        >>> format_experiment_event(
        ...     "experiment_completed", "exp_001", duration_sec=120.5, accuracy=0.95
        ... )
        {'event': 'experiment_completed', 'experiment_id': 'exp_001', ...}
    """
    return {
        "event": event,
        "experiment_id": experiment_id,
        **kwargs,
    }
