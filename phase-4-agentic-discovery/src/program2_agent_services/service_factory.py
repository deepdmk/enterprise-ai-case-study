"""
Agent Service Factory

Creates FastAPI applications for A2A agent services.
"""

from pathlib import Path
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..shared.a2a_protocol import A2ACapability, A2ARequest, A2AResponse
from ..shared.discovery_backend import DiscoveryBackend, InMemoryDiscoveryBackend
from ..shared.call_logger import A2ACallLogger
from ..shared.moe_loader import MoEModelLoader
from .agent_wrapper import A2AAgent


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    agent_id: str
    agent_name: str


class CapabilityResponse(BaseModel):
    """Capability response"""
    agent_id: str
    name: str
    description: str
    domains: list
    example_queries: list


def create_agent_app(
    agent_id: str,
    capability: A2ACapability,
    discovery_backend: Optional[DiscoveryBackend] = None,
    call_logger: Optional[A2ACallLogger] = None,
    agent_registry: Optional[Dict[str, str]] = None,
    test_mode: bool = False
) -> tuple[FastAPI, A2AAgent]:
    """
    Create a FastAPI application for an A2A agent service.

    Args:
        agent_id: Unique agent identifier
        capability: Agent capability description
        discovery_backend: Discovery backend (optional)
        call_logger: Call logger (optional)
        agent_registry: Registry of agent URLs
        test_mode: If True, use mock implementations

    Returns:
        Tuple of (FastAPI app, A2AAgent instance)
    """
    # Create FastAPI app
    app = FastAPI(
        title=f"{capability.name} Agent Service",
        description=capability.description,
        version="1.0.0"
    )

    # Load model if not in test mode
    model = None
    tokenizer = None

    if not test_mode:
        try:
            # Extract unit name from agent_id (e.g., "fundraising-agent" -> "fundraising")
            unit_name = agent_id.replace("-agent", "").replace("-", "_")

            loader = MoEModelLoader()
            model = loader.load_unit_model(
                unit_name=unit_name,
                with_a2a_adapter=True
            )
            tokenizer = loader.load_tokenizer(unit_name)
            print(f"Loaded MoE model for {unit_name}")
        except Exception as e:
            print(f"Warning: Could not load model for {agent_id}: {e}")
            print("Falling back to mock mode")
            test_mode = True

    # Create agent
    agent = A2AAgent(
        agent_id=agent_id,
        capability=capability,
        model=model,
        tokenizer=tokenizer,
        discovery_backend=discovery_backend,
        call_logger=call_logger,
        agent_registry=agent_registry,
        test_mode=test_mode
    )

    # Register agent with discovery backend
    if discovery_backend:
        discovery_backend.register_agent(capability)

    # Define routes
    @app.get("/health", response_model=HealthResponse)
    async def health():
        """Health check endpoint"""
        return HealthResponse(
            status="healthy",
            agent_id=agent_id,
            agent_name=capability.name
        )

    @app.get("/capability", response_model=CapabilityResponse)
    async def get_capability():
        """Get agent capability information"""
        return CapabilityResponse(
            agent_id=capability.agent_id,
            name=capability.name,
            description=capability.description,
            domains=capability.domains,
            example_queries=capability.example_queries
        )

    @app.post("/a2a")
    async def process_a2a_request(request_dict: dict) -> dict:
        """
        Process an A2A protocol request.

        Args:
            request_dict: A2A request as dictionary

        Returns:
            A2A response as dictionary
        """
        try:
            # Parse request
            request = A2ARequest.from_dict(request_dict)

            # Process request
            response = agent.process_request(request)

            # Return response
            return response.to_dict()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/query")
    async def simple_query(query: dict) -> dict:
        """
        Simple query endpoint (non-A2A).

        Args:
            query: Dictionary with "goal" field

        Returns:
            Simple response dictionary
        """
        try:
            # Convert to A2A request
            request = A2ARequest(
                goal=query.get("goal", ""),
                target=agent_id,
                parameters=query.get("parameters", {})
            )

            # Process
            response = agent.process_request(request)

            # Return simplified response
            return {
                "status": response.status.value,
                "content": response.content,
                "execution_time_ms": response.execution_time_ms
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app, agent


def create_multi_agent_system(
    capabilities: Dict[str, A2ACapability],
    base_port: int = 8000,
    discovery_backend: Optional[DiscoveryBackend] = None,
    call_logger: Optional[A2ACallLogger] = None,
    test_mode: bool = False
) -> Dict[str, tuple[FastAPI, A2AAgent, int]]:
    """
    Create a multi-agent system with multiple agent services.

    Args:
        capabilities: Dictionary mapping agent IDs to capabilities
        base_port: Starting port number
        discovery_backend: Shared discovery backend
        call_logger: Shared call logger
        test_mode: If True, use mock implementations

    Returns:
        Dictionary mapping agent IDs to (app, agent, port) tuples
    """
    # Use in-memory discovery if none provided
    if discovery_backend is None:
        discovery_backend = InMemoryDiscoveryBackend()

    # Build agent registry (maps agent IDs to URLs)
    agent_registry = {}
    for i, agent_id in enumerate(capabilities.keys()):
        port = base_port + i + 1
        agent_registry[agent_id] = f"http://localhost:{port}"

    # Create agent services
    services = {}
    for i, (agent_id, capability) in enumerate(capabilities.items()):
        port = base_port + i + 1

        app, agent = create_agent_app(
            agent_id=agent_id,
            capability=capability,
            discovery_backend=discovery_backend,
            call_logger=call_logger,
            agent_registry=agent_registry,
            test_mode=test_mode
        )

        services[agent_id] = (app, agent, port)

    return services
