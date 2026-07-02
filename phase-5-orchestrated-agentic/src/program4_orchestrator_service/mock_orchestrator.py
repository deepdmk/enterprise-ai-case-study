"""
Mock Orchestrator Client for Test Mode.

Enables UI testing without running orchestrator service or Phase 4 agents.
Provides canned responses and simulated routing decisions.
"""

import random
import time
from typing import Any

from phase0_infra.habitat_logging import get_logger

from ..shared.routing_schema import (
    RoutingDecision,
    OrchestratedResponse,
    AgentResponse,
    AgentType,
    WorkflowType,
    AgentCall,
)

logger = get_logger(__name__)


# Canned responses by agent type
CANNED_RESPONSES = {
    AgentType.FUNDRAISING: {
        "investor": """## Investor Capacity Analysis

Based on the investor profile analysis, here are the key findings:

**Gates Foundation**
- Investment Capacity: $50-100M annually in health/agriculture
- Geographic Focus: Sub-Saharan Africa, South Asia
- Alignment Score: 92%

**Key Recommendations:**
1. Focus initial outreach on health systems strengthening
2. Emphasize measurable outcomes and sustainability
3. Prepare detailed M&E framework before engagement

*Analysis based on historical funding patterns and stated priorities.*""",
        "portfolio": """## Portfolio Review Summary

**Current Active Investments:**
- Health Sector: 45% ($234M)
- Agriculture: 30% ($156M)
- Education: 25% ($130M)

**Performance Metrics:**
- Average ROI: 12.3% social return
- Project Success Rate: 87%
- Avg Project Duration: 4.2 years

**Recommendations:**
Diversify into climate adaptation; current portfolio underweight in this growing sector.""",
        "default": """## Fundraising Analysis

Investor landscape analysis complete. The current funding environment shows moderate competition with several emerging opportunities in the health and climate sectors.

Key action items:
1. Update investor relationship database
2. Prepare targeted outreach materials
3. Schedule quarterly review meetings""",
    },
    AgentType.BUSINESS_DEVELOPMENT: {
        "rfp": """## RFP Analysis Summary

**Solicitation:** USAID/Kenya Health Systems Strengthening
**Value:** $15-25M over 5 years
**Deadline:** 45 days

**Key Requirements:**
- Prime must have 3+ similar projects in region
- DUNS registration and SAM.gov active
- Cost-share: 10% minimum

**Competitive Landscape:**
- Expected bidders: 4-6 organizations
- Key competitors: Abt, DAI, Chemonics

**Recommendation:** GO decision with teaming strategy for local implementation partner.""",
        "competitive": """## Competitive Landscape Analysis

**Market Position:**
- Regional ranking: #4 in East Africa
- Market share: 12% (growing)
- Win rate (last 12 months): 34%

**Competitor Analysis:**
1. DAI - Strong USAID relationships
2. Chemonics - Largest local presence
3. RTI - Technical expertise leader

**Strategic Recommendations:**
- Strengthen local partnerships
- Invest in technical differentiation
- Focus on niche sectors with less competition""",
        "default": """## Business Development Update

Pipeline analysis indicates strong opportunities in Q2-Q3. Current proposal win probability metrics are trending positive.

Priority actions:
1. Finalize teaming agreements for upcoming bids
2. Complete past performance documentation
3. Update cost models for regional labor rates""",
    },
    AgentType.FIELD_OPERATIONS: {
        "kenya": """## Kenya Regional Assessment

**Operational Environment:**
- Political Stability: Green
- Security Status: Yellow (regional variation)
- Economic Outlook: Positive (5.2% GDP growth)

**Active Projects:** 3
- Health Systems Strengthening: On track
- Agricultural Value Chains: Minor delays
- Education Access: Exceeding targets

**Key Risks:**
1. Currency fluctuation (medium impact)
2. Staff retention in rural areas (high impact)

**Recommendations:** Proceed with planned expansion; implement retention bonuses for field staff.""",
        "project": """## Project Performance Dashboard

**Program: Community Health Initiative**
**Status:** On Track

**Output Indicators:**
- Health workers trained: 450/500 (90%)
- Facilities upgraded: 28/30 (93%)
- Community sessions: 1,200/1,000 (120%)

**Outcome Progress:**
- Service utilization: +35% vs baseline
- Patient satisfaction: 4.2/5.0

**Budget Status:** 72% burn rate at month 9 (on track)
**Risk Level:** Green""",
        "regional": """## Regional Market Intelligence

**Coverage Area:** East Africa (Kenya, Uganda, Tanzania)

**Economic Indicators:**
- Regional GDP growth: 5.1% average
- Inflation: 7.2% (declining)
- Currency stability: Moderate

**Operational Highlights:**
- Strong partner network: 12 local organizations
- Staff capacity: 150+ local employees
- Infrastructure: 5 regional offices

**Growth Opportunities:**
- Climate adaptation programs
- Digital health initiatives
- Youth employment projects""",
        "default": """## Field Operations Summary

Regional operations are performing within expected parameters. All active projects maintaining acceptable progress toward milestones.

Key updates:
1. Quarterly reviews completed for all sites
2. Partner capacity assessments on schedule
3. Risk mitigation measures in place""",
    },
}


