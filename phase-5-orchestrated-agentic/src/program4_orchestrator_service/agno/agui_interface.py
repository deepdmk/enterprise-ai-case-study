"""
AG-UI Interface (Optional)

Provides AG-UI streaming interface for real-time agent activity visualization.
Enables CopilotKit integration for rapid frontend development.
"""

from typing import Optional
from habitat_logging import get_logger
from agno.team.team import Team

logger = get_logger(__name__)


def create_agui_interface(
    team: Team,
    path: str = "/agui",
    name: Optional[str] = None,
    description: Optional[str] = None,
    enabled: bool = True
):
    """
    Create AG-UI interface for the orchestrator team.

    AG-UI provides:
    - Real-time streaming of agent responses
    - Tool activity and delegation visibility
    - CopilotKit integration for frontend development
    - Debuggable agent interactions

    Args:
        team: Agno Team instance
        path: URL path for AG-UI endpoint (default: /agui)
        name: Display name for the interface
        description: Description of the orchestrator
        enabled: Whether to enable AG-UI

    Returns:
        AGUI instance (or None if not enabled or not available)

    Note:
        AG-UI requires agno>=2.4.0 and is an optional feature.
        If agno.interfaces.agui is not available, this returns None.
    """
    if not enabled:
        logger.info("agui_disabled")
        return None

    try:
        # Try to import AGUI from agno
        from agno.interfaces.agui import AGUI

        # Create AGUI interface
        agui = AGUI(
            team=team,
            path=path,
            name=name or "Phase 5 Orchestrator",
            description=description or (
                "Enterprise AI orchestrator with AG-UI streaming. "
                "Coordinates Fundraising, Business Development, and Field Operations agents."
            )
        )

        logger.info(
            "agui_interface_created",
            path=path,
            name=name or "Phase 5 Orchestrator"
        )

        return agui

    except ImportError as e:
        logger.warning(
            "agui_not_available",
            error=str(e),
            message="AG-UI requires agno>=2.4.0 with interfaces support"
        )
        return None

    except Exception as e:
        logger.error("agui_creation_failed", error=str(e))
        return None


def mount_agui_routes(app, agui):
    """
    Mount AG-UI routes to FastAPI app.

    Args:
        app: FastAPI application
        agui: AGUI instance

    Note:
        This adds the following endpoints:
        - POST /agui/stream - SSE stream for real-time events
        - GET /agui/events - Event stream for tool activity
        - Compatible with CopilotKit frontends
    """
    if agui is None:
        logger.info("agui_routes_not_mounted", reason="agui is None")
        return

    try:
        # Mount AG-UI router to FastAPI app
        app.include_router(agui.router)

        logger.info(
            "agui_routes_mounted",
            path=agui.path,
            endpoints=[
                f"{agui.path}/stream",
                f"{agui.path}/events"
            ]
        )

    except Exception as e:
        logger.error("agui_routes_mount_failed", error=str(e))


def create_streaming_response(agui, query: str):
    """
    Create a streaming response for AG-UI.

    This can be used in FastAPI endpoints to stream agent activity to the frontend.

    Args:
        agui: AGUI instance
        query: User query

    Returns:
        Streaming response (async generator)

    Example:
        ```python
        @app.post("/agui/orchestrate")
        async def orchestrate_stream(request: Request):
            query = request.json()["query"]
            return create_streaming_response(agui, query)
        ```
    """
    if agui is None:
        raise ValueError("AG-UI is not available")

    # AG-UI provides streaming via its router
    # This is a helper for custom endpoints
    return agui.stream_response(query)
