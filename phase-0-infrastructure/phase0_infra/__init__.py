"""Phase 0 infrastructure for Emergent Enterprise AI.

Single namespace package for all shared infrastructure consumed by
phases 1-5:

- ``phase0_infra.registries``      — dataset/model registries, experiment tracker
- ``phase0_infra.config``          — base settings, conventions, retry, boundary schemas
- ``phase0_infra.evaluation``      — evaluation metrics schemas
- ``phase0_infra.habitat_logging`` — structured logging (structlog)

Basic usage:
    >>> from phase0_infra.registries import DataRegistry, ModelRegistry
    >>> from phase0_infra.habitat_logging import configure_logging, get_logger
    >>> from phase0_infra.config import HabitatBaseSettings, make_id, parse_id
"""

__version__ = "0.1.0"
