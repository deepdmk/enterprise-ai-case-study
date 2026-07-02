"""
Program 1: Data Conversion - Main Entry Point

Converts Phase 4 discovery logs to training format for orchestrator fine-tuning.
"""

import argparse
from pathlib import Path
import sys
from phase0_infra.habitat_logging import get_logger

from config.settings import get_settings
from .discovery_converter import DiscoveryConverter
from .intent_generator import IntentGenerator
from .data_augmenter import DataAugmenter
from .splitter import DataSplitter
from ..shared.phase0_integration import get_phase0_integration

logger = get_logger(__name__)


def import_phase4_data(args, settings):
    """Import Phase 4 discovery data"""
    logger.info("step_1_import_phase4", test_mode=args.test_mode)

    converter = DiscoveryConverter(settings.paths.phase4_exports_dir)

    # Import to local directory
    if args.test_mode:
        logger.info("test_mode_using_mock_data")
        examples = converter.create_mock_data(count=settings.data_conversion.test_mode_samples)
    else:
        examples = converter.convert_training_examples(test_mode=False)

    # Export to local imports directory
    converter.export_training_data(examples, settings.paths.phase4_imports_dir)

    logger.info("import_complete", count=len(examples))
    return examples


def generate_intents(args, settings, base_examples):
    """Generate synthetic user intents"""
    logger.info("step_2_generate_intents", test_mode=args.test_mode)

    generator = IntentGenerator()

    max_per_workflow = settings.data_conversion.max_synthetic_intents
    if args.test_mode:
        max_per_workflow = 2  # Limit in test mode

    synthetic_examples = generator.generate_intents(
        existing_examples=base_examples,
        max_per_workflow=max_per_workflow
    )

    logger.info("intents_generated", count=len(synthetic_examples))
    return base_examples + synthetic_examples


def augment_data(args, settings, examples):
    """Augment data through paraphrasing and variations"""
    logger.info("step_3_augment_data", test_mode=args.test_mode)

    augmenter = DataAugmenter()

    augmentation_factor = settings.data_conversion.augmentation_factor
    if args.test_mode:
        augmentation_factor = 1  # Minimal augmentation in test mode

    augmented = augmenter.augment_examples(
        examples=examples,
        augmentation_factor=augmentation_factor,
        test_mode=args.test_mode
    )

    # Balance dataset
    balanced = augmenter.balance_dataset(augmented)

    logger.info("augmentation_complete", count=len(balanced))
    return balanced


def create_splits(args, settings, examples):
    """Create train/val/test splits"""
    logger.info("step_4_create_splits", test_mode=args.test_mode)

    splitter = DataSplitter(
        train_ratio=settings.data_conversion.train_split,
        val_ratio=settings.data_conversion.val_split,
        test_ratio=settings.data_conversion.test_split
    )

    train, val, test = splitter.split(examples, stratify_by="agent")

    # Export splits
    splitter.export_splits(train, val, test, settings.paths.training_dir)

    # Register with Phase 0 (if available)
    phase0 = get_phase0_integration(settings.paths.data_dir, test_mode=args.test_mode)
    if phase0["available"]:
        phase0["data_registry"].register_converted_dataset(
            dataset_id="phase-5/orchestrator/converted/v1",
            train_path=settings.paths.training_dir / "train_chat.jsonl",
            val_path=settings.paths.training_dir / "val_chat.jsonl",
            test_path=settings.paths.training_dir / "test_chat.jsonl",
            train_samples=len(train),
            val_samples=len(val),
            test_samples=len(test),
            source_description="Phase 4 discovery logs converted to orchestrator training data",
            tags=["orchestrator", "routing", "chatml", "phase-4-derived"]
        )

    logger.info(
        "splits_created",
        train=len(train),
        val=len(val),
        test=len(test)
    )

    return train, val, test


def run_full_pipeline(args, settings):
    """Run full data conversion pipeline"""
    logger.info("running_full_pipeline", test_mode=args.test_mode)

    # Step 1: Import Phase 4 data
    base_examples = import_phase4_data(args, settings)

    # Step 2: Generate synthetic intents
    examples_with_intents = generate_intents(args, settings, base_examples)

    # Step 3: Augment data
    augmented_examples = augment_data(args, settings, examples_with_intents)

    # Step 4: Create splits
    train, val, test = create_splits(args, settings, augmented_examples)

    logger.info(
        "pipeline_complete",
        total_examples=len(augmented_examples),
        train=len(train),
        val=len(val),
        test=len(test)
    )

    print("\n" + "="*80)
    print("Data Conversion Pipeline Complete")
    print("="*80)
    print(f"Total examples: {len(augmented_examples)}")
    print(f"Training set:   {len(train)}")
    print(f"Validation set: {len(val)}")
    print(f"Test set:       {len(test)}")
    print(f"\nOutputs saved to: {settings.paths.training_dir}")
    print("="*80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 1: Data Conversion - Convert Phase 4 discovery logs to training format"
    )

    # Actions
    parser.add_argument(
        "--import-phase4",
        action="store_true",
        help="Import Phase 4 discovery data"
    )
    parser.add_argument(
        "--generate-intents",
        action="store_true",
        help="Generate synthetic user intents"
    )
    parser.add_argument(
        "--augment",
        action="store_true",
        help="Augment data through paraphrasing"
    )
    parser.add_argument(
        "--create-splits",
        action="store_true",
        help="Create train/val/test splits"
    )
    parser.add_argument(
        "--full-pipeline",
        action="store_true",
        help="Run full pipeline (all steps)"
    )

    # Configuration
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (small sample, fast)"
    )

    args = parser.parse_args()

    # Load settings
    config_path = Path(args.config)
    settings = get_settings(config_path if config_path.exists() else None)

    # Override test mode from args
    if args.test_mode:
        settings.test_mode = True

    # Check if any action was specified
    if not any([
        args.import_phase4,
        args.generate_intents,
        args.augment,
        args.create_splits,
        args.full_pipeline
    ]):
        parser.print_help()
        sys.exit(1)

    try:
        if args.full_pipeline:
            run_full_pipeline(args, settings)

        else:
            # Run individual steps
            if args.import_phase4:
                import_phase4_data(args, settings)

            if args.generate_intents:
                # Need base examples
                converter = DiscoveryConverter(settings.paths.phase4_exports_dir)
                if args.test_mode:
                    base_examples = converter.create_mock_data(100)
                else:
                    base_examples = converter.convert_training_examples()

                generate_intents(args, settings, base_examples)

            if args.augment:
                # Need base examples
                from .discovery_converter import DiscoveryConverter
                converter = DiscoveryConverter(settings.paths.phase4_exports_dir)
                if args.test_mode:
                    examples = converter.create_mock_data(100)
                else:
                    examples = converter.convert_training_examples()

                augment_data(args, settings, examples)

            if args.create_splits:
                # Need examples
                from .discovery_converter import DiscoveryConverter
                converter = DiscoveryConverter(settings.paths.phase4_exports_dir)
                if args.test_mode:
                    examples = converter.create_mock_data(100)
                else:
                    examples = converter.convert_training_examples()

                create_splits(args, settings, examples)

        logger.info("program_complete")

    except Exception as e:
        logger.error("program_failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
