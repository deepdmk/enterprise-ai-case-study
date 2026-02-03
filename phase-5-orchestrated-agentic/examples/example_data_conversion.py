"""
Example: Data Conversion

Demonstrates how to convert Phase 4 discovery logs to training data.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.program1_data_conversion.discovery_converter import DiscoveryConverter
from src.program1_data_conversion.intent_generator import IntentGenerator
from src.program1_data_conversion.data_augmenter import DataAugmenter
from src.program1_data_conversion.splitter import DataSplitter


def main():
    """Run data conversion example"""
    print("="*80)
    print("Example: Data Conversion Pipeline")
    print("="*80)

    # Step 1: Create mock data (for demo purposes)
    print("\nStep 1: Creating mock training data...")
    converter = DiscoveryConverter()
    examples = converter.create_mock_data(count=20)
    print(f"Created {len(examples)} training examples")

    # Show sample
    print("\nSample example:")
    sample = examples[0]
    print(f"  Query: {sample.query}")
    print(f"  Entry Agent: {sample.entry_agent}")
    print(f"  Optimal Depth: {sample.optimal_depth}")

    # Step 2: Generate synthetic intents
    print("\nStep 2: Generating synthetic intents...")
    generator = IntentGenerator()
    synthetic = generator.generate_intents(examples, max_per_workflow=2)
    print(f"Generated {len(synthetic)} synthetic examples")

    all_examples = examples + synthetic
    print(f"Total examples: {len(all_examples)}")

    # Step 3: Augment data
    print("\nStep 3: Augmenting data...")
    augmenter = DataAugmenter()
    augmented = augmenter.augment_examples(
        all_examples,
        augmentation_factor=2,
        test_mode=True
    )
    print(f"Augmented to {len(augmented)} examples")

    # Step 4: Create splits
    print("\nStep 4: Creating train/val/test splits...")
    splitter = DataSplitter(train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
    train, val, test = splitter.split(augmented, stratify_by="agent")

    print(f"Training set:   {len(train)} examples")
    print(f"Validation set: {len(val)} examples")
    print(f"Test set:       {len(test)} examples")

    # Step 5: Export
    output_dir = Path("data/examples/training")
    print(f"\nStep 5: Exporting to {output_dir}...")
    splitter.export_splits(train, val, test, output_dir)

    print("\nExported files:")
    for file in output_dir.glob("*.jsonl"):
        print(f"  {file.name}")

    print("\n" + "="*80)
    print("Example complete!")
    print("="*80)


if __name__ == "__main__":
    main()
