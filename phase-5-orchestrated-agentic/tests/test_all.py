"""
Comprehensive tests for Phase 5.
"""

import pytest
from pathlib import Path
import json

# Program 1: Data Conversion
from src.program1_data_conversion.discovery_converter import DiscoveryConverter
from src.program1_data_conversion.intent_generator import IntentGenerator
from src.program1_data_conversion.data_augmenter import DataAugmenter
from src.program1_data_conversion.splitter import DataSplitter

# Program 2: SLM Fine-tuning
from src.program2_slm_finetuning.trainer import OrchestratorTrainer
from src.program2_slm_finetuning.checkpointer import Checkpointer

# Program 4: Orchestrator Service
from src.program4_orchestrator_service.routing_engine import RoutingEngine
from src.program4_orchestrator_service.response_synthesizer import ResponseSynthesizer

# Shared
from src.shared.routing_schema import (
    TrainingExample, AgentType, AgentResponse, RoutingDecision,
    WorkflowType, OrchestratedResponse
)
from src.shared.phase4_importer import Phase4Importer


class TestDataConversion:
    """Tests for Program 1: Data Conversion"""

    def test_discovery_converter_create_mock_data(self):
        """Test mock data creation"""
        converter = DiscoveryConverter()
        examples = converter.create_mock_data(count=10)

        assert len(examples) == 10
        assert all(isinstance(ex, TrainingExample) for ex in examples)
        assert all(ex.optimal_depth >= 1 and ex.optimal_depth <= 4 for ex in examples)

    def test_intent_generator(self, sample_training_examples):
        """Test intent generation"""
        generator = IntentGenerator()
        intents = generator.generate_intents(sample_training_examples, max_per_workflow=2)

        assert len(intents) > 0
        assert all(isinstance(intent, TrainingExample) for intent in intents)
        assert all(intent.metadata.get("synthetic") for intent in intents)

    def test_data_augmenter(self, sample_training_examples):
        """Test data augmentation"""
        augmenter = DataAugmenter()
        augmented = augmenter.augment_examples(
            sample_training_examples,
            augmentation_factor=2,
            test_mode=True
        )

        # Should include originals + augmented
        assert len(augmented) >= len(sample_training_examples)

    def test_data_splitter(self, sample_training_examples, temp_dir):
        """Test data splitting"""
        splitter = DataSplitter(train_ratio=0.6, val_ratio=0.2, test_ratio=0.2)
        train, val, test = splitter.split(sample_training_examples, stratify_by="agent")

        total = len(train) + len(val) + len(test)
        assert total == len(sample_training_examples)

        # Export splits
        splitter.export_splits(train, val, test, temp_dir)

        # Verify files created
        assert (temp_dir / "train.jsonl").exists()
        assert (temp_dir / "val.jsonl").exists()
        assert (temp_dir / "test.jsonl").exists()

    def test_chat_format_conversion(self, sample_training_examples):
        """Test ChatML format conversion"""
        example = sample_training_examples[0]
        chat_format = example.to_chat_format()

        assert "messages" in chat_format
        assert len(chat_format["messages"]) == 3  # system, user, assistant
        assert chat_format["messages"][0]["role"] == "system"
        assert chat_format["messages"][1]["role"] == "user"
        assert chat_format["messages"][2]["role"] == "assistant"


class TestFineTuning:
    """Tests for Program 2: SLM Fine-tuning"""

    def test_mock_adapter_creation(self, temp_dir):
        """Test mock adapter creation"""
        output_dir = temp_dir / "mock_adapter"
        OrchestratorTrainer.create_mock_adapter(output_dir)

        assert (output_dir / "adapter_config.json").exists()
        assert (output_dir / "adapter_model.bin").exists()

    def test_checkpointer(self, temp_dir):
        """Test checkpointing"""
        checkpointer = Checkpointer(temp_dir / "checkpoints", max_checkpoints=3)

        # Test metadata operations
        assert checkpointer.get_latest_checkpoint() is None

        # Create mock checkpoint metadata
        checkpointer._update_metadata("checkpoint-1", 100, {"loss": 0.5})
        checkpointer._update_metadata("checkpoint-2", 200, {"loss": 0.3})

        latest = checkpointer.get_latest_checkpoint()
        assert latest == "checkpoint-2"

        best = checkpointer.get_best_checkpoint(metric="loss", minimize=True)
        assert best == "checkpoint-2"


