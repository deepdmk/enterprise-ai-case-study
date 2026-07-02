"""Program 2: Fine-tuning Task SLMs with Unsloth/Transformers."""

import argparse
import json
import sys
from pathlib import Path

# Configure paths once at module load - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from both local config and phase-0-infrastructure
from config.settings import Settings, get_settings, load_task_definitions
from phase0_infra.habitat_logging import configure_logging, get_logger
from phase0_infra.registries.experiment_tracker import ExperimentTracker
from phase0_infra.registries.schemas import (
    Phase,
    HyperparameterConfig,
    TrainingMetrics,
)
from src.shared.data_formatter import load_jsonl
from src.shared.environment_detector import detect_environment, print_environment_info
from src.shared.model_registry import ModelRegistry

logger = get_logger(__name__)


def get_next_version(
    registry_dir: Path,
    unit_id: str,
    task_id: str,
) -> str:
    """
    Get the next version number for a model from the registry.

    Args:
        registry_dir: Path to the registry directory
        unit_id: Unit identifier
        task_id: Task identifier

    Returns:
        Next version string (e.g., "v1", "v2", etc.)
    """
    try:
        registry = ModelRegistry(registry_dir)
        existing = registry.get_latest(unit_id, task_id)

        if existing:
            # Extract version number and increment
            current_version = int(existing.version.replace("v", ""))
            return f"v{current_version + 1}"
        return "v1"
    except Exception as e:
        logger.warning(
            "version_detection_failed",
            unit=unit_id,
            task=task_id,
            error=str(e),
            fallback="v1",
        )
        return "v1"


def load_training_data(
    processed_dir: Path,
    unit_id: str,
    task_id: str,
) -> tuple[list[dict], list[dict]]:
    """
    Load processed training data.

    Args:
        processed_dir: Base processed data directory
        unit_id: Unit identifier
        task_id: Task identifier

    Returns:
        Tuple of (train_examples, val_examples)
    """
    task_dir = processed_dir / unit_id / task_id

    train_file = task_dir / "train.jsonl"
    val_file = task_dir / "val.jsonl"

    if not train_file.exists():
        raise FileNotFoundError(f"Training data not found: {train_file}")

    train_data = load_jsonl(train_file)
    val_data = load_jsonl(val_file) if val_file.exists() else []

    logger.info(
        "training_data_loaded",
        train_samples=len(train_data),
        val_samples=len(val_data),
    )

    return train_data, val_data


def create_dataset(examples: list[dict]):
    """Create HuggingFace Dataset from examples."""
    from datasets import Dataset

    return Dataset.from_list(examples)


