"""Tests for Program 6: Staff Interface functionality."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import Settings
from src.program6_interface.feedback import InterfaceFeedbackCollector, InterfaceFeedbackEntry
from src.program6_interface.mock_inference import (
    ExpertActivation,
    MockInferenceResult,
    MockMoEInference,
)


class TestMockMoEInference:
    """Tests for MockMoEInference class."""

    def test_init_empty_exports_dir(self, tmp_path):
        """Test initialization with empty exports directory."""
        exports_dir = tmp_path / "exports"
        exports_dir.mkdir()

        inference = MockMoEInference(exports_dir)

        assert inference.exports_dir == exports_dir
        assert len(inference.get_available_units()) == 0

    def test_init_with_registries(self, tmp_path):
        """Test initialization loads expert registries."""
        exports_dir = tmp_path / "exports"

        # Create mock registry for fundraising
        fundraising_dir = exports_dir / "fundraising" / "routing"
        fundraising_dir.mkdir(parents=True)
        registry = {
            "unit_id": "fundraising",
            "total_experts": 2,
            "experts": {
                "0": {"expert_id": 0, "task_id": "investor_profiling", "model_id": "fund_inv_v1"},
                "1": {"expert_id": 1, "task_id": "funding_opportunity", "model_id": "fund_opp_v1"},
            },
        }
        with open(fundraising_dir / "expert_registry.json", "w") as f:
            json.dump(registry, f)

        inference = MockMoEInference(exports_dir)

        assert "fundraising" in inference.get_available_units()
        assert "fundraising" in inference.expert_registries

    def test_generate_unknown_unit(self, tmp_path):
        """Test generation with unknown unit returns error."""
        exports_dir = tmp_path / "exports"
        exports_dir.mkdir()

        inference = MockMoEInference(exports_dir)
        result = inference.generate("unknown_unit", "test prompt")

        assert "Error" in result.response
        assert "not found" in result.response

    def test_generate_with_valid_unit(self, tmp_path):
        """Test generation returns canned response."""
        exports_dir = tmp_path / "exports"

        # Create mock registry
        unit_dir = exports_dir / "fundraising" / "routing"
        unit_dir.mkdir(parents=True)
        registry = {
            "unit_id": "fundraising",
            "total_experts": 2,
            "experts": {
                "0": {"expert_id": 0, "task_id": "investor_profiling", "model_id": "fund_inv_v1"},
                "1": {"expert_id": 1, "task_id": "funding_opportunity", "model_id": "fund_opp_v1"},
            },
        }
        with open(unit_dir / "expert_registry.json", "w") as f:
            json.dump(registry, f)

        inference = MockMoEInference(exports_dir)
        result = inference.generate("fundraising", "Profile this investor")

        assert isinstance(result, MockInferenceResult)
        assert len(result.response) > 0
        assert result.tokens_generated > 0
        assert len(result.activations) > 0

    def test_generate_keyword_matching(self, tmp_path):
        """Test that keyword matching selects appropriate responses."""
        exports_dir = tmp_path / "exports"

        unit_dir = exports_dir / "fundraising" / "routing"
        unit_dir.mkdir(parents=True)
        registry = {
            "unit_id": "fundraising",
            "total_experts": 1,
            "experts": {"0": {"expert_id": 0, "task_id": "test", "model_id": "test_v1"}},
        }
        with open(unit_dir / "expert_registry.json", "w") as f:
            json.dump(registry, f)

        inference = MockMoEInference(exports_dir)

        # Test investor keyword
        result = inference.generate("fundraising", "investor profile analysis")
        assert "investor" in result.response.lower() or "foundation" in result.response.lower()

        # Test funding keyword
        result = inference.generate("fundraising", "analyze funding opportunities")
        assert "funding" in result.response.lower() or "opportunity" in result.response.lower()


class TestExpertActivation:
    """Tests for ExpertActivation dataclass."""

    def test_creation(self):
        """Test ExpertActivation creation."""
        activation = ExpertActivation(
            expert_id=0,
            task_id="investor_profiling",
            model_id="fund_inv_v1",
            activation_score=0.85,
        )

        assert activation.expert_id == 0
        assert activation.task_id == "investor_profiling"
        assert activation.model_id == "fund_inv_v1"
        assert activation.activation_score == 0.85


class TestMockInferenceResult:
    """Tests for MockInferenceResult dataclass."""

    def test_defaults(self):
        """Test MockInferenceResult defaults."""
        result = MockInferenceResult(response="test response")

        assert result.response == "test response"
        assert result.activations == []
        assert result.tokens_generated == 0


class TestInterfaceFeedbackCollector:
    """Tests for InterfaceFeedbackCollector class."""

    def test_init(self, tmp_path):
        """Test FeedbackCollector initialization."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback")

        assert collector.feedback_dir.exists()
        assert not collector.test_mode

    def test_init_test_mode(self, tmp_path):
        """Test FeedbackCollector initialization in test mode."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback", test_mode=True)

        assert collector.test_mode

    def test_create_session(self, tmp_path):
        """Test session creation."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback")
        session_id = collector.create_session()

        assert session_id is not None
        assert len(session_id) == 36  # UUID format

    def test_record_interaction(self, tmp_path):
        """Test interaction recording."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback")
        session_id = collector.create_session()

        feedback_id = collector.record_interaction(
            session_id=session_id,
            unit_id="fundraising",
            prompt="Test prompt",
            response="Test response",
            activated_experts=[{"expert_id": 0, "score": 0.9}],
            generation_params={"temperature": 0.7},
        )

        assert feedback_id is not None
        assert feedback_id in collector._active_interactions

    def test_submit_feedback(self, tmp_path):
        """Test feedback submission."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback", test_mode=True)
        session_id = collector.create_session()

        feedback_id = collector.record_interaction(
            session_id=session_id,
            unit_id="fundraising",
            prompt="Test prompt",
            response="Test response",
            activated_experts=[],
            generation_params={},
        )

        collector.submit_feedback(
            feedback_id=feedback_id,
            thumbs_up=True,
            rating=5,
            comment="Great response!",
        )

        # Verify feedback was written
        assert feedback_id not in collector._active_interactions
        assert any((tmp_path / "feedback").glob("test_interface_feedback_*.jsonl"))

    def test_submit_feedback_not_found(self, tmp_path):
        """Test feedback submission with invalid ID."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback")

        # Should not raise, just log warning
        collector.submit_feedback(
            feedback_id="nonexistent-id",
            thumbs_up=True,
        )

    def test_get_stats_empty(self, tmp_path):
        """Test stats with no feedback."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback")
        stats = collector.get_stats()

        assert stats["total_feedback"] == 0
        assert stats["positive"] == 0
        assert stats["negative"] == 0
        assert stats["by_unit"] == {}

    def test_get_stats_with_data(self, tmp_path):
        """Test stats with feedback data."""
        collector = InterfaceFeedbackCollector(tmp_path / "feedback", test_mode=True)
        session_id = collector.create_session()

        # Submit multiple feedback entries
        for i, (unit, thumbs) in enumerate([
            ("fundraising", True),
            ("fundraising", True),
            ("business_development", False),
            ("field_operations", None),
        ]):
            feedback_id = collector.record_interaction(
                session_id=session_id,
                unit_id=unit,
                prompt=f"Prompt {i}",
                response=f"Response {i}",
                activated_experts=[],
                generation_params={},
            )
            collector.submit_feedback(feedback_id=feedback_id, thumbs_up=thumbs)

        stats = collector.get_stats()

        assert stats["total_feedback"] == 4
        assert stats["positive"] == 2
        assert stats["negative"] == 1
        assert stats["neutral"] == 1
        assert stats["by_unit"]["fundraising"] == 2
        assert stats["by_unit"]["business_development"] == 1


class TestInterfaceFeedbackEntry:
    """Tests for InterfaceFeedbackEntry dataclass."""

    def test_to_dict(self):
        """Test serialization to dict."""
        entry = InterfaceFeedbackEntry(
            feedback_id="test-id",
            session_id="session-id",
            timestamp="2024-01-15T10:00:00",
            unit_id="fundraising",
            prompt="Test prompt",
            response="Test response",
            activated_experts=[{"expert_id": 0}],
            generation_params={"temperature": 0.7},
            thumbs_up=True,
            rating=5,
            comment="Great!",
        )

        data = entry.to_dict()

        assert data["feedback_id"] == "test-id"
        assert data["unit_id"] == "fundraising"
        assert data["thumbs_up"] is True
        assert data["rating"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
