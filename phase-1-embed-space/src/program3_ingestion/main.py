"""
Program 3: Ingestion Pipeline

Ingests data from PostgreSQL databases into ChromaDB:
1. Reads records from source databases
2. Chunks text
3. Generates embeddings using fine-tuned model
4. Stores embeddings + metadata in ChromaDB (NOT the text)

Usage:
    python -m src.program3_ingestion.main --config config/config.yaml
    python -m src.program3_ingestion.main --incremental  # Incremental sync
    python -m src.program3_ingestion.main --test-mode    # Use mock data
"""

import argparse
import asyncio
import json
from pathlib import Path

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import Settings, load_settings
from phase0_infra.habitat_logging import configure_logging, get_logger

from src.shared.chromadb_client import ChromaDBClient
from src.shared.database import DatabaseConnectionManager, MockDatabaseManager
from src.shared.embedding_model import EmbeddingModelManager

from .pipeline import IngestionPipeline, IngestionStats

logger = get_logger(__name__)


def create_mock_database_manager(settings: Settings) -> MockDatabaseManager:
    """Create a mock database manager with sample data."""
    from src.program1_dataset_generator.extractors.text_extractor import generate_mock_samples

    mock_manager = MockDatabaseManager(settings.databases)

    # Generate mock data for each configured database/table
    for db_name, db_config in settings.databases.items():
        for table_config in db_config.tables:
            # Generate mock records
            samples = generate_mock_samples(
                num_samples=100,
                source_db=db_name,
                source_table=table_config.name,
            )

            # Convert to dict format expected by mock manager
            mock_records = []
            for sample in samples:
                record = {
                    table_config.id_column: sample.doc_id,
                    table_config.timestamp_column: "2024-01-01T00:00:00",
                }
                # Add text columns
                for col in table_config.text_columns:
                    record[col] = sample.combined_text
                # Add metadata columns
                for col in table_config.additional_metadata:
                    record[col] = sample.metadata.get(col, f"mock_{col}")
                mock_records.append(record)

            mock_manager.add_mock_data(db_name, table_config.name, mock_records)

    return mock_manager


async def run_ingestion(
    settings: Settings,
    test_mode: bool = False,
    incremental: bool = False,
) -> IngestionStats:
    """
    Run the ingestion pipeline.

    Args:
        settings: Application settings.
        test_mode: If True, use mock data.
        incremental: If True, only ingest new/updated records.

    Returns:
        IngestionStats with results.
    """
    # Initialize database manager
    db_manager: DatabaseConnectionManager | MockDatabaseManager
    if test_mode:
        logger.info("using_mock_database")
        db_manager = create_mock_database_manager(settings)
        await db_manager.initialize()
    else:
        db_manager = DatabaseConnectionManager(settings.databases)
        await db_manager.initialize()

    try:
        # Initialize ChromaDB client
        chromadb_client = ChromaDBClient(settings.chromadb)
        chromadb_client.connect()

        # Initialize embedding model
        embedding_manager = EmbeddingModelManager(settings.embedding)

        # Create pipeline
        pipeline = IngestionPipeline(
            db_manager=db_manager,
            chromadb_client=chromadb_client,
            embedding_manager=embedding_manager,
            config=settings.ingestion,
        )

        # Run ingestion
        stats = await pipeline.run(
            databases=settings.databases,
            incremental=incremental,
        )

        return stats

    finally:
        await db_manager.close()


def print_stats(stats: IngestionStats) -> None:
    """Print ingestion statistics."""
    print("\n" + "=" * 50)
    print("INGESTION COMPLETE")
    print("=" * 50)
    print(f"\nTotal Records Processed: {stats.total_records}")
    print(f"Total Chunks Created:    {stats.total_chunks}")
    print(f"Total Embeddings:        {stats.total_embeddings}")
    print(f"Duration:                {stats.duration_seconds:.2f} seconds")

    if stats.records_by_db:
        print("\nRecords by Database:")
        for db, count in stats.records_by_db.items():
            print(f"  {db}: {count}")

    if stats.chunks_by_db:
        print("\nChunks by Database:")
        for db, count in stats.chunks_by_db.items():
            print(f"  {db}: {count}")

    if stats.errors:
        print(f"\nErrors ({len(stats.errors)}):")
        for error in stats.errors[:5]:  # Show first 5
            print(f"  - {error}")
        if len(stats.errors) > 5:
            print(f"  ... and {len(stats.errors) - 5} more")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ingest data from PostgreSQL to ChromaDB"
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
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Only ingest new/updated records since last sync",
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Only show collection statistics, don't ingest",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(level="INFO", format="console")

    # Load settings
    if args.config and Path(args.config).exists():
        settings = load_settings(args.config)
    else:
        settings = Settings()

    if args.stats_only:
        # Just show collection stats
        chromadb_client = ChromaDBClient(settings.chromadb)
        chromadb_client.connect()
        collection_stats = chromadb_client.get_collection_stats()
        print(f"\nCollection: {collection_stats.name}")
        print(f"Count:      {collection_stats.count}")
        print(f"Metadata:   {json.dumps(collection_stats.metadata, indent=2)}")
        return

    # Run ingestion
    stats = asyncio.run(
        run_ingestion(
            settings=settings,
            test_mode=args.test_mode,
            incremental=args.incremental,
        )
    )

    print_stats(stats)


if __name__ == "__main__":
    main()
