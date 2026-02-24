"""LoRA configuration utilities for fine-tuning."""

from dataclasses import dataclass
from typing import Any

from config.settings import LoRAConfig, Settings


@dataclass
class LoRATrainingArgs:
    """Combined LoRA and training arguments."""

    # LoRA parameters
    r: int = 16
    lora_alpha: int = 16
    lora_dropout: float = 0
    target_modules: list[str] | None = None
    use_rslora: bool = True
    bias: str = "none"

    # Training parameters
    epochs: int = 3
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 3e-4
    warmup_steps: int = 10
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    lr_scheduler_type: str = "linear"
    logging_steps: int = 10
    save_steps: int = 100
    eval_steps: int = 100
    fp16: bool = True
    bf16: bool = False
    seed: int = 42

    # Model parameters
    max_seq_length: int = 2048

    def __post_init__(self):
        if self.target_modules is None:
            self.target_modules = [
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "up_proj",
                "down_proj",
                "gate_proj",
            ]

    @classmethod
    def from_settings(cls, settings: Settings, test_mode: bool = False) -> "LoRATrainingArgs":
        """Create from Settings object."""
        lora = settings.lora
        training = settings.get_effective_training_config()

        return cls(
            # LoRA
            r=lora.r,
            lora_alpha=lora.lora_alpha,
            lora_dropout=lora.lora_dropout,
            target_modules=lora.target_modules,
            use_rslora=lora.use_rslora,
            bias=lora.bias,
            # Training
            epochs=training.epochs,
            batch_size=training.batch_size,
            gradient_accumulation_steps=training.gradient_accumulation_steps,
            learning_rate=training.learning_rate,
            warmup_steps=training.warmup_steps,
            weight_decay=training.weight_decay,
            max_grad_norm=training.max_grad_norm,
            lr_scheduler_type=training.lr_scheduler_type,
            logging_steps=training.logging_steps,
            save_steps=training.save_steps,
            eval_steps=training.eval_steps,
            fp16=training.fp16,
            bf16=training.bf16,
            seed=training.seed,
            # Model
            max_seq_length=settings.model.max_seq_length,
        )

    def to_sft_config(self) -> dict[str, Any]:
        """Convert to SFTTrainer configuration dictionary."""
        return {
            "max_seq_length": self.max_seq_length,
            "num_train_epochs": self.epochs,
            "per_device_train_batch_size": self.batch_size,
            "gradient_accumulation_steps": self.gradient_accumulation_steps,
            "learning_rate": self.learning_rate,
            "warmup_steps": self.warmup_steps,
            "weight_decay": self.weight_decay,
            "max_grad_norm": self.max_grad_norm,
            "lr_scheduler_type": self.lr_scheduler_type,
            "logging_steps": self.logging_steps,
            "save_steps": self.save_steps,
            "eval_steps": self.eval_steps if self.eval_steps else None,
            "fp16": self.fp16,
            "bf16": self.bf16,
            "seed": self.seed,
            "optim": "adamw_8bit",
            "output_dir": "outputs",
        }

    def to_lora_config(self) -> LoRAConfig:
        """Convert to LoRAConfig for model_loader."""
        # target_modules is guaranteed non-None after __post_init__
        assert self.target_modules is not None, "target_modules should be set by __post_init__"
        return LoRAConfig(
            r=self.r,
            lora_alpha=self.lora_alpha,
            lora_dropout=self.lora_dropout,
            target_modules=self.target_modules,
            use_rslora=self.use_rslora,
            bias=self.bias,
        )


def get_default_lora_config() -> LoRAConfig:
    """Get default LoRA configuration for Phase 2."""
    return LoRAConfig(
        r=16,
        lora_alpha=16,
        lora_dropout=0,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "up_proj",
            "down_proj",
            "gate_proj",
        ],
        use_rslora=True,
        bias="none",
        task_type="CAUSAL_LM",
    )


def get_peft_lora_config(lora_config: LoRAConfig | None = None) -> Any:
    """
    Get PEFT LoraConfig object.

    Args:
        lora_config: LoRA configuration (uses default if not provided)

    Returns:
        PEFT LoraConfig object
    """
    from peft import LoraConfig as PeftLoraConfig

    config = lora_config or get_default_lora_config()

    return PeftLoraConfig(
        r=config.r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=config.target_modules,
        bias=config.bias,
        task_type=config.task_type,
    )
