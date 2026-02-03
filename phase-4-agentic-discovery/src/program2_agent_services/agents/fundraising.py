"""
Fundraising Agent
Handles investor profiles, interests, and capacity.
"""

from ...shared.a2a_protocol import A2ACapability


def get_capability() -> A2ACapability:
    """Get Fundraising agent capability"""
    return A2ACapability(
        agent_id="fundraising-agent",
        name="Fundraising",
        description="Provides investor profiles, investment capacity analysis, and sector interest matching",
        domains=[
            "investor profiles",
            "investment capacity",
            "sector interests",
            "investor matching"
        ],
        example_queries=[
            "What is the investment capacity of INV-123?",
            "Which sectors does investor INV-456 focus on?",
            "List all angel investors in the health sector",
            "Find investors interested in early-stage technology startups",
            "Profile investor INV-789 including recent investments"
        ],
        dependencies=[
            "business-development-agent",
            "field-operations-agent"
        ],
        max_cascade_depth=3
    )
