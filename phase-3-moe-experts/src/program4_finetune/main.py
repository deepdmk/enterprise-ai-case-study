"""Program 4: Optional MoE fine-tuning to improve routing."""

import argparse
import sys
from pathlib import Path

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import Settings, get_settings
from phase0_infra.habitat_logging import configure_logging, get_logger
from src.program4_finetune.moe_trainer import (
    FineTuneResult,
    MockFineTuner,
    MoEFineTuner,
)

logger = get_logger(__name__)


def run_finetune(
    settings: Settings,
    model_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    training_data: str | Path | None = None,
    epochs: int | None = None,
) -> FineTuneResult:
    """
    Run MoE fine-tuning.

    Args:
        settings: Application settings
        model_path: Path to merged MoE model
        output_dir: Output directory
        training_data: Path to training data
        epochs: Number of training epochs

    Returns:
        FineTuneResult
    """
    base_path = Path(__file__).parent.parent.parent

    print("\n" + "=" * 60)
    print("Phase 3: MoE Fine-tuning (Optional)")
    print("=" * 60)

    # Determine paths
    if model_path is None:
        model_path = base_path / settings.paths.merged_dir / "enterprise_moe_14x8b"
    model_path = Path(model_path)

    if output_dir is None:
        output_dir = base_path / settings.paths.merged_dir / "enterprise_moe_14x8b_finetuned"
    output_dir = Path(output_dir)

    print(f"\nModel path: {model_path}")
    print(f"Output dir: {output_dir}")
    print(f"Epochs: {epochs or settings.finetune.epochs}")
    print(f"Batch size: {settings.finetune.batch_size}")
    print(f"Learning rate: {settings.finetune.learning_rate}")
    print(f"LoRA rank: {settings.finetune.lora_r}")

    if not model_path.exists():
        print(f"\nError: Model not found at {model_path}")
        sys.exit(1)

    # Initialize trainer
    trainer = MoEFineTuner(settings)

    # Run fine-tuning
    print("\nStarting fine-tuning...")
    result = trainer.finetune(
        model_path=model_path,
        output_dir=output_dir,
        training_data_path=training_data,
        epochs=epochs,
    )

    # Report results
    print("\n" + "-" * 40)
    print("Fine-tuning Results:")

    if result.success:
        print(f"  Status: Success")
        print(f"  Output: {result.output_path}")
        if result.duration_seconds:
            print(f"  Duration: {result.duration_seconds:.1f} seconds")
        if result.metrics:
            print(f"\nMetrics:")
            for key, value in result.metrics.items():
                print(f"  {key}: {value}")
    else:
        print(f"  Status: Failed")
        print(f"  Error: {result.error}")

    print("=" * 60)

    return result


def run_test_mode(settings: Settings) -> FineTuneResult:
    """
    Run test mode fine-tuning (mock).

    Args:
        settings: Application settings

    Returns:
        FineTuneResult
    """
    base_path = Path(__file__).parent.parent.parent

    print("\n" + "=" * 60)
    print("Phase 3: MoE Fine-tuning (TEST MODE)")
    print("=" * 60)

    # Use mock model path
    mock_model_path = base_path / settings.paths.merged_dir / "mock_moe"
    output_dir = base_path / settings.paths.merged_dir / "mock_moe_finetuned"

    if not mock_model_path.exists():
        print(f"\nError: Mock model not found at {mock_model_path}")
        print("Run 'python -m src.program3_merge.main --test-mode' first.")
        sys.exit(1)

    print(f"\nMock model path: {mock_model_path}")
    print(f"Output dir: {output_dir}")

    # Use mock trainer
    mock_trainer = MockFineTuner(settings)
    result = mock_trainer.create_mock_finetune(
        model_path=mock_model_path,
        output_dir=output_dir,
    )

    print("\n" + "-" * 40)
    print("Mock Fine-tuning Results:")

    if result.success:
        print(f"  Status: Success (Mock)")
        print(f"  Output: {result.output_path}")
        if result.metrics:
            print(f"\nMock Metrics:")
            for key, value in result.metrics.items():
                print(f"  {key}: {value}")
    else:
        print(f"  Status: Failed")
        print(f"  Error: {result.error}")

    print("=" * 60)

    return result


def check_dependencies() -> bool:
    """Check if required dependencies are available."""
    try:
        import peft
        import transformers
        import trl

        return True
    except ImportError:
        return False


def main():
    """Main entry point for Program 4: Fine-tune."""
    parser = argparse.ArgumentParser(
        description="Optional MoE fine-tuning to improve routing"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        help="Path to merged MoE model",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for fine-tuned model",
    )
    parser.add_argument(
        "--training-data",
        type=str,
        help="Path to training data file",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (mock fine-tuning)",
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check if dependencies are available",
    )

    args = parser.parse_args()

    # Check dependencies
    if args.check_deps:
        if check_dependencies():
            print("All dependencies available")
            sys.exit(0)
        else:
            print("Missing dependencies. Install with:")
            print("  pip install peft transformers trl")
            sys.exit(1)

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

    # Check if fine-tuning is enabled
    if not settings.finetune.enabled and not args.test_mode:
        print("\nFine-tuning is disabled in configuration.")
        print("Set 'finetune.enabled: true' in config.yaml or use --test-mode")
        sys.exit(0)

    # Run appropriate mode
    if args.test_mode:
        run_test_mode(settings)
    else:
        if not check_dependencies():
            print("\nError: Required dependencies not installed.")
            print("Install with: pip install peft transformers trl")
            sys.exit(1)

        run_finetune(
            settings=settings,
            model_path=args.model_path,
            output_dir=args.output_dir,
            training_data=args.training_data,
            epochs=args.epochs,
        )


if __name__ == "__main__":
    main()
