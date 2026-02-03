"""Optional MoE fine-tuning to improve routing."""

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

from config.settings import Settings

logger = get_logger(__name__)


@dataclass
class FineTuneResult:
    """Result of MoE fine-tuning operation."""

    success: bool
    model_path: Path
    output_path: Path
    start_time: datetime
    end_time: datetime | None = None
    metrics: dict[str, float] = field(default_factory=dict)
    error: str | None = None

    @property
    def duration_seconds(self) -> float | None:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "model_path": str(self.model_path),
            "output_path": str(self.output_path),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "metrics": self.metrics,
            "error": self.error,
        }


class MoEFineTuner:
    """Fine-tune merged MoE model to improve routing."""

    def __init__(self, settings: Settings):
        """
        Initialize the fine-tuner.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.merged_dir = self.base_path / settings.paths.merged_dir

    def finetune(
        self,
        model_path: str | Path,
        output_dir: str | Path,
        training_data_path: str | Path | None = None,
        epochs: int | None = None,
        batch_size: int | None = None,
        learning_rate: float | None = None,
    ) -> FineTuneResult:
        """
        Fine-tune merged MoE model.

        Args:
            model_path: Path to merged MoE model
            output_dir: Output directory for fine-tuned model
            training_data_path: Path to training data
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate

        Returns:
            FineTuneResult
        """
        model_path = Path(model_path)
        output_dir = Path(output_dir)
        start_time = datetime.utcnow()

        result = FineTuneResult(
            success=False,
            model_path=model_path,
            output_path=output_dir,
            start_time=start_time,
        )

        # Apply settings defaults
        epochs = epochs or self.settings.finetune.epochs
        batch_size = batch_size or self.settings.finetune.batch_size
        learning_rate = learning_rate or self.settings.finetune.learning_rate

        try:
            # Validate model exists
            if not model_path.exists():
                result.error = f"Model not found: {model_path}"
                result.end_time = datetime.utcnow()
                return result

            # Run fine-tuning
            result = self._run_lora_finetune(
                model_path=model_path,
                output_dir=output_dir,
                training_data_path=training_data_path,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate,
                result=result,
            )

        except Exception as e:
            result.error = str(e)
            logger.error("finetune_exception", error=str(e))

        result.end_time = datetime.utcnow()
        return result

    def _run_lora_finetune(
        self,
        model_path: Path,
        output_dir: Path,
        training_data_path: Path | None,
        epochs: int,
        batch_size: int,
        learning_rate: float,
        result: FineTuneResult,
    ) -> FineTuneResult:
        """Execute LoRA fine-tuning on MoE model."""
        try:
            from peft import LoraConfig, get_peft_model
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                TrainingArguments,
            )
            from trl import SFTTrainer

            logger.info(
                "starting_finetune",
                model=str(model_path),
                epochs=epochs,
                lr=learning_rate,
            )

            # Load model
            model = AutoModelForCausalLM.from_pretrained(
                str(model_path),
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True,
            )
            tokenizer = AutoTokenizer.from_pretrained(str(model_path))

            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            # Configure LoRA
            lora_config = LoraConfig(
                r=self.settings.finetune.lora_r,
                lora_alpha=self.settings.finetune.lora_alpha,
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                lora_dropout=0.1,
                bias="none",
                task_type="CAUSAL_LM",
            )

            model = get_peft_model(model, lora_config)

            # Load training data
            if training_data_path:
                dataset = self._load_training_data(training_data_path)
            else:
                # Use synthetic data for router fine-tuning
                dataset = self._generate_synthetic_routing_data()

            # Training arguments
            output_dir.mkdir(parents=True, exist_ok=True)

            training_args = TrainingArguments(
                output_dir=str(output_dir),
                num_train_epochs=epochs,
                per_device_train_batch_size=batch_size,
                learning_rate=learning_rate,
                warmup_steps=10,
                logging_steps=10,
                save_steps=100,
                fp16=True,
                report_to="none",
            )

            # Initialize trainer
            trainer = SFTTrainer(
                model=model,
                train_dataset=dataset,
                args=training_args,
                tokenizer=tokenizer,
                max_seq_length=512,
            )

            # Train
            train_result = trainer.train()

            # Save model
            trainer.save_model(str(output_dir / "final"))
            tokenizer.save_pretrained(str(output_dir / "final"))

            # Collect metrics
            result.metrics = {
                "train_loss": train_result.training_loss,
                "train_runtime": train_result.metrics.get("train_runtime", 0),
                "train_samples_per_second": train_result.metrics.get(
                    "train_samples_per_second", 0
                ),
            }
            result.success = True

            logger.info(
                "finetune_complete",
                output=str(output_dir),
                train_loss=result.metrics.get("train_loss"),
            )

            # Save metadata
            self._save_finetune_metadata(result, output_dir)

        except ImportError as e:
            result.error = f"Required packages not installed: {e}"
            logger.error("missing_dependencies", error=str(e))

        return result

    def _load_training_data(self, data_path: Path):
        """Load training data for fine-tuning."""
        from datasets import load_dataset

        if str(data_path).endswith(".json"):
            return load_dataset("json", data_files=str(data_path))["train"]
        elif str(data_path).endswith(".jsonl"):
            return load_dataset("json", data_files=str(data_path))["train"]
        else:
            return load_dataset(str(data_path))["train"]

    def _generate_synthetic_routing_data(self):
        """Generate synthetic data for router fine-tuning."""
        from datasets import Dataset

        # Create synthetic routing examples
        examples = [
            {
                "text": "Profile the investor: John Smith is a venture capitalist...",
                "routing_hint": "investor_profiling",
            },
            {
                "text": "Analyze the RFP requirements: The client seeks...",
                "routing_hint": "rfp_analysis",
            },
            {
                "text": "Assess market conditions in Southeast Asia...",
                "routing_hint": "market_intelligence",
            },
        ]

        # Repeat for diversity
        examples = examples * 10

        return Dataset.from_list(examples)

    def _save_finetune_metadata(self, result: FineTuneResult, output_dir: Path) -> None:
        """Save fine-tuning metadata."""
        metadata_path = output_dir / "finetune_metadata.json"

        with open(metadata_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

        logger.info("metadata_saved", path=str(metadata_path))


class MockFineTuner:
    """Mock fine-tuner for testing."""

    def __init__(self, settings: Settings):
        """Initialize mock fine-tuner."""
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent

    def create_mock_finetune(
        self,
        model_path: Path,
        output_dir: Path,
    ) -> FineTuneResult:
        """Create mock fine-tuned model structure."""
        import json
        import shutil

        start_time = datetime.utcnow()

        result = FineTuneResult(
            success=False,
            model_path=model_path,
            output_path=output_dir,
            start_time=start_time,
        )

        try:
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            final_dir = output_dir / "final"
            final_dir.mkdir(exist_ok=True)

            # Copy model config if exists
            if (model_path / "config.json").exists():
                shutil.copy(model_path / "config.json", final_dir / "config.json")

            # Create mock LoRA adapter config
            adapter_config = {
                "peft_type": "LORA",
                "r": self.settings.finetune.lora_r,
                "lora_alpha": self.settings.finetune.lora_alpha,
                "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
                "lora_dropout": 0.1,
                "bias": "none",
                "base_model_name_or_path": str(model_path),
            }

            with open(final_dir / "adapter_config.json", "w") as f:
                json.dump(adapter_config, f, indent=2)

            # Mock training metrics
            result.metrics = {
                "train_loss": 0.5,
                "train_runtime": 100.0,
                "train_samples_per_second": 10.0,
                "mock": True,
            }
            result.success = True
            result.end_time = datetime.utcnow()

            # Save metadata
            metadata = result.to_dict()
            metadata["mock"] = True
            with open(output_dir / "finetune_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            logger.info("mock_finetune_complete", output=str(output_dir))

        except Exception as e:
            result.error = str(e)
            result.end_time = datetime.utcnow()
            logger.error("mock_finetune_failed", error=str(e))

        return result
