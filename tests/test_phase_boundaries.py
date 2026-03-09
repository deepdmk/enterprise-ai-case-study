"""Cross-phase integration tests.

Validates data contracts at phase boundaries:
- Phase 2 → Phase 3: Task SLM adapter exports
- Phase 3 → Phase 4: MoE agent config exports
- Phase 4 → Phase 5: Discovery data exports

These tests use mock/test data to validate schema compliance
without requiring actual ML models or GPU resources.
"""

import json
import sys
from pathlib import Path

import pytest

# Add Phase 0 to path for schema imports
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "phase-0-infrastructure"))


class TestPhase0Conventions:
    """Test Phase 0 shared conventions and utilities."""

    def test_agent_name_mapping_roundtrip(self):
        """Test unit_to_agent_id and agent_id_to_unit are inverses."""
        from config.conventions import agent_id_to_unit, unit_to_agent_id, UNIT_IDS, AGENT_IDS

        for unit_id in UNIT_IDS:
            agent_id = unit_to_agent_id(unit_id)
            assert agent_id in AGENT_IDS
            assert agent_id_to_unit(agent_id) == unit_id

    def test_agent_name_mapping_known_values(self):
        """Test specific mappings are correct."""
        from config.conventions import agent_id_to_unit, unit_to_agent_id

        assert unit_to_agent_id("fundraising") == "fundraising-agent"
        assert unit_to_agent_id("business_development") == "business-development-agent"
        assert unit_to_agent_id("field_operations") == "field-operations-agent"

        assert agent_id_to_unit("fundraising-agent") == "fundraising"
        assert agent_id_to_unit("business-development-agent") == "business_development"
        assert agent_id_to_unit("field-operations-agent") == "field_operations"

    def test_invalid_agent_name_raises(self):
        """Test that invalid names raise ValueError."""
        from config.conventions import agent_id_to_unit, unit_to_agent_id

        with pytest.raises(ValueError):
            unit_to_agent_id("invalid_unit")

        with pytest.raises(ValueError):
            agent_id_to_unit("invalid-agent")

    def test_agent_ports(self):
        """Test agent port assignments."""
        from config.conventions import AGENT_PORTS, get_agent_url

        assert AGENT_PORTS["fundraising-agent"] == 8001
        assert AGENT_PORTS["business-development-agent"] == 8002
        assert AGENT_PORTS["field-operations-agent"] == 8003

        assert get_agent_url("fundraising-agent") == "http://localhost:8001"


class TestPhaseBoundarySchemas:
    """Test Pydantic schemas for phase boundary data validation."""

    def test_phase4_training_example_valid(self):
        """Test valid Phase 4 training example passes validation."""
        from config.phase_boundary_schemas import Phase4TrainingExample

        example = Phase4TrainingExample(
            query="What is the investment capacity?",
            entry_agent="fundraising-agent",
            optimal_depth=2,
            call_sequence=[{"depth": 0, "target": "fundraising-agent", "goal": "query"}],
            final_response="The investment capacity is...",
            metadata={"success": True},
        )
        assert example.query == "What is the investment capacity?"
        assert example.entry_agent == "fundraising-agent"

    def test_phase4_training_example_invalid_agent(self):
        """Test invalid agent name is rejected."""
        from config.phase_boundary_schemas import Phase4TrainingExample

        with pytest.raises(Exception):
            Phase4TrainingExample(
                query="test",
                entry_agent="invalid-agent",
                optimal_depth=2,
            )

    def test_phase4_training_example_invalid_depth(self):
        """Test invalid depth is rejected."""
        from config.phase_boundary_schemas import Phase4TrainingExample

        with pytest.raises(Exception):
            Phase4TrainingExample(
                query="test",
                entry_agent="fundraising-agent",
                optimal_depth=5,  # Max is 4
            )

    def test_validate_phase4_training_examples(self):
        """Test batch validation of Phase 4 training examples."""
        from config.phase_boundary_schemas import validate_phase4_training_examples

        examples = [
            {
                "query": "Valid query 1",
                "entry_agent": "fundraising-agent",
                "optimal_depth": 2,
            },
            {
                "query": "Valid query 2",
                "entry_agent": "business-development-agent",
                "optimal_depth": 3,
            },
            {
                "query": "Invalid query",
                "entry_agent": "nonexistent-agent",
                "optimal_depth": 2,
            },
            {
                "query": "",  # Empty query
                "entry_agent": "fundraising-agent",
                "optimal_depth": 2,
            },
        ]

        validated, result = validate_phase4_training_examples(examples)

        # First two should pass, last two should fail
        assert result.records_validated >= 2
        assert result.records_skipped >= 1
        assert len(result.errors) >= 1

    def test_phase3_agent_export_schema(self):
        """Test Phase 3 agent export config schema."""
        from config.phase_boundary_schemas import Phase3AgentExport, ExpertInfo

        export = Phase3AgentExport(
            agent={"id": "fundraising_agent", "name": "Fundraising Agent", "description": "test"},
            model={
                "type": "moe",
                "architecture": "mixtral",
                "path": "./model",
                "num_experts": 5,
                "experts_per_token": 2,
                "experts": [
                    ExpertInfo(expert_id=0, task_id="investor_profiling", positive_prompts=["test"]),
                ],
            },
            routing={
                "method": "semantic",
                "gate_mode": "hidden",
                "embedding_model": "BAAI/bge-base-en-v1.5",
            },
            tasks=["investor_profiling"],
        )
        assert export.agent["id"] == "fundraising_agent"
        assert export.model.num_experts == 5

    def test_phase4_export_summary_schema(self):
        """Test Phase 4 export summary schema."""
        from config.phase_boundary_schemas import Phase4ExportSummary

        summary = Phase4ExportSummary(
            optimal_depths={"workflow_1": 2, "workflow_2": 3},
            workflows={"workflow_1": {"total_calls": 100, "success_rate": 0.95}},
        )
        assert summary.optimal_depths["workflow_1"] == 2


