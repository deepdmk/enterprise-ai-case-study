"""Configuration module for phase-0-infrastructure.

This module provides base settings classes and configuration utilities
for all phases of the emergent-enterprise-ai project.

Basic usage:
    >>> from phase0_infra.config import HabitatBaseSettings, make_id, parse_id
    >>>
    >>> # Create a resource ID
    >>> resource_id = make_id(phase=2, unit="program1", task="format-alpaca", version="v1.0.0")
    >>> print(resource_id)
    "2/program1/format-alpaca/v1.0.0"
    >>>
    >>> # Parse a resource ID (phase is returned as an int)
    >>> components = parse_id(resource_id)
    >>> print(components)
    {"phase": 2, "unit": "program1", "task": "format-alpaca", "version": "v1.0.0"}
"""

from .base_settings import HabitatBaseSettings, PhaseSettings
from .conventions import ID_FORMAT, make_id, parse_id

__all__ = [
    "HabitatBaseSettings",
    "PhaseSettings",
    "make_id",
    "parse_id",
    "ID_FORMAT",
]
