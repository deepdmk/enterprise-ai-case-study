"""
Tests for Agno Framework Integration

Tests the Agno-based orchestrator implementation including:
- VLLMModel provider
- RemoteAgent members
- Team coordination
- Legacy adapter
- Training logger
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any

# Import components to test
from src.program4_orchestrator_service.agno.model_provider import create_vllm_model
from src.program4_orchestrator_service.agno.members import (
    create_fundraising_member,
    create_business_dev_member,
    create_field_ops_member,
    create_all_members
)
from src.program4_orchestrator_service.agno.coordinator import (
    create_coordinator_instructions,
    create_coordinator_system_prompt,
    create_coordinator_description
)
from src.program4_orchestrator_service.agno.team import create_orchestrator_team
from src.program4_orchestrator_service.agno.legacy_adapter import LegacyAdapter
from src.program4_orchestrator_service.agno.training_logger import TrainingLogger
from src.shared.routing_schema import (
    OrchestratedResponse,
    RoutingDecision,
    AgentResponse,
    AgentType,
    WorkflowType,
    AgentCall
)
from agno.models.vllm import VLLM
from agno.models.openai.like import OpenAILike
from agno.team.mode import TeamMode


# Test Model Provider
class TestModelProvider:
    """Test built-in VLLM model provider"""

    def test_create_vllm_model_standard(self):
        """Test create_vllm_model factory function for standard VLLM"""
        model = create_vllm_model(
            inference_url="http://localhost:8100/generate",
            model_id="test-model",
            use_openai_compatible=False
        )

        assert isinstance(model, VLLM)
        assert model.id == "test-model"
        # base_url should end with /
        assert model.base_url.endswith("/")

    def test_create_vllm_model_openai_compatible(self):
        """Test create_vllm_model factory function for OpenAI-compatible endpoint"""
        model = create_vllm_model(
            inference_url="http://localhost:8100",
            model_id="test-model",
            use_openai_compatible=True
        )

        assert isinstance(model, OpenAILike)
        assert model.id == "test-model"
        # base_url should end with /v1
        assert model.base_url.endswith("/v1")

    def test_create_vllm_model_url_normalization(self):
        """Test URL normalization for different formats"""
        # Test standard VLLM URL normalization
        model1 = create_vllm_model(
            inference_url="http://localhost:8100",
            model_id="test-model"
        )
        assert model1.base_url == "http://localhost:8100/"

        model2 = create_vllm_model(
            inference_url="http://localhost:8100/",
            model_id="test-model"
        )
        assert model2.base_url == "http://localhost:8100/"

        # Test OpenAI-compatible URL normalization
        model3 = create_vllm_model(
            inference_url="http://localhost:8100",
            model_id="test-model",
            use_openai_compatible=True
        )
        assert model3.base_url.endswith("/v1")

        model4 = create_vllm_model(
            inference_url="http://localhost:8100/v1",
            model_id="test-model",
            use_openai_compatible=True
        )
        assert model4.base_url == "http://localhost:8100/v1"


# Test RemoteAgent Members
class TestRemoteAgentMembers:
    """Test RemoteAgent member creation"""

    def test_create_fundraising_member(self):
        """Test fundraising member creation"""
        member = create_fundraising_member(base_url="http://localhost:8001")

        # Agno 2.4.1 RemoteAgent only has base_url, agent_id, protocol
        assert member.base_url == "http://localhost:8001"
        assert member.agent_id == "fundraising-agent"
        assert member.protocol == "a2a"

    def test_create_business_dev_member(self):
        """Test business development member creation"""
        member = create_business_dev_member(base_url="http://localhost:8002")

        assert member.base_url == "http://localhost:8002"
        assert member.agent_id == "business-development-agent"
        assert member.protocol == "a2a"

    def test_create_field_ops_member(self):
        """Test field operations member creation"""
        member = create_field_ops_member(base_url="http://localhost:8003")

        assert member.base_url == "http://localhost:8003"
        assert member.agent_id == "field-operations-agent"
        assert member.protocol == "a2a"

    def test_create_all_members(self):
        """Test creating all members from registry"""
        agent_registry = {
            "fundraising-agent": "http://localhost:8001",
            "business-development-agent": "http://localhost:8002",
            "field-operations-agent": "http://localhost:8003"
        }

        members = create_all_members(agent_registry)

        assert len(members) == 3
        assert all(hasattr(m, 'agent_id') for m in members)
        assert all(hasattr(m, 'base_url') for m in members)
        assert all(hasattr(m, 'protocol') for m in members)


# Test Coordinator Configuration
class TestCoordinatorConfiguration:
    """Test coordinator configuration functions"""

    def test_create_coordinator_instructions(self):
        """Test coordinator instructions creation"""
        instructions = create_coordinator_instructions()

        assert isinstance(instructions, list)
        assert len(instructions) > 0
        assert any("orchestrator" in instr.lower() for instr in instructions)
        assert any("fundraising" in instr.lower() for instr in instructions)

    def test_create_coordinator_system_prompt(self):
        """Test system prompt creation"""
        prompt = create_coordinator_system_prompt()

        assert isinstance(prompt, str)
        assert "orchestrator" in prompt.lower()
        assert "fundraising-agent" in prompt
        assert "business-development-agent" in prompt
        assert "field-operations-agent" in prompt

    def test_create_coordinator_description(self):
        """Test description creation"""
        description = create_coordinator_description()

        assert isinstance(description, str)
        assert "orchestrator" in description.lower()


# Test Team Creation
class TestTeamCreation:
    """Test Agno Team creation"""

    def test_create_orchestrator_team_test_mode(self):
        """Test team creation in test mode"""
        agent_registry = {
            "fundraising-agent": "http://localhost:8001",
            "business-development-agent": "http://localhost:8002",
            "field-operations-agent": "http://localhost:8003"
        }

        team = create_orchestrator_team(
            inference_server_url="http://localhost:8100/generate",
            agent_registry=agent_registry,
            test_mode=True
        )

        assert team.name == "Phase5Orchestrator"
        assert team.mode == TeamMode.route
        assert len(team.members) == 3

    def test_create_orchestrator_team_production_mode(self):
        """Test team creation in production mode"""
        agent_registry = {
            "fundraising-agent": "http://localhost:8001"
        }

        team = create_orchestrator_team(
            inference_server_url="http://localhost:8100/generate",
            agent_registry=agent_registry,
            test_mode=False,
            model_timeout=15.0,
            model_max_tokens=256
        )

        assert team.name == "Phase5Orchestrator"
        assert team.mode == TeamMode.route
        assert len(team.members) == 1


# Test Legacy Adapter
class TestLegacyAdapter:
    """Test LegacyAdapter for backward compatibility"""

    def test_detect_workflow(self):
        """Test workflow detection"""
        mock_team = Mock()
        adapter = LegacyAdapter(mock_team)

        # Test funding opportunity detection
        workflow = adapter._detect_workflow("Evaluate this funding opportunity")
        assert workflow == WorkflowType.EVALUATE_FUNDING_OPPORTUNITY

        # Test investor capacity detection
        workflow = adapter._detect_workflow("Assess investor capacity")
        assert workflow == WorkflowType.ASSESS_INVESTOR_CAPACITY

        # Test competitive landscape detection
        workflow = adapter._detect_workflow("Analyze competitive landscape")
        assert workflow == WorkflowType.ANALYZE_COMPETITIVE_LANDSCAPE

        # Test regional project detection (avoid "evaluate" keyword which matches funding opportunity)
        workflow = adapter._detect_workflow("Assess regional project in Kenya")
        assert workflow == WorkflowType.EVALUATE_REGIONAL_PROJECT

    def test_detect_workflow_ordering(self):
        """Test that 'Evaluate regional project' matches EVALUATE_REGIONAL_PROJECT, not EVALUATE_FUNDING_OPPORTUNITY"""
        mock_team = Mock()
        adapter = LegacyAdapter(mock_team)

        # This should match EVALUATE_REGIONAL_PROJECT because "regional" is more specific
        workflow = adapter._detect_workflow("Evaluate regional project in East Africa")
        assert workflow == WorkflowType.EVALUATE_REGIONAL_PROJECT

        # "evaluate" alone should still match EVALUATE_FUNDING_OPPORTUNITY
        workflow = adapter._detect_workflow("Evaluate this opportunity")
        assert workflow == WorkflowType.EVALUATE_FUNDING_OPPORTUNITY

    def test_map_name_to_agent_type(self):
        """Test agent name to AgentType mapping"""
        mock_team = Mock()
        adapter = LegacyAdapter(mock_team)

        assert adapter._map_name_to_agent_type("Fundraising Agent") == AgentType.FUNDRAISING
        assert adapter._map_name_to_agent_type("Business Development Agent") == AgentType.BUSINESS_DEVELOPMENT
        assert adapter._map_name_to_agent_type("Field Operations Agent") == AgentType.FIELD_OPERATIONS
        assert adapter._map_name_to_agent_type("Unknown Agent") == AgentType.FIELD_OPERATIONS  # Default

    def test_extract_routing_decision(self):
        """Test routing decision extraction from Agno result"""
        mock_team = Mock()
        adapter = LegacyAdapter(mock_team)

        # Mock Agno result
        mock_result = Mock()
        mock_result.content = "Entry agent: fundraising-agent\nOptimal depth: 3\nRationale: Investor query"

        decision = adapter._extract_routing_decision("Test query", mock_result)

        assert isinstance(decision, RoutingDecision)
        assert decision.entry_agent == AgentType.FUNDRAISING
        assert decision.optimal_depth == 3
        assert "Investor query" in decision.reasoning


# Test Training Logger
class TestTrainingLogger:
    """Test TrainingLogger for data capture"""

    def test_training_logger_initialization(self, tmp_path):
        """Test logger initialization"""
        log_dir = str(tmp_path / "training_logs")
        logger = TrainingLogger(log_dir=log_dir, enabled=True)

        assert logger.enabled
        assert logger.log_dir.exists()
        # Log file is created on first write, not on initialization
        assert hasattr(logger, 'log_file')

    def test_log_orchestration(self, tmp_path):
        """Test orchestration logging"""
        log_dir = str(tmp_path / "training_logs")
        logger = TrainingLogger(log_dir=log_dir, enabled=True)

        # Create mock orchestrated response
        response = OrchestratedResponse(
            query="Test query",
            routing_decision=RoutingDecision(
                workflow=WorkflowType.UNKNOWN,
                entry_agent=AgentType.FUNDRAISING,
                optimal_depth=2,
                agent_calls=[],
                reasoning="Test reasoning",
                estimated_latency_ms=100,
                success_probability=0.9
            ),
            agent_responses=[],
            synthesized_response="Test response",
            total_latency_ms=150,
            success=True
        )

        logger.log_orchestration(response)

        # Verify log file has content
        assert logger.log_file.exists()
        with open(logger.log_file, 'r') as f:
            content = f.read()
            assert "Test query" in content
            assert "fundraising-agent" in content

    def test_get_stats(self, tmp_path):
        """Test statistics retrieval"""
        log_dir = str(tmp_path / "training_logs")
        logger = TrainingLogger(log_dir=log_dir, enabled=True)

        # Log some entries
        response = OrchestratedResponse(
            query="Test query",
            routing_decision=RoutingDecision(
                workflow=WorkflowType.UNKNOWN,
                entry_agent=AgentType.FUNDRAISING,
                optimal_depth=2,
                agent_calls=[],
                reasoning="Test",
                estimated_latency_ms=100,
                success_probability=0.9
            ),
            agent_responses=[],
            synthesized_response="Test",
            total_latency_ms=150,
            success=True
        )

        logger.log_orchestration(response)

        stats = logger.get_stats()

        assert stats["total_logs"] == 1
        assert stats["successful"] == 1
        assert stats["failed"] == 0
        assert stats["success_rate"] == 1.0

    def test_training_logger_disabled(self, tmp_path):
        """Test logger when disabled"""
        log_dir = str(tmp_path / "training_logs")
        logger = TrainingLogger(log_dir=log_dir, enabled=False)

        assert not logger.enabled

        # Logging should be no-op
        response = OrchestratedResponse(
            query="Test query",
            routing_decision=RoutingDecision(
                workflow=WorkflowType.UNKNOWN,
                entry_agent=AgentType.FUNDRAISING,
                optimal_depth=2,
                agent_calls=[],
                reasoning="Test",
                estimated_latency_ms=100,
                success_probability=0.9
            ),
            agent_responses=[],
            synthesized_response="Test",
            total_latency_ms=150,
            success=True
        )

        logger.log_orchestration(response)  # Should not raise error

    def test_training_logger_disabled_get_stats(self, tmp_path):
        """Test get_stats when logger is disabled doesn't crash (bug 1.3 fix)"""
        log_dir = str(tmp_path / "training_logs")
        logger = TrainingLogger(log_dir=log_dir, enabled=False)

        # This should not raise AttributeError
        stats = logger.get_stats()
        assert stats["total_logs"] == 0


# Integration Tests
class TestAgnoIntegration:
    """Integration tests for Agno framework"""

    @pytest.mark.asyncio
    async def test_full_orchestration_flow_mock(self, tmp_path):
        """Test full orchestration flow with mocked components"""
        # This is a high-level integration test
        # In practice, you'd mock the HTTP calls to Phase 4 agents

        agent_registry = {
            "fundraising-agent": "http://localhost:8001"
        }

        # Create team
        team = create_orchestrator_team(
            inference_server_url="http://localhost:8100/generate",
            agent_registry=agent_registry,
            test_mode=True
        )

        # Create adapter
        adapter = LegacyAdapter(team)

        # Mock team.arun to return a result (use AsyncMock for async methods)
        mock_result = Mock()
        mock_result.content = "Entry agent: fundraising-agent\nOptimal depth: 2\nInvestor found: INV-123"
        mock_result.messages = []
        mock_result.success = True

        # Use AsyncMock for async method
        with patch.object(team, 'arun', new_callable=AsyncMock, return_value=mock_result):
            response = await adapter.orchestrate("Find investor INV-123")

            assert isinstance(response, OrchestratedResponse)
            assert response.success
            assert response.query == "Find investor INV-123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
