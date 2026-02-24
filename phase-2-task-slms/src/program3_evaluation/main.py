"""Program 3: Evaluation of Task SLMs."""

import argparse
import json
from pathlib import Path

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from both local config and phase-0-infrastructure
from config.settings import Settings, get_settings, load_task_definitions
from habitat_logging import configure_logging, get_logger
from src.program3_evaluation.evaluators.metrics import TaskSLMEvaluator
from src.program3_evaluation.reporters.report_generator import generate_evaluation_report
from src.shared.data_formatter import load_jsonl
from src.shared.environment_detector import detect_environment, get_device
from src.shared.model_loader import ModelLoader

logger = get_logger(__name__)


def load_evaluation_data(
    processed_dir: Path,
    unit_id: str,
    task_id: str,
    max_samples: int | None = None,
) -> list[dict]:
    """
    Load data for evaluation.

    Args:
        processed_dir: Base processed data directory
        unit_id: Unit identifier
        task_id: Task identifier
        max_samples: Maximum samples to load

    Returns:
        List of evaluation examples
    """
    task_dir = processed_dir / unit_id / task_id

    # Try validation set first, fall back to examples
    val_file = task_dir / "val.jsonl"
    examples_file = task_dir / "examples.jsonl"

    if val_file.exists():
        data = load_jsonl(val_file)
    elif examples_file.exists():
        data = load_jsonl(examples_file)
    else:
        raise FileNotFoundError(f"No evaluation data found in {task_dir}")

    if max_samples and len(data) > max_samples:
        data = data[:max_samples]

    logger.info("evaluation_data_loaded", samples=len(data))
    return data


def evaluate_task_slm(
    settings: Settings,
    unit_id: str,
    task_id: str,
    adapter_path: str | Path | None = None,
    num_samples: int | None = None,
) -> dict:
    """
    Evaluate a trained Task SLM.

    Args:
        settings: Application settings
        unit_id: Unit identifier
        task_id: Task identifier
        adapter_path: Path to trained adapter (auto-detect if not provided)
        num_samples: Number of samples to evaluate

    Returns:
        Evaluation metrics dictionary
    """
    base_path = Path(__file__).parent.parent.parent
    env_info = detect_environment()
    device = get_device()

    # Load task definition
    unit_config = next((u for u in settings.units if u.id == unit_id), None)
    if not unit_config:
        raise ValueError(f"Unit not found: {unit_id}")

    unit_def = load_task_definitions(unit_config.tasks_file, base_path)
    task_def = next((t for t in unit_def.tasks if t.id == task_id), None)
    if not task_def:
        raise ValueError(f"Task not found: {task_id}")

    # Find adapter path if not provided
    if adapter_path is None:
        models_dir = base_path / settings.paths.models_dir / unit_id
        if not models_dir.exists():
            raise FileNotFoundError(f"No models found for {unit_id}")

        # Find latest version
        task_dirs = sorted(
            [d for d in models_dir.iterdir() if d.name.startswith(task_id)],
            reverse=True,
        )
        if not task_dirs:
            raise FileNotFoundError(f"No trained model found for {task_id}")
        adapter_path = task_dirs[0]

    adapter_path = Path(adapter_path)
    logger.info("evaluating_model", adapter_path=str(adapter_path))

    # Load model
    loader = ModelLoader(settings)
    model, tokenizer = loader.load_for_inference(adapter_path)

    # Load evaluation data
    num_samples = num_samples or settings.evaluation.num_eval_samples
    processed_dir = base_path / settings.paths.processed_dir
    eval_data = load_evaluation_data(processed_dir, unit_id, task_id, num_samples)

    # Create evaluator
    evaluator = TaskSLMEvaluator(
        model=model,
        tokenizer=tokenizer,
        required_sections=task_def.required_sections,
        device=device,
    )

    # Determine model ID
    model_id = f"{unit_id}/{task_id}_{adapter_path.name}"

    # Run evaluation
    logger.info("starting_evaluation", samples=len(eval_data))
    report = evaluator.evaluate_batch(
        examples=eval_data,
        system_prompt=task_def.system_prompt,
        max_new_tokens=settings.evaluation.max_new_tokens,
        model_id=model_id,
    )

    # Add metadata
    report.metadata = {
        "unit_id": unit_id,
        "task_id": task_id,
        "adapter_path": str(adapter_path),
        "base_model": settings.model.base_model,
        "device": device,
    }

    # Generate reports (including phase-0 standardized format by default)
    eval_dir = base_path / settings.paths.evaluations_dir / unit_id / adapter_path.name
    dataset_id = f"{unit_id}/{task_id}_eval_set"
    report_paths = generate_evaluation_report(
        report,
        eval_dir,
        formats=["json", "md", "phase0"],  # Include phase-0 format
        dataset_id=dataset_id,
    )

    # Return summary
    summary = {
        "model_id": model_id,
        "num_samples": report.num_samples,
        "format_compliance": report.avg_format_compliance,
        "content_coverage": report.avg_content_coverage,
        "latency_ms": report.avg_latency_ms,
        "tokens_per_second": report.avg_tokens_per_second,
        "section_coverage": report.section_coverage,
        "report_paths": {k: str(v) for k, v in report_paths.items()},
    }

    logger.info(
        "evaluation_complete",
        model_id=model_id,
        format_compliance=f"{report.avg_format_compliance:.1%}",
        content_coverage=f"{report.avg_content_coverage:.1%}",
    )

    return summary


def main():
    """Main entry point for evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate Task SLMs")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--unit",
        type=str,
        required=True,
        help="Unit to evaluate",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task to evaluate",
    )
    parser.add_argument(
        "--adapter-path",
        type=str,
        help="Path to trained adapter (auto-detect if not provided)",
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        help="Number of samples to evaluate",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Use test mode settings",
    )
    args = parser.parse_args()

    # Load settings
    config_path = Path(__file__).parent.parent.parent / args.config
    settings = get_settings(config_path)
    settings.test_mode = args.test_mode

    # Configure logging
    configure_logging(
        level=settings.logging.level.upper(),
        format=settings.logging.format if hasattr(settings.logging, 'format') else "console"
    )

    logger.info(
        "evaluation_started",
        unit=args.unit,
        task=args.task,
        adapter_path=args.adapter_path,
    )

    try:
        summary = evaluate_task_slm(
            settings=settings,
            unit_id=args.unit,
            task_id=args.task,
            adapter_path=args.adapter_path,
            num_samples=args.num_samples,
        )

        # Print summary
        print("\n" + "=" * 60)
        print("Evaluation Summary")
        print("=" * 60)
        print(f"Model:              {summary['model_id']}")
        print(f"Samples:            {summary['num_samples']}")
        print(f"Format Compliance:  {summary['format_compliance']:.1%}")
        print(f"Content Coverage:   {summary['content_coverage']:.1%}")
        print(f"Avg Latency:        {summary['latency_ms']:.1f} ms")
        print(f"Tokens/Second:      {summary['tokens_per_second']:.1f}")
        print(f"\nReports saved to:")
        for fmt, path in summary["report_paths"].items():
            print(f"  {fmt}: {path}")
        print("=" * 60)

    except Exception as e:
        logger.exception("evaluation_failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
