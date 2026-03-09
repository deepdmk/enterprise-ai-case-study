"""Tests for Program 3: MoE Merge functionality."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import Settings
from src.program3_merge.merger import MergeResult, MockMerger, MoEMerger, check_mergekit_available


class TestMoEMerger:
    """Tests for MoEMerger class."""

    def test_init(self, test_settings):
        """Test MoEMerger initialization."""
        merger = MoEMerger(test_settings)

        assert merger.settings == test_settings
        assert merger.base_path.exists()
        assert merger.configs_dir is not None
        assert merger.merged_dir is not None

    def test_merge_config_not_found(self, test_settings, tmp_path):
        """Test merge with non-existent config file."""
        merger = MoEMerger(test_settings)

        result = merger.merge(
            config_path=tmp_path / "nonexistent.yaml",
            output_dir=tmp_path / "output",
        )

        assert not result.success
        assert "not found" in result.error.lower()

    def test_merge_dry_run(self, test_settings, tmp_path, mock_mergekit_config):
        """Test merge dry run validation."""
        merger = MoEMerger(test_settings)

        # Create config file
        config_path = tmp_path / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(mock_mergekit_config, f)

        result = merger.merge(
            config_path=config_path,
            output_dir=tmp_path / "output",
            dry_run=True,
        )

        assert result.success
        assert result.metadata.get("num_experts") == 2

    def test_merge_invalid_config(self, test_settings, tmp_path):
        """Test merge with invalid config."""
        merger = MoEMerger(test_settings)

        # Create invalid config file
        config_path = tmp_path / "invalid_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({"invalid": "config"}, f)

        result = merger.merge(
            config_path=config_path,
            output_dir=tmp_path / "output",
        )

        assert not result.success
        assert "validation failed" in result.error.lower()


class TestMockMerger:
    """Tests for MockMerger class."""

    def test_init(self, test_settings):
        """Test MockMerger initialization."""
        merger = MockMerger(test_settings)

        assert merger.settings == test_settings
        assert merger.base_path.exists()
        assert merger.merged_dir is not None

    def test_create_mock_merge(self, test_settings, tmp_path, mock_mergekit_config):
        """Test creating mock merged model."""
        merger = MockMerger(test_settings)

        # Create config file
        config_path = tmp_path / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(mock_mergekit_config, f)

        output_dir = tmp_path / "mock_output"
        result = merger.create_mock_merge(
            config_path=config_path,
            output_dir=output_dir,
        )

        assert result.success
        assert result.metadata.get("mock") is True
        assert result.metadata.get("num_experts") == 2

        # Check created files
        assert (output_dir / "config.json").exists()
        assert (output_dir / "tokenizer_config.json").exists()
        assert (output_dir / "model.safetensors.index.json").exists()

        # Validate config.json content
        with open(output_dir / "config.json") as f:
            config = json.load(f)
        assert config["model_type"] == "mixtral"
        assert config["num_local_experts"] == 2

    def test_create_mock_merge_invalid_config(self, test_settings, tmp_path):
        """Test mock merge with non-existent config."""
        merger = MockMerger(test_settings)

        result = merger.create_mock_merge(
            config_path=tmp_path / "nonexistent.yaml",
            output_dir=tmp_path / "output",
        )

        assert not result.success
        assert result.error is not None


class TestMergeResult:
    """Tests for MergeResult dataclass."""

    def test_duration_seconds(self):
        """Test duration calculation."""
        from datetime import datetime, timedelta

        start = datetime.utcnow()
        end = start + timedelta(seconds=10)

        result = MergeResult(
            success=True,
            output_dir=Path("/output"),
            config_path=Path("/config.yaml"),
            start_time=start,
            end_time=end,
        )

        assert result.duration_seconds == 10.0

    def test_duration_seconds_no_end(self):
        """Test duration with no end time."""
        from datetime import datetime

        result = MergeResult(
            success=False,
            output_dir=Path("/output"),
            config_path=Path("/config.yaml"),
            start_time=datetime.utcnow(),
        )

        assert result.duration_seconds is None

    def test_to_dict(self):
        """Test serialization to dict."""
        from datetime import datetime

        start = datetime.utcnow()
        result = MergeResult(
            success=True,
            output_dir=Path("/output"),
            config_path=Path("/config.yaml"),
            start_time=start,
            metadata={"key": "value"},
        )

        data = result.to_dict()

        assert data["success"] is True
        assert data["output_dir"] == "/output"
        assert data["config_path"] == "/config.yaml"
        assert data["metadata"] == {"key": "value"}


class TestCheckMergekitAvailable:
    """Tests for mergekit availability check."""

    def test_check_not_available(self):
        """Test when mergekit is not installed."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            assert check_mergekit_available() is False

    def test_check_timeout(self):
        """Test when check times out."""
        import subprocess

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="mergekit-moe", timeout=10)
            assert check_mergekit_available() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
