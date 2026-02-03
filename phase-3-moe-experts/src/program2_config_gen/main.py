"""Program 2: Generate mergekit-moe configuration - one per unit.

Creates 3 separate MoE configs for 3 separate models.
"""

import argparse
import sys
from pathlib import Path

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import local config BEFORE adding phase-0 to path to avoid conflicts
from config.settings import Settings, get_settings

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import configure_logging, get_logger
from src.program2_config_gen.mergekit_config import PerUnitMergekitConfigBuilder
from src.program2_config_gen.routing_config import RoutingConfigBuilder
from src.shared.phase2_importer import load_import_manifest

logger = get_logger(__name__)


def run_config_generation(
    settings: Settings,
    import_dir: str | None = None,
) -> None:
    """
    Generate mergekit-moe configuration for each unit.

    Args:
        settings: Application settings
        import_dir: Override import directory
    """
    base_path = Path(__file__).parent.parent.parent

    # Determine import directory
    if import_dir:
        imports_path = Path(import_dir)
    else:
        imports_path = base_path / settings.paths.imports_dir

    print("\n" + "=" * 60)
    print("Phase 3: Generate MoE Configurations")
    print("  (Creating one config per unit for 3 MoE models)")
    print("=" * 60)

    # Load import manifest
    print(f"\nLoading imports from: {imports_path}")
    import_result = load_import_manifest(imports_path)

    print(f"Found {len(import_result.adapters)} adapters across {len(import_result.units)} units")
    print(f"Base model: {import_result.base_model}")

    # Build configs for all units
    config_builder = PerUnitMergekitConfigBuilder(settings)
    configs = config_builder.build_all_configs(import_result=import_result)

    print(f"\nGenerated {len(configs)} MoE configurations:")

    for unit_id, config_path in configs.items():
        with open(config_path) as f:
            config = yaml.safe_load(f)

        num_experts = len(config.get("experts", []))
        experts_per_token = config.get("experts_per_token", 2)

        print(f"\n  {unit_id}:")
        print(f"    Config: {config_path.name}")
        print(f"    Experts: {num_experts}")
        print(f"    Experts per token: {experts_per_token}")

    # Generate routing configs for each unit
    routing_builder = RoutingConfigBuilder(settings)
    configs_dir = base_path / settings.paths.configs_dir

    print("\nGenerating routing configurations...")
    for unit_id in import_result.units:
        unit_adapters = import_result.get_adapters_by_unit(unit_id)
        routing_path = routing_builder.build_routing_config(
            adapters=unit_adapters,
            output_filename=f"{unit_id}_routing.json",
            include_embeddings=False,
        )
        print(f"  {unit_id}: {routing_path.name}")

    print("\n" + "=" * 60)
    print("Configuration generation complete!")
    print(f"  Configs directory: {configs_dir}")
    print("=" * 60)


def run_test_mode(settings: Settings) -> None:
    """
    Generate test mode configurations for each unit.

    Args:
        settings: Application settings
    """
    print("\n" + "=" * 60)
    print("Phase 3: Generate Configuration (TEST MODE)")
    print("  (Creating test configs for 3 mock MoE models)")
    print("=" * 60)

    base_path = Path(__file__).parent.parent.parent
    imports_path = base_path / settings.paths.imports_dir

    # Load import manifest
    try:
        import_result = load_import_manifest(imports_path)
    except FileNotFoundError:
        print("\nError: No import manifest found.")
        print("Run 'python -m src.program1_import.main --test-mode' first.")
        sys.exit(1)

    print(f"\nFound {len(import_result.adapters)} mock adapters across {len(import_result.units)} units")

    # Build test configs
    config_builder = PerUnitMergekitConfigBuilder(settings)
    configs = config_builder.build_test_configs()

    print(f"\nGenerated {len(configs)} test MoE configurations:")

    for unit_id, config_path in sorted(configs.items()):
        with open(config_path) as f:
            config = yaml.safe_load(f)

        num_experts = len(config.get("experts", []))
        print(f"\n  {unit_id}:")
        print(f"    Config: {config_path.name}")
        print(f"    Experts: {num_experts}")
        print(f"    Base model: {config.get('base_model')}")

    # Generate routing configs
    routing_builder = RoutingConfigBuilder(settings)

    print("\nGenerating routing configurations...")
    for unit_id in import_result.units:
        unit_adapters = import_result.get_adapters_by_unit(unit_id)
        routing_path = routing_builder.build_routing_config(
            adapters=unit_adapters,
            output_filename=f"{unit_id}_routing.json",
        )
        print(f"  {unit_id}: {routing_path.name}")

    print("\n" + "=" * 60)
    print("Test configuration complete!")
    print("=" * 60)


def main():
    """Main entry point for Program 2: Config Generation."""
    parser = argparse.ArgumentParser(
        description="Generate mergekit-moe configuration for each unit"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--import-dir",
        type=str,
        help="Override import directory",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Override config output directory",
    )
    parser.add_argument(
        "--unit",
        type=str,
        help="Generate config for specific unit only",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode",
    )
    parser.add_argument(
        "--show-config",
        type=str,
        help="Display an existing config file",
    )

    args = parser.parse_args()

    # Handle show-config
    if args.show_config:
        config_path = Path(args.show_config)
        if not config_path.exists():
            print(f"Config file not found: {config_path}")
            sys.exit(1)

        with open(config_path) as f:
            config = yaml.safe_load(f)

        print(yaml.dump(config, default_flow_style=False, sort_keys=False))
        return

    # Load settings
    config_path = Path(__file__).parent.parent.parent / args.config
    if config_path.exists():
        settings = get_settings(config_path)
    else:
        settings = get_settings()

    # Apply command line overrides
    settings.test_mode = args.test_mode

    if args.output_dir:
        settings.paths.configs_dir = Path(args.output_dir)

    # Configure logging
    configure_logging(level=settings.logging.level.upper(), format="console")

    # Run appropriate mode
    if args.test_mode:
        run_test_mode(settings)
    else:
        run_config_generation(
            settings,
            import_dir=args.import_dir,
        )


if __name__ == "__main__":
    main()
