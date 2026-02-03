"""Program 5: Export merged MoE models for Phase 4 A2A agents - one per unit."""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import local config BEFORE adding phase-0 to path to avoid conflicts
from config.settings import Settings, get_settings

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import configure_logging, get_logger
from registries.model_registry import ModelRegistry
from registries.schemas import ModelStatus
from src.program5_export.phase4_exporter import ExportResult, Phase4Exporter
from src.program5_export.routing_metadata import (
    RoutingMetadata,
    export_a2a_routing_config,
)
from src.shared.phase2_importer import load_import_manifest

logger = get_logger(__name__)


def _update_registry_export_status(
    registry: ModelRegistry,
    unit_id: str,
    export_result: ExportResult,
) -> None:
    """
    Update model registry with export status.

    Args:
        registry: ModelRegistry instance
        unit_id: Unit identifier
        export_result: ExportResult from successful export
    """
    model_id = f"3/{unit_id}/moe/v1"

    try:
        # Check if model exists in registry
        model = registry.get(model_id)
        if model:
            # Update status to EXPORTED
            registry.update_status(model_id, ModelStatus.EXPORTED)
            logger.info(
                "registry_export_status_updated",
                model_id=model_id,
                unit=unit_id,
                export_dir=str(export_result.export_dir),
            )
        else:
            logger.warning(
                "model_not_found_in_registry",
                model_id=model_id,
                unit=unit_id,
            )
    except Exception as e:
        logger.error(
            "registry_update_failed",
            model_id=model_id,
            error=str(e),
        )


def run_export_all(
    settings: Settings,
    generate_agent_configs: bool = True,
    generate_routing_embeddings: bool = True,
) -> dict[str, ExportResult]:
    """
    Export all units' MoE models for Phase 4.

    Args:
        settings: Application settings
        generate_agent_configs: Generate A2A agent configs
        generate_routing_embeddings: Compute routing embeddings

    Returns:
        Dictionary mapping unit_id to ExportResult
    """
    base_path = Path(__file__).parent.parent.parent

    print("\n" + "=" * 60)
    print("Phase 3: Export for Phase 4 A2A Agents")
    print("  (Exporting 3 MoE packages, one per unit)")
    print("=" * 60)

    # Load adapter metadata from imports
    imports_dir = base_path / settings.paths.imports_dir
    try:
        import_result = load_import_manifest(imports_dir)
        adapters = import_result.adapters
        print(f"\nLoaded {len(adapters)} adapter metadata records across {len(import_result.units)} units")
    except FileNotFoundError:
        print("\nError: No import manifest found.")
        print("Run 'python -m src.program1_import.main' first.")
        sys.exit(1)

    # Initialize exporter
    exporter = Phase4Exporter(settings)

    # Initialize model registry
    data_dir = base_path / settings.paths.data_dir
    registry = ModelRegistry(data_dir=data_dir, test_mode=settings.test_mode)

    # Run export for all units
    results = exporter.export_all(
        adapters=adapters,
        generate_agent_configs=generate_agent_configs and settings.export_config.generate_agent_configs,
        generate_routing_embeddings=generate_routing_embeddings and settings.export_config.generate_routing_embeddings,
    )

    # Report results and update registry
    print("\n" + "=" * 60)
    print("Export Summary:")
    for unit_id, result in sorted(results.items()):
        status = "OK" if result.success else "FAIL"
        num_experts = result.metadata.get("num_experts", 0)
        print(f"\n  {unit_id}: {status}")
        print(f"    Experts: {num_experts}")
        print(f"    Model: {'Yes' if result.model_exported else 'No'}")
        print(f"    Routing: {'Yes' if result.routing_exported else 'No'}")
        print(f"    Agent config: {'Yes' if result.agent_config_exported else 'No'}")
        if result.errors:
            for error in result.errors:
                print(f"    Error: {error}")

        # Update registry for successful exports
        if result.success and result.model_exported:
            _update_registry_export_status(registry, unit_id, result)

    print("\n" + "=" * 60)
    all_success = all(r.success for r in results.values())
    if all_success:
        print("All exports completed successfully!")
    else:
        print("Some exports completed with errors")
    print("=" * 60)

    return results


