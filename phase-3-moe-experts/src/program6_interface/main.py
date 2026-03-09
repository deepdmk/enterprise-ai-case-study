"""Program 6: Staff interface for MoE model interaction."""

import argparse
from pathlib import Path

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import get_settings
from habitat_logging import configure_logging, get_logger

from src.program6_interface.gradio_app import create_moe_interface_app

logger = get_logger(__name__)


def main():
    """Main entry point for Program 6: Staff Interface."""
    parser = argparse.ArgumentParser(
        description="Launch staff interface for MoE model interaction"
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
        help="Server host (default: from config)",
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Server port (default: from config)",
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create public sharing link",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode with mock responses (no GPU required)",
    )

    args = parser.parse_args()

    # Load settings
    config_path = Path(__file__).parent.parent.parent / args.config
    if config_path.exists():
        settings = get_settings(config_path)
    else:
        settings = get_settings()

    # Apply command line overrides
    settings.test_mode = args.test_mode

    # Configure logging
    configure_logging(level=settings.logging.level.upper(), format="console")

    # Print startup banner
    print("\n" + "=" * 60)
    print("Phase 3: MoE Staff Interface")
    if args.test_mode:
        print("  [TEST MODE] Using mock responses")
    print("=" * 60)

    # Create and launch app
    app = create_moe_interface_app(
        settings=settings,
        test_mode=args.test_mode,
    )

    host = args.host or settings.interface.gradio.host
    port = args.port or settings.interface.gradio.port
    share = args.share or settings.interface.gradio.share

    print(f"\nStarting server at http://{host}:{port}")
    if share:
        print("Public sharing enabled")

    print("\n" + "-" * 60)

    app.launch(
        host=host,
        port=port,
        share=share,
    )


if __name__ == "__main__":
    main()
