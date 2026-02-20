"""Tests for DataRegistry."""


import pytest

from registries.data_registry import DataRegistry
from registries.schemas import (
    DatasetStatus,
    DataType,
    Phase,
    RegisteredDataset,
)


class TestDataRegistry:
    """Test DataRegistry class."""

    @pytest.fixture
    def registry(self, temp_storage_dir):
        """Create a DataRegistry instance with test mode."""
        return DataRegistry(data_dir=temp_storage_dir, test_mode=True)

    def test_initialization(self, registry, temp_storage_dir):
        """Test registry initialization."""
        assert registry.data_dir == temp_storage_dir
        # File doesn't exist until first save
        # assert registry.registry_file.exists()  # Removed - file created on first save

    def test_register_dataset(self, registry, sample_dataset):
        """Test registering a dataset."""
        result = registry.register(sample_dataset)

        assert result.dataset_id == sample_dataset.dataset_id
        assert result.phase == sample_dataset.phase

    def test_register_duplicate_dataset_raises_error(self, registry, sample_dataset):
        """Test that registering duplicate dataset raises ValueError."""
        registry.register(sample_dataset)

        with pytest.raises(ValueError, match="Dataset already exists"):
            registry.register(sample_dataset)

    def test_get_existing_dataset(self, registry, sample_dataset):
        """Test getting an existing dataset."""
        registry.register(sample_dataset)
        retrieved = registry.get(sample_dataset.dataset_id)

        assert retrieved is not None
        assert retrieved.dataset_id == sample_dataset.dataset_id
        assert retrieved.phase == sample_dataset.phase
        assert retrieved.unit == sample_dataset.unit

    def test_get_nonexistent_dataset_returns_none(self, registry):
        """Test getting nonexistent dataset returns None."""
        result = registry.get("nonexistent_dataset")
        assert result is None

    def test_list_all_datasets(self, registry):
        """Test listing all datasets."""
        dataset1 = RegisteredDataset(
            dataset_id="dataset_1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train1.jsonl",
            train_samples=100,
            source_description="Dataset 1",
        )
        dataset2 = RegisteredDataset(
            dataset_id="dataset_2",
            phase=Phase.PHASE_2,
            unit="unit2",
            task="task2",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/train2.jsonl",
            train_samples=200,
            source_description="Dataset 2",
        )

        registry.register(dataset1)
        registry.register(dataset2)

        datasets = registry.list()
        assert len(datasets) == 2

    def test_list_with_phase_filter(self, registry):
        """Test listing datasets filtered by phase."""
        dataset1 = RegisteredDataset(
            dataset_id="dataset_1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train1.jsonl",
            train_samples=100,
            source_description="Dataset 1",
        )
        dataset2 = RegisteredDataset(
            dataset_id="dataset_2",
            phase=Phase.PHASE_2,
            unit="unit2",
            task="task2",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/train2.jsonl",
            train_samples=200,
            source_description="Dataset 2",
        )

        registry.register(dataset1)
        registry.register(dataset2)

        datasets = registry.list(phase=Phase.PHASE_1)
        assert len(datasets) == 1
        assert datasets[0].dataset_id == "dataset_1"

    def test_list_with_unit_filter(self, registry):
        """Test listing datasets filtered by unit."""
        dataset1 = RegisteredDataset(
            dataset_id="dataset_1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train1.jsonl",
            train_samples=100,
            source_description="Dataset 1",
        )
        dataset2 = RegisteredDataset(
            dataset_id="dataset_2",
            phase=Phase.PHASE_1,
            unit="unit2",
            task="task2",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/train2.jsonl",
            train_samples=200,
            source_description="Dataset 2",
        )

        registry.register(dataset1)
        registry.register(dataset2)

        datasets = registry.list(unit="unit1")
        assert len(datasets) == 1
        assert datasets[0].unit == "unit1"

    def test_list_with_data_type_filter(self, registry):
        """Test listing datasets filtered by data type."""
        dataset1 = RegisteredDataset(
            dataset_id="dataset_1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train1.jsonl",
            train_samples=100,
            source_description="Dataset 1",
        )
        dataset2 = RegisteredDataset(
            dataset_id="dataset_2",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task2",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/train2.jsonl",
            train_samples=200,
            source_description="Dataset 2",
        )

        registry.register(dataset1)
        registry.register(dataset2)

        datasets = registry.list(data_type=DataType.TASK_EXAMPLES)
        assert len(datasets) == 1
        assert datasets[0].data_type == DataType.TASK_EXAMPLES

    def test_list_with_status_filter(self, registry):
        """Test listing datasets filtered by status."""
        dataset1 = RegisteredDataset(
            dataset_id="dataset_1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train1.jsonl",
            train_samples=100,
            source_description="Dataset 1",
            status=DatasetStatus.REGISTERED,
        )
        dataset2 = RegisteredDataset(
            dataset_id="dataset_2",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task2",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/train2.jsonl",
            train_samples=200,
            source_description="Dataset 2",
            status=DatasetStatus.VALIDATED,
        )

        registry.register(dataset1)
        registry.register(dataset2)

        datasets = registry.list(status=DatasetStatus.VALIDATED)
        assert len(datasets) == 1
        assert datasets[0].status == DatasetStatus.VALIDATED

    def test_list_with_multiple_filters(self, registry):
        """Test listing datasets with multiple filters."""
        dataset1 = RegisteredDataset(
            dataset_id="dataset_1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train1.jsonl",
            train_samples=100,
            source_description="Dataset 1",
        )
        dataset2 = RegisteredDataset(
            dataset_id="dataset_2",
            phase=Phase.PHASE_1,
            unit="unit2",
            task="task2",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train2.jsonl",
            train_samples=200,
            source_description="Dataset 2",
        )

        registry.register(dataset1)
        registry.register(dataset2)

        datasets = registry.list(phase=Phase.PHASE_1, unit="unit1", data_type=DataType.TASK_EXAMPLES)
        assert len(datasets) == 1
        assert datasets[0].dataset_id == "dataset_1"

    def test_update_status(self, registry, sample_dataset):
        """Test updating dataset status."""
        registry.register(sample_dataset)
        registry.update_status(sample_dataset.dataset_id, DatasetStatus.VALIDATED)

        updated = registry.get(sample_dataset.dataset_id)
        assert updated.status == DatasetStatus.VALIDATED

    def test_update_status_nonexistent_dataset_raises_error(self, registry):
        """Test updating status of nonexistent dataset raises KeyError."""
        with pytest.raises(KeyError, match="Dataset not found"):
            registry.update_status("nonexistent", DatasetStatus.VALIDATED)

    def test_get_lineage_with_parent(self, registry):
        """Test getting dataset lineage with parent."""
        # Create parent dataset
        parent = RegisteredDataset(
            dataset_id="parent_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/parent.jsonl",
            train_samples=100,
            source_description="Parent dataset",
        )
        registry.register(parent)

        # Create child dataset
        child = RegisteredDataset(
            dataset_id="child_dataset",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/child.jsonl",
            train_samples=50,
            source_description="Child dataset",
            parent_dataset_id="parent_dataset",
        )
        registry.register(child)

        lineage = registry.get_lineage("child_dataset")
        assert len(lineage) == 1
        assert lineage[0].dataset_id == "parent_dataset"

    def test_get_lineage_with_grandparent(self, registry):
        """Test getting dataset lineage with grandparent."""
        # Create grandparent
        grandparent = RegisteredDataset(
            dataset_id="grandparent",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.RAW_DOCUMENTS,
            train_path="/path/to/grandparent.jsonl",
            train_samples=200,
            source_description="Grandparent dataset",
        )
        registry.register(grandparent)

        # Create parent
        parent = RegisteredDataset(
            dataset_id="parent",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/parent.jsonl",
            train_samples=100,
            source_description="Parent dataset",
            parent_dataset_id="grandparent",
        )
        registry.register(parent)

        # Create child
        child = RegisteredDataset(
            dataset_id="child",
            phase=Phase.PHASE_2,
            unit="unit1",
            task="task1",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/child.jsonl",
            train_samples=50,
            source_description="Child dataset",
            parent_dataset_id="parent",
        )
        registry.register(child)

        lineage = registry.get_lineage("child")
        assert len(lineage) == 2
        assert lineage[0].dataset_id == "parent"
        assert lineage[1].dataset_id == "grandparent"

    def test_get_lineage_no_parent(self, registry, sample_dataset):
        """Test getting lineage for dataset with no parent."""
        registry.register(sample_dataset)
        lineage = registry.get_lineage(sample_dataset.dataset_id)
        assert len(lineage) == 0

    def test_get_lineage_nonexistent_dataset(self, registry):
        """Test getting lineage for nonexistent dataset."""
        lineage = registry.get_lineage("nonexistent")
        assert len(lineage) == 0

    def test_validate_dataset_success(self, registry, temp_storage_dir):
        """Test validating dataset with existing paths."""
        # Create actual files
        train_file = temp_storage_dir / "train.jsonl"
        train_file.touch()

        dataset = RegisteredDataset(
            dataset_id="test_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_file),
            train_samples=100,
            source_description="Test dataset",
        )
        registry.register(dataset)

        result = registry.validate_dataset("test_dataset")
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_dataset_missing_train_path(self, registry, sample_dataset):
        """Test validating dataset with missing train path."""
        registry.register(sample_dataset)
        result = registry.validate_dataset(sample_dataset.dataset_id)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("Training path does not exist" in err for err in result.errors)

    def test_validate_dataset_missing_optional_paths(self, registry, temp_storage_dir):
        """Test validating dataset with missing optional paths."""
        # Create train file but not val/test
        train_file = temp_storage_dir / "train.jsonl"
        train_file.touch()

        dataset = RegisteredDataset(
            dataset_id="test_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path=str(train_file),
            val_path="/nonexistent/val.jsonl",
            test_path="/nonexistent/test.jsonl",
            train_samples=100,
            source_description="Test dataset",
        )
        registry.register(dataset)

        result = registry.validate_dataset("test_dataset")
        assert result.is_valid is True  # Valid because train exists
        assert len(result.warnings) == 2  # Warnings for val and test

    def test_validate_dataset_nonexistent(self, registry):
        """Test validating nonexistent dataset."""
        result = registry.validate_dataset("nonexistent")
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "Dataset not found" in result.errors[0]

    def test_summary_empty_registry(self, registry):
        """Test summary for empty registry."""
        summary = registry.summary()
        assert summary["total_datasets"] == 0
        assert summary["by_status"] == {}
        assert summary["by_phase"] == {}

    def test_summary_with_datasets(self, registry):
        """Test summary with multiple datasets."""
        dataset1 = RegisteredDataset(
            dataset_id="dataset_1",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train1.jsonl",
            train_samples=100,
            source_description="Dataset 1",
            status=DatasetStatus.REGISTERED,
        )
        dataset2 = RegisteredDataset(
            dataset_id="dataset_2",
            phase=Phase.PHASE_1,
            unit="unit2",
            task="task2",
            data_type=DataType.PREFERENCE_PAIRS,
            train_path="/path/to/train2.jsonl",
            train_samples=200,
            val_samples=50,
            source_description="Dataset 2",
            status=DatasetStatus.VALIDATED,
        )

        registry.register(dataset1)
        registry.register(dataset2)

        summary = registry.summary()
        assert summary["total_datasets"] == 2
        assert summary["by_status"]["registered"] == 1
        assert summary["by_status"]["validated"] == 1
        assert summary["by_phase"]["1"] == 2
        assert summary["total_samples"]["train"] == 300
        assert summary["total_samples"]["val"] == 50

    def test_persistence_across_instances(self, temp_storage_dir):
        """Test that registry persists across instances."""
        # Create first instance and register dataset
        registry1 = DataRegistry(data_dir=temp_storage_dir, test_mode=True)
        dataset = RegisteredDataset(
            dataset_id="test_dataset",
            phase=Phase.PHASE_1,
            unit="unit1",
            task="task1",
            data_type=DataType.TASK_EXAMPLES,
            train_path="/path/to/train.jsonl",
            train_samples=100,
            source_description="Test dataset",
        )
        registry1.register(dataset)

        # Create second instance and verify data persists
        registry2 = DataRegistry(data_dir=temp_storage_dir, test_mode=True)
        retrieved = registry2.get("test_dataset")

        assert retrieved is not None
        assert retrieved.dataset_id == "test_dataset"
        assert retrieved.unit == "unit1"
