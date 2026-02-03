"""
Tests for Discovery Backend
"""

import pytest
from pathlib import Path

from src.shared.discovery_backend import InMemoryDiscoveryBackend
from src.shared.a2a_protocol import A2ACapability


class TestInMemoryDiscoveryBackend:
    """Test in-memory discovery backend"""

    @pytest.fixture
    def backend(self):
        """Create backend instance"""
        return InMemoryDiscoveryBackend()

    @pytest.fixture
    def test_capability(self):
        """Create test capability"""
        return A2ACapability(
            agent_id="test-agent",
            name="Test Agent",
            description="A test agent for testing",
            domains=["testing", "examples"],
            example_queries=["test query 1", "test query 2"]
        )

    def test_register_agent(self, backend, test_capability):
        """Test registering an agent"""
        backend.register_agent(test_capability)

        retrieved = backend.get_agent("test-agent")
        assert retrieved is not None
        assert retrieved.agent_id == "test-agent"

    def test_list_agents(self, backend, test_capability):
        """Test listing agents"""
        backend.register_agent(test_capability)

        agents = backend.list_agents()
        assert len(agents) == 1
        assert agents[0].agent_id == "test-agent"

    def test_discover_agents(self, backend, test_capability):
        """Test agent discovery"""
        backend.register_agent(test_capability)

        # Search for agent
        results = backend.discover_agents("test query", top_k=1)

        assert len(results) > 0
        capability, score = results[0]
        assert capability.agent_id == "test-agent"
        assert score > 0

    def test_discover_no_match(self, backend, test_capability):
        """Test discovery with no match"""
        backend.register_agent(test_capability)

        # Search for something completely unrelated
        results = backend.discover_agents("completely unrelated xyz", min_score=0.5)

        # Should return empty or low-scored results
        assert len(results) == 0 or results[0][1] < 0.5

    def test_get_nonexistent_agent(self, backend):
        """Test getting non-existent agent"""
        result = backend.get_agent("nonexistent")
        assert result is None

    def test_multiple_agents(self, backend):
        """Test registering multiple agents"""
        cap1 = A2ACapability(
            agent_id="agent-1",
            name="Agent 1",
            description="First agent",
            domains=["domain1"]
        )

        cap2 = A2ACapability(
            agent_id="agent-2",
            name="Agent 2",
            description="Second agent",
            domains=["domain2"]
        )

        backend.register_agent(cap1)
        backend.register_agent(cap2)

        agents = backend.list_agents()
        assert len(agents) == 2
