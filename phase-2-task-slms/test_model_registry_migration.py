#!/usr/bin/env python3
"""Test script to verify Phase 0 model registry integration.

This script validates that the compatibility shim in src/shared/model_registry.py
correctly wraps the Phase 0 ModelRegistry while maintaining backward compatibility
with the Phase 2 API.
"""

import sys
import tempfile
from pathlib import Path

# Add project root to path for config resolution
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import model_registry directly using importlib to avoid shared/__init__.py heavy imports
import importlib.util
spec = importlib.util.spec_from_file_location(
    "model_registry",
    project_root / "src" / "shared" / "model_registry.py"
)
model_registry_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_registry_module)

ModelRegistry = model_registry_module.ModelRegistry
ModelEntry = model_registry_module.ModelEntry
ModelMetrics = model_registry_module.ModelMetrics
TrainingConfig = model_registry_module.TrainingConfig


def test_basic_operations():
    """Test basic registry operations."""
    print("Testing basic operations...")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize registry
        registry = ModelRegistry(tmpdir)
        assert hasattr(registry, '_registry'), "Should have _registry attribute"
        print("  ✓ Registry initialized with Phase 0 backend")

        # Create training config
        training_config = TrainingConfig(
            epochs=3,
            batch_size=4,
            learning_rate=3e-4,
            lora_r=16,
            lora_alpha=16,
            base_model="test-model",
            train_samples=100,
            val_samples=20
        )

        # Register a model
        entry = registry.register(
            unit_id="fundraising",
            task_id="portfolio_analysis",
            adapter_path="/tmp/adapter",
            base_model="test-model",
            training_config=training_config,
            positive_prompts=["analyze portfolio"],
            negative_prompts=["unrelated query"]
        )

        assert entry.model_id == "fundraising/portfolio_analysis_v1"
        assert entry.unit_id == "fundraising"
        assert entry.task_id == "portfolio_analysis"
        assert entry.version == "v1"
        assert entry.status == "trained"
        print(f"  ✓ Model registered: {entry.model_id}")

        # Get model by ID
        retrieved = registry.get(entry.model_id)
        assert retrieved is not None
        assert retrieved.model_id == entry.model_id
        print(f"  ✓ Model retrieved by ID: {retrieved.model_id}")

        # Get latest model
        latest = registry.get_latest("fundraising", "portfolio_analysis")
        assert latest is not None
        assert latest.model_id == entry.model_id
        print(f"  ✓ Latest model retrieved: {latest.model_id}")

        # List models
        models = registry.list_models()
        assert len(models) == 1
        assert models[0].model_id == entry.model_id
        print(f"  ✓ Listed {len(models)} model(s)")

        # List models by unit
        models_by_unit = registry.list_models(unit_id="fundraising")
        assert len(models_by_unit) == 1
        print(f"  ✓ Listed models by unit")

        # List models by task
        models_by_task = registry.list_models(task_id="portfolio_analysis")
        assert len(models_by_task) == 1
        print(f"  ✓ Listed models by task")

        # List by unit grouped by task
        by_task = registry.list_by_unit("fundraising")
        assert "portfolio_analysis" in by_task
        assert len(by_task["portfolio_analysis"]) == 1
        print(f"  ✓ Listed models grouped by task")


def test_metrics_and_status():
    """Test metrics and status updates."""
    print("\nTesting metrics and status updates...")

    with tempfile.TemporaryDirectory() as tmpdir:
        registry = ModelRegistry(tmpdir)

        # Register a model
        entry = registry.register(
            unit_id="test_unit",
            task_id="test_task",
            adapter_path="/tmp/adapter",
            base_model="test-model",
        )

        # Update metrics
        metrics = ModelMetrics(
            train_loss=0.5,
            eval_loss=0.6,
            format_compliance=0.95,
            content_coverage=0.90,
            generation_latency_ms=100.0,
            tokens_per_second=50.0
        )
        registry.update_metrics(entry.model_id, metrics)
        print(f"  ✓ Metrics updated")

        # Retrieve and check metrics
        retrieved = registry.get(entry.model_id)
        assert retrieved.metrics.train_loss == 0.5
        assert retrieved.metrics.eval_loss == 0.6
        print(f"  ✓ Metrics retrieved correctly")

        # Update status
        registry.update_status(entry.model_id, "evaluated")
        retrieved = registry.get(entry.model_id)
        assert retrieved.status == "evaluated"
        print(f"  ✓ Status updated to: {retrieved.status}")

        # List by status
        evaluated_models = registry.list_models(status="evaluated")
        assert len(evaluated_models) == 1
        print(f"  ✓ Listed models by status")


