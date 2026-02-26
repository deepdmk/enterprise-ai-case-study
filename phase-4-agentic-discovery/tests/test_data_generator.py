"""
Tests for A2A Training Data Generator
"""

import pytest
import json
import tempfile
from pathlib import Path

from src.program1_a2a_finetuning.data_generator import (
    A2ATrainingExample,
    A2ADataGenerator
)


class TestA2ATrainingExample:
    """Test A2ATrainingExample dataclass"""

    def test_create_example(self):
        """Test creating a training example"""
        example = A2ATrainingExample(
            category="direct_task",
            context="Test context",
            user_query="Test query",
            expected_action="respond_directly",
            expected_output="Test output"
        )

        assert example.category == "direct_task"
        assert example.depth == 0
        assert example.max_depth == 3

    def test_example_to_dict(self):
        """Test example serialization"""
        example = A2ATrainingExample(
            category="single_agent_call",
            context="Test context",
            user_query="Test query",
            expected_action="call_agent",
            expected_output="<a2a_call>...</a2a_call>",
            depth=1,
            max_depth=3
        )

        data = example.to_dict()

        assert data["category"] == "single_agent_call"
        assert data["depth"] == 1
        assert data["max_depth"] == 3

    def test_example_with_custom_depth(self):
        """Test example with custom depth settings"""
        example = A2ATrainingExample(
            category="depth_limit_handling",
            context="Test context",
            user_query="Test query",
            expected_action="respond_directly",
            expected_output="Output",
            depth=2,
            max_depth=2
        )

        assert example.depth == 2
        assert example.max_depth == 2


