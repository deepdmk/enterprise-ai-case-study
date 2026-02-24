"""Unsloth-based trainer for fast fine-tuning on Linux/CUDA."""

from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from both local config and phase-0-infrastructure
from config.settings import Settings
from habitat_logging import get_logger

from datasets import Dataset
from src.program2_fine_tuning.callbacks import get_training_callbacks
from src.program2_fine_tuning.lora_config import LoRATrainingArgs
from src.program2_fine_tuning.token_utils import calculate_token_lengths

logger = get_logger(__name__)


class UnslothTrainer:
    """Trainer using Unsloth for optimized fine-tuning."""

    def __init__(
        self,
        settings: Settings,
        training_args: LoRATrainingArgs | None = None,
    ):
        """
        Initialize the Unsloth trainer.

        Args:
            settings: Application settings
            training_args: Training arguments (derived from settings if not provided)
        """
        self.settings = settings
        self.training_args = training_args or LoRATrainingArgs.from_settings(
            settings, test_mode=settings.test_mode
        )
        self._model = None
        self._tokenizer = None
        self._trainer = None

    def load_model(self, base_model: str | None = None) -> tuple[Any, Any]:
        """
        Load and prepare model for training.

        Args:
            base_model: Base model name (uses settings default if not provided)

        Returns:
            Tuple of (model, tokenizer)
        """
        from unsloth import FastLanguageModel

        model_name = base_model or self.settings.model.base_model

        logger.info(
            "loading_model_unsloth",
            model=model_name,
            max_seq_length=self.training_args.max_seq_length,
        )

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=self.training_args.max_seq_length,
            dtype=None,  # Auto-detect
            load_in_4bit=self.settings.model.load_in_4bit,
        )

        # Apply LoRA
        model = FastLanguageModel.get_peft_model(
            model,
            r=self.training_args.r,
            lora_alpha=self.training_args.lora_alpha,
            lora_dropout=self.training_args.lora_dropout,
            target_modules=self.training_args.target_modules,
            use_rslora=self.training_args.use_rslora,
            bias=self.training_args.bias,
        )

        self._model = model
        self._tokenizer = tokenizer

        logger.info("model_prepared_unsloth")
        return model, tokenizer

    def train(
        self,
        train_dataset: Dataset,
        eval_dataset: Dataset | None = None,
        output_dir: str | Path = "outputs",
    ) -> dict[str, Any]:
        """
        Train the model.

        Args:
            train_dataset: Training dataset with 'text' column
            eval_dataset: Optional evaluation dataset
            output_dir: Directory for outputs

        Returns:
            Training results dictionary
        """
        from trl import SFTTrainer
        from transformers import TrainingArguments

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if self._model is None or self._tokenizer is None:
            self.load_model()

        # Configure training arguments
        training_arguments = TrainingArguments(
            output_dir=str(output_dir),
            num_train_epochs=self.training_args.epochs,
            per_device_train_batch_size=self.training_args.batch_size,
            gradient_accumulation_steps=self.training_args.gradient_accumulation_steps,
            learning_rate=self.training_args.learning_rate,
            warmup_steps=self.training_args.warmup_steps,
            weight_decay=self.training_args.weight_decay,
            max_grad_norm=self.training_args.max_grad_norm,
            lr_scheduler_type=self.training_args.lr_scheduler_type,
            logging_steps=self.training_args.logging_steps,
            save_steps=self.training_args.save_steps,
            eval_steps=self.training_args.eval_steps if eval_dataset else None,
            evaluation_strategy="steps" if eval_dataset else "no",
            fp16=self.training_args.fp16,
            bf16=self.training_args.bf16,
            seed=self.training_args.seed,
            optim="adamw_8bit",
            report_to="none",
            save_total_limit=2,
        )

        # Get callbacks
        callbacks = get_training_callbacks(
            output_dir=output_dir,
            use_early_stopping=eval_dataset is not None,
        )

        # Create trainer
        trainer = SFTTrainer(
            model=self._model,
            tokenizer=self._tokenizer,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            args=training_arguments,
            callbacks=callbacks,
            dataset_text_field="text",
            max_seq_length=self.training_args.max_seq_length,
            packing=False,
        )

        self._trainer = trainer

        logger.info(
            "training_starting",
            train_samples=len(train_dataset),
            eval_samples=len(eval_dataset) if eval_dataset else 0,
            epochs=self.training_args.epochs,
        )

        # Train
        train_result = trainer.train()

        # Get metrics
        metrics = train_result.metrics
        metrics["train_samples"] = len(train_dataset)

        if eval_dataset:
            eval_metrics = trainer.evaluate()
            metrics.update(eval_metrics)

        logger.info(
            "training_completed",
            train_loss=metrics.get("train_loss"),
            eval_loss=metrics.get("eval_loss"),
        )

        return metrics

    def save(
        self,
        output_path: str | Path,
        save_merged: bool = False,
    ) -> Path:
        """
        Save the trained model.

        Args:
            output_path: Directory to save model
            save_merged: Whether to save merged model (larger)

        Returns:
            Path to saved model
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        if save_merged:
            self._model.save_pretrained_merged(
                str(output_path),
                self._tokenizer,
                save_method="merged_16bit",
            )
            logger.info("model_saved_merged", path=str(output_path))
        else:
            self._model.save_pretrained(str(output_path))
            self._tokenizer.save_pretrained(str(output_path))
            logger.info("adapter_saved", path=str(output_path))

        return output_path

    @property
    def model(self) -> Any:
        """Get the model."""
        return self._model

    @property
    def tokenizer(self) -> Any:
        """Get the tokenizer."""
        return self._tokenizer


def train_with_unsloth(
    train_dataset: Dataset,
    settings: Settings,
    output_dir: str | Path,
    eval_dataset: Dataset | None = None,
    base_model: str | None = None,
    experiment_tracker: Any | None = None,
    experiment_id: str | None = None,
) -> tuple[Path, dict[str, Any]]:
    """
    Convenience function to train a model with Unsloth.

    Args:
        train_dataset: Training dataset
        settings: Application settings
        output_dir: Directory for outputs
        eval_dataset: Optional evaluation dataset
        base_model: Base model name
        experiment_tracker: Optional experiment tracker instance
        experiment_id: Optional experiment ID for tracking

    Returns:
        Tuple of (adapter_path, metrics)
    """
    trainer = UnslothTrainer(settings)
    trainer.load_model(base_model)

    # Calculate actual token lengths now that tokenizer is available
    if experiment_tracker and experiment_id:
        from registries.schemas import DataCharacteristics

        avg_input, avg_output, avg_total = calculate_token_lengths(
            train_dataset,
            trainer.tokenizer,
            max_samples=500,  # Sample for performance on large datasets
        )
        characteristics = DataCharacteristics(
            num_samples=len(train_dataset),
            avg_input_length=avg_input,
            avg_output_length=avg_output,
        )
        experiment_tracker.log_data_characteristics(experiment_id, characteristics)
        logger.info(
            "data_characteristics_logged",
            num_samples=len(train_dataset),
            avg_input_tokens=round(avg_input, 1),
            avg_output_tokens=round(avg_output, 1),
        )

    metrics = trainer.train(
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        output_dir=output_dir,
    )
    adapter_path = trainer.save(output_dir)
    return adapter_path, metrics
