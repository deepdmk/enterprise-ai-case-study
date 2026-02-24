"""Tests for Program 4: MoE Fine-tuning functionality."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import Settings
from src.program4_finetune.moe_trainer import FineTuneResult, MockFineTuner, MoEFineTuner


class TestMoEFineTuner:
    """Tests for MoEFineTuner class."""

    def test_init(self, test_settings):
        """Test MoEFineTuner initialization."""
        trainer = MoEFineTuner(test_settings)

        assert trainer.settings == test_settings
        assert trainer.base_path.exists()
        assert trainer.merged_dir is not None

    def test_finetune_model_not_found(self, test_settings, tmp_path):
        """Test finetune with non-existent model."""
        trainer = MoEFineTuner(test_settings)

        result = trainer.finetune(
            model_path=tmp_path / "nonexistent_model",
            output_dir=tmp_path / "output",
        )

        assert not result.success
        assert "not found" in result.error.lower()

    def test_finetune_settings_defaults(self, test_settings, tmp_path, mock_moe_model):
        """Test that settings defaults are applied."""
        trainer = MoEFineTuner(test_settings)

        # Mock the _run_lora_finetune method to avoid actual training
        with patch.object(trainer, "_run_lora_finetune") as mock_train:
            mock_result = FineTuneResult(
                success=True,
                model_path=mock_moe_model,
                output_path=tmp_path / "output",
                start_time=MagicMock(),
            )
            mock_train.return_value = mock_result

            result = trainer.finetune(
                model_path=mock_moe_model,
                output_dir=tmp_path / "output",
            )

            # Verify defaults from settings were used
            call_args = mock_train.call_args
            assert call_args.kwargs["epochs"] == test_settings.finetune.epochs
            assert call_args.kwargs["batch_size"] == test_settings.finetune.batch_size
            assert call_args.kwargs["learning_rate"] == test_settings.finetune.learning_rate


class TestMockFineTuner:
    """Tests for MockFineTuner class."""

    def test_init(self, test_settings):
        """Test MockFineTuner initialization."""
        trainer = MockFineTuner(test_settings)

        assert trainer.settings == test_settings
        assert trainer.base_path.exists()

    def test_create_mock_finetune(self, test_settings, tmp_path, mock_moe_model):
        """Test creating mock fine-tuned model."""
        trainer = MockFineTuner(test_settings)

        output_dir = tmp_path / "mock_finetune_output"
        result = trainer.create_mock_finetune(
            model_path=mock_moe_model,
            output_dir=output_dir,
        )

        assert result.success
        assert result.metrics.get("mock") is True
        assert "train_loss" in result.metrics
        assert "train_runtime" in result.metrics

        # Check created files
        assert (output_dir / "final").exists()
        assert (output_dir / "final" / "adapter_config.json").exists()
        assert (output_dir / "finetune_metadata.json").exists()

        # Validate adapter config
        with open(output_dir / "final" / "adapter_config.json") as f:
            adapter_config = json.load(f)
        assert adapter_config["peft_type"] == "LORA"
        assert adapter_config["r"] == test_settings.finetune.lora_r
        assert adapter_config["lora_alpha"] == test_settings.finetune.lora_alpha

    def test_create_mock_finetune_invalid_model(self, test_settings, tmp_path):
        """Test mock finetune handles missing model gracefully."""
        trainer = MockFineTuner(test_settings)

        # Non-existent model path
        model_path = tmp_path / "nonexistent_model"
        output_dir = tmp_path / "output"

        result = trainer.create_mock_finetune(
            model_path=model_path,
            output_dir=output_dir,
        )

        # Should still succeed (mock doesn't require real model)
        assert result.success


class TestFineTuneResult:
    """Tests for FineTuneResult dataclass."""

    def test_duration_seconds(self):
        """Test duration calculation."""
        from datetime import datetime, timedelta

        start = datetime.utcnow()
        end = start + timedelta(seconds=30)

        result = FineTuneResult(
            success=True,
            model_path=Path("/model"),
            output_path=Path("/output"),
            start_time=start,
            end_time=end,
            metrics={"train_loss": 0.5},
        )

        assert result.duration_seconds == 30.0

    def test_duration_seconds_no_end(self):
        """Test duration with no end time."""
        from datetime import datetime

        result = FineTuneResult(
            success=False,
            model_path=Path("/model"),
            output_path=Path("/output"),
            start_time=datetime.utcnow(),
        )

        assert result.duration_seconds is None

    def test_to_dict(self):
        """Test serialization to dict."""
        from datetime import datetime

        start = datetime.utcnow()
        result = FineTuneResult(
            success=True,
            model_path=Path("/model"),
            output_path=Path("/output"),
            start_time=start,
            metrics={"train_loss": 0.5},
        )

        data = result.to_dict()

        assert data["success"] is True
        assert data["model_path"] == "/model"
        assert data["output_path"] == "/output"
        assert data["metrics"] == {"train_loss": 0.5}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
