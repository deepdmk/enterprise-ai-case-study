"""
A2A Agent Wrapper

Wraps MoE models with A2A protocol capabilities.
Handles request parsing, response generation, and cascading calls.
"""

import time
import re
import json
import uuid
from datetime import datetime
from typing import Optional, Any
import httpx

from ..shared.a2a_protocol import (
    A2ARequest,
    A2AResponse,
    A2AMetadata,
    ResponseStatus,
    A2ACapability
)
from ..shared.discovery_backend import DiscoveryBackend
from ..shared.call_logger import A2ACallLogger
from ..shared.moe_loader import MockMoEModel, MockTokenizer


class A2AAgent:
    """
    Agent wrapper that adds A2A protocol capabilities to MoE models.

    Handles:
    - A2A request parsing
    - Depth limit enforcement
    - Cascading calls to other agents
    - Response generation
    - Call logging
    """

    def __init__(
        self,
        agent_id: str,
        capability: A2ACapability,
        model: Optional[Any] = None,
        tokenizer: Optional[Any] = None,
        discovery_backend: Optional[DiscoveryBackend] = None,
        call_logger: Optional[A2ACallLogger] = None,
        agent_registry: Optional[dict[str, str]] = None,
        test_mode: bool = False
    ):
        """
        Initialize A2A agent.

        Args:
            agent_id: Unique agent identifier
            capability: Agent capability description
            model: MoE model (or None for mock)
            tokenizer: Tokenizer (or None for mock)
            discovery_backend: Discovery backend for finding agents
            call_logger: Logger for A2A calls
            agent_registry: Registry mapping agent IDs to URLs
            test_mode: If True, use mock implementations
        """
        self.agent_id = agent_id
        self.capability = capability
        self.discovery_backend = discovery_backend
        self.call_logger = call_logger
        self.agent_registry = agent_registry or {}
        self.test_mode = test_mode
        self.default_timeout_ms = 5000  # Default timeout in milliseconds

        # Use mock model if test_mode or no model provided
        if test_mode or model is None:
            self.model = MockMoEModel(agent_id)
            self.tokenizer = MockTokenizer()
        else:
            self.model = model
            self.tokenizer = tokenizer

    async def process_request(self, request: A2ARequest) -> A2AResponse:
        """
        Process an A2A request.

        Args:
            request: The A2A request

        Returns:
            A2A response
        """
        start_time = time.time()

        # Ensure metadata exists
        if not request.metadata:
            request.metadata = A2AMetadata(
                call_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                call_depth=0,
                max_depth=3,
                source_agent="user",
                target_agent=self.agent_id
            )

        # Check depth limit
        if request.metadata.call_depth >= request.metadata.max_depth:
            return self._depth_limit_response(request, start_time)

        try:
            # Generate response using model
            response_content = self._generate_response(request)

            # Check if response contains A2A calls
            a2a_calls = self._extract_a2a_calls(response_content)

            if a2a_calls:
                # Process cascading calls
                final_content = await self._process_cascading_calls(
                    request,
                    a2a_calls,
                    response_content
                )
                cascaded_agents = [call["target"] for call in a2a_calls]
            else:
                # Direct response
                final_content = response_content
                cascaded_agents = []

            execution_time = (time.time() - start_time) * 1000

            response = A2AResponse(
                status=ResponseStatus.SUCCESS,
                content=final_content,
                metadata=request.metadata,
                cascaded_calls=cascaded_agents,
                execution_time_ms=execution_time
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            response = A2AResponse(
                status=ResponseStatus.ERROR,
                content=None,
                metadata=request.metadata,
                error_message=str(e),
                execution_time_ms=execution_time
            )

        # Log the call
        if self.call_logger:
            self.call_logger.log_call(request, response)

        return response

    def _generate_response(self, request: A2ARequest) -> str:
        """
        Generate response using the MoE model.

        Args:
            request: The A2A request

        Returns:
            Generated response text
        """
        # Build prompt with A2A context
        prompt = self._build_prompt(request)

        if self.test_mode:
            # Mock response
            return self._generate_mock_response(request)

        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        # Generate
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True
        )

        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract just the assistant's response
        response = self._extract_assistant_response(response, prompt)

        return response

    def _build_prompt(self, request: A2ARequest) -> str:
        """Build prompt for the model"""
        system_msg = f"""You are the {self.capability.name} agent with A2A protocol capabilities.

Your responsibilities: {', '.join(self.capability.domains)}

Available agents to call:
{self._format_dependencies()}

Current context: Call depth: {request.metadata.call_depth}/{request.metadata.max_depth}

To call another agent, use:
<a2a_call>
{{"goal": "what you need", "target": "agent-id", "parameters": {{}}}}
</a2a_call>
"""

        user_msg = request.goal

        # Simple ChatML format
        prompt = f"{system_msg}\n\nUser: {user_msg}\n\nAssistant:"

        return prompt

    def _format_dependencies(self) -> str:
        """Format available dependencies"""
        if not self.capability.dependencies:
            return "- None (handle all queries directly)"

        lines = []
        for dep in self.capability.dependencies:
            lines.append(f"- {dep}")
        return "\n".join(lines)

    def _generate_mock_response(self, request: A2ARequest) -> str:
        """Generate mock response for testing"""
        # Simulate different response types based on query
        goal_lower = request.goal.lower()

        # Check if query needs another agent
        needs_agent_call = any(
            keyword in goal_lower
            for keyword in ["compare", "comprehensive", "including", "with"]
        )

        if needs_agent_call and self.capability.dependencies:
            # Generate mock A2A call
            target = self.capability.dependencies[0]
            a2a_call = {
                "goal": f"Get information from {target}",
                "target": target,
                "parameters": {}
            }
            return f"I need to call another agent:\n<a2a_call>\n{json.dumps(a2a_call, indent=2)}\n</a2a_call>"
        else:
            # Direct response
            return f"Mock response for: {request.goal}"

    def _extract_assistant_response(self, full_response: str, prompt: str) -> str:
        """Extract just the assistant's response from the full generation"""
        # Remove the prompt
        if prompt in full_response:
            response = full_response[len(prompt):].strip()
        else:
            response = full_response

        return response

    def _extract_a2a_calls(self, response: str) -> list:
        """
        Extract A2A calls from response text.

        Args:
            response: Generated response text

        Returns:
            List of A2A call dictionaries
        """
        calls = []

        # Find all <a2a_call> blocks
        pattern = r'<a2a_call>(.*?)</a2a_call>'
        matches = re.findall(pattern, response, re.DOTALL)

        for match in matches:
            try:
                call = json.loads(match.strip())
                if "goal" in call and "target" in call:
                    calls.append(call)
            except json.JSONDecodeError:
                continue

        return calls

    async def _process_cascading_calls(
        self,
        original_request: A2ARequest,
        a2a_calls: list,
        original_response: str
    ) -> str:
        """
        Process cascading A2A calls.

        Args:
            original_request: The original request
            a2a_calls: List of A2A calls to make
            original_response: The original response text

        Returns:
            Final response incorporating cascade results
        """
        cascade_results = []

        for call in a2a_calls:
            target_agent = call["target"]
            goal = call["goal"]
            parameters = call.get("parameters", {})

            # Make cascading call
            result = await self._call_agent(
                target_agent=target_agent,
                goal=goal,
                parameters=parameters,
                parent_metadata=original_request.metadata
            )

            cascade_results.append({
                "agent": target_agent,
                "result": result
            })

        # Combine original response with cascade results
        final_response = original_response

        # Remove A2A call blocks from response
        final_response = re.sub(r'<a2a_call>.*?</a2a_call>', '', final_response, flags=re.DOTALL)

        # Add cascade results
        if cascade_results:
            final_response += "\n\nAgent Responses:\n"
            for result in cascade_results:
                final_response += f"\n{result['agent']}: {result['result']}\n"

        return final_response

    async def _call_agent(
        self,
        target_agent: str,
        goal: str,
        parameters: dict[str, Any],
        parent_metadata: A2AMetadata
    ) -> str:
        """
        Make a call to another agent.

        Args:
            target_agent: Target agent ID
            goal: What we need from the agent
            parameters: Additional parameters
            parent_metadata: Metadata from parent request

        Returns:
            Response content from the agent
        """
        # Build cascading request
        cascade_request = A2ARequest(
            goal=goal,
            target=target_agent,
            parameters=parameters,
            metadata=A2AMetadata(
                call_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                call_depth=parent_metadata.call_depth + 1,
                max_depth=parent_metadata.max_depth,
                source_agent=self.agent_id,
                target_agent=target_agent,
                trace_id=parent_metadata.trace_id or parent_metadata.call_id
            )
        )

        # Get agent URL from registry
        agent_url = self.agent_registry.get(target_agent)

        if not agent_url:
            return f"Error: Agent {target_agent} not found"

        # Use metadata timeout or default
        timeout_seconds = (parent_metadata.timeout_ms or self.default_timeout_ms) / 1000

        try:
            # Make async HTTP call
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{agent_url}/a2a",
                    json=cascade_request.to_dict(),
                    timeout=timeout_seconds
                )
                response.raise_for_status()

            a2a_response = A2AResponse.from_dict(response.json())

            if a2a_response.status == ResponseStatus.SUCCESS:
                return a2a_response.content
            else:
                return f"Error from {target_agent}: {a2a_response.error_message}"

        except httpx.TimeoutException:
            return f"Timeout calling {target_agent}"
        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                return f"Server error from {target_agent}: {e.response.status_code}"
            return f"Client error from {target_agent}: {e.response.status_code}"
        except httpx.RequestError as e:
            return f"Network error calling {target_agent}: {str(e)}"

    def _depth_limit_response(
        self,
        request: A2ARequest,
        start_time: float
    ) -> A2AResponse:
        """Generate response when depth limit is reached"""
        execution_time = (time.time() - start_time) * 1000

        return A2AResponse(
            status=ResponseStatus.DEPTH_EXCEEDED,
            content="Cannot process request: depth limit reached",
            metadata=request.metadata,
            error_message=f"Depth {request.metadata.call_depth} exceeds max {request.metadata.max_depth}",
            execution_time_ms=execution_time
        )
