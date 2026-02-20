"""Tests for habitat_logging module."""

import pytest

from habitat_logging.config import configure_logging, get_logger
from habitat_logging.formatters import (
    LOG_EVENTS,
    format_experiment_event,
    format_registry_event,
    format_validation_event,
    get_event_description,
)


class TestLogEvents:
    """Tests for LOG_EVENTS constant."""

    def test_log_events_is_dict(self):
        """Test LOG_EVENTS is a dictionary."""
        assert isinstance(LOG_EVENTS, dict)

    def test_log_events_contains_registry_events(self):
        """Test LOG_EVENTS contains registry-related events."""
        assert "registry_loaded" in LOG_EVENTS
        assert "registry_saved" in LOG_EVENTS
        assert "dataset_registered" in LOG_EVENTS
        assert "model_registered" in LOG_EVENTS

    def test_log_events_contains_experiment_events(self):
        """Test LOG_EVENTS contains experiment-related events."""
        assert "experiment_started" in LOG_EVENTS
        assert "experiment_completed" in LOG_EVENTS
        assert "experiment_failed" in LOG_EVENTS

    def test_log_events_contains_validation_events(self):
        """Test LOG_EVENTS contains validation-related events."""
        assert "validation_passed" in LOG_EVENTS
        assert "validation_failed" in LOG_EVENTS

    def test_log_events_values_are_strings(self):
        """Test all LOG_EVENTS values are non-empty strings."""
        for event, description in LOG_EVENTS.items():
            assert isinstance(description, str)
            assert len(description) > 0


class TestGetEventDescription:
    """Tests for get_event_description function."""

    def test_known_event(self):
        """Test get_event_description returns description for known event."""
        description = get_event_description("registry_loaded")
        assert description == "Registry file loaded from disk"

    def test_unknown_event_returns_event_name(self):
        """Test get_event_description returns event name for unknown event."""
        unknown_event = "custom_unknown_event"
        description = get_event_description(unknown_event)
        assert description == unknown_event

    def test_all_known_events_have_descriptions(self):
        """Test all events in LOG_EVENTS have valid descriptions."""
        for event in LOG_EVENTS:
            description = get_event_description(event)
            assert description != event  # Should return actual description


class TestFormatRegistryEvent:
    """Tests for format_registry_event function."""

    def test_basic_format(self):
        """Test basic registry event formatting."""
        result = format_registry_event(
            event="registry_loaded",
            registry_type="dataset",
            path="/data/registry.json"
        )

        assert result["event"] == "registry_loaded"
        assert result["registry_type"] == "dataset"
        assert result["path"] == "/data/registry.json"

    def test_with_additional_kwargs(self):
        """Test registry event with additional kwargs."""
        result = format_registry_event(
            event="registry_loaded",
            registry_type="model",
            path="/data/models.json",
            count=42,
            version="1.0"
        )

        assert result["count"] == 42
        assert result["version"] == "1.0"

    def test_returns_dict(self):
        """Test format_registry_event returns a dictionary."""
        result = format_registry_event(
            event="dataset_registered",
            registry_type="dataset",
            path="/path"
        )
        assert isinstance(result, dict)

    def test_kwargs_with_list_values(self):
        """Test kwargs can contain list values."""
        result = format_registry_event(
            event="registry_loaded",
            registry_type="dataset",
            path="/path",
            tags=["tag1", "tag2"]
        )
        assert result["tags"] == ["tag1", "tag2"]


class TestFormatValidationEvent:
    """Tests for format_validation_event function."""

    def test_validation_passed(self):
        """Test formatting validation passed event."""
        result = format_validation_event(
            event="validation_passed",
            validator="DatasetValidator",
            passed=True
        )

        assert result["event"] == "validation_passed"
        assert result["validator"] == "DatasetValidator"
        assert result["passed"] is True

    def test_validation_failed_with_errors(self):
        """Test formatting validation failed event with errors."""
        result = format_validation_event(
            event="validation_failed",
            validator="SchemaValidator",
            passed=False,
            errors=["missing field: name", "invalid type"]
        )

        assert result["event"] == "validation_failed"
        assert result["passed"] is False
        assert result["errors"] == ["missing field: name", "invalid type"]

    def test_with_warnings(self):
        """Test formatting validation event with warnings."""
        result = format_validation_event(
            event="validation_passed",
            validator="ConfigValidator",
            passed=True,
            warnings=["deprecated field"]
        )

        assert result["warnings"] == ["deprecated field"]


class TestFormatExperimentEvent:
    """Tests for format_experiment_event function."""

    def test_experiment_started(self):
        """Test formatting experiment started event."""
        result = format_experiment_event(
            event="experiment_started",
            experiment_id="exp_001"
        )

        assert result["event"] == "experiment_started"
        assert result["experiment_id"] == "exp_001"

    def test_experiment_completed_with_metrics(self):
        """Test formatting experiment completed event with metrics."""
        result = format_experiment_event(
            event="experiment_completed",
            experiment_id="exp_001",
            duration_sec=120.5,
            accuracy=0.95,
            loss=0.05
        )

        assert result["duration_sec"] == 120.5
        assert result["accuracy"] == 0.95
        assert result["loss"] == 0.05

    def test_experiment_failed_with_error(self):
        """Test formatting experiment failed event with error."""
        result = format_experiment_event(
            event="experiment_failed",
            experiment_id="exp_002",
            error="Out of memory"
        )

        assert result["event"] == "experiment_failed"
        assert result["error"] == "Out of memory"


class TestConfigureLogging:
    """Tests for configure_logging function."""

    def test_configure_console_format(self):
        """Test configuring logging with console format."""
        # Should not raise
        configure_logging(level="INFO", format="console")

    def test_configure_json_format(self):
        """Test configuring logging with JSON format."""
        # Should not raise
        configure_logging(level="DEBUG", format="json")

    def test_invalid_format_raises_error(self):
        """Test invalid format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid format"):
            configure_logging(format="xml")

    def test_different_log_levels(self):
        """Test configuring different log levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            # Should not raise
            configure_logging(level=level, format="console")

    def test_case_insensitive_level(self):
        """Test log level is case-insensitive."""
        # Should not raise
        configure_logging(level="debug", format="console")
        configure_logging(level="Debug", format="console")


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_logger(self):
        """Test get_logger returns a logger instance."""
        configure_logging(level="INFO", format="console")
        logger = get_logger("test_module")
        assert logger is not None

    def test_logger_has_log_methods(self):
        """Test returned logger has standard log methods."""
        configure_logging(level="INFO", format="console")
        logger = get_logger("test_module")

        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_different_logger_names(self):
        """Test getting loggers with different names."""
        configure_logging(level="INFO", format="console")

        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        # Both should be valid loggers
        assert logger1 is not None
        assert logger2 is not None

    def test_logger_can_log(self):
        """Test logger can actually log without errors."""
        configure_logging(level="DEBUG", format="json")
        logger = get_logger("test_logging")

        # These should not raise
        logger.debug("debug message", key="value")
        logger.info("info message", count=42)
        logger.warning("warning message")
