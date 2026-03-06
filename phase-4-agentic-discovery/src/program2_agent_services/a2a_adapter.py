"""
Standard A2A Protocol Adapter

Translates between Agno's standard A2A REST format and Phase 4's custom
A2A protocol, enabling Agno RemoteAgent compatibility.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import time

from ..shared.a2a_protocol import A2ARequest, A2AResponse


class AgentCard(BaseModel):
    """Standard A2A agent card for discovery."""
    name: str
    description: str
    url: str
    version: str = "1.0.0"
    capabilities: dict = {}


def mount_a2a_adapter(
    app: FastAPI,
    agent_id: str,
    agent_name: str,
    agent_description: str,
    base_url: str = "http://localhost:8000"
) -> None:
    """
    Mount standard A2A adapter routes alongside existing Phase 4 endpoints.

    Adds:
    - GET /.well-known/agent.json  (agent discovery)
    - POST /  (standard A2A message endpoint)

    Args:
        app: FastAPI application to mount routes on
        agent_id: Agent identifier
        agent_name: Human-readable agent name
        agent_description: Agent description
        base_url: Base URL where this agent is hosted
    """

    @app.get("/.well-known/agent.json")
    async def agent_card():
        """Standard A2A discovery endpoint."""
        return {
            "name": agent_name,
            "description": agent_description,
            "url": base_url,
            "version": "1.0.0",
            "capabilities": {
                "streaming": False,
                "pushNotifications": False,
            },
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "skills": [
                {
                    "id": agent_id,
                    "name": agent_name,
                    "description": agent_description,
                }
            ],
        }

    @app.post("/")
    async def standard_a2a_message(request: Request):
        """
        Standard A2A message endpoint.

        Translates incoming standard A2A requests to Phase 4 A2ARequest format,
        processes via the existing /a2a endpoint logic, and translates back.
        """
        body = await request.json()

        # Extract message from standard A2A format
        message = body.get("message", {})
        parts = message.get("parts", [])
        text_content = ""
        for part in parts:
            if part.get("type") == "text":
                text_content = part.get("text", "")
                break

        if not text_content and isinstance(message, str):
            text_content = message

        # Build Phase 4 A2ARequest dict
        phase4_request = {
            "goal": text_content,
            "target": agent_id,
            "parameters": body.get("metadata", {}),
        }

        # Call existing /a2a endpoint logic internally
        try:
            a2a_request = A2ARequest.from_dict(phase4_request)

            # Find the agent wrapper from app state or call /a2a directly
            # We import the process function from the app's routes
            from starlette.testclient import TestClient
            # Instead of importing test client, route through the app directly
            # by accessing the agent stored during app creation
            agent_wrapper = getattr(app.state, "agent_wrapper", None)
            if agent_wrapper is None:
                return JSONResponse(
                    status_code=500,
                    content={"error": "Agent wrapper not initialized"}
                )

            response = agent_wrapper.process_request(a2a_request)

            # Translate Phase 4 response to standard A2A format
            task_id = str(uuid.uuid4())
            return {
                "id": task_id,
                "status": {
                    "state": "completed" if response.status.value == "success" else "failed",
                },
                "artifacts": [
                    {
                        "parts": [
                            {
                                "type": "text",
                                "text": response.content,
                            }
                        ],
                    }
                ],
                "metadata": {
                    "execution_time_ms": response.execution_time_ms,
                    "agent_id": agent_id,
                },
            }

        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "id": str(uuid.uuid4()),
                    "status": {"state": "failed"},
                    "error": str(e),
                },
            )
