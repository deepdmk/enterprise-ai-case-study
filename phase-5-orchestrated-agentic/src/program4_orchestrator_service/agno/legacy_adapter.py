"""
Legacy API Adapter

Adapts Agno Team responses to the legacy OrchestratedResponse format,
ensuring backward compatibility with existing API contracts.
"""

from typing import Dict, Any, List, Optional
import time
import re
import structlog
from agno.team import Team

from ...shared.routing_schema import (
    RoutingDecision,
    AgentResponse,
    OrchestratedResponse,
    AgentType,
    WorkflowType,
    AgentCall
)

logger = structlog.get_logger()


class LegacyAdapter:
    """
    Adapts Agno Team responses to legacy API format.

    This adapter bridges the gap between Agno's Team API and the
    existing Phase 5 API contracts, ensuring seamless migration.
    """

    def __init__(self, team: Team):
        """
        Initialize legacy adapter.

        Args:
            team: Agno Team instance
        """
        self.team = team
        self.logger = logger.bind(component="legacy_adapter")

    async def orchestrate(
        self,
        query: str,
        execute: bool = True
    ) -> OrchestratedResponse:
        """
        Run orchestration and return legacy-formatted response.

        Args:
            query: User query
            execute: If False, only return routing decision (not fully supported in Agno mode)

        Returns:
            OrchestratedResponse in legacy format
        """
        start_time = time.time()

        try:
            # Run Agno team
            result = await self.team.arun(query)

            # Extract components from result
            routing_decision = self._extract_routing_decision(query, result)
            agent_responses = self._extract_agent_responses(result)
            synthesized_response = self._extract_synthesized_response(result)

            total_latency_ms = int((time.time() - start_time) * 1000)

            # Determine success
            success = True
            if hasattr(result, 'success'):
                success = result.success
            elif agent_responses:
                success = any(r.success for r in agent_responses)

            orchestrated_response = OrchestratedResponse(
                query=query,
                routing_decision=routing_decision,
                agent_responses=agent_responses,
                synthesized_response=synthesized_response,
                total_latency_ms=total_latency_ms,
                success=success,
                metadata={
                    "agno_mode": True,
                    "team_name": self.team.name
                }
            )

            self.logger.info(
                "legacy_orchestration_complete",
                query=query[:50],
                total_latency_ms=total_latency_ms,
                success=success
            )

            return orchestrated_response

        except Exception as e:
            self.logger.error("legacy_orchestration_failed", query=query[:50], error=str(e))

            total_latency_ms = int((time.time() - start_time) * 1000)

            # Create error response
            error_response = OrchestratedResponse(
                query=query,
                routing_decision=self._create_fallback_routing(query),
                agent_responses=[],
                synthesized_response=f"Orchestration failed: {str(e)}",
                total_latency_ms=total_latency_ms,
                success=False,
                metadata={
                    "agno_mode": True,
                    "error": str(e)
                }
            )

            return error_response

    def _extract_routing_decision(self, query: str, result: Any) -> RoutingDecision:
        """
        Extract routing decision from Agno result.

        Parses the coordinator's reasoning to reconstruct the routing decision.

        Args:
            query: Original query
            result: Agno team result

        Returns:
            RoutingDecision
        """
        # Extract coordinator's reasoning from messages
        coordinator_reasoning = ""
        entry_agent = AgentType.FIELD_OPERATIONS  # Default
        optimal_depth = 2  # Default

        # Try to extract from result.messages or result.content
        content = ""
        if hasattr(result, 'content'):
            content = result.content
        elif hasattr(result, 'messages') and result.messages:
            # Find coordinator's message
            for msg in result.messages:
                if msg.get('role') == 'assistant' and 'coordinator' in msg.get('name', '').lower():
                    content = msg.get('content', '')
                    break

        # Parse routing decision from content
        if content:
            coordinator_reasoning = content

            # Extract entry agent
            if "fundraising" in content.lower():
                entry_agent = AgentType.FUNDRAISING
            elif "business development" in content.lower() or "business-development" in content.lower():
                entry_agent = AgentType.BUSINESS_DEVELOPMENT
            elif "field operations" in content.lower() or "field-operations" in content.lower():
                entry_agent = AgentType.FIELD_OPERATIONS

            # Extract optimal depth
            depth_match = re.search(r'depth[:\s]+(\d+)', content.lower())
            if depth_match:
                optimal_depth = int(depth_match.group(1))
                optimal_depth = max(1, min(4, optimal_depth))  # Clamp to [1, 4]

        # Detect workflow type
        workflow = self._detect_workflow(query)

        # Create agent calls (based on extracted routing)
        agent_calls = [
            AgentCall(
                step=1,
                agent=entry_agent,
                operation="process_query",
                expected_depth=optimal_depth - 1
            )
        ]

        return RoutingDecision(
            workflow=workflow,
            entry_agent=entry_agent,
            optimal_depth=optimal_depth,
            agent_calls=agent_calls,
            reasoning=coordinator_reasoning or "Agno coordinator routing decision",
            estimated_latency_ms=optimal_depth * 150,
            success_probability=0.95,
            metadata={
                "agno_mode": True,
                "extracted_from_coordinator": True
            }
        )

    def _extract_agent_responses(self, result: Any) -> List[AgentResponse]:
        """
        Extract agent responses from Agno result.

        Args:
            result: Agno team result

        Returns:
            List of AgentResponse
        """
        agent_responses = []

        # Check if result has messages with member responses
        if hasattr(result, 'messages') and result.messages:
            for msg in result.messages:
                role = msg.get('role', '')
                name = msg.get('name', '')
                content = msg.get('content', '')

                # Identify agent responses (role=assistant, name contains agent name)
                if role == 'assistant' and any(
                    agent_name in name.lower()
                    for agent_name in ['fundraising', 'business', 'field']
                ):
                    # Map name to AgentType
                    agent = self._map_name_to_agent_type(name)

                    agent_response = AgentResponse(
                        agent=agent,
                        operation="process_query",
                        success=True,
                        response=content,
                        latency_ms=0,  # Not tracked individually in Agno
                        cascaded_calls=[]  # Extract if available
                    )

                    agent_responses.append(agent_response)

        return agent_responses

    def _extract_synthesized_response(self, result: Any) -> str:
        """
        Extract synthesized response from Agno result.

        Args:
            result: Agno team result

        Returns:
            Synthesized response string
        """
        if hasattr(result, 'content'):
            return result.content

        # Fallback: concatenate all assistant messages
        if hasattr(result, 'messages') and result.messages:
            responses = []
            for msg in result.messages:
                if msg.get('role') == 'assistant':
                    responses.append(msg.get('content', ''))

            if responses:
                return "\n\n".join(responses)

        return "No response generated."

    def _detect_workflow(self, query: str) -> WorkflowType:
        """
        Detect workflow type from query.

        Args:
            query: User query

        Returns:
            WorkflowType
        """
        query_lower = query.lower()

        if "funding opportunity" in query_lower or "evaluate" in query_lower:
            return WorkflowType.EVALUATE_FUNDING_OPPORTUNITY
        elif "investor capacity" in query_lower or "investment capacity" in query_lower:
            return WorkflowType.ASSESS_INVESTOR_CAPACITY
        elif "competitive landscape" in query_lower or "market fit" in query_lower:
            return WorkflowType.ANALYZE_COMPETITIVE_LANDSCAPE
        elif "regional" in query_lower or "country" in query_lower:
            return WorkflowType.EVALUATE_REGIONAL_PROJECT
        else:
            return WorkflowType.UNKNOWN

    def _map_name_to_agent_type(self, name: str) -> AgentType:
        """
        Map agent name to AgentType.

        Args:
            name: Agent name from Agno message

        Returns:
            AgentType
        """
        name_lower = name.lower()

        if "fundraising" in name_lower:
            return AgentType.FUNDRAISING
        elif "business" in name_lower:
            return AgentType.BUSINESS_DEVELOPMENT
        elif "field" in name_lower:
            return AgentType.FIELD_OPERATIONS
        else:
            return AgentType.FIELD_OPERATIONS  # Default

    def _create_fallback_routing(self, query: str) -> RoutingDecision:
        """
        Create fallback routing decision for error cases.

        Args:
            query: User query

        Returns:
            RoutingDecision
        """
        return RoutingDecision(
            workflow=WorkflowType.UNKNOWN,
            entry_agent=AgentType.FIELD_OPERATIONS,
            optimal_depth=2,
            agent_calls=[],
            reasoning="Fallback routing due to error",
            estimated_latency_ms=0,
            success_probability=0.0,
            metadata={"fallback": True}
        )

    async def route(self, query: str) -> RoutingDecision:
        """
        Get routing decision only (without executing agents).

        Note: In Agno mode, the coordinator makes decisions during execution,
        so this method runs a lightweight orchestration to extract the routing.

        Args:
            query: User query

        Returns:
            RoutingDecision
        """
        # Run orchestration
        orchestrated_response = await self.orchestrate(query, execute=True)

        # Return routing decision
        return orchestrated_response.routing_decision