def train_task_slm(
    settings: Settings,
    unit_id: str,
    task_id: str,
    output_dir: Path | None = None,
    force_backend: str | None = None,
    experiment_tracker: ExperimentTracker | None = None,
) -> tuple[Path, dict]:
    """
    Train a single Task SLM.

    Args:
        settings: Application settings
        unit_id: Unit identifier
        task_id: Task identifier
        output_dir: Output directory (auto-generated if not provided)
        force_backend: Force specific backend ('unsloth' or 'transformers')
        experiment_tracker: Optional experiment tracker instance

    Returns:
        Tuple of (adapter_path, metrics)
    """
    base_path = Path(__file__).parent.parent.parent

    # Detect environment
    env_info = detect_environment()
    backend = force_backend or env_info.recommended_backend

    logger.info(
        "training_task_slm",
        unit=unit_id,
        task=task_id,
        backend=backend,
    )

    # Load task definition for metadata
    unit_config = next((u for u in settings.units if u.id == unit_id), None)
    if not unit_config:
        raise ValueError(f"Unit not found: {unit_id}")

    unit_def = load_task_definitions(unit_config.tasks_file, base_path)
    task_def = next((t for t in unit_def.tasks if t.id == task_id), None)
    if not task_def:
        raise ValueError(f"Task not found: {task_id}")

    # Load training data
    processed_dir = base_path / settings.paths.processed_dir
    train_data, val_data = load_training_data(processed_dir, unit_id, task_id)

    if not train_data:
        raise ValueError(f"No training data found for {unit_id}/{task_id}")

    # Start experiment tracking
    experiment = None
    if experiment_tracker:
        experiment = experiment_tracker.start_experiment(
            phase=Phase.PHASE_2,
            unit=unit_id,
            task=task_id,
            notes=f"Training with {backend} backend",
        )
        logger.info(
            "experiment_started",
            experiment_id=experiment.experiment_id,
        )

        # Note: Data characteristics (token lengths) are logged in the trainer
        # after the tokenizer is loaded, for accurate token counts

        # Log hyperparameters
        hyperparameters = HyperparameterConfig(
            epochs=settings.training.epochs,
            batch_size=settings.training.batch_size,
            learning_rate=settings.training.learning_rate,
            lora_r=settings.lora.r,
            lora_alpha=settings.lora.lora_alpha,
            warmup_steps=settings.training.warmup_steps,
            weight_decay=settings.training.weight_decay,
        )
        experiment_tracker.log_hyperparameters(
            experiment.experiment_id,
            hyperparameters,
        )

    # Create datasets
    train_dataset = create_dataset(train_data)
    val_dataset = create_dataset(val_data) if val_data else None

    # Determine output directory with auto-incremented version
    version = None
    if output_dir is None:
        registry_dir = base_path / settings.paths.registry_dir
        version = get_next_version(registry_dir, unit_id, task_id)
        output_dir = base_path / settings.paths.models_dir / unit_id / f"{task_id}_{version}"
        logger.info(
            "output_directory_determined",
            unit=unit_id,
            task=task_id,
            version=version,
            output_dir=str(output_dir),
        )
    else:
        # Extract version from output_dir if provided
        dir_name = output_dir.name
        if "_v" in dir_name:
            version = "v" + dir_name.split("_v")[-1]
    output_dir.mkdir(parents=True, exist_ok=True)

    # Train based on backend
    if backend == "unsloth" and env_info.can_use_unsloth:
        from src.program2_fine_tuning.trainer_unsloth import train_with_unsloth

        adapter_path, metrics = train_with_unsloth(
            train_dataset=train_dataset,
            settings=settings,
            output_dir=output_dir,
            eval_dataset=val_dataset,
            experiment_tracker=experiment_tracker,
            experiment_id=experiment.experiment_id if experiment else None,
        )
    else:
        from src.program2_fine_tuning.trainer_transformers import train_with_transformers

        adapter_path, metrics = train_with_transformers(
            train_dataset=train_dataset,
            settings=settings,
            output_dir=output_dir,
            eval_dataset=val_dataset,
            experiment_tracker=experiment_tracker,
            experiment_id=experiment.experiment_id if experiment else None,
        )

    # Log training metrics
    if experiment_tracker and experiment:
        training_metrics = TrainingMetrics(
            train_loss=metrics.get("train_loss", 0.0),
            eval_loss=metrics.get("eval_loss"),
        )
        experiment_tracker.log_training_metrics(
            experiment.experiment_id,
            training_metrics,
        )

    # Save training metadata
    metadata = {
        "unit_id": unit_id,
        "task_id": task_id,
        "task_name": task_def.name,
        "version": version or "v1",  # Include version in metadata
        "base_model": settings.model.base_model,
        "backend": backend,
        "train_samples": len(train_data),
        "val_samples": len(val_data) if val_data else 0,
        "metrics": metrics,
        "positive_prompts": task_def.positive_prompts,
        "negative_prompts": task_def.negative_prompts,
        "lora_config": {
            "r": settings.lora.r,
            "lora_alpha": settings.lora.lora_alpha,
            "target_modules": settings.lora.target_modules,
        },
    }

    if experiment:
        metadata["experiment_id"] = experiment.experiment_id

    with open(output_dir / "training_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(
        "training_complete",
        unit=unit_id,
        task=task_id,
        adapter_path=str(adapter_path),
        train_loss=metrics.get("train_loss"),
    )

    return adapter_path, metrics


