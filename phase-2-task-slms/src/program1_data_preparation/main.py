"""Program 1: Data Preparation for Task SLM fine-tuning."""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports - MUST BE FIRST for correct config resolution
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import local config BEFORE adding phase-0 to path
from config.settings import Settings, get_settings, load_task_definitions

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import configure_logging, get_logger
from registries.data_registry import DataRegistry
from registries.schemas import DataType, Phase, RegisteredDataset
from src.program1_data_preparation.collectors.base import (
    CSVCollector,
    DirectoryCollector,
    JSONCollector,
    JSONLCollector,
)
from src.program1_data_preparation.validators.quality import (
    DataValidator,
    validate_and_deduplicate,
)
from src.shared.data_formatter import DataFormatter, save_jsonl, split_dataset
from src.shared.mock_data_generator import MockDataGenerator

logger = get_logger(__name__)


def prepare_task_data(
    settings: Settings,
    unit_id: str,
    task_id: str | None = None,
    test_mode: bool = False,
    data_registry: DataRegistry | None = None,
) -> dict[str, dict[str, int]]:
    """
    Prepare training data for a unit's tasks.

    Args:
        settings: Application settings
        unit_id: Unit to prepare data for
        task_id: Optional specific task (all tasks if not specified)
        test_mode: Use mock data generation

    Returns:
        Dictionary with statistics per task
    """
    # Find unit configuration
    unit_config = next((u for u in settings.units if u.id == unit_id), None)
    if not unit_config:
        raise ValueError(f"Unit not found: {unit_id}")

    # Load task definitions
    base_path = Path(__file__).parent.parent.parent
    unit_def = load_task_definitions(unit_config.tasks_file, base_path)

    # Filter to specific task if requested
    tasks = unit_def.tasks
    if task_id:
        tasks = [t for t in tasks if t.id == task_id]
        if not tasks:
            raise ValueError(f"Task not found: {task_id}")

    # Prepare output directory
    processed_dir = base_path / settings.paths.processed_dir / unit_id
    processed_dir.mkdir(parents=True, exist_ok=True)

    stats = {}

    for task in tasks:
        logger.info(
            "preparing_task_data",
            unit=unit_id,
            task=task.id,
            test_mode=test_mode,
        )

        task_dir = processed_dir / task.id
        task_dir.mkdir(parents=True, exist_ok=True)

        if test_mode:
            # Generate mock data
            examples = _generate_mock_data(settings, unit_id, task.id)
        else:
            # Collect real data
            examples = _collect_real_data(settings, unit_id, task.id)

        # Validate and deduplicate
        validator = DataValidator(
            required_output_sections=task.required_sections,
        )
        clean_examples, report, duplicates = validate_and_deduplicate(
            examples, validator=validator
        )

        if len(clean_examples) == 0:
            logger.warning("no_valid_examples", unit=unit_id, task=task.id)
            stats[task.id] = {"total": 0, "train": 0, "val": 0, "invalid": report.invalid_examples}
            continue

        # Split into train/val
        train_examples, val_examples = split_dataset(
            clean_examples,
            train_ratio=settings.data.train_split,
            shuffle=settings.data.shuffle,
            seed=settings.training.seed,
        )

        # Format with system prompt
        formatter = DataFormatter(task.system_prompt)

        # Save formatted data
        train_formatted = formatter.format_batch(train_examples)
        val_formatted = formatter.format_batch(val_examples)

        train_path = task_dir / "train.jsonl"
        val_path = task_dir / "val.jsonl"

        save_jsonl(train_formatted, train_path)
        save_jsonl(val_formatted, val_path)

        # Also save raw examples for reference
        save_jsonl(clean_examples, task_dir / "examples.jsonl")

        stats[task.id] = {
            "total": len(clean_examples),
            "train": len(train_examples),
            "val": len(val_examples),
            "invalid": report.invalid_examples,
            "duplicates_removed": duplicates,
        }

        logger.info(
            "task_data_prepared",
            unit=unit_id,
            task=task.id,
            train=len(train_examples),
            val=len(val_examples),
        )

        # Register dataset with data registry
        if data_registry:
            dataset_id = f"2/{unit_id}/{task.id}/v1"
            source_desc = (
                f"Task examples for {task.name} ({task.id}). "
                f"Data source: {'mock data generator' if test_mode else 'collected from raw data files'}. "
                f"Validated with {len(task.required_sections)} required output sections."
            )

            try:
                registered_dataset = RegisteredDataset(
                    dataset_id=dataset_id,
                    phase=Phase.PHASE_2,
                    unit=unit_id,
                    task=task.id,
                    data_type=DataType.TASK_EXAMPLES,
                    train_path=str(train_path.absolute()),
                    val_path=str(val_path.absolute()) if val_path.exists() else None,
                    train_samples=len(train_examples),
                    val_samples=len(val_examples) if val_examples else 0,
                    source_description=source_desc,
                    tags=["phase2", "task-slm", unit_id, task.id] + (["test-mode"] if test_mode else []),
                )

                data_registry.register(registered_dataset)

                logger.info(
                    "dataset_registered",
                    dataset_id=dataset_id,
                    unit=unit_id,
                    task=task.id,
                    train_samples=len(train_examples),
                    val_samples=len(val_examples),
                )
            except ValueError as e:
                # Dataset already exists - log warning but don't fail
                logger.warning(
                    "dataset_registration_failed",
                    dataset_id=dataset_id,
                    error=str(e),
                )
            except Exception as e:
                logger.error(
                    "dataset_registration_error",
                    dataset_id=dataset_id,
                    error=str(e),
                )

    return stats


