"""Program 4: Model Registry for tracking and exporting Task SLMs."""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import local config BEFORE adding phase-0 to path to avoid conflicts
from config.settings import Settings, get_settings, load_task_definitions

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import configure_logging, get_logger
from src.program4_model_registry.exporter import ModelExporter, create_routing_embeddings
from src.shared.model_registry import (
    ModelEntry,
    ModelMetrics,
    ModelRegistry,
    TrainingConfig,
)

logger = get_logger(__name__)


def register_trained_model(
    registry: ModelRegistry,
    settings: Settings,
    unit_id: str,
    task_id: str,
    adapter_path: str | Path,
    metrics: dict | None = None,
) -> ModelEntry:
    """
    Register a newly trained model.

    Args:
        registry: Model registry
        settings: Application settings
        unit_id: Unit identifier
        task_id: Task identifier
        adapter_path: Path to trained adapter
        metrics: Training/evaluation metrics

    Returns:
        Created ModelEntry
    """
    base_path = Path(__file__).parent.parent.parent
    adapter_path = Path(adapter_path)

    # Load task definition for prompts
    unit_config = next((u for u in settings.units if u.id == unit_id), None)
    if not unit_config:
        raise ValueError(f"Unit not found: {unit_id}")

    unit_def = load_task_definitions(unit_config.tasks_file, base_path)
    task_def = next((t for t in unit_def.tasks if t.id == task_id), None)
    if not task_def:
        raise ValueError(f"Task not found: {task_id}")

    # Load training metadata if available
    metadata_file = adapter_path / "training_metadata.json"
    training_config = None
    if metadata_file.exists():
        with open(metadata_file) as f:
            metadata = json.load(f)
            training_config = TrainingConfig(
                epochs=metadata.get("lora_config", {}).get("epochs", settings.training.epochs),
                batch_size=settings.training.batch_size,
                learning_rate=settings.training.learning_rate,
                lora_r=metadata.get("lora_config", {}).get("r", settings.lora.r),
                lora_alpha=metadata.get("lora_config", {}).get("lora_alpha", settings.lora.lora_alpha),
                base_model=metadata.get("base_model", settings.model.base_model),
                train_samples=metadata.get("train_samples", 0),
                val_samples=metadata.get("val_samples", 0),
            )

    # Create metrics object
    model_metrics = None
    if metrics:
        model_metrics = ModelMetrics(
            train_loss=metrics.get("train_loss"),
            eval_loss=metrics.get("eval_loss"),
            format_compliance=metrics.get("format_compliance"),
            content_coverage=metrics.get("content_coverage"),
            generation_latency_ms=metrics.get("latency_ms"),
            tokens_per_second=metrics.get("tokens_per_second"),
        )

    # Register model
    entry = registry.register(
        unit_id=unit_id,
        task_id=task_id,
        adapter_path=str(adapter_path),
        base_model=settings.model.base_model,
        training_config=training_config,
        positive_prompts=task_def.positive_prompts,
        negative_prompts=task_def.negative_prompts,
    )

    # Update metrics if provided
    if model_metrics:
        registry.update_metrics(entry.model_id, model_metrics)

    logger.info(
        "model_registered",
        model_id=entry.model_id,
        adapter_path=str(adapter_path),
    )

    return entry


def scan_and_register_models(
    registry: ModelRegistry,
    settings: Settings,
) -> list[ModelEntry]:
    """
    Scan models directory and register any unregistered models.

    Args:
        registry: Model registry
        settings: Application settings

    Returns:
        List of newly registered models
    """
    base_path = Path(__file__).parent.parent.parent
    models_dir = base_path / settings.paths.models_dir

    if not models_dir.exists():
        logger.warning("models_directory_not_found", path=str(models_dir))
        return []

    registered = []

    # Iterate through unit directories
    for unit_dir in models_dir.iterdir():
        if not unit_dir.is_dir():
            continue

        unit_id = unit_dir.name

        # Iterate through task/version directories
        for task_dir in unit_dir.iterdir():
            if not task_dir.is_dir():
                continue

            # Parse task_id from directory name (format: task_id_version)
            parts = task_dir.name.rsplit("_", 1)
            if len(parts) != 2:
                continue

            task_id = parts[0]

            # Check if already registered
            existing = registry.get_latest(unit_id, task_id)
            if existing and existing.adapter_path == str(task_dir):
                continue

            # Check if this is a valid adapter directory
            if not (task_dir / "adapter_model.safetensors").exists() and \
               not (task_dir / "adapter_config.json").exists():
                continue

            try:
                entry = register_trained_model(
                    registry=registry,
                    settings=settings,
                    unit_id=unit_id,
                    task_id=task_id,
                    adapter_path=task_dir,
                )
                registered.append(entry)
            except Exception as e:
                logger.warning(
                    "registration_failed",
                    path=str(task_dir),
                    error=str(e),
                )

    return registered


