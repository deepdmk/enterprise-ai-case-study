"""Tests for ModelRegistry."""

import pytest
from pathlib import Path

from registries.model_registry import ModelRegistry
from registries.schemas import (
    Phase,
    ModelType,
    ModelStatus,
    RegisteredModel,
)


class TestModelRegistry:
    """Test ModelRegistry class."""

    @pytest.fixture
    def registry(self, temp_storage_dir):
        """Create a ModelRegistry instance with test mode."""
        return ModelRegistry(data_dir=temp_storage_dir, test_mode=True)

    def test_initialization(self, registry, temp_storage_dir):
        """Test registry initialization."""
        assert registry.data_dir == temp_storage_dir
        # File doesn't exist until first save
        # assert registry.registry_file.exists()  # Removed - file created on first save
        assert registry.test_mode is True

    def test_register_model(self, registry, sample_model):
        """Test registering a model."""
        result = registry.register(sample_model)

        assert result.model_id == sample_model.model_id
        assert result.phase == sample_model.phase

    def test_register_duplicate_model_raises_error(self, registry, sample_model):
        """Test that registering duplicate model raises ValueError."""
        registry.register(sample_model)

        with pytest.raises(ValueError, match="Model already registered"):
            registry.register(sample_model)

    def test_get_existing_model(self, registry, sample_model):
        """Test getting an existing model."""
        registry.register(sample_model)
        retrieved = registry.get(sample_model.model_id)

        assert retrieved is not None
        assert retrieved.model_id == sample_model.model_id
        assert retrieved.phase == sample_model.phase
        assert retrieved.unit == sample_model.unit

    def test_get_nonexistent_model_returns_none(self, registry):
        """Test getting nonexistent model returns None."""
        result = registry.get("nonexistent_model")
        assert result is None

    def test_get_latest_model(self, registry):
        """Test getting latest model version for unit/task."""
        model1 = RegisteredModel(
            model_id="unit1/task1_v1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model2 = RegisteredModel(
            model_id="unit1/task1_v2",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model3 = RegisteredModel(
            model_id="unit1/task1_v3",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )

        registry.register(model1)
        registry.register(model2)
        registry.register(model3)

        latest = registry.get_latest("unit1", "task1")
        assert latest is not None
        assert latest.model_id == "unit1/task1_v3"

    def test_get_latest_no_models(self, registry):
        """Test getting latest model when none exist."""
        latest = registry.get_latest("unit1", "task1")
        assert latest is None

    def test_list_all_models(self, registry):
        """Test listing all models."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_3,
            unit="unit2",
            task="task2",
            model_type=ModelType.MOE,
            base_model="meta-llama/Llama-3.1-8B",
        )

        registry.register(model1)
        registry.register(model2)

        models = registry.list()
        assert len(models) == 2

    def test_list_with_phase_filter(self, registry):
        """Test listing models filtered by phase."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_3,
            unit="unit2",
            task="task2",
            model_type=ModelType.MOE,
            base_model="meta-llama/Llama-3.1-8B",
        )

        registry.register(model1)
        registry.register(model2)

        models = registry.list(phase=Phase.PHASE_2)
        assert len(models) == 1
        assert models[0].model_id == "model_1"

    def test_list_with_unit_filter(self, registry):
        """Test listing models filtered by unit."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_2,
            unit="unit2",
            task="task2",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )

        registry.register(model1)
        registry.register(model2)

        models = registry.list(unit="unit1")
        assert len(models) == 1
        assert models[0].unit == "unit1"

    def test_list_with_task_filter(self, registry):
        """Test listing models filtered by task."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task2",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )

        registry.register(model1)
        registry.register(model2)

        models = registry.list(task="task1")
        assert len(models) == 1
        assert models[0].task == "task1"

    def test_list_with_model_type_filter(self, registry):
        """Test listing models filtered by model type."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_3,
            unit="unit1",
            task="task1",
            model_type=ModelType.MOE,
            base_model="meta-llama/Llama-3.1-8B",
        )

        registry.register(model1)
        registry.register(model2)

        models = registry.list(model_type=ModelType.MOE)
        assert len(models) == 1
        assert models[0].model_type == ModelType.MOE

    def test_list_with_status_filter(self, registry):
        """Test listing models filtered by status."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.REGISTERED,
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task2",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.EVALUATED,
        )

        registry.register(model1)
        registry.register(model2)

        models = registry.list(status=ModelStatus.EVALUATED)
        assert len(models) == 1
        assert models[0].status == ModelStatus.EVALUATED

    def test_list_with_multiple_filters(self, registry):
        """Test listing models with multiple filters."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.EVALUATED,
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_2,
            unit="unit2",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.EVALUATED,
        )

        registry.register(model1)
        registry.register(model2)

        models = registry.list(
            phase=Phase.PHASE_2,
            unit="unit1",
            model_type=ModelType.FINE_TUNED,
            status=ModelStatus.EVALUATED,
        )
        assert len(models) == 1
        assert models[0].model_id == "model_1"

    def test_update_status(self, registry, sample_model):
        """Test updating model status."""
        registry.register(sample_model)
        registry.update_status(sample_model.model_id, ModelStatus.TRAINED)

        updated = registry.get(sample_model.model_id)
        assert updated.status == ModelStatus.TRAINED

    def test_update_status_nonexistent_model_raises_error(self, registry):
        """Test updating status of nonexistent model raises KeyError."""
        with pytest.raises(KeyError, match="Model not found"):
            registry.update_status("nonexistent", ModelStatus.TRAINED)

    def test_update_metrics(self, registry, sample_model):
        """Test updating model metrics."""
        registry.register(sample_model)

        metrics = {
            "accuracy": 0.95,
            "f1_score": 0.92,
            "loss": 0.15,
        }
        registry.update_metrics(sample_model.model_id, metrics)

        updated = registry.get(sample_model.model_id)
        # Metrics are stored as tags with "metric:" prefix
        assert "metric:accuracy=0.95" in updated.tags
        assert "metric:f1_score=0.92" in updated.tags
        assert "metric:loss=0.15" in updated.tags

    def test_update_metrics_replaces_old_metrics(self, registry, sample_model):
        """Test that updating metrics replaces old metrics."""
        registry.register(sample_model)

        # First update
        metrics1 = {"accuracy": 0.90}
        registry.update_metrics(sample_model.model_id, metrics1)

        # Second update
        metrics2 = {"accuracy": 0.95, "loss": 0.15}
        registry.update_metrics(sample_model.model_id, metrics2)

        updated = registry.get(sample_model.model_id)
        # Should only have new metrics
        assert "metric:accuracy=0.95" in updated.tags
        assert "metric:loss=0.15" in updated.tags
        # Old metric should be replaced
        assert "metric:accuracy=0.90" not in updated.tags

    def test_update_metrics_nonexistent_model_raises_error(self, registry):
        """Test updating metrics of nonexistent model raises KeyError."""
        with pytest.raises(KeyError, match="Model not found"):
            registry.update_metrics("nonexistent", {"accuracy": 0.95})

    def test_get_lineage(self, registry, sample_model):
        """Test getting model lineage."""
        registry.register(sample_model)
        lineage = registry.get_lineage(sample_model.model_id)

        assert lineage["model_id"] == sample_model.model_id
        assert lineage["source_dataset_id"] == sample_model.source_dataset_id
        assert lineage["phase"] == sample_model.phase
        assert lineage["unit"] == sample_model.unit
        assert lineage["task"] == sample_model.task

    def test_get_lineage_nonexistent_model_raises_error(self, registry):
        """Test getting lineage of nonexistent model raises KeyError."""
        with pytest.raises(KeyError, match="Model not found"):
            registry.get_lineage("nonexistent")

    def test_get_routing_config_empty(self, registry):
        """Test getting routing config from empty registry."""
        config = registry.get_routing_config()

        assert config["version"] == "1.0"
        assert config["models"] == []
        assert "generated_at" in config

    def test_get_routing_config_with_eligible_models(self, registry):
        """Test getting routing config with eligible models."""
        # Create models with different statuses
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.EVALUATED,
            adapter_path="/path/to/adapter1",
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_2,
            unit="unit2",
            task="task2",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.EXPORTED,
            adapter_path="/path/to/adapter2",
        )
        model3 = RegisteredModel(
            model_id="model_3",
            phase=Phase.PHASE_2,
            unit="unit3",
            task="task3",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.REGISTERED,  # Not eligible
            adapter_path="/path/to/adapter3",
        )

        registry.register(model1)
        registry.register(model2)
        registry.register(model3)

        config = registry.get_routing_config()

        # Only EVALUATED and EXPORTED models should be included
        assert len(config["models"]) == 2
        model_ids = [m["model_id"] for m in config["models"]]
        assert "model_1" in model_ids
        assert "model_2" in model_ids
        assert "model_3" not in model_ids

    def test_export_for_deployment(self, registry, temp_storage_dir, sample_model):
        """Test exporting model for deployment."""
        registry.register(sample_model)

        export_dir = temp_storage_dir / "exports"
        export_data = registry.export_for_deployment(sample_model.model_id, export_dir)

        # Verify export data
        assert export_data["model_id"] == sample_model.model_id
        assert export_data["phase"] == sample_model.phase
        assert export_data["unit"] == sample_model.unit
        assert export_data["task"] == sample_model.task
        assert "exported_at" in export_data

        # Verify export file was created
        assert export_dir.exists()
        export_files = list(export_dir.glob("*.json"))
        assert len(export_files) == 1

    def test_export_for_deployment_updates_status(self, registry, temp_storage_dir, sample_model):
        """Test that export updates model status to EXPORTED."""
        registry.register(sample_model)
        assert sample_model.status == ModelStatus.REGISTERED

        export_dir = temp_storage_dir / "exports"
        registry.export_for_deployment(sample_model.model_id, export_dir)

        updated = registry.get(sample_model.model_id)
        assert updated.status == ModelStatus.EXPORTED

    def test_export_for_deployment_nonexistent_model_raises_error(self, registry, temp_storage_dir):
        """Test exporting nonexistent model raises KeyError."""
        export_dir = temp_storage_dir / "exports"

        with pytest.raises(KeyError, match="Model not found"):
            registry.export_for_deployment("nonexistent", export_dir)

    def test_summary_empty_registry(self, registry):
        """Test summary for empty registry."""
        summary = registry.summary()
        assert summary["total_models"] == 0
        assert summary["by_status"] == {}
        assert summary["by_phase"] == {}

    def test_summary_with_models(self, registry):
        """Test summary with multiple models."""
        model1 = RegisteredModel(
            model_id="model_1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.REGISTERED,
        )
        model2 = RegisteredModel(
            model_id="model_2",
            phase=Phase.PHASE_2,
            unit="unit2",
            task="task2",
            model_type=ModelType.MOE,
            base_model="meta-llama/Llama-3.1-8B",
            status=ModelStatus.EVALUATED,
        )

        registry.register(model1)
        registry.register(model2)

        summary = registry.summary()
        assert summary["total_models"] == 2
        assert summary["by_status"]["registered"] == 1
        assert summary["by_status"]["evaluated"] == 1
        assert summary["by_phase"]["2"] == 2
        assert summary["by_unit"]["unit1"] == 1
        assert summary["by_unit"]["unit2"] == 1
        assert summary["by_model_type"]["fine_tuned"] == 1
        assert summary["by_model_type"]["moe"] == 1

    def test_persistence_across_instances(self, temp_storage_dir):
        """Test that registry persists across instances."""
        # Create first instance and register model
        registry1 = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        model = RegisteredModel(
            model_id="test_model",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        registry1.register(model)

        # Create second instance and verify data persists
        registry2 = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        retrieved = registry2.get("test_model")

        assert retrieved is not None
        assert retrieved.model_id == "test_model"
        assert retrieved.unit == "unit1"
