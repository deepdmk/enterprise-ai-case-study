"""
Program 2: SLM Fine-tuning - Main Entry Point

Fine-tunes orchestrator models using LoRA.
"""

import argparse
from pathlib import Path
import sys
from habitat_logging import get_logger

from config.settings import get_settings
from .trainer import OrchestratorTrainer
from .evaluator import OrchestratorEvaluator
from ..shared.phase0_integration import get_phase0_integration

logger = get_logger(__name__)


def train_model(args, settings):
    """Train orchestrator model"""
    logger.info("step_1_train_model", test_mode=args.test_mode)

    # Prepare paths
    train_chat_path = settings.paths.training_dir / "train_chat.jsonl"
    val_chat_path = settings.paths.training_dir / "val_chat.jsonl"

    if not train_chat_path.exists():
        logger.error("training_data_not_found", path=str(train_chat_path))
        print(f"Error: Training data not found at {train_chat_path}")
        print("Run: phase5-convert --full-pipeline --test-mode")
        sys.exit(1)

    # Initialize trainer
    base_model = settings.slm_finetuning.base_model
    output_dir = settings.paths.models_dir / "orchestrator_slm"

    trainer = OrchestratorTrainer(
        base_model_name=base_model,
        output_dir=output_dir,
        device=settings.device,
        test_mode=args.test_mode
    )

    if args.test_mode:
        # Create mock adapter
        logger.info("test_mode_creating_mock_adapter")
        OrchestratorTrainer.create_mock_adapter(output_dir / "final")
        return output_dir / "final"

    # Prepare datasets
    train_prepared = settings.paths.training_dir / "train_prepared.jsonl"
    val_prepared = settings.paths.training_dir / "val_prepared.jsonl"

    if not train_prepared.exists():
        logger.info("preparing_training_dataset")
        trainer.prepare_dataset_for_training(train_chat_path, train_prepared)
        if val_chat_path.exists():
            trainer.prepare_dataset_for_training(val_chat_path, val_prepared)

    # LoRA configuration
    lora_config = {
        "r": settings.slm_finetuning.lora_rank,
        "lora_alpha": settings.slm_finetuning.lora_alpha,
        "target_modules": settings.slm_finetuning.target_modules,
        "lora_dropout": settings.slm_finetuning.lora_dropout,
        "bias": "none",
        "task_type": "CAUSAL_LM"
    }

    # Load model
    trainer.load_model_and_tokenizer(
        lora_config=lora_config,
        load_in_8bit=(settings.device == "cuda")
    )

    # Training arguments
    training_args = {
        "num_train_epochs": settings.slm_finetuning.num_epochs,
        "per_device_train_batch_size": settings.slm_finetuning.batch_size,
        "gradient_accumulation_steps": settings.slm_finetuning.gradient_accumulation_steps,
        "learning_rate": settings.slm_finetuning.learning_rate,
        "max_seq_length": settings.slm_finetuning.max_seq_length,
        "warmup_steps": settings.slm_finetuning.warmup_steps,
        "eval_steps": settings.slm_finetuning.eval_steps,
        "save_steps": settings.slm_finetuning.save_steps,
    }

    # Start Phase 0 experiment tracking
    phase0 = get_phase0_integration(settings.paths.data_dir, test_mode=args.test_mode)
    experiment_id = "phase-5/orchestrator/fine-tuning/v1"
    if phase0["available"]:
        phase0["experiment_tracker"].log_finetuning_experiment(
            experiment_id=experiment_id,
            config={
                "base_model": base_model,
                "lora_config": lora_config,
                "training_args": training_args,
                "dataset": "phase-5/orchestrator/converted/v1"
            }
        )

    # Train
    result = trainer.train(
        train_dataset_path=train_prepared,
        val_dataset_path=val_prepared if val_prepared.exists() else None,
        training_args=training_args
    )

    logger.info("training_complete", result=result)

    # Complete Phase 0 experiment
    if phase0["available"]:
        phase0["experiment_tracker"].complete_experiment(
            experiment_id=experiment_id,
            final_metrics={
                "training_loss": result.get('training_loss', 0.0),
                "global_steps": result.get('global_step', 0)
            }
        )

        # Register model
        phase0["model_registry"].register_orchestrator_model(
            model_id="phase-5/orchestrator/qwen2.5-7b/v1",
            model_path=Path(result['output_dir']),
            base_model=base_model,
            source_dataset_id="phase-5/orchestrator/converted/v1",
            lora_config=lora_config,
            tags=["orchestrator", "routing", "lora"]
        )

    print("\n" + "="*80)
    print("Training Complete")
    print("="*80)
    print(f"Output directory: {result['output_dir']}")
    print(f"Training loss: {result.get('training_loss', 'N/A')}")
    print(f"Steps: {result.get('global_step', 'N/A')}")
    print("="*80 + "\n")

    return Path(result['output_dir'])


