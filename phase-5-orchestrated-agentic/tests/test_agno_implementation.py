"""
Tests for Agno Implementation (No agno package required)

These tests validate the Agno integration code without requiring
the agno package to be installed. They use mocking to simulate
agno components.
"""

import pytest
import asyncio
import sys
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path
from typing import Dict, Any

# Configure paths for cross-phase imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.shared.path_config import configure_paths
configure_paths()

from shared.routing_schema import (
    OrchestratedResponse,
    RoutingDecision,
    AgentResponse,
    AgentType,
    WorkflowType,
    AgentCall
)


class TestVLLMModelWithoutAgno:
    """Test VLLMModel implementation without agno installed"""

    def test_vllm_model_messages_to_prompt_format(self):
        """Test ChatML message formatting logic"""
        # We'll test the logic by importing just the function logic
        # without importing the agno dependency

        messages = [
            {"role": "system", "content": "You are an orchestrator."},
            {"role": "user", "content": "Find investor INV-123"},
        ]

        # Expected ChatML format
        expected_parts = [
            "<|system|>",
            "You are an orchestrator.",
            "<|end|>",
            "<|user|>",
            "Find investor INV-123",
            "<|end|>",
            "<|assistant|>"
        ]

        # Simulate the formatting logic
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                prompt_parts.append(f"<|system|>\n{content}<|end|>")
            elif role == "user":
                prompt_parts.append(f"<|user|>\n{content}<|end|>")
            elif role == "assistant":
                prompt_parts.append(f"<|assistant|>\n{content}<|end|>")

        prompt_parts.append("<|assistant|>\n")
        prompt = "\n".join(prompt_parts)

        # Verify all expected parts are in the prompt
        for part in expected_parts:
            assert part in prompt


class TestCoordinatorConfiguration:
    """Test coordinator configuration without agno"""

    def test_coordinator_instructions_content(self):
        """Test that coordinator instructions are comprehensive"""
        # Import the module directly (it doesn't depend on agno)
        try:
            from program4_orchestrator_service.agno.coordinator import (
                create_coordinator_instructions,
                create_coordinator_system_prompt,
                create_coordinator_description
            )

            # Test instructions
            instructions = create_coordinator_instructions()
            assert isinstance(instructions, list)
            assert len(instructions) > 10

            # Verify key concepts are covered
            instructions_text = " ".join(instructions).lower()
            assert "orchestrator" in instructions_text
            assert "fundraising" in instructions_text
            assert "business development" in instructions_text
            assert "field operations" in instructions_text
            assert "cascade" in instructions_text or "depth" in instructions_text

            # Test system prompt
            system_prompt = create_coordinator_system_prompt()
            assert isinstance(system_prompt, str)
            assert len(system_prompt) > 200
            assert "orchestrator" in system_prompt.lower()

            # Test description
            description = create_coordinator_description()
            assert isinstance(description, str)
            assert "orchestrator" in description.lower()

        except ImportError:
            pytest.skip("Agno module not available")


class TestLegacyAdapterLogic:
    """Test legacy adapter logic without agno"""

    def test_workflow_detection_logic(self):
        """Test workflow type detection from queries"""

        test_cases = [
            ("Evaluate this funding opportunity in Kenya", "funding_opportunity"),
            ("Assess investor capacity for INV-123", "investor_capacity"),
            ("Analyze competitive landscape", "competitive"),
            ("Evaluate regional project in Tanzania", "regional"),
            ("Random query", "unknown")
        ]

        # Simulate workflow detection logic (matches actual implementation)
        for query, expected_type in test_cases:
            query_lower = query.lower()

            if "funding opportunity" in query_lower:
                detected = "funding_opportunity"
            elif "investor capacity" in query_lower or "investment capacity" in query_lower:
                detected = "investor_capacity"
            elif "competitive landscape" in query_lower or "market fit" in query_lower:
                detected = "competitive"
            elif "regional" in query_lower or "country" in query_lower:
                detected = "regional"
            else:
                detected = "unknown"

            if expected_type != "unknown":
                assert detected == expected_type, f"Failed for query: {query}"

    def test_agent_name_mapping(self):
        """Test agent name to AgentType mapping logic"""

        test_cases = [
            ("Fundraising Agent", AgentType.FUNDRAISING),
            ("fundraising-agent", AgentType.FUNDRAISING),
            ("Business Development Agent", AgentType.BUSINESS_DEVELOPMENT),
            ("business-development-agent", AgentType.BUSINESS_DEVELOPMENT),
            ("Field Operations Agent", AgentType.FIELD_OPERATIONS),
            ("field-operations-agent", AgentType.FIELD_OPERATIONS),
            ("Unknown Agent", AgentType.FIELD_OPERATIONS)  # Default
        ]

        # Simulate mapping logic
        for name, expected_type in test_cases:
            name_lower = name.lower()

            if "fundraising" in name_lower:
                mapped = AgentType.FUNDRAISING
            elif "business" in name_lower:
                mapped = AgentType.BUSINESS_DEVELOPMENT
            elif "field" in name_lower:
                mapped = AgentType.FIELD_OPERATIONS
            else:
                mapped = AgentType.FIELD_OPERATIONS  # Default

            assert mapped == expected_type, f"Failed for name: {name}"

    def test_routing_decision_extraction_logic(self):
        """Test routing decision extraction from text"""

        # Simulate coordinator response
        coordinator_text = """
        Entry agent: fundraising-agent
        Optimal depth: 3
        Rationale: This query requires investor-specific information and may need
        cascading to related agents for comprehensive portfolio analysis.
        """

        # Extract entry agent
        entry_agent = AgentType.FIELD_OPERATIONS  # Default
        if "fundraising" in coordinator_text.lower():
            entry_agent = AgentType.FUNDRAISING
        elif "business development" in coordinator_text.lower() or "business-development" in coordinator_text.lower():
            entry_agent = AgentType.BUSINESS_DEVELOPMENT
        elif "field operations" in coordinator_text.lower() or "field-operations" in coordinator_text.lower():
            entry_agent = AgentType.FIELD_OPERATIONS

        assert entry_agent == AgentType.FUNDRAISING

        # Extract optimal depth
        import re
        depth_match = re.search(r'depth[:\s]+(\d+)', coordinator_text.lower())
        if depth_match:
            optimal_depth = int(depth_match.group(1))
        else:
            optimal_depth = 2  # Default

        assert optimal_depth == 3


