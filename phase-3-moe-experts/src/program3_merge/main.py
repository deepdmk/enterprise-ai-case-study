"""Program 3: Execute mergekit-moe merge - one per unit.

Creates 3 separate MoE models for the 3 organizational units.
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
from registries.model_registry import ModelRegistry
from registries.schemas import Phase, ModelType, ModelStatus
from src.program3_merge.merger import (
    MergeResult,
    MockMerger,
    MoEMerger,
    check_mergekit_available,
)
from src.program3_merge.progress_tracker import ProgressTracker, print_progress_bar
from src.shared.config_generator import load_mergekit_config

logger = get_logger(__name__)


def _register_moe_model(
    registry: ModelRegistry,
    unit_id: str,
    result: MergeResult,
    config: dict,
    settings: Settings,
) -> None:
    """
    Register a merged MoE model in the model registry.

    Args:
        registry: ModelRegistry instance
        unit_id: Unit identifier (e.g., "fundraising")
        result: MergeResult from successful merge
        config: Loaded mergekit config
        settings: Application settings
    """
    from registries.schemas import RegisteredModel

    # Extract expert names and architecture info for tags
    experts = config.get("experts", [])
    expert_names = []
    for expert in experts:
        source_model = expert.get("source_model", "")
        # Extract task name from source model path if possible
        if "/" in source_model:
            expert_names.append(source_model.split("/")[-1])
        else:
            expert_names.append(source_model)

    # Build tags with expert info and architecture details
    tags = [
        f"num_experts:{len(experts)}",
        f"architecture:{config.get('architecture', 'mixtral')}",
        f"gate_mode:{config.get('gate_mode', 'hidden')}",
        f"experts_per_token:{config.get('experts_per_token', 2)}",
        f"dtype:{config.get('dtype', 'float16')}",
    ]

    # Add expert names as tags
    for expert_name in expert_names:
        tags.append(f"expert:{expert_name}")

    # Create model registration
    model = RegisteredModel(
        model_id=f"3/{unit_id}/moe/v1",
        phase=Phase.PHASE_3,
        unit=unit_id,
        task="moe",  # MoE combines multiple tasks
        model_type=ModelType.MOE,
        base_model=config.get("base_model", ""),
        model_path=str(result.output_dir),
        adapter_path=None,  # MoE models don't use adapters
        status=ModelStatus.TRAINED,
        source_dataset_id=None,  # Could link to phase-2 adapters if needed
        positive_prompts=[],
        negative_prompts=[],
        tags=tags,
    )

    try:
        registry.register(model)
        logger.info(
            "moe_model_registered",
            model_id=model.model_id,
            unit=unit_id,
            num_experts=len(experts),
        )
    except ValueError as e:
        # Model already registered
        logger.warning("moe_model_already_registered", model_id=model.model_id, error=str(e))


def run_merge_all(
    settings: Settings,
    use_cuda: bool | None = None,
    dry_run: bool = False,
) -> dict[str, MergeResult]:
    """
    Merge all units' MoE models.

    Args:
        settings: Application settings
        use_cuda: Override CUDA setting
        dry_run: Validate config without merging

    Returns:
        Dictionary mapping unit_id to MergeResult
    """
    base_path = Path(__file__).parent.parent.parent
    configs_dir = base_path / settings.paths.configs_dir
    merged_dir = base_path / settings.paths.merged_dir

    print("\n" + "=" * 60)
    print("Phase 3: Execute MoE Merge")
    print("  (Creating 3 separate MoE models, one per unit)")
    print("=" * 60)

    # Find all unit configs
    config_files = list(configs_dir.glob("*_moe.yaml"))
    if not config_files:
        print("\nError: No MoE config files found.")
        print("Run 'python -m src.program2_config_gen.main' first.")
        sys.exit(1)

    print(f"\nFound {len(config_files)} unit configurations")

    # Check mergekit availability
    if not dry_run and not check_mergekit_available():
        print("\nWarning: mergekit-moe not found. Install with: pip install mergekit")
        print("Running in dry-run mode instead.")
        dry_run = True

    # Determine CUDA
    cuda = use_cuda if use_cuda is not None else settings.merge.use_cuda
    print(f"CUDA: {'enabled' if cuda else 'disabled'}")

    if dry_run:
        print("\n[DRY RUN] Validating configurations only...")

    # Initialize model registry
    data_dir = base_path / settings.paths.data_dir
    registry = ModelRegistry(data_dir=data_dir, test_mode=settings.test_mode)

    results = {}
    merger = MoEMerger(settings)

    for config_path in sorted(config_files):
        unit_id = config_path.stem.replace("_moe", "")
        output_dir = merged_dir / f"{unit_id}_moe"

        print(f"\n--- {unit_id} ---")
        print(f"Config: {config_path.name}")

        # Load and display config info
        config = load_mergekit_config(config_path)
        num_experts = len(config.get("experts", []))
        print(f"Experts: {num_experts}")

        result = merger.merge(
            config_path=config_path,
            output_dir=output_dir,
            use_cuda=cuda,
            dry_run=dry_run,
        )

        results[unit_id] = result

        status = "VALID" if dry_run and result.success else ("SUCCESS" if result.success else "FAILED")
        print(f"Status: {status}")

        if result.error:
            print(f"Error: {result.error}")
        elif result.duration_seconds and not dry_run:
            print(f"Duration: {result.duration_seconds:.1f}s")

        # Register successful merge in model registry
        if result.success and not dry_run:
            _register_moe_model(registry, unit_id, result, config, settings)

    # Summary
    print("\n" + "=" * 60)
    print("Merge Summary:")
    for unit_id, result in results.items():
        status = "OK" if result.success else "FAIL"
        print(f"  {unit_id}: {status}")
    print("=" * 60)

    return results


def run_merge_unit(
    settings: Settings,
    unit_id: str,
    use_cuda: bool | None = None,
    dry_run: bool = False,
) -> MergeResult:
    """
    Merge a single unit's MoE model.

    Args:
        settings: Application settings
        unit_id: Unit to merge
        use_cuda: Override CUDA setting
        dry_run: Validate config without merging

    Returns:
        MergeResult
    """
    base_path = Path(__file__).parent.parent.parent
    configs_dir = base_path / settings.paths.configs_dir
    merged_dir = base_path / settings.paths.merged_dir

    config_path = configs_dir / f"{unit_id}_moe.yaml"
    output_dir = merged_dir / f"{unit_id}_moe"

    if not config_path.exists():
        print(f"Error: Config not found for unit: {unit_id}")
        print(f"Expected: {config_path}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print(f"Phase 3: Merge {unit_id} MoE")
    print("=" * 60)

    config = load_mergekit_config(config_path)
    num_experts = len(config.get("experts", []))

    print(f"\nConfiguration:")
    print(f"  Config: {config_path}")
    print(f"  Experts: {num_experts}")
    print(f"  Output: {output_dir}")

    cuda = use_cuda if use_cuda is not None else settings.merge.use_cuda
    print(f"  CUDA: {'enabled' if cuda else 'disabled'}")

    # Initialize model registry
    data_dir = base_path / settings.paths.data_dir
    registry = ModelRegistry(data_dir=data_dir, test_mode=settings.test_mode)

    merger = MoEMerger(settings)
    result = merger.merge(
        config_path=config_path,
        output_dir=output_dir,
        use_cuda=cuda,
        dry_run=dry_run,
    )

    print("\n" + "-" * 40)
    if result.success:
        if dry_run:
            print("Configuration validated!")
        else:
            print("Merge completed!")
            print(f"Output: {result.output_dir}")
            if result.duration_seconds:
                print(f"Duration: {result.duration_seconds:.1f}s")

            # Register successful merge in model registry
            _register_moe_model(registry, unit_id, result, config, settings)
    else:
        print("Merge failed!")
        print(f"Error: {result.error}")
    print("=" * 60)

    return result


def run_test_mode(settings: Settings) -> dict[str, MergeResult]:
    """
    Run test mode merge for all units (mock without GPU).

    Args:
        settings: Application settings

    Returns:
        Dictionary mapping unit_id to MergeResult
    """
    base_path = Path(__file__).parent.parent.parent
    configs_dir = base_path / settings.paths.configs_dir
    merged_dir = base_path / settings.paths.merged_dir

    print("\n" + "=" * 60)
    print("Phase 3: Execute Merge (TEST MODE)")
    print("  (Creating 3 mock MoE models)")
    print("=" * 60)

    # Find all unit configs
    config_files = list(configs_dir.glob("*_moe.yaml"))
    if not config_files:
        print("\nError: No MoE config files found.")
        print("Run 'python -m src.program2_config_gen.main --test-mode' first.")
        sys.exit(1)

    print(f"\nFound {len(config_files)} unit configurations")

    # Initialize model registry
    data_dir = base_path / settings.paths.data_dir
    registry = ModelRegistry(data_dir=data_dir, test_mode=settings.test_mode)

    results = {}
    mock_merger = MockMerger(settings)

    for config_path in sorted(config_files):
        unit_id = config_path.stem.replace("_moe", "")
        output_dir = merged_dir / f"{unit_id}_moe"

        print(f"\n--- {unit_id} ---")

        config = load_mergekit_config(config_path)
        num_experts = len(config.get("experts", []))
        print(f"Creating mock MoE with {num_experts} experts...")

        result = mock_merger.create_mock_merge(
            config_path=config_path,
            output_dir=output_dir,
        )

        results[unit_id] = result
        print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
        print(f"Output: {output_dir}")

        # Register successful mock merge in model registry
        if result.success:
            _register_moe_model(registry, unit_id, result, config, settings)

    # Summary
    print("\n" + "=" * 60)
    print("Test Merge Summary:")
    for unit_id, result in sorted(results.items()):
        num_experts = result.metadata.get("num_experts", "?")
        status = "OK" if result.success else "FAIL"
        print(f"  {unit_id}: {status} ({num_experts} experts)")
    print("=" * 60)

    return results


def main():
    """Main entry point for Program 3: Merge."""
    parser = argparse.ArgumentParser(
        description="Execute mergekit-moe merge for each unit"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to application configuration file",
    )
    parser.add_argument(
        "--unit",
        type=str,
        help="Merge specific unit only (e.g., fundraising)",
    )
    parser.add_argument(
        "--cuda",
        action="store_true",
        help="Use CUDA for merge",
    )
    parser.add_argument(
        "--no-cuda",
        action="store_true",
        help="Disable CUDA for merge",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configs without merging",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (mock merge)",
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

    # Determine CUDA setting
    use_cuda = None
    if args.cuda:
        use_cuda = True
    elif args.no_cuda:
        use_cuda = False

    # Configure logging
    configure_logging(level=settings.logging.level.upper(), format="console")

    # Run appropriate mode
    if args.test_mode:
        run_test_mode(settings)
    elif args.unit:
        run_merge_unit(
            settings=settings,
            unit_id=args.unit,
            use_cuda=use_cuda,
            dry_run=args.dry_run,
        )
    else:
        run_merge_all(
            settings=settings,
            use_cuda=use_cuda,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
