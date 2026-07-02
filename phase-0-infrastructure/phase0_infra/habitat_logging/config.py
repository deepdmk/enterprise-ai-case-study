"""Logging configuration using structlog.

This module provides centralized logging configuration for all phase-0-infrastructure
components and downstream phases. It supports both human-readable console output
and machine-parseable JSON formatting.
"""

import logging
import sys
from typing import Any, cast

import structlog
from structlog.types import Processor


class _HabitatBoundLogger(structlog.stdlib.BoundLogger):
    """BoundLogger that avoids double-rendered tracebacks.

    ``structlog.stdlib.BoundLogger.exception`` proxies to the stdlib's
    ``Logger.exception``, which sets ``exc_info=True`` on the stdlib side —
    so the handler appends the traceback a second time after structlog's
    renderer already rendered it. Proxy to ``error`` instead: structlog's
    processor chain (ConsoleRenderer / format_exc_info) is the single
    source of exception rendering.
    """

    def exception(self, event: str | None = None, *args: Any, **kw: Any) -> Any:
        kw.setdefault("exc_info", True)
        return self._proxy_to_logger("error", event, *args, **kw)


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

    numeric_level = logging.getLevelName(level.upper())
    if not isinstance(numeric_level, int):
        raise ValueError(
            f"Invalid level: {level}. Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL"
        )

    # Set standard library logging level.
    # force=True so repeated configure_logging() calls take effect
    # (basicConfig is otherwise a no-op once handlers exist).
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=numeric_level,
        force=True,
    )

    # Common processors for both formats
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
    ]

    if format == "console":
        # Console format: colored and human-readable.
        # NOTE: no ExceptionRenderer/format_exc_info here — ConsoleRenderer
        # renders pretty tracebacks itself only when exc_info is still present.
        processors: list[Processor] = shared_processors + [
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
        wrapper_class=_HabitatBoundLogger,
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
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name))
