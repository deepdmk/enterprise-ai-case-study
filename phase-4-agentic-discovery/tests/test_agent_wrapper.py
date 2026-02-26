"""
Tests for A2A Agent Wrapper
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from src.shared.a2a_protocol import (
    A2ARequest,
    A2AResponse,
    A2AMetadata,
    A2ACapability,
    ResponseStatus
)
from src.program2_agent_services.agent_wrapper import A2AAgent


@pytest.fixture
def test_capability():
    """Create test capability"""
    return A2ACapability(
        agent_id="test-agent",
        name="Test Agent",
        description="A test agent for unit testing",
        domains=["testing", "validation"],
        example_queries=["test query"],
        dependencies=["other-agent"],
        max_cascade_depth=3
    )


@pytest.fixture
def test_agent(test_capability):
    """Create test agent"""
    return A2AAgent(
        agent_id="test-agent",
        capability=test_capability,
        test_mode=True
    )


@pytest.fixture
def test_metadata():
    """Create test metadata"""
    return A2AMetadata(
        call_id="test-123",
        timestamp=datetime.now(),
        call_depth=0,
        max_depth=3,
        source_agent="user",
        target_agent="test-agent"
    )


class TestA2AAgentInit:
    """Test agent initialization"""

    def test_create_agent(self, test_capability):
        """Test creating an A2A agent"""
        agent = A2AAgent(
            agent_id="test-agent",
            capability=test_capability,
            test_mode=True
        )

        assert agent.agent_id == "test-agent"
        assert agent.capability == test_capability
        assert agent.test_mode is True
        assert agent.default_timeout_ms == 5000

    def test_agent_with_custom_registry(self, test_capability):
        """Test agent with custom agent registry"""
        registry = {
            "other-agent": "http://localhost:8002"
        }

        agent = A2AAgent(
            agent_id="test-agent",
            capability=test_capability,
            agent_registry=registry,
            test_mode=True
        )

        assert agent.agent_registry == registry

    def test_agent_uses_mock_model_in_test_mode(self, test_capability):
        """Test that agent uses mock model when in test mode"""
        agent = A2AAgent(
            agent_id="test-agent",
            capability=test_capability,
            test_mode=True
        )

        assert agent.model is not None
        assert agent.tokenizer is not None


class TestProcessRequest:
    """Test request processing"""

    @pytest.mark.asyncio
    async def test_process_simple_request(self, test_agent, test_metadata):
        """Test processing a simple request"""
        request = A2ARequest(
            goal="Test query",
            target="test-agent",
            metadata=test_metadata
        )

        response = await test_agent.process_request(request)

        assert response.status == ResponseStatus.SUCCESS
        assert response.content is not None
        assert response.execution_time_ms > 0

    @pytest.mark.asyncio
    async def test_process_request_creates_metadata(self, test_agent):
        """Test that metadata is created if not provided"""
        request = A2ARequest(
            goal="Test query",
            target="test-agent"
        )

        response = await test_agent.process_request(request)

        assert response.metadata is not None
        assert response.metadata.call_depth == 0

    @pytest.mark.asyncio
    async def test_depth_limit_exceeded(self, test_agent):
        """Test depth limit handling"""
        metadata = A2AMetadata(
            call_id="test-123",
            timestamp=datetime.now(),
            call_depth=3,  # At limit
            max_depth=3,
            source_agent="user",
            target_agent="test-agent"
        )

        request = A2ARequest(
            goal="Test query",
            target="test-agent",
            metadata=metadata
        )

        response = await test_agent.process_request(request)

        assert response.status == ResponseStatus.DEPTH_EXCEEDED
        assert "depth limit reached" in response.content.lower()

    @pytest.mark.asyncio
    async def test_depth_at_exactly_max_depth(self, test_agent):
        """Test that depth exactly at max_depth triggers limit"""
        metadata = A2AMetadata(
            call_id="test-123",
            timestamp=datetime.now(),
            call_depth=2,
            max_depth=2,
            source_agent="user",
            target_agent="test-agent"
        )

        request = A2ARequest(
            goal="Test query",
            target="test-agent",
            metadata=metadata
        )

        response = await test_agent.process_request(request)

        assert response.status == ResponseStatus.DEPTH_EXCEEDED


class TestA2ACallExtraction:
    """Test A2A call extraction from responses"""

    def test_extract_single_call(self, test_agent):
        """Test extracting a single A2A call"""
        response_text = '''
        I need more information.
        <a2a_call>
        {"goal": "Get investor info", "target": "fundraising-agent", "parameters": {}}
        </a2a_call>
        '''

        calls = test_agent._extract_a2a_calls(response_text)

        assert len(calls) == 1
        assert calls[0]["target"] == "fundraising-agent"
        assert calls[0]["goal"] == "Get investor info"

    def test_extract_multiple_calls(self, test_agent):
        """Test extracting multiple A2A calls"""
        response_text = '''
        <a2a_call>
        {"goal": "Get investor info", "target": "fundraising-agent", "parameters": {}}
        </a2a_call>
        <a2a_call>
        {"goal": "Get RFP data", "target": "business-development-agent", "parameters": {}}
        </a2a_call>
        '''

        calls = test_agent._extract_a2a_calls(response_text)

        assert len(calls) == 2
        assert calls[0]["target"] == "fundraising-agent"
        assert calls[1]["target"] == "business-development-agent"

    def test_extract_no_calls(self, test_agent):
        """Test when no A2A calls are present"""
        response_text = "This is a direct response without any agent calls."

        calls = test_agent._extract_a2a_calls(response_text)

        assert len(calls) == 0

    def test_extract_malformed_json(self, test_agent):
        """Test handling malformed JSON in A2A call"""
        response_text = '''
        <a2a_call>
        {invalid json}
        </a2a_call>
        '''

        calls = test_agent._extract_a2a_calls(response_text)

        assert len(calls) == 0

    def test_extract_missing_required_fields(self, test_agent):
        """Test handling A2A call missing required fields"""
        response_text = '''
        <a2a_call>
        {"some_field": "value"}
        </a2a_call>
        '''

        calls = test_agent._extract_a2a_calls(response_text)

        assert len(calls) == 0


class TestMockResponseGeneration:
    """Test mock response generation"""

    def test_mock_direct_response(self, test_agent, test_metadata):
        """Test generating mock direct response"""
        request = A2ARequest(
            goal="Simple test query",
            target="test-agent",
            metadata=test_metadata
        )

        response = test_agent._generate_mock_response(request)

        assert "Mock response" in response

    def test_mock_response_with_agent_call(self, test_agent, test_metadata):
        """Test mock response generates A2A call for complex queries"""
        request = A2ARequest(
            goal="Compare investor with other sources",
            target="test-agent",
            metadata=test_metadata
        )

        response = test_agent._generate_mock_response(request)

        # Should contain A2A call because of "compare" keyword
        assert "<a2a_call>" in response or "Mock response" in response


class TestCallAgent:
    """Test agent-to-agent calls"""

    @pytest.mark.asyncio
    async def test_call_agent_not_in_registry(self, test_agent, test_metadata):
        """Test calling agent not in registry"""
        result = await test_agent._call_agent(
            target_agent="unknown-agent",
            goal="Test goal",
            parameters={},
            parent_metadata=test_metadata
        )

        assert "not found" in result.lower()

    @pytest.mark.asyncio
    async def test_call_agent_timeout(self, test_capability, test_metadata):
        """Test timeout handling"""
        agent = A2AAgent(
            agent_id="test-agent",
            capability=test_capability,
            agent_registry={"other-agent": "http://localhost:9999"},
            test_mode=True
        )

        with patch('httpx.AsyncClient') as mock_client:
            import httpx
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.TimeoutException("timeout")
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await agent._call_agent(
                target_agent="other-agent",
                goal="Test goal",
                parameters={},
                parent_metadata=test_metadata
            )

            assert "timeout" in result.lower()

    @pytest.mark.asyncio
    async def test_call_agent_network_error(self, test_capability, test_metadata):
        """Test network error handling"""
        agent = A2AAgent(
            agent_id="test-agent",
            capability=test_capability,
            agent_registry={"other-agent": "http://localhost:9999"},
            test_mode=True
        )

        with patch('httpx.AsyncClient') as mock_client:
            import httpx
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.RequestError("connection failed")
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await agent._call_agent(
                target_agent="other-agent",
                goal="Test goal",
                parameters={},
                parent_metadata=test_metadata
            )

            assert "network error" in result.lower()

    @pytest.mark.asyncio
    async def test_call_agent_server_error(self, test_capability, test_metadata):
        """Test server error handling"""
        agent = A2AAgent(
            agent_id="test-agent",
            capability=test_capability,
            agent_registry={"other-agent": "http://localhost:9999"},
            test_mode=True
        )

        with patch('httpx.AsyncClient') as mock_client:
            import httpx
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.HTTPStatusError(
                "server error",
                request=MagicMock(),
                response=mock_response
            )
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await agent._call_agent(
                target_agent="other-agent",
                goal="Test goal",
                parameters={},
                parent_metadata=test_metadata
            )

            assert "server error" in result.lower()


class TestPromptBuilding:
    """Test prompt construction"""

    def test_build_prompt(self, test_agent, test_metadata):
        """Test prompt building"""
        request = A2ARequest(
            goal="Test query",
            target="test-agent",
            metadata=test_metadata
        )

        prompt = test_agent._build_prompt(request)

        assert "Test Agent" in prompt
        assert "Test query" in prompt
        assert "depth" in prompt.lower()

    def test_format_dependencies(self, test_agent):
        """Test dependency formatting"""
        deps = test_agent._format_dependencies()

        assert "other-agent" in deps

    def test_format_no_dependencies(self, test_capability):
        """Test formatting when no dependencies"""
        test_capability.dependencies = []
        agent = A2AAgent(
            agent_id="test-agent",
            capability=test_capability,
            test_mode=True
        )

        deps = agent._format_dependencies()

        assert "None" in deps