def _generate_mock_data(
    settings: Settings,
    unit_id: str,
    task_id: str,
) -> list[dict[str, str]]:
    """Generate mock training data for test mode."""
    generator = MockDataGenerator(seed=settings.training.seed)
    num_samples = settings.get_effective_samples()

    try:
        examples = generator.generate_for_unit(
            unit_id=unit_id,
            tasks=[],  # Not used when calling generate_mock_dataset directly
            samples_per_task=num_samples,
        ).get(task_id, [])

        # If no templates found, fall back to direct generation
        if not examples:
            from src.shared.mock_data_generator import generate_mock_dataset

            examples = generate_mock_dataset(
                unit_id=unit_id,
                task_id=task_id,
                num_samples=num_samples,
                seed=settings.training.seed,
            )

        logger.info(
            "mock_data_generated",
            unit=unit_id,
            task=task_id,
            count=len(examples),
        )
        return examples

    except ValueError as e:
        logger.warning("mock_generation_failed", error=str(e))
        # Return minimal examples for testing
        return [
            {
                "input": f"Test input for {task_id} task {i}",
                "output": f"Test output for {task_id} task {i}. This is sample content.",
            }
            for i in range(num_samples)
        ]


def _collect_real_data(
    settings: Settings,
    unit_id: str,
    task_id: str,
) -> list[dict[str, str]]:
    """Collect real training data from files."""
    base_path = Path(__file__).parent.parent.parent
    raw_dir = base_path / settings.paths.raw_dir / unit_id / task_id

    if not raw_dir.exists():
        logger.warning("raw_data_dir_not_found", path=str(raw_dir))
        return []

    # Try to collect from directory
    collector = DirectoryCollector(
        directory=raw_dir,
        pattern="*.*",  # Match all supported formats
    )

    try:
        return collector.collect()
    except Exception as e:
        logger.error("data_collection_failed", error=str(e))
        return []


