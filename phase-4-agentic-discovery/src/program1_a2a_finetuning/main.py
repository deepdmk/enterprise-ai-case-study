"""
Program 1: A2A Fine-Tuning
Main entry point for A2A protocol fine-tuning.

Usage:
    # Generate training data
    python -m src.program1_a2a_finetuning.main --generate-data --unit fundraising

    # Train A2A adapter
    python -m src.program1_a2a_finetuning.main --train --unit fundraising

    # Validate trained adapter
    python -m src.program1_a2a_finetuning.main --validate --unit fundraising

    # Full pipeline
    python -m src.program1_a2a_finetuning.main --full-pipeline --unit fundraising
"""

import argparse
from pathlib import Path
import sys

from .data_generator import A2ADataGenerator
from .a2a_formatter import A2ADataFormatter
from .trainer import A2AFineTuner
from ..shared.phase0_integration import get_phase0_integration


def generate_data(unit_name: str, num_examples: int, test_mode: bool) -> Path:
    """
    Generate A2A training data for a unit.

    Args:
        unit_name: Unit to generate data for
        num_examples: Number of examples to generate
        test_mode: Whether to use test mode (smaller dataset)

    Returns:
        Path to generated dataset
    """
    print(f"\n{'='*60}")
    print(f"Generating A2A Training Data for {unit_name}")
    print(f"{'='*60}\n")

    # Initialize generator
    generator = A2ADataGenerator(unit_name)

    # Generate examples
    print(f"Generating {num_examples} training examples...")
    examples = generator.generate_dataset(num_examples, test_mode=test_mode)

    # Show distribution
    categories = {}
    for ex in examples:
        categories[ex.category] = categories.get(ex.category, 0) + 1

    print("\nDataset distribution:")
    for category, count in sorted(categories.items()):
        percentage = (count / len(examples)) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")

    # Save raw dataset
    raw_output = Path("data/training") / unit_name / "a2a_examples.json"
    generator.save_dataset(examples, str(raw_output))

    # Format for training
    print("\nFormatting examples for training...")
    formatter = A2ADataFormatter(unit_name)
    formatted = formatter.format_examples(examples)

    # Save formatted dataset
    formatted_output = Path("data/training") / unit_name / "a2a_training.jsonl"
    formatter.to_jsonl(formatted, str(formatted_output))

    # Register dataset with Phase 0
    phase0 = get_phase0_integration(Path("data"), test_mode=test_mode)
    if phase0["available"]:
        phase0["data_registry"].register_a2a_training_dataset(
            dataset_id=f"phase-4/{unit_name}/a2a-training/v1",
            unit_name=unit_name,
            train_path=formatted_output,
            num_examples=len(examples),
            category_distribution=categories,
            tags=["a2a", "protocol", "fine-tuning"]
        )

    print(f"\n✓ Data generation complete!")
    print(f"  Raw examples: {raw_output}")
    print(f"  Training data: {formatted_output}")

    return formatted_output


def train_model(unit_name: str, dataset_path: Path, test_mode: bool) -> Path:
    """
    Train A2A adapter for a unit.

    Args:
        unit_name: Unit to train
        dataset_path: Path to training dataset
        test_mode: Whether to use test mode (mock training)

    Returns:
        Path to trained adapter
    """
    # Determine base model path
    base_model_path = Path("../phase-3-moe-experts/data/exports/phase4") / unit_name
    if not base_model_path.exists():
        base_model_path = Path("data/models") / unit_name

    # Initialize trainer
    trainer = A2AFineTuner(
        unit_name=unit_name,
        base_model_path=base_model_path if base_model_path.exists() else None,
        test_mode=test_mode
    )

    # Train
    result = trainer.train(dataset_path, test_mode=test_mode)

    return trainer.output_dir


