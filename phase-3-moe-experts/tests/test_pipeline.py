"""Tests for the Phase 3 MoE merge pipeline."""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import Settings, get_settings
from src.shared.config_generator import MoEConfigGenerator, validate_mergekit_config
from src.shared.model_validator import MoEValidator, quick_validate_adapter
from src.shared.phase2_importer import AdapterInfo, Phase2Importer


@pytest.fixture
def test_settings():
    """Create test settings."""
    settings = Settings()
    settings.test_mode = True
    return settings


@pytest.fixture
def mock_export_dir():
    """Get mock export directory."""
    return Path(__file__).parent / "fixtures" / "mock_phase2_export"


@pytest.fixture
def temp_import_dir(tmp_path):
    """Create temporary import directory."""
    return tmp_path / "imports"


class TestPhase2Importer:
    """Tests for Phase 2 import functionality."""

    def test_load_manifest(self, mock_export_dir):
        """Test loading export manifest."""
        manifest_path = mock_export_dir / "export_manifest.json"
        assert manifest_path.exists()

        with open(manifest_path) as f:
            manifest = json.load(f)

        assert "units" in manifest
        assert "base_model" in manifest
        assert len(manifest["units"]) == 3  # fundraising, business_development, field_operations

    def test_discover_adapters(self, mock_export_dir, temp_import_dir):
        """Test adapter discovery from manifest."""
        importer = Phase2Importer(
            phase2_export_dir=mock_export_dir,
            import_dir=temp_import_dir,
        )

        # Load manifest
        manifest = importer._load_manifest()
        adapters = importer._discover_from_manifest(manifest)

        assert len(adapters) == 5  # 2 fundraising + 1 business_dev + 2 field_ops
        assert all(isinstance(a, AdapterInfo) for a in adapters)

        # Check adapter details
        unit_ids = [a.unit_id for a in adapters]
        assert "fundraising" in unit_ids
        assert "business_development" in unit_ids
        assert "field_operations" in unit_ids

    def test_import_with_fixtures(self, mock_export_dir, temp_import_dir):
        """Test full import with fixture data."""
        importer = Phase2Importer(
            phase2_export_dir=mock_export_dir,
            import_dir=temp_import_dir,
            required_units=[],  # Don't require specific units
        )

        result = importer.import_all(copy_files=True)

        assert result.total_adapters == 5  # 2 fundraising + 1 business_dev + 2 field_ops
        assert len(result.units) == 3  # fundraising, business_development, field_operations
        assert temp_import_dir.exists()


class TestMoEConfigGenerator:
    """Tests for MoE config generation."""

    def test_build_expert_config(self):
        """Test building expert config from adapter."""
        generator = MoEConfigGenerator()

        adapter = AdapterInfo(
            model_id="test_adapter",
            unit_id="test_unit",
            task_id="test_task",
            version="v1",
            source_path=Path("/source"),
            import_path=Path("/import/model"),
            base_model="test_model",
            positive_prompts=["Test prompt 1", "Test prompt 2"],
            negative_prompts=["Negative 1"],
        )

        config = generator._build_expert_config(adapter)

        assert config["source_model"] == "/import/model"
        assert len(config["positive_prompts"]) == 2
        assert len(config["negative_prompts"]) == 1

    def test_validate_config(self):
        """Test config validation."""
        valid_config = {
            "base_model": "test/model",
            "architecture": "mixtral",
            "gate_mode": "hidden",
            "dtype": "float16",
            "experts": [
                {"source_model": "/path/to/expert1"},
                {"source_model": "/path/to/expert2"},
            ],
        }

        errors = validate_mergekit_config(valid_config)
        assert len(errors) == 0

    def test_validate_config_missing_fields(self):
        """Test validation catches missing fields."""
        invalid_config = {
            "architecture": "mixtral",
        }

        errors = validate_mergekit_config(invalid_config)
        assert len(errors) > 0
        assert any("base_model" in e for e in errors)
        assert any("experts" in e for e in errors)

    def test_validate_config_invalid_architecture(self):
        """Test validation catches invalid architecture."""
        config = {
            "base_model": "test",
            "architecture": "invalid_arch",
            "experts": [{"source_model": "/path"}],
        }

        errors = validate_mergekit_config(config)
        assert any("architecture" in e for e in errors)


class TestMoEValidator:
    """Tests for model validation."""

    def test_validate_adapter(self, mock_export_dir):
        """Test adapter validation."""
        validator = MoEValidator()

        adapter_path = (
            mock_export_dir / "fundraising" / "investor_profiling" / "v1" / "model"
        )
        result = validator.validate_adapter(adapter_path)

        # Should be valid (has adapter_config.json)
        assert result.is_valid
        assert "adapter_config" in result.info

    def test_validate_missing_adapter(self, tmp_path):
        """Test validation of missing adapter."""
        validator = MoEValidator()

        result = validator.validate_adapter(tmp_path / "nonexistent")

        assert not result.is_valid
        assert len(result.errors) > 0

    def test_quick_validate_adapter(self, mock_export_dir):
        """Test quick adapter validation."""
        adapter_path = (
            mock_export_dir / "fundraising" / "investor_profiling" / "v1" / "model"
        )

        assert quick_validate_adapter(adapter_path)
        assert not quick_validate_adapter(Path("/nonexistent"))


class TestAdapterInfo:
    """Tests for AdapterInfo dataclass."""

    def test_to_dict(self):
        """Test AdapterInfo serialization."""
        adapter = AdapterInfo(
            model_id="test_id",
            unit_id="unit",
            task_id="task",
            version="v1",
            source_path=Path("/source"),
            import_path=Path("/import"),
            base_model="model",
            positive_prompts=["prompt"],
            negative_prompts=["neg"],
        )

        data = adapter.to_dict()

        assert data["model_id"] == "test_id"
        assert data["unit_id"] == "unit"
        assert data["source_path"] == "/source"
        assert len(data["positive_prompts"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