class TestOrchestratorService:
    """Tests for Program 4: Orchestrator Service"""

    @pytest.mark.asyncio
    async def test_routing_engine_fallback(self):
        """Test rule-based fallback routing"""
        engine = RoutingEngine(
            inference_server_url="http://localhost:8100",
            test_mode=True
        )

        # Test investor query
        decision = await engine.route("What is the capacity of INV-123?")
        assert decision.entry_agent == AgentType.FUNDRAISING

        # Test RFP query
        decision = await engine.route("What RFPs are open?")
        assert decision.entry_agent == AgentType.BUSINESS_DEVELOPMENT

        # Test regional query
        decision = await engine.route("Evaluate Kenya project")
        assert decision.entry_agent == AgentType.FIELD_OPERATIONS

    @pytest.mark.asyncio
    async def test_routing_engine_workflow_ordering(self):
        """Test that 'Evaluate regional project' matches EVALUATE_REGIONAL_PROJECT, not EVALUATE_FUNDING_OPPORTUNITY"""
        engine = RoutingEngine(
            inference_server_url="http://localhost:8100",
            test_mode=True
        )

        decision = await engine.route("Evaluate regional project in East Africa")
        assert decision.workflow == WorkflowType.EVALUATE_REGIONAL_PROJECT

    @pytest.mark.asyncio
    async def test_routing_engine_avg_latency_no_division_by_zero(self):
        """Test that routing engine handles zero requests without division by zero"""
        engine = RoutingEngine(
            inference_server_url="http://localhost:8100",
            test_mode=True
        )

        # Stats should start at zero without error
        stats = engine.get_stats()
        assert stats["avg_latency_ms"] == 0

        # After one route, stats should be valid
        await engine.route("Test query")
        stats = engine.get_stats()
        assert stats["avg_latency_ms"] >= 0

    def test_response_synthesizer(self):
        """Test response synthesis"""
        synthesizer = ResponseSynthesizer(strategy="concatenation")

        agent_responses = [
            AgentResponse(
                agent=AgentType.FIELD_OPERATIONS,
                operation="evaluate",
                success=True,
                response="Kenya evaluation complete",
                latency_ms=100,
                cascaded_calls=[]
            ),
            AgentResponse(
                agent=AgentType.FUNDRAISING,
                operation="check_capacity",
                success=True,
                response="Investor capacity confirmed",
                latency_ms=150,
                cascaded_calls=[]
            )
        ]

        # Create mock routing decision
        decision = RoutingDecision(
            workflow=WorkflowType.EVALUATE_FUNDING_OPPORTUNITY,
            entry_agent=AgentType.FIELD_OPERATIONS,
            optimal_depth=2,
            reasoning="Test routing"
        )

        synthesized = synthesizer.synthesize(
            "Test query",
            decision,
            agent_responses
        )

        assert "Kenya evaluation complete" in synthesized
        assert "Investor capacity confirmed" in synthesized

    def test_response_synthesizer_empty_responses(self):
        """Test synthesis with empty responses list"""
        synthesizer = ResponseSynthesizer(strategy="concatenation")

        decision = RoutingDecision(
            workflow=WorkflowType.UNKNOWN,
            entry_agent=AgentType.FIELD_OPERATIONS,
            optimal_depth=2,
            reasoning="Test routing"
        )

        result = synthesizer.synthesize("Test query", decision, [])
        assert "No successful agent responses" in result

    def test_response_synthesizer_hierarchical_empty(self):
        """Test hierarchical synthesis with empty responses doesn't crash on division by zero"""
        synthesizer = ResponseSynthesizer(strategy="hierarchical")

        decision = RoutingDecision(
            workflow=WorkflowType.UNKNOWN,
            entry_agent=AgentType.FIELD_OPERATIONS,
            optimal_depth=2,
            reasoning="Test routing"
        )

        # Empty list should not cause division by zero
        result = synthesizer.synthesize("Test query", decision, [])
        assert "Success rate: 0%" in result

    def test_orchestrated_response_none_routing_decision(self):
        """Test OrchestratedResponse accepts None routing_decision (bug 1.1 fix)"""
        response = OrchestratedResponse(
            query="Test query",
            routing_decision=None,
            agent_responses=[],
            synthesized_response="Error occurred",
            total_latency_ms=100,
            success=False
        )
        assert response.routing_decision is None
        assert not response.success

    def test_response_summary(self):
        """Test response summary generation"""
        synthesizer = ResponseSynthesizer()

        agent_responses = [
            AgentResponse(
                agent=AgentType.FIELD_OPERATIONS,
                operation="test",
                success=True,
                response="Response 1",
                latency_ms=100,
                cascaded_calls=["fundraising-agent"]
            ),
            AgentResponse(
                agent=AgentType.FUNDRAISING,
                operation="test",
                success=False,
                response="Error",
                latency_ms=50,
                cascaded_calls=[]
            )
        ]

        summary = synthesizer.summarize_responses(agent_responses)

        assert summary["total"] == 2
        assert summary["successful"] == 1
        assert summary["failed"] == 1
        assert summary["success_rate"] == 0.5
        assert summary["total_latency_ms"] == 150
        assert "fundraising-agent" in summary["cascaded_agents"]


