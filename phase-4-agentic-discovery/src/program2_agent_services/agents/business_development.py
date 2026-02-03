"""
Business Development Agent
Handles RFP data and competitive funding landscape.
"""

from ...shared.a2a_protocol import A2ACapability


def get_capability() -> A2ACapability:
    """Get Business Development agent capability"""
    return A2ACapability(
        agent_id="business-development-agent",
        name="Business Development",
        description="Tracks RFP opportunities, analyzes competitive funding landscape, and identifies funding trends",
        domains=[
            "RFP data",
            "competitive landscape",
            "funding opportunities",
            "funding trends"
        ],
        example_queries=[
            "What RFPs are available in the health sector?",
            "Show competitive landscape for education funding",
            "List recent funding opportunities in East Africa",
            "Which funders are most active in agriculture?",
            "Analyze RFP-2024-001 requirements and competitiveness"
        ],
        dependencies=[
            "fundraising-agent",
            "field-operations-agent"
        ],
        max_cascade_depth=3
    )
