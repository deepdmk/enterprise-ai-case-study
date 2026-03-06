"""
FastAPI Endpoint Tests for Phase 5 Orchestrator Service

Tests /health, /route, /orchestrate, /stats endpoints in legacy mode.
"""

import pytest
from fastapi.testclient import TestClient

from src.program4_orchestrator_service.service import create_app
from src.shared.routing_schema import WorkflowType


@pytest.fixture
def legacy_app():
    """Create app in legacy test mode"""
    agent_registry = {
        "fundraising-agent": "http://localhost:8001",
        "business-development-agent": "http://localhost:8002",
        "field-operations-agent": "http://localhost:8003"
    }

    app = create_app(
        inference_server_url="http://localhost:8100",
        agent_registry=agent_registry,
        test_mode=True,
        use_agno=False,
    )
    return app


@pytest.fixture
def client(legacy_app):
    """Create test client"""
    return TestClient(legacy_app)


class TestHealthEndpoint:
    """Tests for /health endpoint"""

    def test_health_returns_200(self, client):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["mode"] == "legacy"
        assert data["test_mode"] is True

    def test_health_includes_agent_info(self, client):
        """Test health check includes agent information"""
        response = client.get("/health")
        data = response.json()
        assert "agents_total" in data
        assert "agent_health" in data


class TestRouteEndpoint:
    """Tests for /route endpoint"""

    def test_route_investor_query(self, client):
        """Test routing an investor query"""
        response = client.post(
            "/route",
            json={"query": "What is the capacity of INV-123?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["routing_decision"]["entry_agent"] == "fundraising-agent"
        assert "latency_ms" in data

    def test_route_rfp_query(self, client):
        """Test routing an RFP query"""
        response = client.post(
            "/route",
            json={"query": "What RFPs are open in education?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["routing_decision"]["entry_agent"] == "business-development-agent"

    def test_route_regional_query(self, client):
        """Test routing a regional query"""
        response = client.post(
            "/route",
            json={"query": "Assess regional capacity in Kenya"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["routing_decision"]["entry_agent"] == "field-operations-agent"


class TestOrchestrateEndpoint:
    """Tests for /orchestrate endpoint"""

    def test_orchestrate_routing_only(self, client):
        """Test orchestration with execute=False"""
        response = client.post(
            "/orchestrate",
            json={"query": "Find investor INV-123", "execute": False}
        )
        assert response.status_code == 200
        data = response.json()
        orch = data["orchestrated_response"]
        assert orch["query"] == "Find investor INV-123"
        assert orch["success"] is True

    def test_orchestrate_with_execution(self, client):
        """Test orchestration with execution (agents will fail in test mode but should not crash)"""
        response = client.post(
            "/orchestrate",
            json={"query": "Find investor INV-123", "execute": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert "orchestrated_response" in data


class TestStatsEndpoint:
    """Tests for /stats endpoint"""

    def test_stats_returns_200(self, client):
        """Test stats endpoint returns 200"""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "legacy"
        assert "routing" in data
        assert "agents" in data

    def test_stats_after_route(self, client):
        """Test stats reflect routing activity"""
        # Make a route request first
        client.post("/route", json={"query": "Test query"})

        response = client.get("/stats")
        data = response.json()
        assert data["routing"]["total_requests"] >= 1

    def test_stats_reset(self, client):
        """Test stats reset"""
        # Make a route request
        client.post("/route", json={"query": "Test query"})

        # Reset stats
        response = client.post("/stats/reset")
        assert response.status_code == 200

        # Verify reset
        response = client.get("/stats")
        data = response.json()
        assert data["routing"]["total_requests"] == 0
