"""
Tests for A2A Protocol
"""

import pytest
from datetime import datetime

from src.shared.a2a_protocol import (
    A2ARequest,
    A2AResponse,
    A2AMetadata,
    A2ACapability,
    MessageType,
    ResponseStatus
)


class TestA2AMetadata:
    """Test A2AMetadata class"""

    def test_create_metadata(self):
        """Test creating A2A metadata"""
        metadata = A2AMetadata(
            call_id="test-123",
            timestamp=datetime.now(),
            call_depth=1,
            max_depth=3,
            source_agent="agent-a",
            target_agent="agent-b"
        )

        assert metadata.call_id == "test-123"
        assert metadata.call_depth == 1
        assert metadata.max_depth == 3

    def test_metadata_to_dict(self):
        """Test metadata serialization"""
        metadata = A2AMetadata(
            call_id="test-123",
            timestamp=datetime.now(),
            call_depth=1,
            max_depth=3,
            source_agent="agent-a",
            target_agent="agent-b"
        )

        data = metadata.to_dict()

        assert data["call_id"] == "test-123"
        assert "timestamp" in data
        assert data["call_depth"] == 1

    def test_metadata_from_dict(self):
        """Test metadata deserialization"""
        data = {
            "call_id": "test-123",
            "timestamp": datetime.now().isoformat(),
            "call_depth": 1,
            "max_depth": 3,
            "source_agent": "agent-a",
            "target_agent": "agent-b",
            "timeout_ms": 5000,
            "retry_count": 0,
            "trace_id": None
        }

        metadata = A2AMetadata.from_dict(data)

        assert metadata.call_id == "test-123"
        assert metadata.call_depth == 1


class TestA2ARequest:
    """Test A2ARequest class"""

    def test_create_request(self):
        """Test creating A2A request"""
        request = A2ARequest(
            goal="Test goal",
            target="test-agent",
            parameters={"key": "value"}
        )

        assert request.goal == "Test goal"
        assert request.target == "test-agent"
        assert request.parameters["key"] == "value"

    def test_request_to_dict(self):
        """Test request serialization"""
        request = A2ARequest(
            goal="Test goal",
            target="test-agent"
        )

        data = request.to_dict()

        assert data["goal"] == "Test goal"
        assert data["target"] == "test-agent"


class TestA2AResponse:
    """Test A2AResponse class"""

    def test_create_response(self):
        """Test creating A2A response"""
        response = A2AResponse(
            status=ResponseStatus.SUCCESS,
            content="Test response"
        )

        assert response.status == ResponseStatus.SUCCESS
        assert response.content == "Test response"

    def test_response_with_error(self):
        """Test error response"""
        response = A2AResponse(
            status=ResponseStatus.ERROR,
            content=None,
            error_message="Something went wrong"
        )

        assert response.status == ResponseStatus.ERROR
        assert response.error_message == "Something went wrong"


class TestA2ACapability:
    """Test A2ACapability class"""

    def test_create_capability(self):
        """Test creating agent capability"""
        capability = A2ACapability(
            agent_id="test-agent",
            name="Test Agent",
            description="A test agent",
            domains=["domain1", "domain2"],
            example_queries=["query1", "query2"],
            dependencies=["other-agent"],
            max_cascade_depth=3
        )

        assert capability.agent_id == "test-agent"
        assert capability.name == "Test Agent"
        assert len(capability.domains) == 2
        assert len(capability.dependencies) == 1

    def test_capability_to_dict(self):
        """Test capability serialization"""
        capability = A2ACapability(
            agent_id="test-agent",
            name="Test Agent",
            description="A test agent",
            domains=["domain1"]
        )

        data = capability.to_dict()

        assert data["agent_id"] == "test-agent"
        assert "domains" in data