class TestSharedUtilities:
    """Tests for shared utilities"""

    def test_phase4_importer_auto_detect(self):
        """Test Phase 4 path auto-detection"""
        importer = Phase4Importer()
        # Just test initialization
        assert importer.exports_dir is not None

    def test_training_example_validation(self):
        """Test TrainingExample validation"""
        example = TrainingExample(
            query="Test query",
            entry_agent=AgentType.FIELD_OPERATIONS,
            optimal_depth=2,
            call_sequence=[],
            final_response="Test response",
            metadata={}
        )

        # Test model dump
        data = example.model_dump()
        assert data["query"] == "Test query"
        assert data["optimal_depth"] == 2

        # Test validation
        with pytest.raises(Exception):
            TrainingExample(
                query="Test",
                entry_agent=AgentType.FIELD_OPERATIONS,
                optimal_depth=10,  # Invalid depth
                call_sequence=[],
                final_response="Test",
                metadata={}
            )


@pytest.mark.integration
class TestIntegration:
    """Integration tests"""

    def test_full_pipeline_mock(self, temp_dir, test_settings):
        """Test full pipeline with mock data"""
        # Step 1: Generate mock data
        converter = DiscoveryConverter()
        examples = converter.create_mock_data(count=50)

        # Step 2: Augment
        augmenter = DataAugmenter()
        augmented = augmenter.augment_examples(examples, augmentation_factor=1, test_mode=True)

        # Step 3: Split
        splitter = DataSplitter()
        train, val, test = splitter.split(augmented)

        # Step 4: Export
        output_dir = temp_dir / "training"
        splitter.export_splits(train, val, test, output_dir)

        # Verify all files exist
        assert (output_dir / "train.jsonl").exists()
        assert (output_dir / "val.jsonl").exists()
        assert (output_dir / "test.jsonl").exists()
        assert (output_dir / "train_chat.jsonl").exists()

        # Verify content
        with open(output_dir / "train_chat.jsonl") as f:
            line = f.readline()
            data = json.loads(line)
            assert "messages" in data
            assert len(data["messages"]) == 3
