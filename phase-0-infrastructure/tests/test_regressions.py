"""Regression tests for bugs found in the phase-0 review (2026-07).

Covers:
- B2: Settings(test_mode=True) silently ignored due to bare validation_alias
- B3: version parsing incompatible with the canonical ID convention
- B4: non-atomic writes / set_if_absent primitive
- B5: lost updates between concurrent registry instances
- B7: count validators skipped for empty lists
"""

import json

import pytest

from phase0_infra.config.base_settings import HabitatBaseSettings
from phase0_infra.config.phase_boundary_schemas import (
    Phase2ExportManifest,
    Phase4ExportBundle,
    Phase4ExportSummary,
)
from phase0_infra.registries.data_registry import DataRegistry
from phase0_infra.registries.model_registry import ModelRegistry, _extract_version
from phase0_infra.registries.schemas import (
    DatasetStatus,
    DataType,
    ModelStatus,
    ModelType,
    Phase,
    RegisteredDataset,
    RegisteredModel,
)
from phase0_infra.registries.storage import JSONStorage


def _make_model(model_id: str, unit: str = "unit1", task: str = "task1") -> RegisteredModel:
    return RegisteredModel(
        model_id=model_id,
        phase=Phase.PHASE_2,
        unit=unit,
        task=task,
        model_type=ModelType.FINE_TUNED,
        base_model="meta-llama/Llama-3.1-8B",
    )


def _make_dataset(dataset_id: str) -> RegisteredDataset:
    return RegisteredDataset(
        dataset_id=dataset_id,
        phase=Phase.PHASE_1,
        unit="unit1",
        task="task1",
        data_type=DataType.TASK_EXAMPLES,
        train_path="/path/to/train.jsonl",
        train_samples=100,
        source_description="regression test dataset",
    )


class TestSettingsAlias:
    """B2: test_mode must be settable via kwarg AND env var."""

    def test_test_mode_constructor_kwarg(self):
        settings = HabitatBaseSettings(test_mode=True)
        assert settings.test_mode is True

    def test_test_mode_env_var(self, monkeypatch):
        monkeypatch.setenv("PHASE0_TEST_MODE", "true")
        settings = HabitatBaseSettings()
        assert settings.test_mode is True

    def test_test_mode_default(self):
        settings = HabitatBaseSettings()
        assert settings.test_mode is False


class TestVersionParsing:
    """B3: version parsing must support both ID conventions."""

    def test_extract_suffix_style(self):
        assert _extract_version("unit1/task1_v3") == (3,)

    def test_extract_canonical_style(self):
        assert _extract_version("2/unit1/task1/v1.2.3") == (1, 2, 3)

    def test_extract_unparseable_defaults_to_zero(self):
        assert _extract_version("no-version-here") == (0,)

    def test_get_latest_with_canonical_ids(self, temp_storage_dir):
        registry = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        registry.register(_make_model("2/unit1/task1/v1.0.0"))
        registry.register(_make_model("2/unit1/task1/v1.2.0"))
        registry.register(_make_model("2/unit1/task1/v1.10.0"))

        latest = registry.get_latest("unit1", "task1")
        assert latest is not None
        # 1.10.0 > 1.2.0 numerically (would sort wrong as a string)
        assert latest.model_id == "2/unit1/task1/v1.10.0"

    def test_export_filename_has_no_slashes(self, temp_storage_dir):
        registry = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        registry.register(_make_model("2/unit1/task1/v1.0.0"))

        export_dir = temp_storage_dir / "exports"
        registry.export_for_deployment("2/unit1/task1/v1.0.0", export_dir)

        files = list(export_dir.iterdir())
        assert len(files) == 1
        assert files[0].name == "unit1_task1_v1.0.0.json"