class TestPhase3ToPhase4Boundary:
    """Test Phase 3 → Phase 4 data contract."""

    def test_phase3_test_exports_exist(self):
        """Verify Phase 3 test export structure."""
        exports_dir = REPO_ROOT / "phase-3-moe-experts" / "data" / "exports" / "phase4_test"

        if not exports_dir.exists():
            pytest.skip("Phase 3 test exports not generated yet")

        # Check expected unit directories
        for unit in ["fundraising", "business_development", "field_operations"]:
            unit_dir = exports_dir / unit
            if unit_dir.exists():
                agent_config = unit_dir / "agent_config"
                assert agent_config.exists(), f"Missing agent_config dir for {unit}"

    def test_phase3_agent_config_schema(self):
        """Validate Phase 3 agent configs against schema."""
        import yaml
        from config.phase_boundary_schemas import Phase3AgentExport

        exports_dir = REPO_ROOT / "phase-3-moe-experts" / "data" / "exports" / "phase4_test"

        if not exports_dir.exists():
            pytest.skip("Phase 3 test exports not generated yet")

        config_files = list(exports_dir.rglob("*_agent.yaml"))
        if not config_files:
            pytest.skip("No agent config files found")

        for config_file in config_files:
            with open(config_file) as f:
                data = yaml.safe_load(f)

            # Should parse without errors
            export = Phase3AgentExport(**data)
            assert export.agent["id"]
            assert export.model.type == "moe"


class TestRetryUtility:
    """Test the shared retry utility."""

    def test_sync_retry_succeeds_eventually(self):
        """Test that retry eventually succeeds."""
        from config.retry import with_retry

        call_count = 0

        @with_retry(max_attempts=3, base_delay=0.01, jitter=False)
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Transient error")
            return "success"

        result = flaky_function()
        assert result == "success"
        assert call_count == 3

    def test_sync_retry_exhausted(self):
        """Test that retry raises after exhausting attempts."""
        from config.retry import with_retry

        @with_retry(max_attempts=2, base_delay=0.01, jitter=False)
        def always_fails():
            raise ConnectionError("Permanent error")

        with pytest.raises(ConnectionError):
            always_fails()

    def test_sync_retry_non_retryable(self):
        """Test that non-retryable exceptions are not retried."""
        from config.retry import with_retry

        call_count = 0

        @with_retry(max_attempts=3, base_delay=0.01)
        def raises_value_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("Not retryable")

        with pytest.raises(ValueError):
            raises_value_error()

        assert call_count == 1  # Should not have retried