def print_registry_summary(registry: ModelRegistry) -> None:
    """Print a summary of the registry."""
    summary = registry.summary()

    print("\n" + "=" * 60)
    print("Model Registry Summary")
    print("=" * 60)
    print(f"Total models: {summary['total_models']}")

    print("\nBy Status:")
    for status, count in summary.get("by_status", {}).items():
        print(f"  {status}: {count}")

    print("\nBy Unit:")
    for unit, count in summary.get("by_unit", {}).items():
        print(f"  {unit}: {count}")

    # List all models
    print("\nRegistered Models:")
    for model in registry.list_models():
        status_icon = {
            "trained": "📦",
            "evaluated": "✅",
            "exported": "🚀",
            "archived": "📁",
        }.get(model.status, "❓")
        print(f"  {status_icon} {model.model_id} ({model.status})")

    print("=" * 60)


def main():
    """Main entry point for model registry operations."""
    parser = argparse.ArgumentParser(description="Model Registry for Task SLMs")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Register command
    register_parser = subparsers.add_parser("register", help="Register a trained model")
    register_parser.add_argument("--unit", type=str, required=True, help="Unit ID")
    register_parser.add_argument("--task", type=str, required=True, help="Task ID")
    register_parser.add_argument("--adapter-path", type=str, required=True, help="Path to adapter")

    # Scan command
    subparsers.add_parser("scan", help="Scan and register new models")

    # List command
    list_parser = subparsers.add_parser("list", help="List registered models")
    list_parser.add_argument("--unit", type=str, help="Filter by unit")
    list_parser.add_argument("--status", type=str, help="Filter by status")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export models for Phase 3")
    export_parser.add_argument("--output-dir", type=str, required=True, help="Output directory")
    export_parser.add_argument("--unit", type=str, help="Export specific unit")
    export_parser.add_argument("--merge", action="store_true", help="Export merged models")

    # Summary command
    subparsers.add_parser("summary", help="Show registry summary")

    # Test mode
    parser.add_argument("--test-mode", action="store_true", help="Use test mode")

    args = parser.parse_args()

    # Load settings
    config_path = Path(__file__).parent.parent.parent / args.config
    settings = get_settings(config_path)
    settings.test_mode = getattr(args, "test_mode", False)

    # Configure logging
    configure_logging(
        level=settings.logging.level.upper(),
        format=settings.logging.format if hasattr(settings.logging, 'format') else "console"
    )

    # Initialize registry
    base_path = Path(__file__).parent.parent.parent
    registry_dir = base_path / settings.paths.registry_dir
    registry = ModelRegistry(registry_dir)

    # Handle commands
    if args.command == "register":
        entry = register_trained_model(
            registry=registry,
            settings=settings,
            unit_id=args.unit,
            task_id=args.task,
            adapter_path=args.adapter_path,
        )
        print(f"Registered: {entry.model_id}")

    elif args.command == "scan":
        registered = scan_and_register_models(registry, settings)
        print(f"Registered {len(registered)} new models")
        for entry in registered:
            print(f"  - {entry.model_id}")

    elif args.command == "list":
        models = registry.list_models(
            unit_id=getattr(args, "unit", None),
            status=getattr(args, "status", None),
        )
        for model in models:
            print(f"{model.model_id} | {model.status} | {model.adapter_path}")

    elif args.command == "export":
        exporter = ModelExporter(registry, settings)

        if args.unit:
            manifest = exporter.export_unit(
                args.unit,
                args.output_dir,
                merge_models=args.merge,
            )
        else:
            manifest = exporter.export_for_moe(
                args.output_dir,
                merge_models=args.merge,
            )

        print(f"Export complete. Manifest saved to {args.output_dir}")

    elif args.command == "summary" or args.command is None:
        print_registry_summary(registry)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
