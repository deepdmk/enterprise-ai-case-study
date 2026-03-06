"""
Routing Engine

SLM-based routing logic for orchestrator.
"""

from typing import Dict, Any, Optional
import time
import httpx
import structlog

from ..shared.routing_schema import RoutingDecision, AgentType, WorkflowType, AgentCall

logger = structlog.get_logger()


class RoutingEngine:
    """
    SLM-based routing engine.

    Uses fine-tuned orchestrator model to make routing decisions.
    """

    def __init__(
        self,
        inference_server_url: str,
        timeout_ms: int = 500,
        test_mode: bool = False
    ):
        """
        Initialize routing engine.

        Args:
            inference_server_url: URL of inference server
            timeout_ms: Routing timeout in milliseconds
            test_mode: If True, use rule-based fallback
        """
        self.inference_server_url = inference_server_url
        self.timeout_ms = timeout_ms
        self.test_mode = test_mode

        self.logger = logger.bind(component="routing_engine")

        # Reusable HTTP client
        self._client = httpx.AsyncClient(timeout=self.timeout_ms / 1000)

        # Routing statistics
        self.stats = {
            "total_requests": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "fallback_routes": 0,
            "avg_latency_ms": 0
        }

    async def route(self, query: str) -> RoutingDecision:
        """
        Generate routing decision for query.

        Args:
            query: User query

        Returns:
            Routing decision
        """
        self.stats["total_requests"] += 1

        start_time = time.time()

        try:
            if self.test_mode:
                # Use rule-based fallback in test mode
                decision = self._fallback_routing(query)
                self.stats["fallback_routes"] += 1
            else:
                # Use SLM-based routing
                decision = await self._slm_routing(query)
                self.stats["successful_routes"] += 1

            latency_ms = (time.time() - start_time) * 1000

            # Update average latency
            n = self.stats["successful_routes"] + self.stats["fallback_routes"]
            if n > 0:
                self.stats["avg_latency_ms"] = (
                    self.stats["avg_latency_ms"] * (n - 1) + latency_ms
                ) / n

            self.logger.info(
                "routing_complete",
                query=query[:50],
                entry_agent=decision.entry_agent,
                optimal_depth=decision.optimal_depth,
                latency_ms=f"{latency_ms:.0f}ms"
            )

            return decision

        except Exception as e:
            self.stats["failed_routes"] += 1
            self.logger.error("routing_failed", query=query[:50], error=str(e))

            # Fallback on error
            return self._fallback_routing(query)

    async def _slm_routing(self, query: str) -> RoutingDecision:
        """
        SLM-based routing using inference server.

        Args:
            query: User query

        Returns:
            Routing decision
        """
        # Build prompt
        prompt = f"""<|system|>
You are an AI orchestrator that coordinates multiple specialized agents.

Your responsibilities:
1. Analyze user queries and determine which agents to call
2. Decide the optimal cascade depth (how many levels of agent calls)
3. Decompose complex queries into sub-tasks
4. Route sub-tasks to appropriate agents
5. Synthesize responses from multiple agents

Available agents:
- fundraising-agent: Investor profiles, capacity, interests
- business-development-agent: RFP data, competitive landscape
- field-operations-agent: Local capacity, project performance

For each query, output:
1. Entry agent (which agent should handle this)
2. Optimal depth (1-4, how many cascade levels needed)
3. Rationale (why this routing and depth)
<|end|>
<|user|>
Query: {query}<|end|>
<|assistant|>
"""

        # Call inference server
        response = await self._client.post(
            self.inference_server_url,
            json={
                "prompt": prompt,
                "max_tokens": 256,
                "temperature": 0.1
            },
        )

        if response.status_code != 200:
            raise Exception(f"Inference server error: HTTP {response.status_code}")

        result = response.json()
        generated_text = result.get("generated_text", "")

        # Parse routing decision
        decision = self._parse_routing_decision(query, generated_text)

        return decision

    def _parse_routing_decision(self, query: str, generated_text: str) -> RoutingDecision:
        """
        Parse routing decision from generated text.

        Args:
            query: Original query
            generated_text: Generated text from model

        Returns:
            Routing decision
        """
        # Extract entry agent
        entry_agent = AgentType.FIELD_OPERATIONS  # Default
        if "fundraising-agent" in generated_text.lower():
            entry_agent = AgentType.FUNDRAISING
        elif "business-development-agent" in generated_text.lower():
            entry_agent = AgentType.BUSINESS_DEVELOPMENT
        elif "field-operations-agent" in generated_text.lower():
            entry_agent = AgentType.FIELD_OPERATIONS

        # Extract optimal depth
        optimal_depth = 2  # Default
        if "Optimal depth:" in generated_text:
            lines = generated_text.split("\n")
            for line in lines:
                if "Optimal depth:" in line:
                    try:
                        depth_str = line.split("Optimal depth:")[-1].strip()
                        optimal_depth = int(depth_str.split()[0])
                        optimal_depth = max(1, min(4, optimal_depth))  # Clamp to [1, 4]
                    except (ValueError, IndexError):
                        pass

        # Extract reasoning
        reasoning = "SLM-based routing decision"
        if "Rationale:" in generated_text:
            lines = generated_text.split("\n")
            for i, line in enumerate(lines):
                if "Rationale:" in line:
                    reasoning = line.split("Rationale:")[-1].strip()
                    # Also include next lines if they're part of rationale
                    for j in range(i + 1, min(i + 3, len(lines))):
                        if lines[j].strip() and not lines[j].startswith("Entry") and not lines[j].startswith("Optimal"):
                            reasoning += " " + lines[j].strip()
                    break

        # Detect workflow type (simple heuristics)
        workflow = self._detect_workflow(query)

        # Create agent calls
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
            reasoning=reasoning,
            estimated_latency_ms=optimal_depth * 150,  # Rough estimate
            success_probability=0.95
        )

    def _fallback_routing(self, query: str) -> RoutingDecision:
        """
        Rule-based fallback routing (for test mode or errors).

        Args:
            query: User query

        Returns:
            Routing decision
        """
        query_lower = query.lower()

        # Simple keyword-based routing
        if any(keyword in query_lower for keyword in ["investor", "inv-", "angel", "portfolio"]):
            entry_agent = AgentType.FUNDRAISING
            depth = 2
        elif any(keyword in query_lower for keyword in ["rfp", "competitive", "funder", "funding opportunity"]):
            entry_agent = AgentType.BUSINESS_DEVELOPMENT
            depth = 2
        elif any(keyword in query_lower for keyword in ["kenya", "country", "region", "local", "capacity"]):
            entry_agent = AgentType.FIELD_OPERATIONS
            depth = 3
        else:
            # Default
            entry_agent = AgentType.FIELD_OPERATIONS
            depth = 2

        workflow = self._detect_workflow(query)

        agent_calls = [
            AgentCall(
                step=1,
                agent=entry_agent,
                operation="process_query",
                expected_depth=depth - 1
            )
        ]

        return RoutingDecision(
            workflow=workflow,
            entry_agent=entry_agent,
            optimal_depth=depth,
            agent_calls=agent_calls,
            reasoning="Rule-based fallback routing",
            estimated_latency_ms=depth * 150,
            success_probability=0.8
        )

    def _detect_workflow(self, query: str) -> WorkflowType:
        """
        Detect workflow type from query.

        Args:
            query: User query

        Returns:
            Workflow type
        """
        query_lower = query.lower()

        # Check more specific patterns before general ones
        if "regional" in query_lower or "country" in query_lower:
            return WorkflowType.EVALUATE_REGIONAL_PROJECT
        elif "investor capacity" in query_lower or "investment capacity" in query_lower:
            return WorkflowType.ASSESS_INVESTOR_CAPACITY
        elif "competitive landscape" in query_lower or "market fit" in query_lower:
            return WorkflowType.ANALYZE_COMPETITIVE_LANDSCAPE
        elif "funding opportunity" in query_lower or "evaluate" in query_lower:
            return WorkflowType.EVALUATE_FUNDING_OPPORTUNITY
        else:
            return WorkflowType.UNKNOWN

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._client.aclose()

    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""
        return self.stats.copy()

    def reset_stats(self) -> None:
        """Reset routing statistics"""
        self.stats = {
            "total_requests": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "fallback_routes": 0,
            "avg_latency_ms": 0
        }