def main():
    """Main entry point for fine-tuning."""
    parser = argparse.ArgumentParser(description="Fine-tune Task SLMs")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--unit",
        type=str,
        help="Unit to train (required unless --show-env)",
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Task to train (required unless --show-env)",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Use test mode settings (1 epoch, small batch)",
    )
    parser.add_argument(
        "--backend",
        type=str,
        choices=["unsloth", "transformers"],
        help="Force specific backend",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Custom output directory",
    )
    parser.add_argument(
        "--show-env",
        action="store_true",
        help="Show environment info and exit",
    )
    args = parser.parse_args()

    # Show environment info if requested
    if args.show_env:
        print_environment_info()
        return

    # Validate required arguments when not showing env
    if not args.unit or not args.task:
        parser.error("--unit and --task are required (unless using --show-env)")

    # Load settings
    config_path = Path(__file__).parent.parent.parent / args.config
    settings = get_settings(config_path)
    settings.test_mode = args.test_mode

    # Configure logging
    configure_logging(
        level=settings.logging.level.upper(),
        format=settings.logging.format if hasattr(settings.logging, 'format') else "console"
    )

    # Validate unit and task IDs early before processing
    base_path = Path(__file__).parent.parent.parent
    valid_units = [u.id for u in settings.units]
    if args.unit not in valid_units:
        print(f"\nError: Invalid unit '{args.unit}'")
        print(f"Available units: {', '.join(valid_units)}")
        sys.exit(1)

    # Validate task ID exists in the unit's task definitions
    unit_config = next(u for u in settings.units if u.id == args.unit)
    try:
        unit_def = load_task_definitions(unit_config.tasks_file, base_path)
        valid_tasks = [t.id for t in unit_def.tasks]
        if args.task not in valid_tasks:
            print(f"\nError: Invalid task '{args.task}' for unit '{args.unit}'")
            print(f"Available tasks: {', '.join(valid_tasks)}")
            sys.exit(1)
    except FileNotFoundError as e:
        print(f"\nError: Could not load task definitions: {e}")
        sys.exit(1)

    logger.info(
        "fine_tuning_started",
        unit=args.unit,
        task=args.task,
        test_mode=args.test_mode,
        backend=args.backend,
    )

    # Initialize experiment tracker
    base_path = Path(__file__).parent.parent.parent
    data_dir = base_path / "data"
    tracker = ExperimentTracker(data_dir=data_dir, test_mode=settings.test_mode)

    experiment_id = None
    try:
        # Print environment info
        print_environment_info()

        # Determine output directory
        output_dir = Path(args.output_dir) if args.output_dir else None

        # Train (tracker is passed to train_task_slm)
        adapter_path, metrics = train_task_slm(
            settings=settings,
            unit_id=args.unit,
            task_id=args.task,
            output_dir=output_dir,
            force_backend=args.backend,
            experiment_tracker=tracker,
        )

        # Get experiment ID and version from metadata file
        # The adapter_path tells us where the model was saved
        actual_output_dir = adapter_path.parent if hasattr(adapter_path, 'parent') else Path(adapter_path).parent
        metadata_file = actual_output_dir / "training_metadata.json"
        version = "v1"  # Default fallback

        if metadata_file.exists():
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
                experiment_id = metadata.get("experiment_id")
                version = metadata.get("version", "v1")

        # Mark experiment as completed with correct version
        if experiment_id:
            model_id = f"{args.unit}_{args.task}_{version}"
            tracker.complete_experiment(experiment_id, model_id=model_id)
            logger.info(
                "experiment_completed",
                experiment_id=experiment_id,
                model_id=model_id,
            )

        # Print summary
        print("\n" + "=" * 60)
        print("Fine-tuning Summary")
        print("=" * 60)
        print(f"Unit:           {args.unit}")
        print(f"Task:           {args.task}")
        print(f"Adapter Path:   {adapter_path}")
        print(f"Train Loss:     {metrics.get('train_loss', 'N/A')}")
        if "eval_loss" in metrics:
            print(f"Eval Loss:      {metrics.get('eval_loss')}")
        if experiment_id:
            print(f"Experiment ID:  {experiment_id}")
        print("=" * 60)

    except Exception as e:
        logger.exception("fine_tuning_failed", error=str(e))

        # Mark experiment as failed if we have an experiment_id
        if experiment_id:
            tracker.fail_experiment(experiment_id, error_message=str(e))
            logger.info(
                "experiment_failed",
                experiment_id=experiment_id,
            )

        sys.exit(1)


if __name__ == "__main__":
    main()
