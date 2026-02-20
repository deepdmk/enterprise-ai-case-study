"""
Program 2: Embedding Model Fine-Tuning

Fine-tunes the base embedding model (all-MiniLM-L6-v2) on enterprise data
using Sentence-Transformers with MultipleNegativesRankingLoss.

Usage:
    python -m src.program2_fine_tuning.main --config config/config.yaml
    python -m src.program2_fine_tuning.main --epochs 1 --test-mode  # Quick test
"""

import argparse
import json
import sys
from pathlib import Path

# Import local config BEFORE adding phase-0 to path
from config.settings import Settings, load_settings

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import configure_logging, get_logger
from registries.experiment_tracker import ExperimentTracker
from registries.model_registry import ModelRegistry
from registries.schemas import (
    DataCharacteristics,
    HyperparameterConfig,
    ModelStatus,
    ModelType,
    Phase,
    RegisteredModel,
    TrainingMetrics,
)

from .evaluator import evaluate_model_on_dataset
from .trainer import EmbeddingTrainer

logger = get_logger(__name__)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fine-tune embedding model on enterprise data"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--train-dataset",
        type=str,
        default=None,
        help="Path to training dataset (overrides config)",
    )
    parser.add_argument(
        "--val-dataset",
        type=str,
        default=None,
        help="Path to validation dataset (overrides config)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=None,
        help="Number of training epochs (overrides config)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Training batch size (overrides config)",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Quick test with minimal training",
    )
    parser.add_argument(
        "--evaluate-only",
        action="store_true",
        help="Only evaluate existing model, don't train",
    )
    parser.add_argument(
        "--no-registry",
        action="store_true",
        help="Disable experiment tracking and model registration",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(level="INFO", format="console")

    # Load settings
    if args.config and Path(args.config).exists():
        settings = load_settings(args.config)
    else:
        settings = Settings()

    config = settings.fine_tuning

    # Apply command line overrides
    if args.epochs:
        config.training.epochs = args.epochs
    if args.batch_size:
        config.training.batch_size = args.batch_size
    if args.test_mode:
        config.training.epochs = 1
        config.training.batch_size = 16

    # Determine dataset paths
    dataset_dir = Path(settings.dataset_generator.output_dir)
    train_path = args.train_dataset or str(dataset_dir / "train.parquet")
    val_path = args.val_dataset or str(dataset_dir / "validation.parquet")

    # Check datasets exist
    if not Path(train_path).exists():
        logger.error("training_dataset_not_found", path=train_path)
        print(f"Training dataset not found at {train_path}")
        print("Run Program 1 first: python -m src.program1_dataset_generator.main")
        return

    if args.evaluate_only:
        # Just evaluate existing model
        model_path = str(Path(config.output_dir) / config.model_name)
        if not Path(model_path).exists():
            logger.error("model_not_found", path=model_path)
            print(f"Model not found at {model_path}")
            return

        eval_path = val_path if Path(val_path).exists() else train_path
        metrics = evaluate_model_on_dataset(model_path, eval_path)

        print("\nEvaluation Results:")
        print(f"  Mean Similarity: {metrics['mean_similarity']:.4f}")
        print(f"  Std Similarity:  {metrics['std_similarity']:.4f}")
        print(f"  Min Similarity:  {metrics['min_similarity']:.4f}")
        print(f"  Max Similarity:  {metrics['max_similarity']:.4f}")
        print(f"  Num Pairs:       {metrics['num_pairs']}")
        return

    # Initialize trainer
    trainer = EmbeddingTrainer(
        base_model=settings.embedding.base_model,
        config=config,
        device=settings.embedding.device,
    )

    # Load datasets
    train_dataset = trainer.load_dataset(train_path)
    val_dataset = trainer.load_dataset(val_path) if Path(val_path).exists() else None

    logger.info(
        "starting_fine_tuning",
        base_model=settings.embedding.base_model,
        train_samples=len(train_dataset),
        val_samples=len(val_dataset) if val_dataset else 0,
        epochs=config.training.epochs,
        batch_size=config.training.batch_size,
    )

    # Initialize registries if not disabled
    experiment_id = None
    if not args.no_registry:
        data_dir = Path("data")
        model_registry = ModelRegistry(data_dir=data_dir, test_mode=args.test_mode)
        experiment_tracker = ExperimentTracker(data_dir=data_dir, test_mode=args.test_mode)

        # Start experiment
        experiment = experiment_tracker.start_experiment(
            phase=Phase.PHASE_1,
            unit="shared",
            task="embeddings",
            notes="Fine-tuning embedding model for unified embedding space",
        )
        experiment_id = experiment.experiment_id
        logger.info("experiment_started", experiment_id=experiment_id)

        # Log data characteristics
        # Calculate average lengths (rough estimate based on typical text length)
        sample_texts = [train_dataset[i]["anchor"] for i in range(min(100, len(train_dataset)))]
        avg_length = sum(len(text.split()) for text in sample_texts) / len(sample_texts)

        experiment_tracker.log_data_characteristics(
            experiment_id=experiment_id,
            characteristics=DataCharacteristics(
                num_samples=len(train_dataset),
                avg_input_length=avg_length,
                avg_output_length=avg_length,  # Same for anchor/positive pairs
            ),
        )

        # Log hyperparameters
        # Calculate warmup steps
        total_steps = (len(train_dataset) // config.training.batch_size) * config.training.epochs
        warmup_steps = int(total_steps * config.training.warmup_ratio)

        experiment_tracker.log_hyperparameters(
            experiment_id=experiment_id,
            hyperparameters=HyperparameterConfig(
                epochs=config.training.epochs,
                batch_size=config.training.batch_size,
                learning_rate=config.training.learning_rate,
                warmup_steps=warmup_steps,
                extra={
                    "fp16": config.training.fp16,
                    "save_strategy": config.training.save_strategy,
                    "loss_type": config.loss.type,
                    "loss_scale": config.loss.scale,
                },
            ),
        )

    # Train
    try:
        result = trainer.train(train_dataset, val_dataset)

        # Save final model
        output_path = Path(config.output_dir) / config.model_name
        trainer.save_model(output_path)
    except Exception as e:
        # Mark experiment as failed if registry tracking is enabled
        if not args.no_registry and experiment_id:
            experiment_tracker.fail_experiment(
                experiment_id=experiment_id,
                error_message=str(e),
            )
            logger.error("training_failed", experiment_id=experiment_id, error=str(e))
        raise

    # Save training metrics
    metrics_path = output_path / "training_metrics.json"
    metrics_dict = {
        "final_loss": result.final_loss,
        "epochs_completed": result.epochs_completed,
        "model_path": result.model_path,
        "base_model": settings.embedding.base_model,
        "training_config": {
            "epochs": config.training.epochs,
            "batch_size": config.training.batch_size,
            "learning_rate": config.training.learning_rate,
        },
    }
    if result.eval_loss is not None:
        metrics_dict["eval_loss"] = result.eval_loss

    with open(metrics_path, "w") as f:
        json.dump(metrics_dict, f, indent=2)

    logger.info(
        "fine_tuning_complete",
        model_path=str(output_path),
        final_loss=result.final_loss,
        eval_loss=result.eval_loss,
    )

    # Registry tracking: log metrics and register model
    if not args.no_registry and experiment_id:
        try:
            # Log training metrics
            experiment_tracker.log_training_metrics(
                experiment_id=experiment_id,
                metrics=TrainingMetrics(
                    train_loss=result.final_loss,
                    eval_loss=result.eval_loss,
                ),
            )

            # Register model
            model_id = "1/shared/embeddings_v1"
            model_registry.register(
                RegisteredModel(
                    model_id=model_id,
                    phase=Phase.PHASE_1,
                    unit="shared",
                    task="embeddings",
                    model_type=ModelType.FINE_TUNED,
                    base_model=settings.embedding.base_model,
                    model_path=str(output_path.absolute()),
                    source_dataset_id="1/training/embeddings/v1",
                    status=ModelStatus.TRAINED,
                    tags=["phase1", "embedding", "sentence-transformer"],
                )
            )

            # Complete experiment
            experiment_tracker.complete_experiment(
                experiment_id=experiment_id,
                model_id=model_id,
            )

            logger.info(
                "registry_tracking_complete",
                experiment_id=experiment_id,
                model_id=model_id,
            )

        except Exception as e:
            logger.error(
                "registry_tracking_failed",
                experiment_id=experiment_id,
                error=str(e),
            )
            # Fail the experiment
            experiment_tracker.fail_experiment(
                experiment_id=experiment_id,
                error_message=str(e),
            )

    print("\nFine-tuning complete!")
    print(f"  Model saved to: {output_path}")
    print(f"  Final loss: {result.final_loss:.4f}")
    if result.eval_loss is not None:
        print(f"  Eval loss: {result.eval_loss:.4f}")
    if not args.no_registry and experiment_id:
        print(f"  Experiment ID: {experiment_id}")

    # Quick evaluation on validation set
    if val_dataset:
        print("\nEvaluating on validation set...")
        metrics = evaluate_model_on_dataset(str(output_path), val_path)
        print(f"  Mean Similarity: {metrics['mean_similarity']:.4f}")


if __name__ == "__main__":
    main()
