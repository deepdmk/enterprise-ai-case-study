"""
Remote Agent Members for Agno Team

Creates RemoteAgent wrappers for Phase 4 A2A agents (MoE-powered).
"""

from phase0_infra.habitat_logging import get_logger
from agno.agent import RemoteAgent

logger = get_logger(__name__)


def create_fundraising_member(base_url: str = "http://localhost:8001") -> RemoteAgent:
    """
    Create RemoteAgent for Fundraising Agent (Phase 4).

    This agent is powered by the Fundraising MoE model with 5 experts:
    - Investor profiling
    - Portfolio analysis
    - Funding capacity assessment
    - Interest matching
    - Historical giving patterns

    Args:
        base_url: Base URL of fundraising agent

    Returns:
        RemoteAgent instance
    """
    # Only supported parameters: base_url, agent_id, protocol, a2a_protocol, timeout
    return RemoteAgent(
        base_url=base_url,
        agent_id="fundraising-agent",
        protocol="a2a",
        a2a_protocol="rest"  # Our Phase 4 agents use REST
    )


def create_business_dev_member(base_url: str = "http://localhost:8002") -> RemoteAgent:
    """
    Create RemoteAgent for Business Development Agent (Phase 4).

    This agent is powered by the Business Development MoE model with 4 experts:
    - RFP tracking and analysis
    - Competitive landscape mapping
    - Funding opportunity assessment
    - Market positioning

    Args:
        base_url: Base URL of business development agent

    Returns:
        RemoteAgent instance
    """
    return RemoteAgent(
        base_url=base_url,
        agent_id="business-development-agent",
        protocol="a2a",
        a2a_protocol="rest"
    )


def create_field_ops_member(base_url: str = "http://localhost:8003") -> RemoteAgent:
    """
    Create RemoteAgent for Field Operations Agent (Phase 4).

    This agent is powered by the Field Operations MoE model with 5 experts:
    - Regional capacity assessment
    - Local market intelligence
    - Project performance tracking
    - Partner relationships
    - On-ground logistics

    Args:
        base_url: Base URL of field operations agent

    Returns:
        RemoteAgent instance
    """
    return RemoteAgent(
        base_url=base_url,
        agent_id="field-operations-agent",
        protocol="a2a",
        a2a_protocol="rest"
    )


def create_all_members(agent_registry: dict[str, str]) -> list[RemoteAgent]:
    """
    Create all RemoteAgent members from agent registry.

    Args:
        agent_registry: Dictionary mapping agent names to URLs

    Returns:
        List of RemoteAgent instances
    """
    members = []

    # Fundraising Agent
    if "fundraising-agent" in agent_registry:
        fundraising = create_fundraising_member(
            base_url=agent_registry["fundraising-agent"]
        )
        members.append(fundraising)
        logger.info("fundraising_member_created", url=agent_registry["fundraising-agent"])

    # Business Development Agent
    if "business-development-agent" in agent_registry:
        business_dev = create_business_dev_member(
            base_url=agent_registry["business-development-agent"]
        )
        members.append(business_dev)
        logger.info("business_dev_member_created", url=agent_registry["business-development-agent"])

    # Field Operations Agent
    if "field-operations-agent" in agent_registry:
        field_ops = create_field_ops_member(
            base_url=agent_registry["field-operations-agent"]
        )
        members.append(field_ops)
        logger.info("field_ops_member_created", url=agent_registry["field-operations-agent"])

    logger.info("all_members_created", count=len(members))

    return members
