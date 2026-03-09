"""
SLM Trainer

Handles LoRA fine-tuning of orchestrator models using SFTTrainer.
"""

from pathlib import Path
from typing import Optional, Any
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset
from habitat_logging import get_logger

logger = get_logger(__name__)


class OrchestratorTrainer:
    """
    Fine-tunes orchestrator models with LoRA.
    """

    def __init__(
        self,
        base_model_name: str,
        output_dir: Path,
        device: Optional[str] = None,
        test_mode: bool = False
    ):
        """
        Initialize trainer.

        Args:
            base_model_name: Base model to fine-tune (e.g., "Qwen/Qwen2.5-7B")
            output_dir: Directory to save outputs
            device: Device to use (cuda/cpu/mps)
            test_mode: If True, use minimal training
        """
        self.base_model_name = base_model_name
        self.output_dir = Path(output_dir)
        self.device = device or self._auto_detect_device()
        self.test_mode = test_mode

        self.logger = logger.bind(component="orchestrator_trainer")

        self.model = None
        self.tokenizer = None

    def _auto_detect_device(self) -> str:
        """Auto-detect available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def load_model_and_tokenizer(
        self,
        lora_config: dict[str, Any],
        load_in_8bit: bool = False,
        load_in_4bit: bool = False
    ) -> None:
        """
        Load base model and tokenizer, apply LoRA.

        Args:
            lora_config: LoRA configuration
            load_in_8bit: Load model in 8-bit
            load_in_4bit: Load model in 4-bit
        """
        self.logger.info(
            "loading_model",
            base_model=self.base_model_name,
            device=self.device,
            load_in_8bit=load_in_8bit,
            load_in_4bit=load_in_4bit
        )

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Model loading kwargs
        model_kwargs = {
            "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
        }

        if self.device == "cuda":
            model_kwargs["device_map"] = "auto"

        if load_in_8bit:
            model_kwargs["load_in_8bit"] = True
        elif load_in_4bit:
            model_kwargs["load_in_4bit"] = True

        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            **model_kwargs
        )

        # Prepare for k-bit training if quantized
        if load_in_8bit or load_in_4bit:
            base_model = prepare_model_for_kbit_training(base_model)

        # Apply LoRA
        lora_config_obj = LoraConfig(**lora_config)
        self.model = get_peft_model(base_model, lora_config_obj)

        self.model.print_trainable_parameters()

        self.logger.info("model_loaded", device=self.device)

    def train(
        self,
        train_dataset_path: Path,
        val_dataset_path: Optional[Path] = None,
        training_args: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Train the model.

        Args:
            train_dataset_path: Path to training dataset (JSONL)
            val_dataset_path: Path to validation dataset (JSONL)
            training_args: Training arguments

        Returns:
            Training statistics
        """
        self.logger.info(
            "starting_training",
            train_dataset=str(train_dataset_path),
            val_dataset=str(val_dataset_path) if val_dataset_path else None
        )

        # Load datasets
        train_dataset = load_dataset("json", data_files=str(train_dataset_path), split="train")

        eval_dataset = None
        if val_dataset_path:
            eval_dataset = load_dataset("json", data_files=str(val_dataset_path), split="train")

        # Prepare training arguments
        if training_args is None:
            training_args = {}

        # Set defaults
        default_args = {
            "output_dir": str(self.output_dir),
            "num_train_epochs": 1 if self.test_mode else 3,
            "per_device_train_batch_size": 1 if self.test_mode else 4,
            "gradient_accumulation_steps": 1 if self.test_mode else 4,
            "learning_rate": 2e-4,
            "max_steps": 10 if self.test_mode else -1,
            "logging_steps": 1 if self.test_mode else 10,
            "save_steps": 5 if self.test_mode else 100,
            "eval_steps": 5 if self.test_mode else 100,
            "save_total_limit": 2,
            "fp16": self.device == "cuda",
            "optim": "adamw_torch",
            "warmup_steps": 10 if self.test_mode else 100,
            "evaluation_strategy": "steps" if eval_dataset else "no",
            "save_strategy": "steps",
            "load_best_model_at_end": True if eval_dataset else False,
        }

        # Merge with provided args
        final_args = {**default_args, **training_args}

        training_arguments = TrainingArguments(**final_args)

        # Create trainer
        trainer = SFTTrainer(
            model=self.model,
            args=training_arguments,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
            max_seq_length=final_args.get("max_seq_length", 2048),
            dataset_text_field="text",  # Assumes dataset has a "text" field
            packing=False,
        )

        # Train
        self.logger.info("training_started")
        result = trainer.train()

        # Save final model
        trainer.save_model(str(self.output_dir / "final"))

        self.logger.info("training_complete", output_dir=str(self.output_dir))

        return {
            "training_loss": result.training_loss,
            "global_step": result.global_step,
            "output_dir": str(self.output_dir)
        }

    def save_adapter(self, output_path: Path) -> None:
        """
        Save LoRA adapter.

        Args:
            output_path: Path to save adapter
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        self.model.save_pretrained(str(output_path))
        self.tokenizer.save_pretrained(str(output_path))

        self.logger.info("adapter_saved", path=str(output_path))

    @staticmethod
    def create_mock_adapter(output_dir: Path) -> None:
        """
        Create mock LoRA adapter for testing.

        Args:
            output_dir: Directory to save mock adapter
        """
        from ..shared.model_loader import OrchestratorModelLoader

        OrchestratorModelLoader.create_mock_model_for_testing(output_dir)

        logger.info("mock_adapter_created", path=str(output_dir))

    def prepare_dataset_for_training(self, chat_dataset_path: Path, output_path: Path) -> None:
        """
        Convert ChatML format to training format.

        Args:
            chat_dataset_path: Path to ChatML dataset (JSONL)
            output_path: Path to save prepared dataset
        """
        import json

        self.logger.info(
            "preparing_dataset",
            input=str(chat_dataset_path),
            output=str(output_path)
        )

        prepared = []

        with open(chat_dataset_path) as f:
            for line in f:
                if not line.strip():
                    continue

                example = json.loads(line)
                messages = example.get("messages", [])

                # Convert to text format for SFTTrainer
                text = self._messages_to_text(messages)

                prepared.append({"text": text})

        # Save prepared dataset
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            for item in prepared:
                f.write(json.dumps(item) + "\n")

        self.logger.info("dataset_prepared", count=len(prepared), output=str(output_path))

    def _messages_to_text(self, messages: list) -> str:
        """
        Convert ChatML messages to text format.

        Args:
            messages: List of message dictionaries

        Returns:
            Formatted text
        """
        text_parts = []

        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "system":
                text_parts.append(f"<|system|>\n{content}<|end|>")
            elif role == "user":
                text_parts.append(f"<|user|>\n{content}<|end|>")
            elif role == "assistant":
                text_parts.append(f"<|assistant|>\n{content}<|end|>")

        return "\n".join(text_parts)