def prepare_all_units(
    settings: Settings,
    test_mode: bool = False,
    data_registry: DataRegistry | None = None,
) -> dict[str, dict[str, dict[str, int]]]:
    """
    Prepare data for all units and tasks.

    Args:
        settings: Application settings
        test_mode: Use mock data generation
        data_registry: Optional data registry for dataset registration

    Returns:
        Nested dictionary with statistics per unit and task
    """
    all_stats = {}

    for unit_config in settings.units:
        logger.info("preparing_unit", unit=unit_config.id)
        try:
            unit_stats = prepare_task_data(
                settings=settings,
                unit_id=unit_config.id,
                test_mode=test_mode,
                data_registry=data_registry,
            )
            all_stats[unit_config.id] = unit_stats
        except Exception as e:
            logger.error("unit_preparation_failed", unit=unit_config.id, error=str(e))
            all_stats[unit_config.id] = {"error": str(e)}

    return all_stats


def main():
    """Main entry point for data preparation."""
    parser = argparse.ArgumentParser(description="Prepare training data for Task SLMs")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--unit",
        type=str,
        help="Specific unit to prepare (default: all units)",
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Specific task to prepare (requires --unit)",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Use mock data generation for testing",
    )
    args = parser.parse_args()

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
        "data_preparation_started",
        test_mode=args.test_mode,
        unit=args.unit,
        task=args.task,
    )

    # Initialize data registry
    base_path = Path(__file__).parent.parent.parent
    data_dir = base_path / settings.paths.data_dir
    data_registry = DataRegistry(data_dir=data_dir, test_mode=args.test_mode)

    logger.info(
        "data_registry_initialized",
        registry_file=str(data_registry.registry_file),
        test_mode=args.test_mode,
    )

    # Warn about test mode
    if args.test_mode:
        print("\n" + "=" * 60)
        print("WARNING: Running in TEST MODE")
        print("=" * 60)
        print("Generating SYNTHETIC mock data for pipeline verification only.")
        print("Do NOT use models trained on mock data for production.")
        print("\nFor production training, prepare real data in:")
        print("  data/raw/{unit}/{task}/*.jsonl")
        print("Then run without --test-mode flag.")
        print("=" * 60 + "\n")

    try:
        if args.unit:
            # Prepare specific unit
            stats = prepare_task_data(
                settings=settings,
                unit_id=args.unit,
                task_id=args.task,
                test_mode=args.test_mode,
                data_registry=data_registry,
            )
            all_stats = {args.unit: stats}
        else:
            # Prepare all units
            all_stats = prepare_all_units(
                settings=settings,
                test_mode=args.test_mode,
                data_registry=data_registry,
            )

        # Print summary
        print("\n" + "=" * 60)
        print("Data Preparation Summary")
        print("=" * 60)

        total_train = 0
        total_val = 0

        for unit_id, unit_stats in all_stats.items():
            print(f"\n{unit_id}:")
            if isinstance(unit_stats, dict) and "error" not in unit_stats:
                for task_id, task_stats in unit_stats.items():
                    train = task_stats.get("train", 0)
                    val = task_stats.get("val", 0)
                    invalid = task_stats.get("invalid", 0)
                    total_train += train
                    total_val += val
                    print(f"  {task_id}: train={train}, val={val}, invalid={invalid}")
            else:
                print(f"  Error: {unit_stats.get('error', 'Unknown error')}")

        print(f"\nTotal: train={total_train}, val={total_val}")
        print("=" * 60)

        # Print data registry summary
        registry_summary = data_registry.summary()
        print("\n" + "=" * 60)
        print("Data Registry Summary")
        print("=" * 60)
        print(f"Total datasets registered: {registry_summary['total_datasets']}")
        if registry_summary['by_unit']:
            print("\nBy unit:")
            for unit, count in registry_summary['by_unit'].items():
                print(f"  {unit}: {count} datasets")
        if registry_summary.get('total_samples'):
            samples = registry_summary['total_samples']
            print(f"\nTotal samples: train={samples.get('train', 0)}, val={samples.get('val', 0)}")
        print("=" * 60)

        logger.info("data_preparation_complete", total_train=total_train, total_val=total_val)

    except Exception as e:
        logger.exception("data_preparation_failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
