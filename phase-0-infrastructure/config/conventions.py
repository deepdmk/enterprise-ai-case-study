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

Agent Name Convention:
    Organizational units use underscores as canonical identifiers (matching Python
    naming and file system conventions). A2A protocol agent IDs use hyphens.

    Units: fundraising, business_development, field_operations
    Agents: fundraising-agent, business-development-agent, field-operations-agent

Usage:
    >>> from config.conventions import make_id, parse_id, unit_to_agent_id, agent_id_to_unit
    >>>
    >>> # Create a resource ID
    >>> resource_id = make_id(phase=2, unit="program1", task="format-alpaca", version="v1.0.0")
    >>> print(resource_id)
    "2/program1/format-alpaca/v1.0.0"
    >>>
    >>> # Convert between unit names and agent IDs
    >>> agent_id_to_unit("fundraising-agent")
    "fundraising"
    >>> unit_to_agent_id("business_development")
    "business-development-agent"
"""

# Standard ID format for all resources
ID_FORMAT = "{phase}/{unit}/{task}/{version}"

# --- Agent Name Conventions ---
# Canonical unit identifiers (underscore format, used in Phase 2-3 for models/configs)
UNIT_IDS = ("fundraising", "business_development", "field_operations")

# A2A protocol agent identifiers (hyphen format, used in Phase 4-5 for network agents)
AGENT_IDS = ("fundraising-agent", "business-development-agent", "field-operations-agent")

# Bidirectional mapping between unit names and agent IDs
_UNIT_TO_AGENT: dict[str, str] = {
    "fundraising": "fundraising-agent",
    "business_development": "business-development-agent",
    "field_operations": "field-operations-agent",
}
_AGENT_TO_UNIT: dict[str, str] = {v: k for k, v in _UNIT_TO_AGENT.items()}

# Default agent ports for A2A protocol services
AGENT_PORTS: dict[str, int] = {
    "fundraising-agent": 8001,
    "business-development-agent": 8002,
    "field-operations-agent": 8003,
}


def unit_to_agent_id(unit_id: str) -> str:
    """Convert a unit identifier to an A2A agent ID.

    Args:
        unit_id: Unit identifier (e.g., "fundraising", "business_development")

    Returns:
        Agent ID string (e.g., "fundraising-agent", "business-development-agent")

    Raises:
        ValueError: If the unit_id is not recognized
    """
    if unit_id not in _UNIT_TO_AGENT:
        raise ValueError(
            f"Unknown unit ID: '{unit_id}'. Valid unit IDs: {', '.join(UNIT_IDS)}"
        )
    return _UNIT_TO_AGENT[unit_id]


def agent_id_to_unit(agent_id: str) -> str:
    """Convert an A2A agent ID to a unit identifier.

    Args:
        agent_id: Agent ID (e.g., "fundraising-agent", "business-development-agent")

    Returns:
        Unit identifier string (e.g., "fundraising", "business_development")

    Raises:
        ValueError: If the agent_id is not recognized
    """
    if agent_id not in _AGENT_TO_UNIT:
        raise ValueError(
            f"Unknown agent ID: '{agent_id}'. Valid agent IDs: {', '.join(AGENT_IDS)}"
        )
    return _AGENT_TO_UNIT[agent_id]


def get_agent_url(agent_id: str, host: str = "localhost") -> str:
    """Get the default URL for an agent.

    Args:
        agent_id: Agent ID (e.g., "fundraising-agent")
        host: Hostname (default: "localhost")

    Returns:
        URL string (e.g., "http://localhost:8001")
    """
    port = AGENT_PORTS.get(agent_id)
    if port is None:
        raise ValueError(
            f"Unknown agent ID: '{agent_id}'. Valid agent IDs: {', '.join(AGENT_IDS)}"
        )
    return f"http://{host}:{port}"


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


def parse_id(id_str: str) -> dict[str, str | int]:
    """Parse a standardized resource ID into its components.

    Args:
        id_str: Resource ID string in the format {phase}/{unit}/{task}/{version}

    Returns:
        Dictionary with keys: phase (int), unit (str), task (str), version (str)

    Raises:
        ValueError: If the ID string doesn't match the expected format

    Example:
        >>> parse_id("2/program1/format-alpaca/v1.0.0")
        {"phase": 2, "unit": "program1", "task": "format-alpaca", "version": "v1.0.0"}
    """
    parts = id_str.split("/")
    if len(parts) != 4:
        raise ValueError(
            f"Invalid ID format: '{id_str}'. "
            f"Expected format: {ID_FORMAT}"
        )

    return {
        "phase": int(parts[0]),
        "unit": parts[1],
        "task": parts[2],
        "version": parts[3]
    }
