"""Centralized logging infrastructure for Emergent Enterprise AI.

This module provides structured logging capabilities using structlog,
supporting both human-readable console output and machine-parseable JSON formatting.

Basic usage:
    >>> from phase0_infra.habitat_logging import configure_logging, get_logger
    >>> configure_logging(level="INFO", format="console")
    >>> logger = get_logger(__name__)
    >>> logger.info("registry_loaded", registry_type="dataset", path="/path/to/file.json")

Using standard events:
    >>> from phase0_infra.habitat_logging import LOG_EVENTS
    >>> logger.info(
    ...     "dataset_registered",
    ...     dataset_id="train_001",
    ...     path="/data/datasets/train.jsonl",
    ...     size_mb=150.5,
    ... )
"""

from .config import configure_logging, get_logger
from .formatters import (
    LOG_EVENTS,
    format_experiment_event,
    format_registry_event,
    format_validation_event,
    get_event_description,
)

__all__ = [
    "configure_logging",
    "get_logger",
    "LOG_EVENTS",
    "get_event_description",
    "format_registry_event",
    "format_validation_event",
    "format_experiment_event",
]