class TestStoragePrimitives:
    """B4: atomic writes and set_if_absent."""

    def test_set_if_absent_first_write_wins(self, temp_storage_dir):
        storage = JSONStorage(temp_storage_dir / "store.json")
        assert storage.set_if_absent("k", {"v": 1}) is True
        assert storage.set_if_absent("k", {"v": 2}) is False
        assert storage.get("k") == {"v": 1}

    def test_write_leaves_valid_json_and_no_temp_files(self, temp_storage_dir):
        storage = JSONStorage(temp_storage_dir / "store.json")
        storage.save({"a": 1, "b": [1, 2, 3]})

        # File is valid JSON with the metadata wrapper
        with open(temp_storage_dir / "store.json") as f:
            raw = json.load(f)
        assert raw["data"] == {"a": 1, "b": [1, 2, 3]}

        # No orphaned temp files
        leftovers = [p for p in temp_storage_dir.iterdir() if p.suffix == ".tmp"]
        assert leftovers == []

    def test_failed_encode_preserves_previous_content(self, temp_storage_dir):
        storage = JSONStorage(temp_storage_dir / "store.json")
        storage.save({"good": True})

        with pytest.raises(ValueError):
            storage.save({"bad": object()})  # not JSON-serializable

        # Previous content intact (old code truncated the file first)
        assert storage.load() == {"good": True}

    def test_save_with_auto_create_false_creates_parent(self, temp_storage_dir):
        target = temp_storage_dir / "nested" / "deep" / "store.json"
        storage = JSONStorage(target, auto_create=False)
        storage.save({"x": 1})
        assert storage.load() == {"x": 1}

    def test_mutate_read_modify_write(self, temp_storage_dir):
        storage = JSONStorage(temp_storage_dir / "store.json")
        storage.save({"count": 1})

        def bump(data):
            data["count"] += 1
            return data

        result = storage.mutate(bump)
        assert result == {"count": 2}
        assert storage.load() == {"count": 2}


class TestConcurrentRegistryInstances:
    """B5: two registry instances must not lose each other's writes."""

    def test_model_registry_no_lost_updates(self, temp_storage_dir):
        reg_a = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        reg_b = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)

        reg_a.register(_make_model("model_a_v1", unit="a"))
        reg_b.register(_make_model("model_b_v1", unit="b"))

        # A fresh instance sees BOTH writes
        reg_c = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        assert reg_c.get("model_a_v1") is not None
        assert reg_c.get("model_b_v1") is not None

    def test_model_registry_duplicate_detected_across_instances(self, temp_storage_dir):
        reg_a = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        reg_b = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)

        reg_a.register(_make_model("dup_v1"))
        with pytest.raises(ValueError, match="already registered"):
            reg_b.register(_make_model("dup_v1"))

    def test_data_registry_no_lost_updates(self, temp_storage_dir):
        reg_a = DataRegistry(data_dir=temp_storage_dir, test_mode=True)
        reg_b = DataRegistry(data_dir=temp_storage_dir, test_mode=True)

        reg_a.register(_make_dataset("ds_a_v1"))
        reg_b.register(_make_dataset("ds_b_v1"))

        reg_c = DataRegistry(data_dir=temp_storage_dir, test_mode=True)
        assert reg_c.get("ds_a_v1") is not None
        assert reg_c.get("ds_b_v1") is not None

    def test_update_status_sees_other_instances_writes(self, temp_storage_dir):
        reg_a = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        reg_b = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)

        # B registered a model A's cache has never seen
        reg_b.register(_make_model("model_b_v1", unit="b"))
        reg_a.update_status("model_b_v1", ModelStatus.TRAINED)

        reg_c = ModelRegistry(data_dir=temp_storage_dir, test_mode=True)
        assert reg_c.get("model_b_v1").status == ModelStatus.TRAINED

    def test_dataset_update_status_sees_other_instances_writes(self, temp_storage_dir):
        reg_a = DataRegistry(data_dir=temp_storage_dir, test_mode=True)
        reg_b = DataRegistry(data_dir=temp_storage_dir, test_mode=True)

        reg_b.register(_make_dataset("ds_b_v1"))
        reg_a.update_status("ds_b_v1", DatasetStatus.VALIDATED)

        reg_c = DataRegistry(data_dir=temp_storage_dir, test_mode=True)
        assert reg_c.get("ds_b_v1").status == DatasetStatus.VALIDATED


class TestCountValidators:
    """B7: totals must be validated even when the list is empty."""

    def test_phase2_manifest_empty_list_mismatch_rejected(self):
        with pytest.raises(ValueError, match="doesn't match"):
            Phase2ExportManifest(
                adapters=[],
                base_model="meta-llama/Llama-3.1-8B",
                total_adapters=5,
            )

    def test_phase2_manifest_empty_list_zero_accepted(self):
        manifest = Phase2ExportManifest(
            adapters=[],
            base_model="meta-llama/Llama-3.1-8B",
            total_adapters=0,
        )
        assert manifest.total_adapters == 0

    def test_phase4_bundle_empty_list_mismatch_rejected(self):
        with pytest.raises(ValueError, match="doesn't match"):
            Phase4ExportBundle(
                training_examples=[],
                summary=Phase4ExportSummary(),
                total_examples=3,
            )

    def test_phase4_bundle_empty_list_zero_accepted(self):
        bundle = Phase4ExportBundle(
            training_examples=[],
            summary=Phase4ExportSummary(),
            total_examples=0,
        )
        assert bundle.total_examples == 0
