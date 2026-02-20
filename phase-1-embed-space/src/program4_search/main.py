"""
Program 4: Search & Parent Document Retrieval Application

Provides a Gradio-based search interface for semantic document search
with parent document retrieval from source databases.

Usage:
    python -m src.program4_search.main --config config/config.yaml
    python -m src.program4_search.main --port 7860
    python -m src.program4_search.main --test-mode  # Use mock data
"""

import argparse
import sys
from pathlib import Path

# Import local config BEFORE adding phase-0 to path
from config.settings import Settings, load_settings

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import configure_logging, get_logger

from src.shared.chromadb_client import ChromaDBClient

from .gradio_app import create_search_app

logger = get_logger(__name__)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Launch semantic search application"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Server host (overrides config)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Server port (overrides config)",
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create public Gradio link",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Use mock data for testing",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(level="INFO", format="console")

    # Load settings
    if args.config and Path(args.config).exists():
        settings = load_settings(args.config)
    else:
        settings = Settings()

    # Check if ChromaDB collection has data
    chromadb_client = ChromaDBClient(settings.chromadb)
    try:
        chromadb_client.connect()
        stats = chromadb_client.get_collection_stats()
        if stats.count == 0:
            print("\nWarning: ChromaDB collection is empty!")
            print("Run Program 3 first to ingest data:")
            print("  python -m src.program3_ingestion.main --test-mode")
            print("\nProceeding with empty collection...\n")
    except Exception as e:
        print(f"\nError connecting to ChromaDB: {e}")
        print("Make sure ChromaDB is running:")
        print("  docker-compose -f docker/docker-compose.yml up -d")
        print("\nProceeding anyway (search will fail)...\n")

    # Create search app
    logger.info(
        "starting_search_app",
        host=args.host or settings.search.gradio.host,
        port=args.port or settings.search.gradio.port,
        test_mode=args.test_mode,
    )

    app = create_search_app(
        settings=settings,
        use_mock_fetcher=args.test_mode,
        test_mode=args.test_mode,
    )

    print("\n" + "=" * 50)
    print("ENTERPRISE DOCUMENT SEARCH")
    print("=" * 50)
    print("\nStarting server...")
    print(f"  Host: {args.host or settings.search.gradio.host}")
    print(f"  Port: {args.port or settings.search.gradio.port}")
    if args.test_mode:
        print("  Mode: TEST (using mock document fetcher)")
    print("\nOpen your browser to access the search interface.")
    print("Press Ctrl+C to stop the server.\n")

    # Launch
    app.launch(
        host=args.host,
        port=args.port,
        share=args.share,
    )


if __name__ == "__main__":
    main()