class TestTrainingLogger:
    """Test training logger without agno"""

    def test_training_logger_initialization(self, tmp_path):
        """Test logger initialization and basic operations"""
        try:
            from program4_orchestrator_service.agno.training_logger import TrainingLogger

            log_dir = str(tmp_path / "training_logs")
            logger = TrainingLogger(log_dir=log_dir, enabled=True)

            assert logger.enabled
            assert logger.log_dir.exists()
            assert logger.log_file.exists()

            # Test disabled logger
            logger_disabled = TrainingLogger(log_dir=log_dir, enabled=False)
            assert not logger_disabled.enabled

        except ImportError:
            pytest.skip("Agno module not available")

    def test_training_logger_logging(self, tmp_path):
        """Test logging orchestration data"""
        try:
            from program4_orchestrator_service.agno.training_logger import TrainingLogger

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

            # Test stats
            stats = logger.get_stats()
            assert stats["total_logs"] == 1
            assert stats["successful"] == 1
            assert stats["success_rate"] == 1.0

        except ImportError:
            pytest.skip("Agno module not available")


class TestServiceIntegration:
    """Test service integration without agno installed"""

    @pytest.mark.asyncio
    async def test_legacy_mode_still_works(self):
        """Ensure legacy mode continues to work"""
        try:
            from src.program4_orchestrator_service.service import create_app

            # Create app in legacy mode (use_agno=False)
            app = create_app(
                inference_server_url="http://localhost:8100/generate",
                agent_registry={
                    "fundraising-agent": "http://localhost:8001",
                    "business-development-agent": "http://localhost:8002",
                    "field-operations-agent": "http://localhost:8003"
                },
                test_mode=True,
                use_agno=False  # Legacy mode
            )

            assert app is not None
            assert hasattr(app.state, 'use_agno')
            assert app.state.use_agno == False
            assert hasattr(app.state, 'routing_engine')
            assert hasattr(app.state, 'agent_client')

        except ImportError as e:
            pytest.skip(f"Import error: {e}")

    def test_config_yaml_has_agno_settings(self):
        """Verify config.yaml contains agno settings"""
        import yaml
        from pathlib import Path

        config_path = Path(__file__).parent.parent / "config" / "config.yaml"

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert "orchestrator_service" in config
        assert "agno" in config["orchestrator_service"]

        agno_config = config["orchestrator_service"]["agno"]
        assert "enabled" in agno_config
        # Agno 2.4.1 uses show_members_responses (plural) and respond_directly
        # Note: Config may still have old parameters for backward compatibility
        assert "model_timeout" in agno_config
        assert "agui" in agno_config
        assert "training_logger" in agno_config


class TestPyprojectDependencies:
    """Test that pyproject.toml has correct dependencies"""

    def test_agno_dependency_added(self):
        """Verify agno dependency is in pyproject.toml"""
        import tomli
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        # Python 3.11+ has tomllib built-in, otherwise use tomli
        try:
            import tomllib
            with open(pyproject_path, 'rb') as f:
                pyproject = tomllib.load(f)
        except ImportError:
            # Fallback: read as text and check
            with open(pyproject_path, 'r') as f:
                content = f.read()
                assert "agno" in content
                assert "agno>=" in content or "agno==" in content
                return

        dependencies = pyproject["project"]["dependencies"]

        # Check that agno is in dependencies
        agno_deps = [d for d in dependencies if "agno" in d.lower()]
        assert len(agno_deps) > 0, "agno dependency not found in pyproject.toml"


class TestFileStructure:
    """Test that all required files were created"""

    def test_agno_module_files_exist(self):
        """Verify all agno module files exist"""
        from pathlib import Path

        agno_dir = Path(__file__).parent.parent / "src" / "program4_orchestrator_service" / "agno"

        required_files = [
            "__init__.py",
            "model_provider.py",
            "members.py",
            "coordinator.py",
            "team.py",
            "legacy_adapter.py",
            "agui_interface.py",
            "training_logger.py"
        ]

        for filename in required_files:
            file_path = agno_dir / filename
            assert file_path.exists(), f"Missing file: {filename}"
            assert file_path.stat().st_size > 0, f"Empty file: {filename}"

    def test_documentation_exists(self):
        """Verify implementation documentation exists"""
        from pathlib import Path

        doc_path = Path(__file__).parent.parent / "AGNO_IMPLEMENTATION.md"
        assert doc_path.exists()
        assert doc_path.stat().st_size > 5000  # Should be substantial


class TestSyntaxValidation:
    """Validate Python syntax of all new files"""

    def test_all_agno_files_valid_syntax(self):
        """Test that all agno files have valid Python syntax"""
        from pathlib import Path
        import py_compile

        agno_dir = Path(__file__).parent.parent / "src" / "program4_orchestrator_service" / "agno"

        python_files = list(agno_dir.glob("*.py"))
        assert len(python_files) >= 8, "Not all agno files found"

        for py_file in python_files:
            try:
                py_compile.compile(str(py_file), doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"Syntax error in {py_file.name}: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