def run_export_unit(
    settings: Settings,
    unit_id: str,
    model_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    generate_agent_config: bool = True,
    generate_routing_embeddings: bool = True,
) -> ExportResult:
    """
    Export a single unit's MoE model for Phase 4.

    Args:
        settings: Application settings
        unit_id: Unit to export
        model_path: Override model path
        output_dir: Override output directory
        generate_agent_config: Generate A2A agent config
        generate_routing_embeddings: Compute routing embeddings

    Returns:
        ExportResult
    """
    base_path = Path(__file__).parent.parent.parent

    print("\n" + "=" * 60)
    print(f"Phase 3: Export {unit_id} MoE for Phase 4")
    print("=" * 60)

    # Load adapter metadata from imports
    imports_dir = base_path / settings.paths.imports_dir
    try:
        import_result = load_import_manifest(imports_dir)
        unit_adapters = import_result.get_adapters_by_unit(unit_id)
        if not unit_adapters:
            print(f"\nError: No adapters found for unit: {unit_id}")
            sys.exit(1)
        print(f"\nLoaded {len(unit_adapters)} adapter metadata records for {unit_id}")
    except FileNotFoundError:
        print("\nError: No import manifest found.")
        print("Run 'python -m src.program1_import.main' first.")
        sys.exit(1)

    # Determine model path
    if model_path is None:
        model_path = base_path / settings.paths.merged_dir / f"{unit_id}_moe"
    model_path = Path(model_path)

    print(f"Model source: {model_path}")
    if not model_path.exists():
        print("  Warning: Model path does not exist")

    # Initialize exporter
    exporter = Phase4Exporter(settings)

    # Initialize model registry
    data_dir = base_path / settings.paths.data_dir
    registry = ModelRegistry(data_dir=data_dir, test_mode=settings.test_mode)

    # Run export
    result = exporter.export_unit(
        unit_id=unit_id,
        model_path=model_path,
        output_dir=output_dir,
        adapters=unit_adapters,
        generate_agent_config=generate_agent_config and settings.export_config.generate_agent_configs,
        generate_routing_embeddings=generate_routing_embeddings and settings.export_config.generate_routing_embeddings,
    )

    # Report result
    print("\n" + "-" * 40)
    print("Export Summary:")
    print(f"  Export directory: {result.export_dir}")
    print(f"  Model exported: {'Yes' if result.model_exported else 'No'}")
    print(f"  Routing exported: {'Yes' if result.routing_exported else 'No'}")
    print(f"  Agent config: {'Yes' if result.agent_config_exported else 'No'}")

    # Update registry for successful export
    if result.success and result.model_exported:
        _update_registry_export_status(registry, unit_id, result)

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

    print("\n" + "=" * 60)
    if result.success:
        print("Export completed successfully!")

        # List exported files
        print("\nExported structure:")
        for item in sorted(result.export_dir.rglob("*")):
            if item.is_file():
                rel_path = item.relative_to(result.export_dir)
                print(f"  {rel_path}")
    else:
        print("Export completed with errors")
    print("=" * 60)

    return result


