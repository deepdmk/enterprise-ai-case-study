"""HuggingFace Transformers-based trainer (fallback for Mac MPS/CPU)."""

from pathlib import Path
from typing import Any

import torch

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from both local config and phase-0-infrastructure
from config.settings import Settings
from habitat_logging import get_logger

from datasets import Dataset
from src.program2_fine_tuning.callbacks import get_training_callbacks
from src.program2_fine_tuning.lora_config import LoRATrainingArgs, get_peft_lora_config
from src.program2_fine_tuning.token_utils import calculate_token_lengths
from src.shared.environment_detector import detect_environment, get_device, get_dtype

logger = get_logger(__name__)


class TransformersTrainer:
    """Trainer using HuggingFace Transformers + PEFT (fallback path)."""

    def __init__(
        self,
        settings: Settings,
        training_args: LoRATrainingArgs | None = None,
    ):
        """
        Initialize the Transformers trainer.

        Args:
            settings: Application settings
            training_args: Training arguments (derived from settings if not provided)
        """
        self.settings = settings
        self.training_args = training_args or LoRATrainingArgs.from_settings(
            settings, test_mode=settings.test_mode
        )
        self.env_info = detect_environment()
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
        from peft import get_peft_model, prepare_model_for_kbit_training
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        model_name = base_model or self.settings.model.base_model

        logger.info(
            "loading_model_transformers",
            model=model_name,
            device=get_device(),
        )

        # Configure quantization for CUDA
        quantization_config = None
        if self.settings.model.load_in_4bit and self.env_info.has_cuda:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=get_dtype(),
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True,
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"

        # Load model
        device_map = "auto" if self.env_info.has_cuda else None

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map=device_map,
            torch_dtype=get_dtype(),
            trust_remote_code=True,
        )

        # Prepare for k-bit training if quantized
        if quantization_config:
            model = prepare_model_for_kbit_training(model)

        # Apply LoRA
        lora_config = get_peft_lora_config(self.training_args.to_lora_config())
        model = get_peft_model(model, lora_config)

        # Move to device if not using device_map
        if device_map is None:
            device = get_device()
            if device != "cpu":
                model = model.to(device)

        # Enable gradient checkpointing for memory efficiency
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()

        self._model = model
        self._tokenizer = tokenizer

        # Log trainable parameters
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        logger.info(
            "model_prepared_transformers",
            trainable_params=f"{trainable_params:,}",
            total_params=f"{total_params:,}",
            trainable_pct=f"{100 * trainable_params / total_params:.2f}%",
        )

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

        # Adjust settings for MPS/CPU
        fp16 = self.training_args.fp16 and self.env_info.has_cuda
        bf16 = self.training_args.bf16 and self.env_info.has_cuda

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
            fp16=fp16,
            bf16=bf16,
            seed=self.training_args.seed,
            optim="adamw_torch",  # Use standard optimizer for MPS
            report_to="none",
            save_total_limit=2,
            gradient_checkpointing=True,
            remove_unused_columns=False,
        )

        # Get callbacks
        callbacks = get_training_callbacks(
            output_dir=output_dir,
            use_early_stopping=eval_dataset is not None,
            log_memory=self.env_info.has_cuda,
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
            backend="transformers",
            device=get_device(),
        )

        # Train
        train_result = trainer.train()

        # Get metrics
        metrics = train_result.metrics
        metrics["train_samples"] = len(train_dataset)
        metrics["backend"] = "transformers"

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
            # Merge and save
            merged_model = self._model.merge_and_unload()
            merged_model.save_pretrained(str(output_path))
            self._tokenizer.save_pretrained(str(output_path))
            logger.info("model_saved_merged", path=str(output_path))
        else:
            # Save adapter only
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


def train_with_transformers(
    train_dataset: Dataset,
    settings: Settings,
    output_dir: str | Path,
    eval_dataset: Dataset | None = None,
    base_model: str | None = None,
    experiment_tracker: Any | None = None,
    experiment_id: str | None = None,
) -> tuple[Path, dict[str, Any]]:
    """
    Convenience function to train a model with Transformers.

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
    trainer = TransformersTrainer(settings)
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
