"""
Agno Team Orchestration

Creates the coordinator team that delegates to Phase 4 agents.
"""

from phase0_infra.habitat_logging import get_logger
from agno.team.team import Team
from agno.team.mode import TeamMode
from agno.models.vllm import VLLM

from .model_provider import create_vllm_model
from .members import create_all_members
from .coordinator import (
    create_coordinator_instructions,
    create_coordinator_description
)

logger = get_logger(__name__)


def create_orchestrator_team(
    inference_server_url: str,
    agent_registry: dict[str, str],
    show_members_responses: bool = True,
    respond_directly: bool = True,
    model_timeout: float = 30.0,
    model_max_tokens: int = 512,
    model_temperature: float = 0.1,
    test_mode: bool = False,
    use_openai_compatible: bool = False
) -> Team:
    """
    Create Agno Team for Phase 5 orchestration.

    The team operates with a coordinator that makes routing decisions:
    - Coordinator: Fine-tuned SLM (Qwen2.5-7B or Phi-4) that makes routing decisions
    - Members: RemoteAgents wrapping Phase 4 A2A agents (MoE-powered)

    Args:
        inference_server_url: URL of vLLM/TGI inference server
        agent_registry: Mapping of agent names to URLs
        show_members_responses: Show member responses in final output
        respond_directly: Members respond directly (vs coordinator synthesizing)
        model_timeout: Inference timeout in seconds
        model_max_tokens: Maximum tokens for model generation
        model_temperature: Sampling temperature
        test_mode: If True, use mock model for testing
        use_openai_compatible: If True, use OpenAI-compatible endpoint

    Returns:
        Team instance configured for orchestration
    """
    logger.info(
        "creating_orchestrator_team",
        inference_url=inference_server_url,
        agents=list(agent_registry.keys()),
        test_mode=test_mode
    )

    # Create model provider
    if test_mode:
        # Use a mock model for testing
        model = create_mock_model()
    else:
        model = create_vllm_model(
            inference_url=inference_server_url,
            model_id="phase5-orchestrator",
            use_openai_compatible=use_openai_compatible,
            max_tokens=model_max_tokens,
            temperature=model_temperature,
        )

    # Create team members
    members = create_all_members(agent_registry)

    if not members:
        logger.warning("no_members_created", agent_registry=agent_registry)
        raise ValueError("No team members created. Check agent_registry configuration.")

    # Create coordinator instructions
    instructions = create_coordinator_instructions()
    description = create_coordinator_description()

    # Create team with Agno Team parameters
    team = Team(
        name="Phase5Orchestrator",
        mode=TeamMode.route,
        model=model,
        members=members,
        description=description,
        instructions=instructions,
        show_members_responses=show_members_responses,
        markdown=True
    )

    logger.info(
        "orchestrator_team_created",
        team_name=team.name,
        member_count=len(members),
        model=str(model)
    )

    return team


def create_mock_model() -> VLLM:
    """
    Create a mock model for testing.

    Returns:
        Mock VLLM instance
    """
    # For testing, create a VLLM model that points to a mock endpoint
    # In practice, the test environment should mock the HTTP calls
    return VLLM(
        id="mock-orchestrator",
        base_url="http://localhost:9999/mock/"
    )


async def run_orchestration(
    team: Team,
    query: str,
    stream: bool = False
) -> dict:
    """
    Run orchestration with the Agno team.

    Args:
        team: Orchestrator team
        query: User query
        stream: Whether to stream responses

    Returns:
        Orchestration result
    """
    logger.info("running_orchestration", query=query[:100], stream=stream)

    try:
        if stream:
            # Stream responses (useful for AG-UI integration)
            result = await team.arun_stream(query)
            # Note: Streaming returns an async generator
            # Caller needs to consume the stream
            return {"stream": result, "success": True}
        else:
            # Non-streaming execution
            result = await team.arun(query)

            logger.info(
                "orchestration_complete",
                query=query[:50],
                success=True
            )

            return {
                "content": result.content,
                "messages": result.messages if hasattr(result, 'messages') else [],
                "metrics": result.metrics if hasattr(result, 'metrics') else {},
                "success": True
            }

    except Exception as e:
        logger.error("orchestration_failed", query=query[:50], error=str(e))
        return {
            "content": f"Orchestration failed: {str(e)}",
            "success": False,
            "error": str(e)
        }