class MockOrchestratorClient:
    """
    Mock orchestrator for test mode - no service required.

    Provides canned responses and simulated routing based on keywords.
    Useful for UI development and demonstrations.
    """

    def __init__(self):
        """Initialize mock orchestrator client."""
        self.stats = {
            "total_routes": 0,
            "total_orchestrations": 0,
            "routes_by_agent": {
                AgentType.FUNDRAISING.value: 0,
                AgentType.BUSINESS_DEVELOPMENT.value: 0,
                AgentType.FIELD_OPERATIONS.value: 0,
            },
        }
        self.logger = logger.bind(component="mock_orchestrator")
        self.logger.info("mock_orchestrator_initialized")

    def route(self, query: str) -> RoutingDecision:
        """
        Return mock routing based on keywords.

        Args:
            query: User query

        Returns:
            RoutingDecision with mock routing
        """
        self.stats["total_routes"] += 1
        query_lower = query.lower()

        # Determine entry agent based on keywords
        if any(kw in query_lower for kw in ["investor", "inv-", "angel", "portfolio", "foundation", "gates"]):
            entry_agent = AgentType.FUNDRAISING
            depth = 2
            workflow = WorkflowType.ASSESS_INVESTOR_CAPACITY
            reasoning = "Query mentions investor analysis or portfolio review. Routing to Fundraising agent for investor intelligence."
        elif any(kw in query_lower for kw in ["rfp", "proposal", "competitive", "bid", "funder", "opportunity"]):
            entry_agent = AgentType.BUSINESS_DEVELOPMENT
            depth = 2
            workflow = WorkflowType.ANALYZE_COMPETITIVE_LANDSCAPE
            reasoning = "Query relates to RFP analysis or competitive landscape. Routing to Business Development agent."
        elif any(kw in query_lower for kw in ["kenya", "uganda", "region", "local", "project", "field", "country"]):
            entry_agent = AgentType.FIELD_OPERATIONS
            depth = 3
            workflow = WorkflowType.EVALUATE_REGIONAL_PROJECT
            reasoning = "Query involves regional assessment or project operations. Routing to Field Operations agent with extended depth for local coordination."
        else:
            # Default routing
            entry_agent = AgentType.FIELD_OPERATIONS
            depth = 2
            workflow = WorkflowType.UNKNOWN
            reasoning = "General query without specific domain indicators. Default routing to Field Operations for broad assessment."

        self.stats["routes_by_agent"][entry_agent.value] += 1

        agent_calls = [
            AgentCall(
                step=1,
                agent=entry_agent,
                operation="process_query",
                expected_depth=depth - 1,
            )
        ]

        return RoutingDecision(
            workflow=workflow,
            entry_agent=entry_agent,
            optimal_depth=depth,
            agent_calls=agent_calls,
            reasoning=reasoning,
            estimated_latency_ms=depth * 150,
            success_probability=0.95,
        )

    def orchestrate(self, query: str) -> OrchestratedResponse:
        """
        Return mock orchestration with canned agent responses.

        Args:
            query: User query

        Returns:
            OrchestratedResponse with mock data
        """
        self.stats["total_orchestrations"] += 1
        start_time = time.time()

        # Get routing decision
        routing_decision = self.route(query)

        # Simulate latency
        simulated_latency_ms = random.randint(50, 200)
        time.sleep(simulated_latency_ms / 1000)  # Small delay for realism

        # Get canned response for entry agent
        entry_response = self._get_canned_response(
            routing_decision.entry_agent, query
        )

        # Build agent responses
        agent_responses = [
            AgentResponse(
                agent=routing_decision.entry_agent,
                operation="process_query",
                success=True,
                response=entry_response,
                latency_ms=simulated_latency_ms,
                cascaded_calls=[],
            )
        ]

        # Add cascaded call if depth > 1
        cascaded_agents = []
        if routing_decision.optimal_depth >= 2:
            # Pick a secondary agent
            secondary_agent = self._get_secondary_agent(routing_decision.entry_agent)
            secondary_latency = random.randint(50, 150)

            secondary_response = self._get_canned_response(secondary_agent, query)

            agent_responses.append(
                AgentResponse(
                    agent=secondary_agent,
                    operation="provide_context",
                    success=True,
                    response=secondary_response,
                    latency_ms=secondary_latency,
                    cascaded_calls=[],
                )
            )
            cascaded_agents.append(secondary_agent.value)

            # Update first response with cascade info
            agent_responses[0].cascaded_calls = cascaded_agents

        # Synthesize final response
        synthesized = self._synthesize_response(query, routing_decision, agent_responses)

        total_latency_ms = int((time.time() - start_time) * 1000)

        return OrchestratedResponse(
            query=query,
            routing_decision=routing_decision,
            agent_responses=agent_responses,
            synthesized_response=synthesized,
            total_latency_ms=total_latency_ms,
            success=True,
        )

    def _get_canned_response(self, agent: AgentType, query: str) -> str:
        """Get appropriate canned response based on agent and query keywords."""
        query_lower = query.lower()
        agent_responses = CANNED_RESPONSES.get(agent, {})

        # Check for keyword matches
        for keyword, response in agent_responses.items():
            if keyword != "default" and keyword in query_lower:
                return response

        return agent_responses.get("default", f"Analysis complete for {agent.value}.")

    def _get_secondary_agent(self, primary: AgentType) -> AgentType:
        """Get a secondary agent for cascading."""
        agents = list(AgentType)
        agents.remove(primary)
        return random.choice(agents)

    def _synthesize_response(
        self,
        query: str,
        routing: RoutingDecision,
        responses: list[AgentResponse],
    ) -> str:
        """Synthesize final response from agent responses."""
        if len(responses) == 1:
            return responses[0].response

        # Combine responses
        parts = [
            "## Orchestrated Response\n",
            f"*Query routed through {len(responses)} agents with depth={routing.optimal_depth}*\n",
        ]

        for resp in responses:
            parts.append(f"\n### {resp.agent.replace('-', ' ').title()}\n")
            parts.append(resp.response)

        parts.append("\n---\n*Response synthesized by Phase 5 Orchestrator*")

        return "\n".join(parts)

    def get_stats(self) -> dict[str, Any]:
        """Return mock stats."""
        return {
            "mode": "mock",
            "total_routes": self.stats["total_routes"],
            "total_orchestrations": self.stats["total_orchestrations"],
            "routes_by_agent": self.stats["routes_by_agent"],
        }

    def health_check(self) -> bool:
        """Always returns True for mock."""
        return True
