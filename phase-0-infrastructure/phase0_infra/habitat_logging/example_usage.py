"""Example usage of the logging module.

This script demonstrates how to use the centralized logging infrastructure
for phase-0-infrastructure and downstream phases.

To run this example:
    1. Install dependencies: pip install -e .
    2. Run: python -m logging.example_usage
"""

from phase0_infra.habitat_logging import (
    LOG_EVENTS,
    configure_logging,
    format_experiment_event,
    format_registry_event,
    format_validation_event,
    get_logger,
)


def demo_console_logging() -> None:
    """Demonstrate console (colored, human-readable) logging."""
    print("=" * 80)
    print("DEMO: Console Logging (Human-Readable)")
    print("=" * 80)

    # Configure console logging
    configure_logging(level="INFO", format="console")
    logger = get_logger(__name__)

    # Basic logging with event name
    logger.info("registry_loaded", registry_type="dataset", path="/data/registry.json", count=42)

    # Using format helpers
    logger.info(**format_registry_event(
        "dataset_registered",
        registry_type="dataset",
        path="/data/datasets/train.jsonl",
        dataset_id="train_001",
        size_mb=150.5,
    ))

    # Validation example
    logger.warning(**format_validation_event(
        "validation_failed",
        validator="DatasetValidator",
        passed=False,
        errors=["missing field: name", "invalid type for field: size"],
    ))

    # Experiment tracking
    logger.info(**format_experiment_event(
        "experiment_started",
        experiment_id="exp_001",
        model="llama-3.1-8b",
        dataset="train_001",
    ))

    logger.info(**format_experiment_event(
        "experiment_completed",
        experiment_id="exp_001",
        duration_sec=120.5,
        accuracy=0.95,
        loss=0.12,
    ))

    # Error example
    try:
        raise ValueError("Simulated error for demonstration")
    except ValueError:
        logger.exception("experiment_failed", experiment_id="exp_002")


def demo_json_logging() -> None:
    """Demonstrate JSON (machine-parseable) logging."""
    print("\n" + "=" * 80)
    print("DEMO: JSON Logging (Machine-Parseable)")
    print("=" * 80)

    # Reconfigure for JSON output
    configure_logging(level="INFO", format="json")
    logger = get_logger(__name__)

    # Same logs as above, but in JSON format
    logger.info("model_registered", model_id="model_001", framework="pytorch", size_mb=3200)
    logger.info(
        "model_exported", model_id="model_001", export_path="/exports/model_001.safetensors"
    )

    logger.info(**format_validation_event(
        "validation_passed",
        validator="ConfigValidator",
        passed=True,
        warnings=["deprecated field: old_param"],
    ))


def demo_available_events() -> None:
    """Display all available LOG_EVENTS."""
    print("\n" + "=" * 80)
    print("AVAILABLE LOG_EVENTS")
    print("=" * 80)
    print(f"\nTotal events: {len(LOG_EVENTS)}\n")

    # Group events by category
    categories = {
        "Registry Operations": [
            "registry_loaded", "registry_saved", "dataset_registered",
            "dataset_updated", "model_registered", "model_updated", "model_exported"
        ],
        "Experiment Tracking": [
            "experiment_started", "experiment_completed", "experiment_failed"
        ],
        "Validation": [
            "validation_passed", "validation_failed"
        ],
    }

    for category, events in categories.items():
        print(f"{category}:")
        for event in events:
            desc = LOG_EVENTS.get(event, "Unknown event")
            print(f"  • {event:25s} - {desc}")
        print()


if __name__ == "__main__":
    # Display available events first
    demo_available_events()

    # Demonstrate console logging
    demo_console_logging()

    # Demonstrate JSON logging
    demo_json_logging()

    print("\n" + "=" * 80)
    print("Demo complete! Check the output above for examples.")
    print("=" * 80)