def validate_model(unit_name: str) -> None:
    """
    Validate trained A2A adapter.

    Args:
        unit_name: Unit to validate
    """
    # Initialize trainer (just for validation)
    trainer = A2AFineTuner(unit_name=unit_name)

    # Run validation
    results = trainer.validate()

    # Print results
    print(f"\nValidation Results:")
    print(f"  Unit: {results['unit_name']}")
    print(f"  Adapter: {results['adapter_path']}")
    print(f"  Test cases: {len(results['test_cases'])}")

    if results['test_cases']:
        success_count = sum(1 for tc in results['test_cases'] if tc['status'] == 'success')
        print(f"  Success rate: {success_count}/{len(results['test_cases'])}")


def full_pipeline(unit_name: str, num_examples: int, test_mode: bool) -> None:
    """
    Run full A2A fine-tuning pipeline.

    Args:
        unit_name: Unit to process
        num_examples: Number of training examples
        test_mode: Whether to use test mode
    """
    print(f"\n{'='*60}")
    print(f"A2A Fine-Tuning Pipeline for {unit_name}")
    print(f"{'='*60}\n")

    # Step 1: Generate data
    print("Step 1/3: Generating training data...")
    dataset_path = generate_data(unit_name, num_examples, test_mode)

    # Step 2: Train
    print("\nStep 2/3: Training A2A adapter...")
    adapter_path = train_model(unit_name, dataset_path, test_mode)

    # Step 3: Validate
    print("\nStep 3/3: Validating adapter...")
    validate_model(unit_name)

    print(f"\n{'='*60}")
    print("✓ Pipeline complete!")
    print(f"{'='*60}\n")
    print(f"Trained adapter saved to: {adapter_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 1: A2A Fine-Tuning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate training data
  python -m src.program1_a2a_finetuning.main --generate-data --unit fundraising

  # Train model
  python -m src.program1_a2a_finetuning.main --train --unit fundraising

  # Validate model
  python -m src.program1_a2a_finetuning.main --validate --unit fundraising

  # Run full pipeline
  python -m src.program1_a2a_finetuning.main --full-pipeline --unit fundraising --test-mode
        """
    )

    # Operation mode
    parser.add_argument("--generate-data", action="store_true",
                       help="Generate training data")
    parser.add_argument("--train", action="store_true",
                       help="Train A2A adapter")
    parser.add_argument("--validate", action="store_true",
                       help="Validate trained adapter")
    parser.add_argument("--full-pipeline", action="store_true",
                       help="Run full pipeline (generate, train, validate)")

    # Required parameters
    parser.add_argument("--unit", required=True,
                       choices=["fundraising", "business_development", "field_operations"],
                       help="Unit to process")

    # Optional parameters
    parser.add_argument("--num-examples", type=int, default=1000,
                       help="Number of training examples to generate (default: 1000)")
    parser.add_argument("--test-mode", action="store_true",
                       help="Use test mode (smaller dataset, mock training)")

    args = parser.parse_args()

    # Validate that at least one operation is specified
    if not any([args.generate_data, args.train, args.validate, args.full_pipeline]):
        parser.error("Must specify at least one operation: --generate-data, --train, --validate, or --full-pipeline")

    try:
        # Run full pipeline
        if args.full_pipeline:
            full_pipeline(args.unit, args.num_examples, args.test_mode)

        # Or run individual steps
        else:
            if args.generate_data:
                dataset_path = generate_data(args.unit, args.num_examples, args.test_mode)
                print(f"\nDataset saved to: {dataset_path}")

            if args.train:
                # Find dataset
                dataset_path = Path("data/training") / args.unit / "a2a_training.jsonl"
                if not dataset_path.exists():
                    print(f"Error: Dataset not found at {dataset_path}")
                    print("Run with --generate-data first")
                    sys.exit(1)

                adapter_path = train_model(args.unit, dataset_path, args.test_mode)
                print(f"\nAdapter saved to: {adapter_path}")

            if args.validate:
                validate_model(args.unit)

    except Exception as e:
        print(f"\nError: {e}")
        if args.test_mode:
            print("\n(Running in test mode - some features use mock implementations)")
        sys.exit(1)


if __name__ == "__main__":
    main()
