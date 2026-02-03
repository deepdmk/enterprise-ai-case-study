"""Configuration conventions and ID management utilities.

This module defines the standard conventions for naming and identifying
resources across all phases of the emergent-enterprise-ai project.

ID Format Convention:
    All resource IDs follow the format: {phase}/{unit}/{task}/{version}

    Example: "2/program1/format-alpaca/v1.0.0"

    Components:
        - phase: Phase number (1-5)
        - unit: Unit or program identifier
        - task: Task or operation name
        - version: Semantic version string (e.g., v1.0.0)

Usage:
    >>> from config.conventions import make_id, parse_id
    >>>
    >>> # Create a resource ID
    >>> resource_id = make_id(phase=2, unit="program1", task="format-alpaca", version="v1.0.0")
    >>> print(resource_id)
    "2/program1/format-alpaca/v1.0.0"
    >>>
    >>> # Parse a resource ID
    >>> components = parse_id(resource_id)
    >>> print(components)
    {"phase": "2", "unit": "program1", "task": "format-alpaca", "version": "v1.0.0"}
"""

# Standard ID format for all resources
ID_FORMAT = "{phase}/{unit}/{task}/{version}"


def make_id(phase: int, unit: str, task: str, version: str) -> str:
    """Create a standardized resource ID from components.

    Args:
        phase: Phase number (1-5)
        unit: Unit or program identifier
        task: Task or operation name
        version: Semantic version string (e.g., v1.0.0)

    Returns:
        Formatted ID string following the standard convention

    Example:
        >>> make_id(2, "program1", "format-alpaca", "v1.0.0")
        "2/program1/format-alpaca/v1.0.0"
    """
    return ID_FORMAT.format(phase=phase, unit=unit, task=task, version=version)


def parse_id(id_str: str) -> dict:
    """Parse a standardized resource ID into its components.

    Args:
        id_str: Resource ID string in the format {phase}/{unit}/{task}/{version}

    Returns:
        Dictionary with keys: phase, unit, task, version

    Raises:
        ValueError: If the ID string doesn't match the expected format

    Example:
        >>> parse_id("2/program1/format-alpaca/v1.0.0")
        {"phase": "2", "unit": "program1", "task": "format-alpaca", "version": "v1.0.0"}
    """
    parts = id_str.split("/")
    if len(parts) != 4:
        raise ValueError(
            f"Invalid ID format: '{id_str}'. "
            f"Expected format: {ID_FORMAT}"
        )

    return {
        "phase": parts[0],
        "unit": parts[1],
        "task": parts[2],
        "version": parts[3]
    }
