"""
Agent Client

Client for communicating with Phase 4 agents via A2A protocol.
"""

from typing import Any, Optional
import time
import asyncio
import httpx
from habitat_logging import get_logger

from ..shared.routing_schema import AgentResponse, AgentType

logger = get_logger(__name__)


class AgentClient:
    """
    Client for Phase 4 A2A agents.

    Handles:
    - Agent discovery from registry
    - A2A protocol requests
    - Error handling and retries
    - Request timeouts
    """

    def __init__(
        self,
        agent_registry: dict[str, str],
        timeout_ms: int = 10000,
        max_concurrent: int = 5,
        max_retries: int = 3,
        retry_base_delay: float = 1.0,
    ):
        """
        Initialize agent client.

        Args:
            agent_registry: Mapping of agent name to URL
            timeout_ms: Request timeout in milliseconds
            max_concurrent: Maximum concurrent agent calls
            max_retries: Maximum retries for transient failures
            retry_base_delay: Base delay in seconds between retries
        """
        self.agent_registry = agent_registry
        self.timeout_ms = timeout_ms
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.retry_base_delay = retry_base_delay

        self.logger = logger.bind(component="agent_client")

        # Semaphore for concurrent requests
        self.semaphore = asyncio.Semaphore(max_concurrent)

        # Reusable HTTP client
        self._client = httpx.AsyncClient(timeout=self.timeout_ms / 1000)

    async def call_agent(
        self,
        agent: AgentType,
        operation: str,
        parameters: Optional[dict[str, Any]] = None,
        max_depth: int = 3
    ) -> AgentResponse:
        """
        Call a Phase 4 agent.

        Args:
            agent: Agent to call
            operation: Operation to perform
            parameters: Operation parameters
            max_depth: Maximum cascade depth

        Returns:
            Agent response
        """
        agent_name = agent.value
        agent_url = self.agent_registry.get(agent_name)

        if not agent_url:
            raise ValueError(f"Agent not found in registry: {agent_name}")

        self.logger.info(
            "calling_agent",
            agent=agent_name,
            operation=operation,
            url=agent_url
        )

        # Build A2A request
        request_payload = {
            "goal": operation,
            "parameters": parameters or {},
            "max_depth": max_depth,
            "timeout_ms": self.timeout_ms
        }

        start_time = time.time()
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                async with self.semaphore:
                    response = await self._client.post(
                        f"{agent_url}/process",
                        json=request_payload,
                    )

                latency_ms = (time.time() - start_time) * 1000

                if response.status_code == 200:
                    result = response.json()

                    agent_response = AgentResponse(
                        agent=agent,
                        operation=operation,
                        success=True,
                        response=result.get("response", ""),
                        latency_ms=int(latency_ms),
                        cascaded_calls=result.get("cascaded_to", [])
                    )

                    self.logger.info(
                        "agent_call_successful",
                        agent=agent_name,
                        latency_ms=f"{latency_ms:.0f}ms",
                        attempt=attempt,
                    )

                    return agent_response

                elif response.status_code >= 500:
                    # Server error — retryable
                    last_error = Exception(f"Agent returned HTTP {response.status_code}")
                    if attempt < self.max_retries:
                        delay = self.retry_base_delay * (2 ** (attempt - 1))
                        self.logger.warning(
                            "agent_call_retry",
                            agent=agent_name,
                            attempt=attempt,
                            delay=delay,
                            status_code=response.status_code,
                        )
                        await asyncio.sleep(delay)
                        continue
                    raise last_error

                else:
                    # Client error (4xx) — not retryable
                    raise Exception(f"Agent returned HTTP {response.status_code}")

            except (httpx.ConnectError, httpx.TimeoutException, ConnectionError, OSError) as e:
                last_error = e
                if attempt < self.max_retries:
                    delay = self.retry_base_delay * (2 ** (attempt - 1))
                    self.logger.warning(
                        "agent_call_retry",
                        agent=agent_name,
                        attempt=attempt,
                        max_retries=self.max_retries,
                        delay=delay,
                        error=str(e),
                    )
                    await asyncio.sleep(delay)
                    continue

                latency_ms = (time.time() - start_time) * 1000
                self.logger.error(
                    "agent_call_failed",
                    agent=agent_name,
                    operation=operation,
                    attempts=self.max_retries,
                    error=str(e),
                )
                return AgentResponse(
                    agent=agent,
                    operation=operation,
                    success=False,
                    response=f"Error after {self.max_retries} attempts: {e}",
                    latency_ms=int(latency_ms),
                    cascaded_calls=[],
                )

            except Exception as e:
                latency_ms = (time.time() - start_time) * 1000
                self.logger.error(
                    "agent_call_failed",
                    agent=agent_name,
                    operation=operation,
                    error=str(e),
                )
                return AgentResponse(
                    agent=agent,
                    operation=operation,
                    success=False,
                    response=f"Error: {e}",
                    latency_ms=int(latency_ms),
                    cascaded_calls=[],
                )

        # Should not reach here, but just in case
        latency_ms = (time.time() - start_time) * 1000
        return AgentResponse(
            agent=agent,
            operation=operation,
            success=False,
            response=f"Error: {last_error}",
            latency_ms=int(latency_ms),
            cascaded_calls=[],
        )

    async def call_multiple_agents(
        self,
        calls: list[dict[str, Any]]
    ) -> list[AgentResponse]:
        """
        Call multiple agents concurrently.

        Args:
            calls: List of agent call configurations

        Returns:
            List of agent responses
        """
        self.logger.info("calling_multiple_agents", count=len(calls))

        tasks = []

        for call in calls:
            agent = call.get("agent")
            operation = call.get("operation", "process_query")
            parameters = call.get("parameters", {})
            max_depth = call.get("max_depth", 3)

            task = self.call_agent(agent, operation, parameters, max_depth)
            tasks.append(task)

        # Execute concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions
        results = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                self.logger.error("agent_call_exception", call_index=i, error=str(response))
                # Create error response
                call = calls[i]
                results.append(
                    AgentResponse(
                        agent=call.get("agent", AgentType.FIELD_OPERATIONS),
                        operation=call.get("operation", "process_query"),
                        success=False,
                        response=f"Exception: {str(response)}",
                        latency_ms=0,
                        cascaded_calls=[]
                    )
                )
            else:
                results.append(response)

        return results

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._client.aclose()

    async def check_agent_health(self, agent: AgentType) -> bool:
        """
        Check if agent is healthy.

        Args:
            agent: Agent to check

        Returns:
            True if healthy, False otherwise
        """
        agent_name = agent.value
        agent_url = self.agent_registry.get(agent_name)

        if not agent_url:
            return False

        try:
            response = await self._client.get(
                f"{agent_url}/health",
                timeout=5.0
            )
            return response.status_code == 200

        except Exception as e:
            self.logger.warning("agent_health_check_failed", agent=agent_name, error=str(e))
            return False

    async def check_all_agents_health(self) -> dict[str, bool]:
        """
        Check health of all agents in registry.

        Returns:
            Dictionary mapping agent name to health status
        """
        tasks = []
        agent_types = []

        for agent in AgentType:
            if agent.value in self.agent_registry:
                tasks.append(self.check_agent_health(agent))
                agent_types.append(agent)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        health_status = {}
        for agent, result in zip(agent_types, results):
            if isinstance(result, Exception):
                health_status[agent.value] = False
            else:
                health_status[agent.value] = result

        return health_status
