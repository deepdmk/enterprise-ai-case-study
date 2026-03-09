"""Tests for Program 5: Phase 4 Export functionality."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import Settings
from src.program5_export.phase4_exporter import ExportResult, Phase4Exporter
from src.shared.phase2_importer import AdapterInfo


class TestPhase4Exporter:
    """Tests for Phase4Exporter class."""

    def test_init(self, test_settings):
        """Test Phase4Exporter initialization."""
        exporter = Phase4Exporter(test_settings)

        assert exporter.settings == test_settings
        assert exporter.base_path.exists()
        assert exporter.merged_dir is not None
        assert exporter.exports_dir is not None

    def test_export_unit_dry_run(self, test_settings, tmp_path, mock_moe_model, mock_adapters):
        """Test export unit in dry run mode."""
        exporter = Phase4Exporter(test_settings)

        # Filter to fundraising adapters only
        fundraising_adapters = [a for a in mock_adapters if a.unit_id == "fundraising"]

        result = exporter.export_unit(
            unit_id="fundraising",
            model_path=mock_moe_model,
            output_dir=tmp_path / "exports" / "fundraising",
            adapters=fundraising_adapters,
            dry_run=True,
        )

        assert result.success
        assert result.metadata.get("dry_run") is True
        # Dry run should not create files
        assert not (tmp_path / "exports" / "fundraising").exists()

    def test_export_unit_dry_run_missing_model(self, test_settings, tmp_path, mock_adapters):
        """Test dry run catches missing model path."""
        exporter = Phase4Exporter(test_settings)

        fundraising_adapters = [a for a in mock_adapters if a.unit_id == "fundraising"]

        result = exporter.export_unit(
            unit_id="fundraising",
            model_path=tmp_path / "nonexistent_model",
            output_dir=tmp_path / "exports" / "fundraising",
            adapters=fundraising_adapters,
            dry_run=True,
        )

        assert not result.success
        assert any("not found" in e.lower() for e in result.errors)

    def test_export_unit_full(self, test_settings, tmp_path, mock_moe_model, mock_adapters):
        """Test full export of a unit."""
        exporter = Phase4Exporter(test_settings)

        fundraising_adapters = [a for a in mock_adapters if a.unit_id == "fundraising"]
        output_dir = tmp_path / "exports" / "fundraising"

        result = exporter.export_unit(
            unit_id="fundraising",
            model_path=mock_moe_model,
            output_dir=output_dir,
            adapters=fundraising_adapters,
            generate_agent_config=True,
            generate_routing_embeddings=False,  # Skip embeddings for speed
        )

        assert result.success
        assert result.model_exported
        assert result.routing_exported
        assert result.agent_config_exported

        # Check created files
        assert (output_dir / "model" / "config.json").exists()
        assert (output_dir / "routing" / "expert_registry.json").exists()
        assert (output_dir / "routing" / "intent_mapping.json").exists()
        assert (output_dir / "agent_config" / "fundraising_agent.yaml").exists()
        assert (output_dir / "export_manifest.json").exists()

    def test_export_unit_atomic_writes(self, test_settings, tmp_path, mock_moe_model, mock_adapters):
        """Test atomic writes - partial exports should not leave state."""
        exporter = Phase4Exporter(test_settings)

        fundraising_adapters = [a for a in mock_adapters if a.unit_id == "fundraising"]
        output_dir = tmp_path / "exports" / "fundraising"

        # Force a failure during export by making adapters invalid
        with patch.object(exporter, "_export_routing") as mock_routing:
            mock_routing.side_effect = OSError("Simulated disk error")

            result = exporter.export_unit(
                unit_id="fundraising",
                model_path=mock_moe_model,
                output_dir=output_dir,
                adapters=fundraising_adapters,
            )

        # Export should fail
        assert not result.success

        # No partial state should be left behind
        assert not output_dir.exists()

    def test_export_all(self, test_settings, tmp_path, mock_moe_model, mock_adapters):
        """Test exporting all units."""
        exporter = Phase4Exporter(test_settings)
        exporter.merged_dir = tmp_path / "merged"
        exporter.exports_dir = tmp_path / "exports"

        # Create mock model for each unit
        for unit_id in ["fundraising", "business_development", "field_operations"]:
            unit_model = exporter.merged_dir / f"{unit_id}_moe"
            unit_model.mkdir(parents=True)
            (unit_model / "config.json").write_text(json.dumps({"model_type": "mixtral"}))

        results = exporter.export_all(
            adapters=mock_adapters,
            generate_agent_configs=True,
            generate_routing_embeddings=False,
            dry_run=True,
        )

        assert len(results) == 3
        assert "fundraising" in results
        assert "business_development" in results
        assert "field_operations" in results


class TestExportResult:
    """Tests for ExportResult dataclass."""

    def test_to_dict(self):
        """Test serialization to dict."""
        result = ExportResult(
            success=True,
            export_dir=Path("/exports/unit"),
            unit_id="fundraising",
            model_exported=True,
            routing_exported=True,
            agent_config_exported=True,
            metadata={"num_experts": 2},
        )

        data = result.to_dict()

        assert data["success"] is True
        assert data["export_dir"] == "/exports/unit"
        assert data["unit_id"] == "fundraising"
        assert data["model_exported"] is True
        assert data["routing_exported"] is True
        assert data["agent_config_exported"] is True
        assert data["metadata"]["num_experts"] == 2

    def test_with_errors(self):
        """Test result with errors."""
        result = ExportResult(
            success=False,
            export_dir=Path("/exports/unit"),
            unit_id="fundraising",
            errors=["Model not found", "Routing failed"],
        )

        data = result.to_dict()

        assert data["success"] is False
        assert len(data["errors"]) == 2


class TestExportIntegration:
    """Integration tests for export workflow."""

    def test_routing_metadata_structure(self, test_settings, tmp_path, mock_moe_model, mock_adapters):
        """Test that routing metadata has correct structure."""
        exporter = Phase4Exporter(test_settings)

        fundraising_adapters = [a for a in mock_adapters if a.unit_id == "fundraising"]
        output_dir = tmp_path / "exports" / "fundraising"

        exporter.export_unit(
            unit_id="fundraising",
            model_path=mock_moe_model,
            output_dir=output_dir,
            adapters=fundraising_adapters,
            generate_routing_embeddings=False,
        )

        # Check expert registry structure
        with open(output_dir / "routing" / "expert_registry.json") as f:
            registry = json.load(f)

        assert "unit_id" in registry
        assert "total_experts" in registry
        assert "experts" in registry
        assert registry["total_experts"] == len(fundraising_adapters)

        # Check intent mapping structure
        with open(output_dir / "routing" / "intent_mapping.json") as f:
            intent_map = json.load(f)

        # Should have task-level intents
        assert any(k.startswith("task:") for k in intent_map.keys())

    def test_agent_config_structure(self, test_settings, tmp_path, mock_moe_model, mock_adapters):
        """Test that agent config has correct structure."""
        exporter = Phase4Exporter(test_settings)

        fundraising_adapters = [a for a in mock_adapters if a.unit_id == "fundraising"]
        output_dir = tmp_path / "exports" / "fundraising"

        exporter.export_unit(
            unit_id="fundraising",
            model_path=mock_moe_model,
            output_dir=output_dir,
            adapters=fundraising_adapters,
        )

        # Check agent config structure
        with open(output_dir / "agent_config" / "fundraising_agent.yaml") as f:
            agent_config = yaml.safe_load(f)

        assert "agent" in agent_config
        assert "model" in agent_config
        assert "routing" in agent_config
        assert "tasks" in agent_config

        assert agent_config["agent"]["id"] == "fundraising_agent"
        assert agent_config["model"]["type"] == "moe"
        assert agent_config["model"]["num_experts"] == len(fundraising_adapters)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
