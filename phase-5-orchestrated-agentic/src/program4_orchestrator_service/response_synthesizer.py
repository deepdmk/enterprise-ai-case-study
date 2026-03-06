"""
Response Synthesizer

Synthesizes responses from multiple agent calls.
"""

from typing import List, Dict, Any
import structlog

from ..shared.routing_schema import AgentResponse, RoutingDecision

logger = structlog.get_logger()


class ResponseSynthesizer:
    """
    Synthesizes multi-agent responses.

    Strategies:
    - Concatenation (simple)
    - Hierarchical aggregation
    - LLM-based synthesis (future)
    """

    def __init__(self, strategy: str = "concatenation"):
        """
        Initialize response synthesizer.

        Args:
            strategy: Synthesis strategy (concatenation, hierarchical, llm)
        """
        self.strategy = strategy
        self.logger = logger.bind(component="response_synthesizer")

    def synthesize(
        self,
        query: str,
        routing_decision: RoutingDecision,
        agent_responses: List[AgentResponse]
    ) -> str:
        """
        Synthesize final response from agent responses.

        Args:
            query: Original user query
            routing_decision: Routing decision made
            agent_responses: Responses from agents

        Returns:
            Synthesized response
        """
        self.logger.info(
            "synthesizing_response",
            query=query[:50],
            num_responses=len(agent_responses),
            strategy=self.strategy
        )

        if self.strategy == "concatenation":
            return self._concatenate_responses(query, agent_responses)
        elif self.strategy == "hierarchical":
            return self._hierarchical_synthesis(query, routing_decision, agent_responses)
        else:
            # Default to concatenation
            return self._concatenate_responses(query, agent_responses)

    def _concatenate_responses(
        self,
        query: str,
        agent_responses: List[AgentResponse]
    ) -> str:
        """
        Simple concatenation of responses.

        Args:
            query: User query
            agent_responses: Agent responses

        Returns:
            Concatenated response
        """
        # Filter successful responses
        successful = [r for r in agent_responses if r.success]

        if not successful:
            return "No successful agent responses received."

        # Build synthesized response
        parts = [f"Query: {query}\n"]

        if len(successful) == 1:
            parts.append(f"\nResponse:\n{successful[0].response}")
        else:
            parts.append(f"\nSynthesized from {len(successful)} agent(s):\n")

            for i, response in enumerate(successful, 1):
                agent_name = response.agent.value if hasattr(response.agent, 'value') else response.agent
                parts.append(f"\n{i}. From {agent_name}:")
                parts.append(f"   {response.response}")

                if response.cascaded_calls:
                    parts.append(f"   (Cascaded to: {', '.join(response.cascaded_calls)})")

        # Add metadata
        total_latency = sum(r.latency_ms for r in agent_responses)
        parts.append(f"\n\nTotal latency: {total_latency}ms")
        parts.append(f"Agents called: {len(agent_responses)}")
        parts.append(f"Successful: {len(successful)}")

        return "\n".join(parts)

    def _hierarchical_synthesis(
        self,
        query: str,
        routing_decision: RoutingDecision,
        agent_responses: List[AgentResponse]
    ) -> str:
        """
        Hierarchical synthesis based on routing structure.

        Args:
            query: User query
            routing_decision: Routing decision
            agent_responses: Agent responses

        Returns:
            Hierarchically synthesized response
        """
        # Group responses by agent
        by_agent = {}
        for response in agent_responses:
            agent_name = response.agent.value if hasattr(response.agent, 'value') else response.agent
            if agent_name not in by_agent:
                by_agent[agent_name] = []
            by_agent[agent_name].append(response)

        # Build hierarchical response
        parts = [f"Query: {query}\n"]
        parts.append(f"Routing Strategy: {routing_decision.reasoning}\n")
        entry_agent_str = routing_decision.entry_agent.value if hasattr(routing_decision.entry_agent, 'value') else routing_decision.entry_agent
        parts.append(f"Entry Agent: {entry_agent_str}")
        parts.append(f"Optimal Depth: {routing_decision.optimal_depth}\n")

        # Primary response (from entry agent)
        entry_agent = entry_agent_str
        if entry_agent in by_agent:
            entry_responses = by_agent[entry_agent]
            parts.append(f"\nPrimary Response ({entry_agent}):")
            for resp in entry_responses:
                if resp.success:
                    parts.append(f"  {resp.response}")

        # Secondary responses (from cascaded agents)
        for agent_name, responses in by_agent.items():
            if agent_name != entry_agent:
                parts.append(f"\nSupporting Information ({agent_name}):")
                for resp in responses:
                    if resp.success:
                        parts.append(f"  {resp.response}")

        # Add performance summary
        total_latency = sum(r.latency_ms for r in agent_responses)
        successful = sum(1 for r in agent_responses if r.success)

        parts.append(f"\n\nPerformance Summary:")
        parts.append(f"  Total latency: {total_latency}ms")
        parts.append(f"  Agents called: {len(agent_responses)}")
        parts.append(f"  Successful calls: {successful}")
        parts.append(f"  Success rate: {successful / len(agent_responses) if agent_responses else 0:.0%}")

        return "\n".join(parts)

    def create_error_response(
        self,
        query: str,
        error_message: str
    ) -> str:
        """
        Create error response.

        Args:
            query: User query
            error_message: Error message

        Returns:
            Error response
        """
        return f"""Query: {query}

Error: {error_message}

The orchestrator was unable to process this query. Please try again or contact support."""

    def summarize_responses(
        self,
        agent_responses: List[AgentResponse]
    ) -> Dict[str, Any]:
        """
        Create summary of agent responses.

        Args:
            agent_responses: Agent responses

        Returns:
            Response summary
        """
        successful = [r for r in agent_responses if r.success]
        failed = [r for r in agent_responses if not r.success]

        summary = {
            "total": len(agent_responses),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(agent_responses) if agent_responses else 0,
            "total_latency_ms": sum(r.latency_ms for r in agent_responses),
            "avg_latency_ms": (
                sum(r.latency_ms for r in agent_responses) / len(agent_responses)
                if agent_responses else 0
            ),
            "agents_called": list(set(
                r.agent.value if hasattr(r.agent, 'value') else r.agent
                for r in agent_responses
            )),
            "cascaded_agents": list(set(
                cascaded
                for r in agent_responses
                for cascaded in r.cascaded_calls
            ))
        }

        return summary