class TestA2ADataGenerator:
    """Test A2ADataGenerator"""

    @pytest.fixture
    def fundraising_generator(self):
        """Create fundraising unit generator"""
        return A2ADataGenerator("fundraising")

    @pytest.fixture
    def business_dev_generator(self):
        """Create business development generator"""
        return A2ADataGenerator("business_development")

    @pytest.fixture
    def field_ops_generator(self):
        """Create field operations generator"""
        return A2ADataGenerator("field_operations")

    def test_create_generator(self, fundraising_generator):
        """Test creating a data generator"""
        assert fundraising_generator.unit_name == "fundraising"
        assert "fundraising" in fundraising_generator.unit_configs

    def test_generate_dataset_distribution(self, fundraising_generator):
        """Test dataset distribution"""
        examples = fundraising_generator.generate_dataset(num_examples=100, test_mode=True)

        # Count categories
        categories = {}
        for example in examples:
            cat = example.category
            categories[cat] = categories.get(cat, 0) + 1

        # Verify approximate distribution (with some tolerance)
        assert categories.get("direct_task", 0) >= 30  # ~40%
        assert categories.get("single_agent_call", 0) >= 20  # ~30%
        assert categories.get("multi_agent_orchestration", 0) >= 5  # ~15%
        assert categories.get("depth_limit_handling", 0) >= 5  # ~10%
        assert categories.get("error_handling", 0) >= 1  # ~5%

    def test_generate_dataset_test_mode(self, fundraising_generator):
        """Test that test mode generates smaller dataset"""
        examples = fundraising_generator.generate_dataset(
            num_examples=1000,
            test_mode=True
        )

        assert len(examples) == 100

    def test_generate_direct_task_examples(self, fundraising_generator):
        """Test direct task example generation"""
        examples = fundraising_generator.generate_direct_task_examples(10)

        assert len(examples) == 10
        for example in examples:
            assert example.category == "direct_task"
            assert example.expected_action == "respond_directly"

    def test_generate_single_call_examples(self, fundraising_generator):
        """Test single call example generation"""
        examples = fundraising_generator.generate_single_call_examples(10)

        assert len(examples) > 0
        for example in examples:
            assert example.category == "single_agent_call"
            assert example.expected_action == "call_agent"
            assert "<a2a_call>" in example.expected_output

    def test_generate_multi_call_examples(self, fundraising_generator):
        """Test multi-call example generation"""
        examples = fundraising_generator.generate_multi_call_examples(10)

        # Note: may generate fewer if unit has < 2 dependencies
        for example in examples:
            assert example.category == "multi_agent_orchestration"
            assert example.expected_action == "orchestrate_calls"

    def test_generate_depth_limit_examples(self, fundraising_generator):
        """Test depth limit example generation"""
        examples = fundraising_generator.generate_depth_limit_examples(10)

        assert len(examples) == 10
        for example in examples:
            assert example.category == "depth_limit_handling"
            # Depth should be at or near max
            assert example.depth >= 2

    def test_generate_error_handling_examples(self, fundraising_generator):
        """Test error handling example generation"""
        examples = fundraising_generator.generate_error_handling_examples(10)

        assert len(examples) == 10
        for example in examples:
            assert example.category == "error_handling"
            assert example.expected_action == "handle_error"

    def test_all_unit_types(
        self,
        fundraising_generator,
        business_dev_generator,
        field_ops_generator
    ):
        """Test all unit types can generate examples"""
        for generator in [fundraising_generator, business_dev_generator, field_ops_generator]:
            examples = generator.generate_dataset(num_examples=50, test_mode=True)
            assert len(examples) > 0

    def test_random_params(self, fundraising_generator):
        """Test random parameter generation"""
        params = fundraising_generator._random_params()

        assert "investor_id" in params
        assert "sector" in params
        assert "rfp_id" in params
        assert "country" in params
        assert "region" in params

        # Check format
        assert params["investor_id"].startswith("INV-")
        assert params["rfp_id"].startswith("RFP-")

    def test_unit_configs(self, fundraising_generator):
        """Test unit configuration structure"""
        configs = fundraising_generator._get_unit_configs()

        assert "fundraising" in configs
        assert "business_development" in configs
        assert "field_operations" in configs

        for unit, config in configs.items():
            assert "name" in config
            assert "domains" in config
            assert "dependencies" in config
            assert "direct_queries" in config

    def test_save_dataset(self, fundraising_generator, temp_dir):
        """Test saving dataset to file"""
        examples = fundraising_generator.generate_dataset(
            num_examples=10,
            test_mode=True
        )

        output_path = temp_dir / "test_dataset.json"
        fundraising_generator.save_dataset(examples, str(output_path))

        assert output_path.exists()

        with open(output_path) as f:
            loaded = json.load(f)

        assert len(loaded) == len(examples)

    def test_generated_examples_have_valid_structure(self, fundraising_generator):
        """Test that all generated examples have valid structure"""
        examples = fundraising_generator.generate_dataset(
            num_examples=50,
            test_mode=True
        )

        for example in examples:
            assert example.category in [
                "direct_task",
                "single_agent_call",
                "multi_agent_orchestration",
                "depth_limit_handling",
                "error_handling"
            ]
            assert len(example.context) > 0
            assert len(example.user_query) > 0
            assert len(example.expected_action) > 0
            assert len(example.expected_output) > 0
            assert 0 <= example.depth <= example.max_depth

    def test_single_call_examples_have_valid_targets(self, fundraising_generator):
        """Test that single call examples target valid agents"""
        examples = fundraising_generator.generate_single_call_examples(20)

        valid_targets = [
            "business-development-agent",
            "field-operations-agent"
        ]

        for example in examples:
            # Parse the A2A call
            output = example.expected_output
            if "<a2a_call>" in output:
                import json
                # Extract JSON from output
                start = output.index("{")
                end = output.rindex("}") + 1
                call_data = json.loads(output[start:end])
                assert call_data["target"] in valid_targets

    def test_dataset_shuffling(self, fundraising_generator):
        """Test that dataset is shuffled"""
        # Generate two datasets and check they're in different order
        examples1 = fundraising_generator.generate_dataset(
            num_examples=100,
            test_mode=True
        )
        examples2 = fundraising_generator.generate_dataset(
            num_examples=100,
            test_mode=True
        )

        # Categories should be shuffled (not all direct_task first)
        first_10_cats_1 = [e.category for e in examples1[:10]]
        first_10_cats_2 = [e.category for e in examples2[:10]]

        # Very unlikely to have same order if shuffled
        # But don't assert equality since shuffle is random
        assert len(set(first_10_cats_1)) > 1 or len(set(first_10_cats_2)) > 1
