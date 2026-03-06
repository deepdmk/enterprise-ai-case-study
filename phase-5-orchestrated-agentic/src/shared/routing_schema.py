"""
Routing Schema - Pydantic Models for Phase 5 Orchestrator

Defines data structures for:
- Routing decisions (which agent, what depth)
- Agent call sequences
- Response synthesis
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class WorkflowType(str, Enum):
    """Known workflow types from Phase 4 discovery"""
    EVALUATE_FUNDING_OPPORTUNITY = "evaluate_funding_opportunity"
    ASSESS_INVESTOR_CAPACITY = "assess_investor_capacity"
    ANALYZE_COMPETITIVE_LANDSCAPE = "analyze_competitive_landscape"
    EVALUATE_REGIONAL_PROJECT = "evaluate_regional_project"
    CROSS_REGIONAL_ANALYSIS = "cross_regional_analysis"
    INVESTOR_PORTFOLIO_REVIEW = "investor_portfolio_review"
    UNKNOWN = "unknown"


class AgentType(str, Enum):
    """Available agent types"""
    FUNDRAISING = "fundraising-agent"
    BUSINESS_DEVELOPMENT = "business-development-agent"
    FIELD_OPERATIONS = "field-operations-agent"


class AgentCall(BaseModel):
    """
    Represents a single agent call in the routing sequence.
    """
    step: int = Field(description="Step number in the sequence (1-indexed)")
    agent: AgentType = Field(description="Target agent to call")
    operation: str = Field(description="Operation/goal for this agent")
    expected_depth: int = Field(default=0, description="Expected cascade depth from this call")
    parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional parameters for the agent call"
    )

    class Config:
        use_enum_values = True


class RoutingDecision(BaseModel):
    """
    Orchestrator's routing decision for a user query.

    This is the primary output of the fine-tuned SLM orchestrator.
    """
    workflow: WorkflowType = Field(description="Detected workflow type")
    entry_agent: AgentType = Field(description="Which agent should handle this query first")
    optimal_depth: int = Field(
        ge=1,
        le=4,
        description="Optimal cascade depth for this query (1-4)"
    )
    agent_calls: List[AgentCall] = Field(
        default_factory=list,
        description="Planned sequence of agent calls"
    )
    reasoning: str = Field(description="Explanation of routing decision")
    estimated_latency_ms: int = Field(
        default=0,
        description="Estimated total latency in milliseconds"
    )
    success_probability: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Estimated probability of successful execution"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )

    class Config:
        use_enum_values = True


class TrainingExample(BaseModel):
    """
    Training example for the orchestrator (converted from Phase 4 data).
    """
    query: str = Field(description="User query")
    entry_agent: AgentType = Field(description="Target entry agent")
    optimal_depth: int = Field(ge=1, le=4, description="Optimal depth")
    call_sequence: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Actual call sequence from Phase 4"
    )
    final_response: str = Field(description="Final response from Phase 4")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata")

    class Config:
        use_enum_values = True

    def to_chat_format(self) -> Dict[str, Any]:
        """
        Convert to ChatML format for training.

        Returns:
            Dictionary with 'messages' key containing chat messages
        """
        system_prompt = """You are an AI orchestrator that coordinates multiple specialized agents.

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
"""

        user_message = f"Query: {self.query}"

        # Generate rationale
        rationale = self._generate_rationale()

        assistant_response = f"""Entry agent: {self.entry_agent}
Optimal depth: {self.optimal_depth}

Rationale: {rationale}
"""

        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_response}
            ],
            "metadata": {
                "query": self.query,
                "optimal_depth": self.optimal_depth,
                "success": self.metadata.get("success", False)
            }
        }

    def _generate_rationale(self) -> str:
        """Generate rationale for the routing decision"""
        agent_rationales = {
            AgentType.FUNDRAISING: "This query requires investor-specific information",
            AgentType.BUSINESS_DEVELOPMENT: "This query focuses on funding opportunities and RFPs",
            AgentType.FIELD_OPERATIONS: "This query requires regional or local capacity information"
        }

        agent_rationale = agent_rationales.get(
            self.entry_agent,
            f"Best handled by {self.entry_agent}"
        )

        depth_rationale = ""
        if self.optimal_depth == 1:
            depth_rationale = "Direct answer without cascading needed"
        elif self.optimal_depth == 2:
            depth_rationale = "Requires one level of cascading to related agent"
        elif self.optimal_depth >= 3:
            depth_rationale = "Complex query requiring multi-agent coordination"

        return f"{agent_rationale}. {depth_rationale}."


class AgentResponse(BaseModel):
    """Response from a single agent call"""
    agent: AgentType = Field(description="Agent that responded")
    operation: str = Field(description="Operation performed")
    success: bool = Field(description="Whether the call succeeded")
    response: str = Field(description="Agent's response")
    latency_ms: int = Field(description="Response latency in milliseconds")
    cascaded_calls: List[str] = Field(
        default_factory=list,
        description="Agents that were cascaded to"
    )

    class Config:
        use_enum_values = True


class OrchestratedResponse(BaseModel):
    """
    Final orchestrated response combining multiple agent responses.
    """
    query: str = Field(description="Original user query")
    routing_decision: Optional[RoutingDecision] = Field(default=None, description="Routing decision made")
    agent_responses: List[AgentResponse] = Field(
        default_factory=list,
        description="Responses from all agents called"
    )
    synthesized_response: str = Field(description="Final synthesized response")
    total_latency_ms: int = Field(description="Total orchestration latency")
    success: bool = Field(description="Overall success status")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )
