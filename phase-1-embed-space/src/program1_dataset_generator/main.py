"""
Program 1: Training Dataset Generator

Extracts samples from PostgreSQL databases and creates training datasets
for fine-tuning the embedding model.

Usage:
    python -m src.program1_dataset_generator.main --config config/config.yaml
    python -m src.program1_dataset_generator.main --test-mode  # Use mock data
"""

import argparse
import asyncio
import random
import sys
from pathlib import Path
from typing import cast

from datasets import Dataset

# Import local config BEFORE adding phase-0 to path
from config.settings import Settings, load_settings

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import configure_logging, get_logger
from registries.data_registry import DataRegistry
from registries.schemas import DataType, Phase, RegisteredDataset

from src.shared.chunking import TextChunker
from src.shared.database import DatabaseConnectionManager

from .extractors.text_extractor import TextDataExtractor, generate_mock_samples
from .pair_generators.contrastive_pairs import (
    ContrastivePair,
    ContrastivePairGenerator,
    PairStrategy,
)

logger = get_logger(__name__)


def pairs_to_dataset(pairs: list[ContrastivePair]) -> Dataset:
    """
    Convert contrastive pairs to a HuggingFace Dataset.

    Args:
        pairs: List of contrastive pairs.

    Returns:
        HuggingFace Dataset with 'anchor' and 'positive' columns.
    """
    data = {
        "anchor": [p.anchor for p in pairs],
        "positive": [p.positive for p in pairs],
    }
    return Dataset.from_dict(data)


def split_dataset(
    dataset: Dataset, train_ratio: float = 0.9, seed: int = 42
) -> tuple[Dataset, Dataset]:
    """
    Split dataset into train and validation sets.

    Args:
        dataset: Dataset to split.
        train_ratio: Ratio of data for training.
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (train_dataset, val_dataset).
    """
    split = dataset.train_test_split(test_size=1 - train_ratio, seed=seed)
    return split["train"], split["test"]


async def run_extraction(
    settings: Settings,
    test_mode: bool = False,
) -> list[ContrastivePair]:
    """
    Run the full extraction and pair generation pipeline.

    Args:
        settings: Application settings.
        test_mode: If True, use mock data instead of real databases.

    Returns:
        List of generated contrastive pairs.
    """
    config = settings.dataset_generator

    if test_mode:
        # Generate mock samples
        logger.info("using_mock_data")
        records = generate_mock_samples(
            num_samples=1000,
            source_db="mock_db",
            source_table="mock_table",
        )
    else:
        # Extract from real databases
        db_manager = DatabaseConnectionManager(settings.databases)
        await db_manager.initialize()

        try:
            extractor = TextDataExtractor(
                db_manager=db_manager,
                min_text_length=config.pair_generation.min_chunk_length,
            )

            records = await extractor.extract_all(
                databases=settings.databases,
                samples_per_table=config.samples_per_table,
            )
        finally:
            await db_manager.close()

    logger.info("extraction_complete", num_records=len(records))

    # Set up chunker and pair generator
    chunker = TextChunker(
        chunk_size=config.chunking.chunk_size,
        chunk_overlap=config.chunking.chunk_overlap,
        min_chunk_length=config.pair_generation.min_chunk_length,
    )

    pair_generator = ContrastivePairGenerator(
        strategy=cast(PairStrategy, config.pair_generation.strategy),
        chunker=chunker,
        min_pair_length=config.pair_generation.min_chunk_length,
    )

    # Generate pairs
    pairs = pair_generator.generate_pairs(records)
    logger.info("pair_generation_complete", num_pairs=len(pairs))

    return pairs


def save_datasets(
    train_dataset: Dataset,
    val_dataset: Dataset,
    output_dir: str | Path,
    data_registry: DataRegistry | None = None,
    test_mode: bool = False,
) -> tuple[Path, Path]:
    """
    Save datasets to disk in Parquet format.

    Args:
        train_dataset: Training dataset.
        val_dataset: Validation dataset.
        output_dir: Directory to save datasets.
        data_registry: Optional data registry for dataset registration.
        test_mode: Whether this is test mode data.

    Returns:
        Tuple of (train_path, val_path).
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    train_path = output_path / "train.parquet"
    val_path = output_path / "validation.parquet"

    train_dataset.to_parquet(str(train_path))
    val_dataset.to_parquet(str(val_path))

    # Save dataset info
    info = {
        "train_samples": len(train_dataset),
        "validation_samples": len(val_dataset),
        "columns": list(train_dataset.column_names),
    }

    import json

    info_path = output_path / "dataset_info.json"
    with open(info_path, "w") as f:
        json.dump(info, f, indent=2)

    logger.info(
        "datasets_saved",
        output_dir=str(output_path),
        train_samples=len(train_dataset),
        val_samples=len(val_dataset),
    )

    # Register datasets with data registry
    if data_registry:
        dataset_id = "1/training/embeddings/v1"
        source_desc = (
            f"Embedding training dataset with contrastive pairs (anchor + positive). "
            f"Data source: {'mock data generator' if test_mode else 'PostgreSQL databases'}. "
            f"Generated from enterprise document corpus for embedding model fine-tuning."
        )

        try:
            registered_dataset = RegisteredDataset(
                dataset_id=dataset_id,
                phase=Phase.PHASE_1,
                data_type=DataType.EMBEDDINGS,
                train_path=str(train_path.absolute()),
                val_path=str(val_path.absolute()),
                train_samples=len(train_dataset),
                val_samples=len(val_dataset),
                source_description=source_desc,
                tags=["phase1", "embeddings", "contrastive-pairs"] + (["test-mode"] if test_mode else []),
            )

            data_registry.register(registered_dataset)

            logger.info(
                "dataset_registered",
                dataset_id=dataset_id,
                train_samples=len(train_dataset),
                val_samples=len(val_dataset),
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

    return train_path, val_path


async def main_async(args: argparse.Namespace, data_registry: DataRegistry | None = None) -> None:
    """Async main function."""
    # Load settings
    if args.config:
        settings = load_settings(args.config)
    else:
        settings = Settings()

    config = settings.dataset_generator

    # Set random seed
    random.seed(config.random_seed)

    # Run extraction
    pairs = await run_extraction(settings, test_mode=args.test_mode)

    if not pairs:
        logger.error("no_pairs_generated")
        return

    # Convert to dataset
    dataset = pairs_to_dataset(pairs)
    logger.info("dataset_created", num_samples=len(dataset))

    # Split into train/val
    train_dataset, val_dataset = split_dataset(
        dataset, train_ratio=config.train_val_split, seed=config.random_seed
    )

    # Save datasets
    save_datasets(
        train_dataset,
        val_dataset,
        config.output_dir,
        data_registry=data_registry,
        test_mode=args.test_mode,
    )

    logger.info(
        "dataset_generation_complete",
        train_samples=len(train_dataset),
        val_samples=len(val_dataset),
    )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate training dataset for embedding fine-tuning"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Use mock data instead of real databases",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(level="INFO", format="console")

    # Initialize data registry
    base_path = Path(__file__).parent.parent.parent
    data_dir = base_path / "data"
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
        print("\nFor production training, configure real databases in:")
        print("  config/config.yaml")
        print("Then run without --test-mode flag.")
        print("=" * 60 + "\n")

    asyncio.run(main_async(args, data_registry=data_registry))


if __name__ == "__main__":
    main()
