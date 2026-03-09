"""
Orchestrator Service

FastAPI service wrapping the SLM orchestrator.
Supports both legacy routing engine and Agno framework.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Any
import time
import uuid
import structlog
from habitat_logging import get_logger

from ..shared.routing_schema import RoutingDecision, OrchestratedResponse
from .routing_engine import RoutingEngine
from .agent_client import AgentClient
from .response_synthesizer import ResponseSynthesizer

logger = get_logger(__name__)


# Request/Response models
class RouteRequest(BaseModel):
    """Request for routing decision"""
    query: str


class RouteResponse(BaseModel):
    """Response with routing decision"""
    routing_decision: RoutingDecision
    latency_ms: int


class OrchestrateRequest(BaseModel):
    """Request for full orchestration"""
    query: str
    execute: bool = True  # If False, only return routing decision


class OrchestrateResponse(BaseModel):
    """Response from orchestration"""
    orchestrated_response: OrchestratedResponse


# Create FastAPI app
def create_app(
    inference_server_url: str,
    agent_registry: dict[str, str],
    routing_timeout_ms: int = 500,
    agent_timeout_ms: int = 10000,
    max_concurrent_agents: int = 5,
    enable_response_synthesis: bool = True,
    test_mode: bool = False,
    # Agno Framework parameters
    use_agno: bool = False,
    agno_config: Optional[dict[str, Any]] = None
) -> FastAPI:
    """
    Create orchestrator FastAPI application.

    Supports both legacy routing engine and Agno framework.

    Args:
        inference_server_url: URL of inference server
        agent_registry: Agent registry
        routing_timeout_ms: Routing timeout
        agent_timeout_ms: Agent call timeout
        max_concurrent_agents: Max concurrent agent calls
        enable_response_synthesis: Enable response synthesis
        test_mode: If True, use mock routing
        use_agno: If True, use Agno framework instead of legacy routing
        agno_config: Agno configuration dictionary

    Returns:
        FastAPI application
    """
    # Track closeable resources for lifespan management
    closeables = []

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: check agent health
        if agent_registry and not test_mode:
            client = AgentClient(agent_registry, timeout_ms=5000)
            health = await client.check_all_agents_health()
            healthy = sum(1 for v in health.values() if v)
            total = len(health)
            logger.info(
                "agent_health_check",
                healthy=healthy,
                total=total,
                status=health,
            )
            if healthy == 0:
                logger.warning(
                    "no_agents_available",
                    message="No agents responded to health check. Service may not function correctly.",
                )
            await client.close()

        yield

        # Shutdown: close resources
        for closeable in closeables:
            if hasattr(closeable, 'close'):
                await closeable.close()

    app = FastAPI(
        title="Phase 5 Orchestrator Service",
        description="SLM-based orchestrator for multi-agent coordination (Legacy + Agno modes)",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Correlation ID middleware
    @app.middleware("http")
    async def add_correlation_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        with structlog.contextvars.bound_contextvars(request_id=request_id):
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response

    # Initialize components based on mode
    if use_agno:
        # Agno mode
        from .agno import (
            create_orchestrator_team,
            LegacyAdapter,
            create_agui_interface,
            TrainingLogger
        )
        from .agno.agui_interface import mount_agui_routes

        agno_config = agno_config or {}

        # Create Agno team (using Agno 2.4.1 API)
        team = create_orchestrator_team(
            inference_server_url=inference_server_url,
            agent_registry=agent_registry,
            show_members_responses=agno_config.get("show_members_responses", True),
            respond_directly=agno_config.get("respond_directly", True),
            model_timeout=agno_config.get("model_timeout", 30.0),
            model_max_tokens=agno_config.get("model_max_tokens", 512),
            model_temperature=agno_config.get("model_temperature", 0.1),
            test_mode=test_mode,
            use_openai_compatible=agno_config.get("use_openai_compatible", False)
        )

        # Create legacy adapter
        legacy_adapter = LegacyAdapter(team)

        # Create training logger
        training_logger_config = agno_config.get("training_logger", {})
        training_logger = TrainingLogger(
            log_dir=training_logger_config.get("log_dir", "data/training/agno_logs"),
            enabled=training_logger_config.get("enabled", True)
        )

        # Create AG-UI interface (optional)
        agui_config = agno_config.get("agui", {})
        if agui_config.get("enabled", False):
            agui = create_agui_interface(
                team=team,
                path=agui_config.get("path", "/agui"),
                enabled=True
            )
            if agui:
                mount_agui_routes(app, agui)

        logger.info("agno_mode_enabled", team_members=len(team.members))

        # Store Agno components in app state
        app.state.use_agno = True
        app.state.team = team
        app.state.legacy_adapter = legacy_adapter
        app.state.training_logger = training_logger

    else:
        # Legacy mode
        routing_engine = RoutingEngine(
            inference_server_url=inference_server_url,
            timeout_ms=routing_timeout_ms,
            test_mode=test_mode
        )

        agent_client = AgentClient(
            agent_registry=agent_registry,
            timeout_ms=agent_timeout_ms,
            max_concurrent=max_concurrent_agents
        )

        response_synthesizer = ResponseSynthesizer(
            strategy="hierarchical" if enable_response_synthesis else "concatenation"
        )

        # Register for cleanup on shutdown
        closeables.extend([routing_engine, agent_client])

        logger.info("legacy_mode_enabled")

        # Store legacy components in app state
        app.state.use_agno = False
        app.state.routing_engine = routing_engine
        app.state.agent_client = agent_client
        app.state.response_synthesizer = response_synthesizer

    # Store common state
    app.state.agent_registry = agent_registry
    app.state.test_mode = test_mode

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        if app.state.use_agno:
            # Agno mode: Check member agents
            from .agent_client import AgentClient
            temp_client = AgentClient(
                agent_registry=app.state.agent_registry,
                timeout_ms=5000,
                max_concurrent=5
            )
            agent_health = await temp_client.check_all_agents_health()

            return {
                "status": "healthy",
                "mode": "agno",
                "test_mode": app.state.test_mode,
                "team_members": len(app.state.team.members),
                "agents_available": sum(1 for h in agent_health.values() if h),
                "agents_total": len(agent_health),
                "agent_health": agent_health
            }
        else:
            # Legacy mode
            agent_health = await app.state.agent_client.check_all_agents_health()

            return {
                "status": "healthy",
                "mode": "legacy",
                "test_mode": app.state.test_mode,
                "agents_available": sum(1 for h in agent_health.values() if h),
                "agents_total": len(agent_health),
                "agent_health": agent_health
            }

    @app.post("/route", response_model=RouteResponse)
    async def route(request: RouteRequest):
        """
        Get routing decision for a query.

        Returns routing decision without executing agent calls.
        """
        start_time = time.time()

        try:
            if app.state.use_agno:
                # Agno mode: Use legacy adapter
                decision = await app.state.legacy_adapter.route(request.query)
            else:
                # Legacy mode: Use routing engine
                decision = await app.state.routing_engine.route(request.query)

            latency_ms = int((time.time() - start_time) * 1000)

            return RouteResponse(
                routing_decision=decision,
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.error("route_failed", query=request.query, error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/orchestrate", response_model=OrchestrateResponse)
    async def orchestrate(request: OrchestrateRequest):
        """
        Full orchestration: routing + agent execution + response synthesis.
        """
        start_time = time.time()

        try:
            if app.state.use_agno:
                # Agno mode: Use legacy adapter
                orchestrated_response = await app.state.legacy_adapter.orchestrate(
                    query=request.query,
                    execute=request.execute
                )

                # Log to training logger
                if hasattr(app.state, 'training_logger'):
                    app.state.training_logger.log_orchestration(orchestrated_response)

                logger.info(
                    "agno_orchestration_complete",
                    query=request.query[:50],
                    total_latency_ms=orchestrated_response.total_latency_ms,
                    success=orchestrated_response.success
                )

                return OrchestrateResponse(orchestrated_response=orchestrated_response)

            else:
                # Legacy mode: Use routing engine + agent client
                # Step 1: Get routing decision
                routing_decision = await app.state.routing_engine.route(request.query)

                logger.info(
                    "routing_complete",
                    query=request.query[:50],
                    entry_agent=routing_decision.entry_agent,
                    optimal_depth=routing_decision.optimal_depth
                )

                # Step 2: Execute agent calls (if requested)
                agent_responses = []
                if request.execute:
                    # Build agent calls from routing decision
                    calls = []
                    for agent_call in routing_decision.agent_calls:
                        calls.append({
                            "agent": agent_call.agent,
                            "operation": agent_call.operation,
                            "parameters": agent_call.parameters or {},
                            "max_depth": routing_decision.optimal_depth
                        })

                    # Execute calls
                    agent_responses = await app.state.agent_client.call_multiple_agents(calls)

                    logger.info(
                        "agent_calls_complete",
                        num_calls=len(agent_responses),
                        successful=sum(1 for r in agent_responses if r.success)
                    )

                # Step 3: Synthesize response
                if agent_responses:
                    synthesized = app.state.response_synthesizer.synthesize(
                        request.query,
                        routing_decision,
                        agent_responses
                    )
                    success = any(r.success for r in agent_responses)
                else:
                    synthesized = f"Routing decision: {routing_decision.reasoning}"
                    success = True

                total_latency_ms = int((time.time() - start_time) * 1000)

                # Build orchestrated response
                orchestrated_response = OrchestratedResponse(
                    query=request.query,
                    routing_decision=routing_decision,
                    agent_responses=agent_responses,
                    synthesized_response=synthesized,
                    total_latency_ms=total_latency_ms,
                    success=success
                )

                logger.info(
                    "legacy_orchestration_complete",
                    query=request.query[:50],
                    total_latency_ms=total_latency_ms,
                    success=success
                )

                return OrchestrateResponse(orchestrated_response=orchestrated_response)

        except Exception as e:
            logger.error("orchestration_failed", query=request.query, error=str(e))

            # Create error response
            if app.state.use_agno:
                error_response = OrchestratedResponse(
                    query=request.query,
                    routing_decision=None,
                    agent_responses=[],
                    synthesized_response=f"Agno orchestration failed: {str(e)}",
                    total_latency_ms=int((time.time() - start_time) * 1000),
                    success=False
                )
            else:
                error_response = OrchestratedResponse(
                    query=request.query,
                    routing_decision=routing_decision if 'routing_decision' in locals() else None,
                    agent_responses=[],
                    synthesized_response=app.state.response_synthesizer.create_error_response(
                        request.query,
                        str(e)
                    ),
                    total_latency_ms=int((time.time() - start_time) * 1000),
                    success=False
                )

            return OrchestrateResponse(orchestrated_response=error_response)

    @app.get("/stats")
    async def stats():
        """Get orchestrator statistics"""
        if app.state.use_agno:
            # Agno mode: Return training logger stats
            stats_dict = {
                "mode": "agno",
                "agents": {
                    "registry_size": len(app.state.agent_registry),
                    "agents": list(app.state.agent_registry.keys())
                }
            }

            if hasattr(app.state, 'training_logger'):
                stats_dict["training_logger"] = app.state.training_logger.get_stats()

            return stats_dict
        else:
            # Legacy mode: Return routing stats
            routing_stats = app.state.routing_engine.get_stats()

            return {
                "mode": "legacy",
                "routing": routing_stats,
                "agents": {
                    "registry_size": len(app.state.agent_registry),
                    "agents": list(app.state.agent_registry.keys())
                }
            }

    @app.post("/stats/reset")
    async def reset_stats():
        """Reset statistics"""
        if app.state.use_agno:
            # Agno mode: No stats to reset (training logger is append-only)
            return {"status": "agno_mode_no_reset", "message": "Training logger is append-only"}
        else:
            # Legacy mode: Reset routing stats
            app.state.routing_engine.reset_stats()
            return {"status": "reset", "mode": "legacy"}

    return app