def test_versioning():
    """Test automatic version increment."""
    print("\nTesting versioning...")

    with tempfile.TemporaryDirectory() as tmpdir:
        registry = ModelRegistry(tmpdir)

        # Register multiple versions
        entry1 = registry.register(
            unit_id="test_unit",
            task_id="test_task",
            adapter_path="/tmp/adapter1",
            base_model="test-model",
        )
        assert entry1.version == "v1"
        print(f"  ✓ First version: {entry1.version}")

        entry2 = registry.register(
            unit_id="test_unit",
            task_id="test_task",
            adapter_path="/tmp/adapter2",
            base_model="test-model",
        )
        assert entry2.version == "v2"
        print(f"  ✓ Second version: {entry2.version}")

        # Get latest should return v2
        latest = registry.get_latest("test_unit", "test_task")
        assert latest.version == "v2"
        print(f"  ✓ Latest version: {latest.version}")

        # List should show both
        models = registry.list_models(unit_id="test_unit", task_id="test_task")
        assert len(models) == 2
        print(f"  ✓ Listed {len(models)} versions")


def test_summary():
    """Test summary statistics."""
    print("\nTesting summary statistics...")

    with tempfile.TemporaryDirectory() as tmpdir:
        registry = ModelRegistry(tmpdir)

        # Register models with different units and statuses
        registry.register(
            unit_id="unit1",
            task_id="task1",
            adapter_path="/tmp/adapter1",
            base_model="test-model",
        )

        entry2 = registry.register(
            unit_id="unit1",
            task_id="task2",
            adapter_path="/tmp/adapter2",
            base_model="test-model",
        )
        registry.update_status(entry2.model_id, "evaluated")

        entry3 = registry.register(
            unit_id="unit2",
            task_id="task1",
            adapter_path="/tmp/adapter3",
            base_model="test-model",
        )
        registry.update_status(entry3.model_id, "exported")

        # Get summary
        summary = registry.summary()
        assert summary["total_models"] == 3
        assert summary["by_unit"]["unit1"] == 2
        assert summary["by_unit"]["unit2"] == 1
        assert summary["by_status"]["trained"] == 1
        assert summary["by_status"]["evaluated"] == 1
        assert summary["by_status"]["exported"] == 1

        print(f"  ✓ Total models: {summary['total_models']}")
        print(f"  ✓ By unit: {summary['by_unit']}")
        print(f"  ✓ By status: {summary['by_status']}")


def test_routing_config():
    """Test routing configuration export."""
    print("\nTesting routing configuration...")

    with tempfile.TemporaryDirectory() as tmpdir:
        registry = ModelRegistry(tmpdir)

        # Register and evaluate models
        entry1 = registry.register(
            unit_id="unit1",
            task_id="task1",
            adapter_path="/tmp/adapter1",
            base_model="test-model",
            positive_prompts=["prompt1", "prompt2"],
            negative_prompts=["negative1"]
        )
        registry.update_status(entry1.model_id, "evaluated")

        entry2 = registry.register(
            unit_id="unit2",
            task_id="task2",
            adapter_path="/tmp/adapter2",
            base_model="test-model",
            positive_prompts=["prompt3"],
        )
        registry.update_status(entry2.model_id, "exported")

        # Not evaluated, should not appear
        registry.register(
            unit_id="unit3",
            task_id="task3",
            adapter_path="/tmp/adapter3",
            base_model="test-model",
        )

        # Get routing config
        config = registry.get_routing_config()
        assert "models" in config
        assert len(config["models"]) == 2  # Only evaluated and exported
        print(f"  ✓ Routing config contains {len(config['models'])} models")

        # Check first model
        model_info = config["models"][0]
        assert "model_id" in model_info
        assert "positive_prompts" in model_info
        print(f"  ✓ Model info includes required fields")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Phase 2 → Phase 0 Model Registry Migration Test")
    print("=" * 60)

    try:
        test_basic_operations()
        test_metrics_and_status()
        test_versioning()
        test_summary()
        test_routing_config()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        print("\nThe Phase 2 model registry is successfully using the")
        print("Phase 0 infrastructure with full backward compatibility.")
        return 0

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
