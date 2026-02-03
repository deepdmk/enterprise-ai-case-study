"""Logging configuration using structlog.

This module provides centralized logging configuration for all phase-0-infrastructure
components and downstream phases. It supports both human-readable console output
and machine-parseable JSON formatting.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor


def add_logger_name(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add logger name to the event dict."""
    event_dict["logger"] = event_dict.get("logger", logger.name)
    return event_dict


def configure_logging(level: str = "INFO", format: str = "console") -> None:
    """Configure structlog with appropriate processors and formatters.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Output format - either "console" (colored, human-readable) or "json"

    Raises:
        ValueError: If format is not "console" or "json"
    """
    if format not in ("console", "json"):
        raise ValueError(f"Invalid format: {format}. Must be 'console' or 'json'")

    # Set standard library logging level
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )

    # Common processors for both formats
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
    ]

    if format == "console":
        # Console format: colored and human-readable
        processors: list[Processor] = shared_processors + [
            structlog.processors.ExceptionRenderer(),
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        # JSON format: machine-parseable
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a configured structlog logger instance.

    Args:
        name: Logger name, typically __name__ of the calling module

    Returns:
        Configured structlog BoundLogger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("registry_loaded", registry_type="dataset", path="/path/to/registry.json")
    """
    return structlog.get_logger(name)
