"""Integration tests for cross-registry workflows."""


import pytest

from registries.data_registry import DataRegistry
from registries.experiment_tracker import ExperimentTracker
from registries.model_registry import ModelRegistry
from registries.schemas import (
    DataCharacteristics,
    DatasetStatus,
    DataType,
    ExperimentStatus,
    HyperparameterConfig,
    ModelStatus,
    ModelType,
    Phase,
    RegisteredDataset,
    RegisteredModel,
    TrainingMetrics,
)


class TestCrossRegistryIntegration:
    """Test cross-registry workflow integration."""

    @pytest.fixture
    def data_registry(self, temp_storage_dir):
        """Create DataRegistry instance."""
        return DataRegistry(data_dir=temp_storage_dir, test_mode=True)

    @pytest.fixture
    def model_registry(self, temp_storage_dir):
        """Create ModelRegistry instance."""
        return ModelRegistry(data_dir=temp_storage_dir, test_mode=True)

    @pytest.fixture
    def experiment_tracker(self, temp_storage_dir):
        """Create ExperimentTracker instance."""
        return ExperimentTracker(data_dir=temp_storage_dir, test_mode=True)

    def test_dataset_to_model_lineage(self, data_registry, model_registry, temp_storage_dir):
        """Test lineage tracking from dataset to model."""
        # Create and register dataset
        train_file = temp_storage_dir / "train.jsonl"
        train_file.touch()

        dataset = RegisteredDataset(
            dataset_id="dataset_v1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_file),
            train_samples=1000,
            source_description="Initial dataset",
        )
        data_registry.register(dataset)

        # Register model with source dataset
        model = RegisteredModel(
            model_id="model_v1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            source_dataset_id="dataset_v1",
        )
        model_registry.register(model)

        # Verify lineage
        model_lineage = model_registry.get_lineage("model_v1")
        assert model_lineage["source_dataset_id"] == "dataset_v1"

        # Verify dataset exists
        source_dataset = data_registry.get("dataset_v1")
        assert source_dataset is not None
        assert source_dataset.dataset_id == "dataset_v1"

    def test_experiment_to_model_linkage(self, model_registry, experiment_tracker):
        """Test linking experiment to resulting model."""
        # Register model first
        model = RegisteredModel(
            model_id="model_v1",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
        )
        model_registry.register(model)

        # Start experiment
        experiment = experiment_tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
        )

        # Complete experiment with model reference
        completed = experiment_tracker.complete_experiment(
            experiment.experiment_id,
            model_id="model_v1",
        )

        # Verify linkage
        assert completed.model_id == "model_v1"

        # Verify model exists
        linked_model = model_registry.get("model_v1")
        assert linked_model is not None
        assert linked_model.model_id == "model_v1"

    def test_full_pipeline_workflow(
        self,
        data_registry,
        model_registry,
        experiment_tracker,
        temp_storage_dir,
    ):
        """
        Test complete workflow:
        Dataset -> Experiment -> Model with full lineage tracking.
        """
        # Step 1: Register dataset
        train_file = temp_storage_dir / "train.jsonl"
        train_file.touch()

        dataset = RegisteredDataset(
            dataset_id="pipeline_dataset_v1",
            phase=Phase.PHASE_1,
            unit="pipeline_unit",
            task="pipeline_task",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_file),
            train_samples=1000,
            val_samples=200,
            source_description="Pipeline test dataset",
        )
        data_registry.register(dataset)
        data_registry.update_status(dataset.dataset_id, DatasetStatus.VALIDATED)

        # Step 2: Start experiment
        experiment = experiment_tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit="pipeline_unit",
            task="pipeline_task",
            notes="Pipeline workflow test",
        )

        # Step 3: Log experiment data
        characteristics = DataCharacteristics(
            num_samples=1000,
            avg_input_length=128.5,
            avg_output_length=64.2,
            vocab_size=50000,
            unique_tasks=5,
        )
        experiment_tracker.log_data_characteristics(experiment.experiment_id, characteristics)

        hyperparameters = HyperparameterConfig(
            epochs=3,
            batch_size=8,
            learning_rate=2e-4,
            lora_r=16,
            lora_alpha=32,
        )
        experiment_tracker.log_hyperparameters(experiment.experiment_id, hyperparameters)

        # Step 4: Register model with dataset reference
        model = RegisteredModel(
            model_id="pipeline_model_v1",
            phase=Phase.PHASE_2,
            unit="pipeline_unit",
            task="pipeline_task",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            adapter_path="/path/to/adapter",
            source_dataset_id="pipeline_dataset_v1",
        )
        model_registry.register(model)
        model_registry.update_status(model.model_id, ModelStatus.TRAINING)

        # Step 5: Log training metrics
        metrics = TrainingMetrics(
            train_loss=0.45,
            eval_loss=0.52,
            format_compliance=0.95,
            content_coverage=0.88,
            tokens_per_second=1500.0,
            training_time_seconds=3600.0,
        )
        experiment_tracker.log_training_metrics(experiment.experiment_id, metrics)

        # Step 6: Complete experiment and link to model
        experiment_tracker.complete_experiment(
            experiment.experiment_id,
            model_id="pipeline_model_v1",
        )

        # Step 7: Update model status
        model_registry.update_status(model.model_id, ModelStatus.TRAINED)
        model_registry.update_metrics(
            model.model_id,
            {"eval_loss": 0.52, "format_compliance": 0.95},
        )

        # Verify complete lineage
        # 1. Dataset exists and is validated
        final_dataset = data_registry.get(dataset.dataset_id)
        assert final_dataset.status == DatasetStatus.VALIDATED

        # 2. Experiment is completed and linked to model
        final_exp = experiment_tracker.get(experiment.experiment_id)
        assert final_exp.status == ExperimentStatus.COMPLETED
        assert final_exp.model_id == model.model_id
        assert final_exp.data_characteristics is not None
        assert final_exp.hyperparameters is not None
        assert final_exp.metrics is not None

        # 3. Model is trained and linked to dataset
        final_model = model_registry.get(model.model_id)
        assert final_model.status == ModelStatus.TRAINED
        assert final_model.source_dataset_id == dataset.dataset_id

        # 4. Model has metrics
        assert "metric:eval_loss=0.52" in final_model.tags
        assert "metric:format_compliance=0.95" in final_model.tags

        # 5. Lineage is traceable
        model_lineage = model_registry.get_lineage(model.model_id)
        assert model_lineage["source_dataset_id"] == dataset.dataset_id

    def test_multiple_models_from_same_dataset(
        self, data_registry, model_registry, temp_storage_dir
    ):
        """Test creating multiple models from the same dataset."""
        # Register dataset
        train_file = temp_storage_dir / "train.jsonl"
        train_file.touch()

        dataset = RegisteredDataset(
            dataset_id="shared_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_file),
            train_samples=1000,
            source_description="Shared dataset",
        )
        data_registry.register(dataset)

        # Register multiple models from same dataset
        for i in range(3):
            model = RegisteredModel(
                model_id=f"model_v{i+1}",
                phase=Phase.PHASE_2,
                unit="unit1",
                task="task1",
                model_type=ModelType.FINE_TUNED,
                base_model="meta-llama/Llama-3.1-8B",
                source_dataset_id="shared_dataset",
            )
            model_registry.register(model)

        # Verify all models reference same dataset
        for i in range(3):
            model = model_registry.get(f"model_v{i+1}")
            assert model.source_dataset_id == "shared_dataset"

        # Verify dataset can be retrieved
        source = data_registry.get("shared_dataset")
        assert source is not None

    def test_dataset_parent_child_with_models(
        self, data_registry, model_registry, temp_storage_dir
    ):
        """Test dataset parent-child relationships with model training."""
        # Create parent dataset
        parent_file = temp_storage_dir / "parent.jsonl"
        parent_file.touch()

        parent_dataset = RegisteredDataset(
            dataset_id="parent_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.RAW_DOCUMENTS,
            train_path=str(parent_file),
            train_samples=5000,
            source_description="Parent raw data",
        )
        data_registry.register(parent_dataset)

        # Create child dataset (processed from parent)
        child_file = temp_storage_dir / "child.jsonl"
        child_file.touch()

        child_dataset = RegisteredDataset(
            dataset_id="child_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(child_file),
            train_samples=2000,
            source_description="Processed task examples",
            parent_dataset_id="parent_dataset",
        )
        data_registry.register(child_dataset)

        # Register model trained on child dataset
        model = RegisteredModel(
            model_id="model_from_child",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            source_dataset_id="child_dataset",
        )
        model_registry.register(model)

        # Verify lineage chain
        dataset_lineage = data_registry.get_lineage("child_dataset")
        assert len(dataset_lineage) == 1
        assert dataset_lineage[0].dataset_id == "parent_dataset"

        model_lineage = model_registry.get_lineage("model_from_child")
        assert model_lineage["source_dataset_id"] == "child_dataset"

    def test_experiment_comparison_workflow(
        self,
        data_registry,
        model_registry,
        experiment_tracker,
        temp_storage_dir,
    ):
        """Test workflow for comparing multiple experiments and selecting best model."""
        # Register dataset
        train_file = temp_storage_dir / "train.jsonl"
        train_file.touch()

        dataset = RegisteredDataset(
            dataset_id="comparison_dataset",
            phase=Phase.PHASE_1,
            unit="comparison_unit",
            task="comparison_task",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_file),
            train_samples=1000,
            source_description="Comparison dataset",
        )
        data_registry.register(dataset)

        # Run 3 experiments with different hyperparameters
        eval_losses = [0.55, 0.48, 0.62]  # Second one is best
        for i, eval_loss in enumerate(eval_losses):
            # Start experiment
            exp = experiment_tracker.start_experiment(
                phase=Phase.PHASE_2,
                unit="comparison_unit",
                task="comparison_task",
                notes=f"Experiment {i+1}",
            )

            # Log hyperparameters (vary learning rate)
            hyperparams = HyperparameterConfig(
                epochs=3,
                batch_size=8,
                learning_rate=1e-4 * (i + 1),  # Different LR for each
            )
            experiment_tracker.log_hyperparameters(exp.experiment_id, hyperparams)

            # Log metrics
            metrics = TrainingMetrics(
                train_loss=0.4 + (i * 0.05),
                eval_loss=eval_loss,
            )
            experiment_tracker.log_training_metrics(exp.experiment_id, metrics)

            # Register model
            model = RegisteredModel(
                model_id=f"comparison_model_v{i+1}",
                phase=Phase.PHASE_2,
                unit="comparison_unit",
                task="comparison_task",
                model_type=ModelType.FINE_TUNED,
                base_model="meta-llama/Llama-3.1-8B",
                source_dataset_id="comparison_dataset",
            )
            model_registry.register(model)

            # Complete experiment with model
            experiment_tracker.complete_experiment(
                exp.experiment_id,
                model_id=model.model_id,
            )

        # Find best configuration
        best_exp = experiment_tracker.find_best_config(
            "comparison_unit",
            "comparison_task",
            metric="eval_loss",
            minimize=True,
        )

        assert best_exp is not None
        assert best_exp.metrics.eval_loss == 0.48  # Best (minimum) eval_loss
        assert best_exp.model_id == "comparison_model_v2"

        # Get the best model
        best_model = model_registry.get(best_exp.model_id)
        assert best_model is not None
        assert best_model.source_dataset_id == "comparison_dataset"

    def test_moe_deployment_workflow(self, model_registry):
        """Test MoE deployment workflow with routing config."""
        # Register multiple task-specific models
        tasks = ["task1", "task2", "task3"]
        units = ["unit1", "unit2"]

        for unit in units:
            for task in tasks:
                model = RegisteredModel(
                    model_id=f"{unit}_{task}_v1",
                    phase=Phase.PHASE_2,
                    unit=unit,
                    task=task,
                    model_type=ModelType.FINE_TUNED,
                    base_model="meta-llama/Llama-3.1-8B",
                    adapter_path=f"/path/to/{unit}/{task}/adapter",
                    positive_prompts=[f"Good prompt for {task}"],
                    negative_prompts=[f"Bad prompt for {task}"],
                )
                model_registry.register(model)
                # Mark some as evaluated/exported
                if task in ["task1", "task2"]:
                    model_registry.update_status(model.model_id, ModelStatus.EVALUATED)

        # Get routing configuration (only evaluated/exported models)
        routing_config = model_registry.get_routing_config()

        assert routing_config["version"] == "1.0"
        assert len(routing_config["models"]) == 4  # 2 units * 2 tasks (task1, task2)

        # Verify structure
        for model_config in routing_config["models"]:
            assert "model_id" in model_config
            assert "adapter_path" in model_config
            assert "positive_prompts" in model_config
            assert "negative_prompts" in model_config

    def test_export_and_deployment_workflow(self, model_registry, temp_storage_dir):
        """Test model export and deployment workflow."""
        # Register model
        model = RegisteredModel(
            model_id="export_test_model_v1",
            phase=Phase.PHASE_2,
            unit="export_unit",
            task="export_task",
            model_type=ModelType.FINE_TUNED,
            base_model="meta-llama/Llama-3.1-8B",
            adapter_path="/path/to/adapter",
            status=ModelStatus.EVALUATED,
        )
        model_registry.register(model)

        # Export for deployment
        export_dir = temp_storage_dir / "exports"
        export_data = model_registry.export_for_deployment(
            model.model_id,
            export_dir,
        )

        # Verify export
        assert export_data["model_id"] == model.model_id
        assert export_dir.exists()

        # Verify status was updated to EXPORTED
        updated_model = model_registry.get(model.model_id)
        assert updated_model.status == ModelStatus.EXPORTED

        # Verify model appears in routing config
        routing_config = model_registry.get_routing_config()
        model_ids = [m["model_id"] for m in routing_config["models"]]
        assert model.model_id in model_ids

    def test_validation_workflow(self, data_registry, temp_storage_dir):
        """Test dataset validation workflow."""
        # Create actual files
        train_file = temp_storage_dir / "train.jsonl"
        val_file = temp_storage_dir / "val.jsonl"
        train_file.touch()
        val_file.touch()

        # Register dataset
        dataset = RegisteredDataset(
            dataset_id="validation_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_file),
            val_path=str(val_file),
            test_path="/nonexistent/test.jsonl",  # This doesn't exist
            train_samples=1000,
            val_samples=200,
            source_description="Validation test dataset",
        )
        data_registry.register(dataset)

        # Validate dataset
        result = data_registry.validate_dataset(dataset.dataset_id)

        # Should be valid (train and val exist, test is optional)
        assert result.is_valid is True
        assert len(result.errors) == 0
        # Should have warning about missing test path
        assert len(result.warnings) == 1
        assert "Test path does not exist" in result.warnings[0]

        # Update status based on validation
        if result.is_valid:
            data_registry.update_status(dataset.dataset_id, DatasetStatus.VALIDATED)

        final_dataset = data_registry.get(dataset.dataset_id)
        assert final_dataset.status == DatasetStatus.VALIDATED
