"""Tests for config module (conventions and base_settings)."""

from pathlib import Path

import pytest

from config.conventions import ID_FORMAT, make_id, parse_id
from config.base_settings import HabitatBaseSettings, PhaseSettings


class TestConventions:
    """Tests for config.conventions module."""

    def test_id_format_constant(self):
        """Test ID_FORMAT constant is correctly defined."""
        assert ID_FORMAT == "{phase}/{unit}/{task}/{version}"

    def test_make_id_basic(self):
        """Test make_id creates correctly formatted ID."""
        result = make_id(phase=2, unit="program1", task="format-alpaca", version="v1.0.0")
        assert result == "2/program1/format-alpaca/v1.0.0"

    def test_make_id_different_phases(self):
        """Test make_id works with different phase numbers."""
        for phase in range(1, 6):
            result = make_id(phase=phase, unit="unit", task="task", version="v1")
            assert result.startswith(f"{phase}/")

    def test_make_id_special_characters_in_task(self):
        """Test make_id handles special characters in task name."""
        result = make_id(phase=1, unit="unit", task="task-with-dashes", version="v1.0.0")
        assert result == "1/unit/task-with-dashes/v1.0.0"

    def test_parse_id_basic(self):
        """Test parse_id correctly parses a valid ID."""
        result = parse_id("2/program1/format-alpaca/v1.0.0")
        assert result == {
            "phase": 2,
            "unit": "program1",
            "task": "format-alpaca",
            "version": "v1.0.0"
        }

    def test_parse_id_returns_int_for_phase(self):
        """Test parse_id returns phase as integer."""
        result = parse_id("3/unit/task/v1")
        assert isinstance(result["phase"], int)
        assert result["phase"] == 3

    def test_parse_id_invalid_format_too_few_parts(self):
        """Test parse_id raises ValueError for too few parts."""
        with pytest.raises(ValueError, match="Invalid ID format"):
            parse_id("2/program1/task")

    def test_parse_id_invalid_format_too_many_parts(self):
        """Test parse_id raises ValueError for too many parts."""
        with pytest.raises(ValueError, match="Invalid ID format"):
            parse_id("2/program1/task/v1/extra")

    def test_parse_id_empty_string(self):
        """Test parse_id raises ValueError for empty string."""
        with pytest.raises(ValueError, match="Invalid ID format"):
            parse_id("")

    def test_make_id_parse_id_roundtrip(self):
        """Test that make_id and parse_id are inverse operations."""
        original_id = make_id(phase=4, unit="fundraising", task="donor-analysis", version="v2.1.0")
        parsed = parse_id(original_id)

        # Reconstruct the ID
        reconstructed = make_id(
            phase=parsed["phase"],
            unit=parsed["unit"],
            task=parsed["task"],
            version=parsed["version"]
        )
        assert reconstructed == original_id


class TestHabitatBaseSettings:
    """Tests for HabitatBaseSettings class."""

    def test_default_values(self):
        """Test default values are set correctly."""
        settings = HabitatBaseSettings()

        assert settings.test_mode is False
        assert settings.data_dir == Path("./data")
        assert settings.log_level == "INFO"
        assert settings.log_format == "console"

    def test_custom_values(self):
        """Test custom values can be set."""
        settings = HabitatBaseSettings(
            data_dir=Path("/custom/path"),
            log_level="DEBUG",
            log_format="json"
        )

        assert settings.data_dir == Path("/custom/path")
        assert settings.log_level == "DEBUG"
        assert settings.log_format == "json"

    def test_test_mode_via_env_alias(self, monkeypatch):
        """Test test_mode can be set via PHASE0_TEST_MODE env var."""
        monkeypatch.setenv("PHASE0_TEST_MODE", "true")
        settings = HabitatBaseSettings()
        assert settings.test_mode is True

    def test_data_dir_accepts_string(self):
        """Test data_dir accepts string and converts to Path."""
        settings = HabitatBaseSettings(data_dir="/some/path")
        assert isinstance(settings.data_dir, Path)
        assert settings.data_dir == Path("/some/path")


class TestPhaseSettings:
    """Tests for PhaseSettings class."""

    def test_required_phase_field(self):
        """Test that phase is a required field."""
        with pytest.raises(Exception):  # ValidationError
            PhaseSettings()

    def test_phase_with_valid_values(self):
        """Test phase accepts valid values 1-5."""
        for phase_num in range(1, 6):
            settings = PhaseSettings(phase=phase_num)
            assert settings.phase == phase_num

    def test_phase_validation_minimum(self):
        """Test phase rejects values below 1."""
        with pytest.raises(Exception):  # ValidationError
            PhaseSettings(phase=0)

    def test_phase_validation_maximum(self):
        """Test phase rejects values above 5."""
        with pytest.raises(Exception):  # ValidationError
            PhaseSettings(phase=6)

    def test_unit_default_none(self):
        """Test unit defaults to None."""
        settings = PhaseSettings(phase=1)
        assert settings.unit is None

    def test_unit_custom_value(self):
        """Test unit accepts custom value."""
        settings = PhaseSettings(phase=2, unit="fundraising")
        assert settings.unit == "fundraising"

    def test_registry_dir_computed(self):
        """Test registry_dir is computed from data_dir."""
        settings = PhaseSettings(phase=1, data_dir=Path("/custom/data"))
        assert settings.registry_dir == Path("/custom/data/registry")

    def test_registry_dir_with_default_data_dir(self):
        """Test registry_dir with default data_dir."""
        settings = PhaseSettings(phase=1)
        assert settings.registry_dir == Path("./data/registry")

    def test_inherits_base_settings(self):
        """Test PhaseSettings inherits from HabitatBaseSettings."""
        settings = PhaseSettings(phase=3, log_level="WARNING")

        assert settings.log_level == "WARNING"
        assert settings.log_format == "console"  # Default from base
        assert settings.test_mode is False  # Default from base

    def test_test_mode_via_env(self, monkeypatch):
        """Test PhaseSettings test_mode can be set via env var."""
        monkeypatch.setenv("PHASE0_TEST_MODE", "true")
        settings = PhaseSettings(phase=1)
        assert settings.test_mode is True
