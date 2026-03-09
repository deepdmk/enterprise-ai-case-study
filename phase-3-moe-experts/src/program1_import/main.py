"""Program 1: Import and validate Phase 2 Task SLM exports.

Organizes imports by unit for creating 3 separate MoE models.
"""

import argparse
import sys
from pathlib import Path

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import Settings, get_settings
from habitat_logging import configure_logging, get_logger
from src.program1_import.importer import MockAdapterGenerator, Phase2AdapterImporter
from src.program1_import.validator import ImportValidator, print_validation_report

logger = get_logger(__name__)


def run_import(settings: Settings, phase2_export_dir: str | None = None) -> None:
    """
    Run Phase 2 import pipeline.

    Args:
        settings: Application settings
        phase2_export_dir: Override Phase 2 export directory
    """
    importer = Phase2AdapterImporter(settings)

    print("\n" + "=" * 60)
    print("Phase 3: Import Phase 2 Task SLM Exports")
    print("  (Organizing by unit for 3 separate MoE models)")
    print("=" * 60)

    result = importer.import_adapters(phase2_export_dir=phase2_export_dir)

    print(f"\nImported {result.total_adapters} adapters across {len(result.units)} units")
    print(f"Base model: {result.base_model}")
    print(f"Import directory: {result.import_dir}")

    # Show per-unit breakdown
    print("\nAdapters per unit:")
    for unit_id in result.units:
        unit_adapters = result.get_adapters_by_unit(unit_id)
        print(f"  {unit_id}: {len(unit_adapters)} adapters")

    # Validate imports
    validator = ImportValidator(expected_base_model=result.base_model)
    validation = validator.validate_import_result(result)

    print_validation_report(validation)

    if not validation.is_valid:
        logger.error("import_validation_failed")
        sys.exit(1)


def run_test_mode(settings: Settings) -> None:
    """
    Run in test mode with mock exports for 3 units.

    Args:
        settings: Application settings
    """
    print("\n" + "=" * 60)
    print("Phase 3: Import (TEST MODE)")
    print("  Generating mock adapters for 3 units")
    print("=" * 60)

    generator = MockAdapterGenerator(settings)
    result = generator.generate_mock_exports()

    print(f"\nGenerated {result.total_adapters} mock adapters across {len(result.units)} units")
    print(f"Base model: {result.base_model}")
    print(f"Import directory: {result.import_dir}")

    # Show per-unit breakdown
    print("\nAdapters per unit (for MoE creation):")
    for unit_id in sorted(result.units):
        unit_adapters = result.get_adapters_by_unit(unit_id)
        print(f"\n  {unit_id} ({len(unit_adapters)} experts):")
        for adapter in unit_adapters:
            print(f"    - {adapter.task_id}")

    # Validate mock imports
    validator = ImportValidator(expected_base_model=result.base_model)
    validation = validator.validate_import_result(result)

    print_validation_report(validation)


def main():
    """Main entry point for Program 1: Import."""
    parser = argparse.ArgumentParser(
        description="Import Phase 2 Task SLM exports for per-unit MoE merging"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--phase2-export",
        type=str,
        help="Path to Phase 2 exports directory",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Override import output directory",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode with mock exports",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing imports, don't copy files",
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

    if args.output_dir:
        settings.paths.imports_dir = Path(args.output_dir)

    # Configure logging
    configure_logging(level=settings.logging.level.upper(), format="console")

    # Run appropriate mode
    if args.test_mode:
        run_test_mode(settings)
    elif args.validate_only:
        # Validate existing imports
        from src.shared.phase2_importer import load_import_manifest

        base_path = Path(__file__).parent.parent.parent
        import_dir = base_path / settings.paths.imports_dir

        result = load_import_manifest(import_dir)
        validator = ImportValidator(expected_base_model=result.base_model)
        validation = validator.validate_import_result(result)
        print_validation_report(validation)
    else:
        run_import(settings, args.phase2_export)


if __name__ == "__main__":
    main()