def evaluate_model(args, settings, model_path=None):
    """Evaluate orchestrator model"""
    logger.info("step_2_evaluate_model", test_mode=args.test_mode)

    # Determine model path
    if model_path is None:
        model_path = settings.paths.models_dir / "orchestrator_slm" / "final"

    if not model_path.exists():
        logger.error("model_not_found", path=str(model_path))
        print(f"Error: Model not found at {model_path}")
        print("Run: phase5-finetune --train --test-mode")
        sys.exit(1)

    # Test dataset
    test_chat_path = settings.paths.training_dir / "test_chat.jsonl"

    if not test_chat_path.exists():
        logger.error("test_data_not_found", path=str(test_chat_path))
        print(f"Error: Test data not found at {test_chat_path}")
        print("Run: phase5-convert --full-pipeline --test-mode")
        sys.exit(1)

    # Initialize evaluator
    evaluator = OrchestratorEvaluator(
        model_path=model_path,
        device=settings.device
    )

    if not args.test_mode:
        # Load model (skip in test mode)
        evaluator.load_model()

    # Evaluate
    max_samples = 10 if args.test_mode else None

    results = evaluator.evaluate(
        test_dataset_path=test_chat_path,
        max_samples=max_samples
    )

    # Export results
    results_path = settings.paths.exports_dir / "evaluation_results.json"
    evaluator.export_results(results, results_path)

    # Compare with baseline
    comparison = evaluator.compare_with_baseline(
        results,
        baseline_accuracy=settings.slm_finetuning.target_accuracy,
        baseline_latency_ms=settings.slm_finetuning.target_latency_ms
    )

    print("\n" + "="*80)
    print("Evaluation Results")
    print("="*80)
    print(f"Test samples:      {results['total_examples']}")
    print(f"Agent accuracy:    {results['accuracy_agent']:.2%}")
    print(f"Depth accuracy:    {results['accuracy_depth']:.2%}")
    print(f"Overall accuracy:  {results['accuracy_both']:.2%}")
    print(f"Avg latency:       {results['avg_latency_ms']:.0f}ms")
    print("\nBaseline Comparison:")
    print(f"Target accuracy:   {comparison['baseline_accuracy']:.2%}")
    print(f"Target latency:    {comparison['baseline_latency_ms']:.0f}ms")
    print(f"Passes targets:    {comparison['passes_accuracy_target'] and comparison['passes_latency_target']}")
    print(f"\nResults saved to:  {results_path}")
    print("="*80 + "\n")

    return results


def export_model(args, settings):
    """Export model for serving"""
    logger.info("step_3_export_model", test_mode=args.test_mode)

    model_path = settings.paths.models_dir / "orchestrator_slm" / "final"
    export_path = settings.paths.exports_dir / "orchestrator_model"

    if not model_path.exists():
        logger.error("model_not_found", path=str(model_path))
        print(f"Error: Model not found at {model_path}")
        sys.exit(1)

    # Copy to exports
    import shutil
    if export_path.exists():
        shutil.rmtree(export_path)

    shutil.copytree(model_path, export_path)

    logger.info("model_exported", path=str(export_path))

    print(f"\nModel exported to: {export_path}\n")

    return export_path


def run_full_pipeline(args, settings):
    """Run full fine-tuning pipeline"""
    logger.info("running_full_pipeline", test_mode=args.test_mode)

    # Step 1: Train
    model_path = train_model(args, settings)

    # Step 2: Evaluate
    evaluate_model(args, settings, model_path)

    # Step 3: Export
    export_model(args, settings)

    logger.info("pipeline_complete")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 2: SLM Fine-tuning - Fine-tune orchestrator models with LoRA"
    )

    # Actions
    parser.add_argument(
        "--train",
        action="store_true",
        help="Train orchestrator model"
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Evaluate trained model"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export model for serving"
    )
    parser.add_argument(
        "--full-pipeline",
        action="store_true",
        help="Run full pipeline (train + evaluate + export)"
    )

    # Configuration
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (mock training, fast)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="Number of training epochs (overrides config)"
    )

    args = parser.parse_args()

    # Load settings
    config_path = Path(args.config)
    settings = get_settings(config_path if config_path.exists() else None)

    # Override settings from args
    if args.test_mode:
        settings.test_mode = True

    if args.epochs:
        settings.slm_finetuning.num_epochs = args.epochs

    # Check if any action was specified
    if not any([args.train, args.evaluate, args.export, args.full_pipeline]):
        parser.print_help()
        sys.exit(1)

    try:
        if args.full_pipeline:
            run_full_pipeline(args, settings)

        else:
            # Run individual steps
            if args.train:
                train_model(args, settings)

            if args.evaluate:
                evaluate_model(args, settings)

            if args.export:
                export_model(args, settings)

        logger.info("program_complete")

    except Exception as e:
        logger.error("program_failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
