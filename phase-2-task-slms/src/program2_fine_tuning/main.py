"""Program 2: Fine-tuning Task SLMs with Unsloth/Transformers."""

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
from registries.experiment_tracker import ExperimentTracker
from registries.schemas import (
    Phase,
    DataCharacteristics,
    HyperparameterConfig,
    TrainingMetrics,
)
from src.shared.data_formatter import load_jsonl
from src.shared.environment_detector import detect_environment, print_environment_info

logger = get_logger(__name__)


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


def calculate_avg_lengths(data: list[dict]) -> tuple[float, float]:
    """
    Calculate average input and output lengths.

    Args:
        data: List of examples with 'text' field

    Returns:
        Tuple of (avg_input_length, avg_output_length) in tokens
    """
    if not data:
        return 0.0, 0.0

    # Simple approximation: split by whitespace
    total_input = 0
    total_output = 0
    count = 0

    for example in data:
        text = example.get("text", "")
        # Split on common separators to find input/output
        if "### Response:" in text:
            parts = text.split("### Response:")
            input_text = parts[0]
            output_text = parts[1] if len(parts) > 1 else ""
        elif "### Output:" in text:
            parts = text.split("### Output:")
            input_text = parts[0]
            output_text = parts[1] if len(parts) > 1 else ""
        else:
            # Approximate: first half is input, second half is output
            tokens = text.split()
            mid = len(tokens) // 2
            input_text = " ".join(tokens[:mid])
            output_text = " ".join(tokens[mid:])

        total_input += len(input_text.split())
        total_output += len(output_text.split())
        count += 1

    avg_input = total_input / count if count > 0 else 0.0
    avg_output = total_output / count if count > 0 else 0.0

    return avg_input, avg_output


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

        # Log data characteristics
        avg_input, avg_output = calculate_avg_lengths(train_data)
        characteristics = DataCharacteristics(
            num_samples=len(train_data),
            avg_input_length=avg_input,
            avg_output_length=avg_output,
        )
        experiment_tracker.log_data_characteristics(
            experiment.experiment_id,
            characteristics,
        )

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

    # Determine output directory
    if output_dir is None:
        version = "v1"  # TODO: Auto-increment from registry
        output_dir = base_path / settings.paths.models_dir / unit_id / f"{task_id}_{version}"
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
        required=True,
        help="Unit to train",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task to train",
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

    # Load settings
    config_path = Path(__file__).parent.parent.parent / args.config
    settings = get_settings(config_path)
    settings.test_mode = args.test_mode

    # Configure logging
    configure_logging(
        level=settings.logging.level.upper(),
        format=settings.logging.format if hasattr(settings.logging, 'format') else "console"
    )

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

        # Get experiment ID from metadata file if available
        if output_dir:
            metadata_file = output_dir / "training_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    experiment_id = metadata.get("experiment_id")
        else:
            # Construct the default output dir to find metadata
            version = "v1"
            default_output_dir = base_path / settings.paths.models_dir / args.unit / f"{args.task}_{version}"
            metadata_file = default_output_dir / "training_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    experiment_id = metadata.get("experiment_id")

        # Mark experiment as completed
        if experiment_id:
            model_id = f"{args.unit}_{args.task}_v1"
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
