"""
Embedding Model Trainer.

Wraps Sentence-Transformers training workflow for fine-tuning embedding models
on enterprise data.
"""

from dataclasses import dataclass
from pathlib import Path

import torch
from datasets import Dataset, load_dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)
from sentence_transformers.losses import MultipleNegativesRankingLoss
from sentence_transformers.training_args import BatchSamplers

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import FineTuningConfig
from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class TrainingResult:
    """Result of a training run."""

    model_path: str
    final_loss: float
    epochs_completed: int
    eval_loss: float | None = None
    best_checkpoint: str | None = None


class EmbeddingTrainer:
    """
    Trainer for fine-tuning embedding models using Sentence-Transformers.

    Uses MultipleNegativesRankingLoss which creates in-batch negatives,
    making it efficient for contrastive learning.
    """

    def __init__(
        self,
        base_model: str,
        config: FineTuningConfig,
        device: str = "auto",
    ):
        """
        Initialize the trainer.

        Args:
            base_model: Name or path of the base model.
            config: Fine-tuning configuration.
            device: Device to use (auto, cuda, cpu, mps).
        """
        self.base_model = base_model
        self.config = config
        self.device = self._select_device(device)
        self._model: SentenceTransformer | None = None

    def _select_device(self, device: str) -> str:
        """Select the best available device."""
        if device != "auto":
            return device

        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def load_model(self) -> SentenceTransformer:
        """Load the base model for fine-tuning."""
        logger.info("loading_base_model", model=self.base_model, device=self.device)

        self._model = SentenceTransformer(self.base_model, device=self.device)

        logger.info(
            "model_loaded",
            model=self.base_model,
            dimension=self._model.get_sentence_embedding_dimension(),
        )

        return self._model

    @property
    def model(self) -> SentenceTransformer:
        """Get the model, loading if necessary."""
        if self._model is None:
            self.load_model()
        return self._model

    def load_dataset(self, dataset_path: str | Path) -> Dataset:
        """
        Load training dataset from Parquet file.

        Args:
            dataset_path: Path to the Parquet file.

        Returns:
            HuggingFace Dataset with anchor and positive columns.
        """
        dataset_path = Path(dataset_path)

        if dataset_path.suffix == ".parquet":
            dataset = load_dataset("parquet", data_files=str(dataset_path), split="train")
        else:
            dataset = load_dataset(str(dataset_path), split="train")

        logger.info("dataset_loaded", path=str(dataset_path), num_samples=len(dataset))
        return dataset

    def setup_loss(self) -> MultipleNegativesRankingLoss:
        """
        Set up the loss function.

        MultipleNegativesRankingLoss uses in-batch negatives:
        - For each (anchor, positive) pair in a batch
        - All other positives in the batch serve as negatives
        - Larger batch size = more negatives = better training
        """
        loss = MultipleNegativesRankingLoss(self.model, scale=self.config.loss.scale)
        logger.info(
            "loss_configured",
            type="MultipleNegativesRankingLoss",
            scale=self.config.loss.scale,
        )
        return loss

    def train(
        self,
        train_dataset: Dataset,
        eval_dataset: Dataset | None = None,
    ) -> TrainingResult:
        """
        Train the model on the dataset.

        Args:
            train_dataset: Training dataset with 'anchor' and 'positive' columns.
            eval_dataset: Optional evaluation dataset.

        Returns:
            TrainingResult with training outcomes.
        """
        training_config = self.config.training
        output_dir = Path(self.config.output_dir) / self.config.model_name

        # Create training arguments, honoring the configured strategies.
        # load_best_model_at_end requires save_strategy == eval_strategy, so
        # it's only enabled when the configured strategies line up.
        use_eval = eval_dataset is not None
        eval_strategy = training_config.evaluation_strategy if use_eval else "no"
        save_strategy = training_config.save_strategy
        load_best = use_eval and save_strategy == eval_strategy
        args = SentenceTransformerTrainingArguments(
            output_dir=str(output_dir),
            num_train_epochs=training_config.epochs,
            per_device_train_batch_size=training_config.batch_size,
            learning_rate=training_config.learning_rate,
            warmup_ratio=training_config.warmup_ratio,
            fp16=training_config.fp16 and self.device == "cuda",
            bf16=False,
            batch_sampler=BatchSamplers.NO_DUPLICATES,
            save_strategy=save_strategy,
            logging_steps=training_config.logging_steps,
            eval_strategy=eval_strategy,
            eval_steps=training_config.eval_steps if eval_strategy == "steps" else None,
            save_total_limit=3,
            load_best_model_at_end=load_best,
        )

        # Set up loss
        loss = self.setup_loss()

        # Create trainer
        trainer = SentenceTransformerTrainer(
            model=self.model,
            args=args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            loss=loss,
        )

        logger.info(
            "training_started",
            epochs=training_config.epochs,
            batch_size=training_config.batch_size,
            train_samples=len(train_dataset),
            eval_samples=len(eval_dataset) if eval_dataset else 0,
        )

        # Train
        trainer.train()

        # Get final loss from training history
        log_history = trainer.state.log_history
        final_loss = log_history[-1].get("train_loss", 0.0) if log_history else 0.0

        # Extract eval_loss if evaluation was performed
        eval_loss = None
        if use_eval:
            # Find the last eval_loss in training history
            for entry in reversed(trainer.state.log_history):
                if "eval_loss" in entry:
                    eval_loss = entry["eval_loss"]
                    break

        logger.info(
            "training_completed",
            final_loss=final_loss,
            eval_loss=eval_loss,
            epochs=training_config.epochs,
        )

        return TrainingResult(
            model_path=str(output_dir),
            final_loss=final_loss,
            epochs_completed=training_config.epochs,
            eval_loss=eval_loss,
        )

    def save_model(self, output_path: str | Path) -> None:
        """
        Save the fine-tuned model.

        Args:
            output_path: Directory to save the model.
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        self.model.save(str(output_path))
        logger.info("model_saved", path=str(output_path))


def quick_train(
    train_dataset_path: str | Path,
    val_dataset_path: str | Path | None = None,
    base_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    output_dir: str = "data/models",
    model_name: str = "enterprise-embed-v1",
    epochs: int = 3,
    batch_size: int = 64,
) -> TrainingResult:
    """
    Quick training function with sensible defaults.

    Args:
        train_dataset_path: Path to training dataset.
        val_dataset_path: Optional path to validation dataset.
        base_model: Base model to fine-tune.
        output_dir: Output directory for model.
        model_name: Name for the fine-tuned model.
        epochs: Number of training epochs.
        batch_size: Training batch size.

    Returns:
        TrainingResult with training outcomes.
    """
    from config.settings import FineTuningConfig, TrainingParamsConfig

    config = FineTuningConfig(
        output_dir=output_dir,
        model_name=model_name,
        training=TrainingParamsConfig(
            epochs=epochs,
            batch_size=batch_size,
        ),
    )

    trainer = EmbeddingTrainer(base_model=base_model, config=config)

    train_dataset = trainer.load_dataset(train_dataset_path)
    val_dataset = trainer.load_dataset(val_dataset_path) if val_dataset_path else None

    return trainer.train(train_dataset, val_dataset)
