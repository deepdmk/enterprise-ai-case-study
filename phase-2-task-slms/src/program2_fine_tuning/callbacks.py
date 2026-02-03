"""Training callbacks for fine-tuning."""

import json
import sys
import time
from pathlib import Path
from typing import Any

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

from transformers import TrainerCallback, TrainerControl, TrainerState, TrainingArguments

logger = get_logger(__name__)


class LoggingCallback(TrainerCallback):
    """Callback for structured logging during training."""

    def __init__(self, log_file: str | Path | None = None):
        """
        Initialize the logging callback.

        Args:
            log_file: Optional path to save logs as JSONL
        """
        self.log_file = Path(log_file) if log_file else None
        self.logs: list[dict[str, Any]] = []
        self.start_time: float | None = None

    def on_train_begin(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Called when training begins."""
        self.start_time = time.time()
        logger.info(
            "training_started",
            max_steps=state.max_steps,
            epochs=args.num_train_epochs,
        )

    def on_log(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        logs: dict[str, Any] | None = None,
        **kwargs,
    ):
        """Called when the trainer logs metrics."""
        if logs is None:
            return

        log_entry = {
            "step": state.global_step,
            "epoch": state.epoch,
            "timestamp": time.time(),
            **logs,
        }

        self.logs.append(log_entry)

        # Log structured message
        logger.info(
            "training_step",
            step=state.global_step,
            epoch=f"{state.epoch:.2f}",
            loss=logs.get("loss"),
            learning_rate=logs.get("learning_rate"),
        )

    def on_train_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Called when training ends."""
        duration = time.time() - self.start_time if self.start_time else 0

        logger.info(
            "training_completed",
            total_steps=state.global_step,
            duration_seconds=f"{duration:.1f}",
        )

        # Save logs if log_file specified
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, "w") as f:
                for entry in self.logs:
                    f.write(json.dumps(entry) + "\n")
            logger.info("training_logs_saved", file=str(self.log_file))

    def on_evaluate(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        metrics: dict[str, Any] | None = None,
        **kwargs,
    ):
        """Called after evaluation."""
        if metrics:
            logger.info(
                "evaluation_completed",
                step=state.global_step,
                eval_loss=metrics.get("eval_loss"),
            )


class EarlyStoppingCallback(TrainerCallback):
    """Callback for early stopping based on validation loss."""

    def __init__(
        self,
        patience: int = 3,
        min_delta: float = 0.01,
    ):
        """
        Initialize early stopping callback.

        Args:
            patience: Number of evaluations without improvement before stopping
            min_delta: Minimum change to qualify as improvement
        """
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss: float | None = None
        self.patience_counter = 0

    def on_evaluate(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        metrics: dict[str, Any] | None = None,
        **kwargs,
    ):
        """Check if training should stop early."""
        if metrics is None:
            return

        eval_loss = metrics.get("eval_loss")
        if eval_loss is None:
            return

        if self.best_loss is None:
            self.best_loss = eval_loss
            return

        if eval_loss < self.best_loss - self.min_delta:
            # Improvement found
            self.best_loss = eval_loss
            self.patience_counter = 0
            logger.info(
                "early_stopping_improvement",
                new_best_loss=eval_loss,
            )
        else:
            # No improvement
            self.patience_counter += 1
            logger.info(
                "early_stopping_no_improvement",
                current_loss=eval_loss,
                best_loss=self.best_loss,
                patience=f"{self.patience_counter}/{self.patience}",
            )

            if self.patience_counter >= self.patience:
                logger.info("early_stopping_triggered")
                control.should_training_stop = True


class MemoryCallback(TrainerCallback):
    """Callback for monitoring GPU memory usage."""

    def __init__(self, log_frequency: int = 100):
        """
        Initialize memory callback.

        Args:
            log_frequency: How often to log memory (in steps)
        """
        self.log_frequency = log_frequency

    def on_step_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Log memory usage periodically."""
        if state.global_step % self.log_frequency != 0:
            return

        try:
            import torch

            if torch.cuda.is_available():
                allocated = torch.cuda.memory_allocated() / 1024**3
                reserved = torch.cuda.memory_reserved() / 1024**3
                logger.info(
                    "gpu_memory",
                    step=state.global_step,
                    allocated_gb=f"{allocated:.2f}",
                    reserved_gb=f"{reserved:.2f}",
                )
        except Exception:
            pass


class SaveBestModelCallback(TrainerCallback):
    """Callback to save the best model based on validation loss."""

    def __init__(self, output_dir: str | Path):
        """
        Initialize save best model callback.

        Args:
            output_dir: Directory to save best model
        """
        self.output_dir = Path(output_dir)
        self.best_loss: float | None = None

    def on_evaluate(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        metrics: dict[str, Any] | None = None,
        model=None,
        **kwargs,
    ):
        """Save model if it's the best so far."""
        if metrics is None or model is None:
            return

        eval_loss = metrics.get("eval_loss")
        if eval_loss is None:
            return

        if self.best_loss is None or eval_loss < self.best_loss:
            self.best_loss = eval_loss
            best_dir = self.output_dir / "best_model"
            best_dir.mkdir(parents=True, exist_ok=True)

            model.save_pretrained(str(best_dir))
            logger.info(
                "best_model_saved",
                eval_loss=eval_loss,
                path=str(best_dir),
            )


def get_training_callbacks(
    output_dir: str | Path,
    use_early_stopping: bool = False,
    early_stopping_patience: int = 3,
    log_memory: bool = True,
) -> list[TrainerCallback]:
    """
    Get a list of training callbacks.

    Args:
        output_dir: Directory for outputs
        use_early_stopping: Whether to use early stopping
        early_stopping_patience: Patience for early stopping
        log_memory: Whether to log memory usage

    Returns:
        List of callbacks
    """
    output_dir = Path(output_dir)
    callbacks = [
        LoggingCallback(log_file=output_dir / "training_logs.jsonl"),
        SaveBestModelCallback(output_dir),
    ]

    if use_early_stopping:
        callbacks.append(EarlyStoppingCallback(patience=early_stopping_patience))

    if log_memory:
        callbacks.append(MemoryCallback())

    return callbacks