def run_test_mode(settings: Settings) -> dict[str, ExportResult]:
    """
    Run test mode export for all units (mock structure).

    Args:
        settings: Application settings

    Returns:
        Dictionary mapping unit_id to ExportResult
    """
    base_path = Path(__file__).parent.parent.parent

    print("\n" + "=" * 60)
    print("Phase 3: Export (TEST MODE)")
    print("  (Exporting 3 mock MoE packages)")
    print("=" * 60)

    # Load import manifest
    imports_dir = base_path / settings.paths.imports_dir
    try:
        import_result = load_import_manifest(imports_dir)
        adapters = import_result.adapters
    except FileNotFoundError:
        print("\nError: No import manifest found.")
        print("Run 'python -m src.program1_import.main --test-mode' first.")
        sys.exit(1)

    print(f"\nLoaded {len(adapters)} mock adapters across {len(import_result.units)} units")

    # Group adapters by unit
    units: dict[str, list] = {}
    for adapter in adapters:
        if adapter.unit_id not in units:
            units[adapter.unit_id] = []
        units[adapter.unit_id].append(adapter)

    # Initialize exporter
    exporter = Phase4Exporter(settings)

    # Initialize model registry
    data_dir = base_path / settings.paths.data_dir
    registry = ModelRegistry(data_dir=data_dir, test_mode=settings.test_mode)

    results = {}

    for unit_id, unit_adapters in sorted(units.items()):
        # Use mock model path
        mock_model_path = base_path / settings.paths.merged_dir / f"{unit_id}_moe"
        output_dir = base_path / settings.paths.exports_dir / "phase4_test" / unit_id

        print(f"\n--- {unit_id} ---")
        print(f"Mock model: {mock_model_path}")
        print(f"Export directory: {output_dir}")

        # Run export (skip embeddings in test mode for speed)
        result = exporter.export_unit(
            unit_id=unit_id,
            model_path=mock_model_path,
            output_dir=output_dir,
            adapters=unit_adapters,
            generate_agent_config=True,
            generate_routing_embeddings=False,  # Skip in test mode
        )

        results[unit_id] = result

        # Generate A2A routing config for this unit
        routing_metadata = RoutingMetadata.from_adapters(
            adapters=unit_adapters,
            experts_per_token=min(
                settings.moe.experts_per_token,
                len(unit_adapters),
            ),
            gate_mode=settings.moe.gate_mode,
            embedding_model=settings.export_config.embedding_model,
        )
        export_a2a_routing_config(routing_metadata, output_dir / "routing")

        status = "OK" if result.success else "FAIL"
        print(f"Status: {status}")

        # Update registry for successful test exports
        if result.success and result.model_exported:
            _update_registry_export_status(registry, unit_id, result)

    # Summary
    print("\n" + "=" * 60)
    print("Test Export Summary:")
    for unit_id, result in sorted(results.items()):
        status = "OK" if result.success else "FAIL"
        num_experts = result.metadata.get("num_experts", 0)
        print(f"  {unit_id}: {status} ({num_experts} experts)")

    # Show structure for first unit
    first_unit = list(results.keys())[0] if results else None
    if first_unit and results[first_unit].success:
        print(f"\nExample export structure ({first_unit}):")
        for item in sorted(results[first_unit].export_dir.rglob("*")):
            if item.is_file():
                rel_path = item.relative_to(results[first_unit].export_dir)
                print(f"  {rel_path}")

    print("=" * 60)

    return results


def main():
    """Main entry point for Program 5: Export."""
    parser = argparse.ArgumentParser(
        description="Export merged MoE models for Phase 4 A2A agents (one per unit)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--unit",
        type=str,
        help="Export specific unit only (e.g., fundraising)",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        help="Path to merged MoE model (for single unit export)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for exports",
    )
    parser.add_argument(
        "--generate-agent-configs",
        action="store_true",
        default=True,
        help="Generate A2A agent configs (default: True)",
    )
    parser.add_argument(
        "--no-agent-configs",
        action="store_true",
        help="Skip agent config generation",
    )
    parser.add_argument(
        "--generate-embeddings",
        action="store_true",
        default=True,
        help="Generate routing embeddings (default: True)",
    )
    parser.add_argument(
        "--no-embeddings",
        action="store_true",
        help="Skip embedding generation",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode",
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

    # Determine feature flags
    generate_agent_configs = not args.no_agent_configs
    generate_embeddings = not args.no_embeddings

    # Run appropriate mode
    if args.test_mode:
        run_test_mode(settings)
    elif args.unit:
        run_export_unit(
            settings=settings,
            unit_id=args.unit,
            model_path=args.model_path,
            output_dir=args.output_dir,
            generate_agent_config=generate_agent_configs,
            generate_routing_embeddings=generate_embeddings,
        )
    else:
        run_export_all(
            settings=settings,
            generate_agent_configs=generate_agent_configs,
            generate_routing_embeddings=generate_embeddings,
        )


if __name__ == "__main__":
    main()
