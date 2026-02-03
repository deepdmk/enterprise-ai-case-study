"""
Field Operations Agent
Handles local capacity, project performance, and regional data.
"""

from ...shared.a2a_protocol import A2ACapability


def get_capability() -> A2ACapability:
    """Get Field Operations agent capability"""
    return A2ACapability(
        agent_id="field-operations-agent",
        name="Field Operations",
        description="Provides local capacity analysis, project performance tracking, and regional insights",
        domains=[
            "local capacity",
            "project performance",
            "regional data",
            "country office coordination"
        ],
        example_queries=[
            "What is the capacity of Kenya office?",
            "Show project performance in Ghana",
            "List active projects in East Africa",
            "Which country offices have expertise in health projects?",
            "Analyze regional capacity for multi-country initiatives"
        ],
        dependencies=[
            "fundraising-agent",
            "business-development-agent"
        ],
        max_cascade_depth=3
    )
