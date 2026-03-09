"""
Model Checkpointer

Manages model checkpoints during training.
"""

from pathlib import Path
from typing import Any, Optional
import json
import shutil
from datetime import datetime
from habitat_logging import get_logger

logger = get_logger(__name__)


class Checkpointer:
    """
    Manages model checkpoints.

    Features:
    - Save/load checkpoints
    - Keep only best N checkpoints
    - Track training metrics
    - Resume from checkpoints
    """

    def __init__(self, checkpoint_dir: Path, max_checkpoints: int = 5):
        """
        Initialize checkpointer.

        Args:
            checkpoint_dir: Directory to save checkpoints
            max_checkpoints: Maximum number of checkpoints to keep
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.max_checkpoints = max_checkpoints
        self.logger = logger.bind(component="checkpointer")

        # Create checkpoint directory
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Metadata file
        self.metadata_file = self.checkpoint_dir / "checkpoints_metadata.json"

    def save_checkpoint(
        self,
        model: Any,
        tokenizer: Any,
        step: int,
        metrics: dict[str, Any],
        checkpoint_name: Optional[str] = None
    ) -> Path:
        """
        Save a checkpoint.

        Args:
            model: Model to save
            tokenizer: Tokenizer to save
            step: Training step
            metrics: Training metrics
            checkpoint_name: Optional checkpoint name

        Returns:
            Path to saved checkpoint
        """
        if checkpoint_name is None:
            checkpoint_name = f"checkpoint-{step}"

        checkpoint_path = self.checkpoint_dir / checkpoint_name
        checkpoint_path.mkdir(parents=True, exist_ok=True)

        # Save model and tokenizer
        model.save_pretrained(str(checkpoint_path))
        tokenizer.save_pretrained(str(checkpoint_path))

        # Save metrics
        metrics_file = checkpoint_path / "metrics.json"
        with open(metrics_file, "w") as f:
            json.dump(
                {
                    **metrics,
                    "step": step,
                    "timestamp": datetime.now().isoformat()
                },
                f,
                indent=2
            )

        # Update metadata
        self._update_metadata(checkpoint_name, step, metrics)

        # Cleanup old checkpoints
        self._cleanup_old_checkpoints()

        self.logger.info(
            "checkpoint_saved",
            checkpoint=checkpoint_name,
            step=step,
            path=str(checkpoint_path)
        )

        return checkpoint_path

    def load_checkpoint(self, checkpoint_name: str) -> dict[str, Any]:
        """
        Load checkpoint metadata.

        Args:
            checkpoint_name: Name of checkpoint to load

        Returns:
            Checkpoint metadata
        """
        checkpoint_path = self.checkpoint_dir / checkpoint_name

        if not checkpoint_path.exists():
            raise ValueError(f"Checkpoint not found: {checkpoint_name}")

        # Load metrics
        metrics_file = checkpoint_path / "metrics.json"
        if metrics_file.exists():
            with open(metrics_file) as f:
                metadata = json.load(f)
        else:
            metadata = {}

        metadata["path"] = str(checkpoint_path)

        self.logger.info("checkpoint_loaded", checkpoint=checkpoint_name)

        return metadata

    def get_best_checkpoint(self, metric: str = "eval_loss", minimize: bool = True) -> Optional[str]:
        """
        Get best checkpoint based on a metric.

        Args:
            metric: Metric to use for comparison
            minimize: If True, lower is better

        Returns:
            Name of best checkpoint
        """
        metadata = self._load_metadata()

        if not metadata.get("checkpoints"):
            return None

        checkpoints = metadata["checkpoints"]

        # Filter checkpoints that have the metric
        valid_checkpoints = [
            cp for cp in checkpoints
            if metric in cp.get("metrics", {})
        ]

        if not valid_checkpoints:
            return None

        # Sort by metric
        sorted_checkpoints = sorted(
            valid_checkpoints,
            key=lambda cp: cp["metrics"][metric],
            reverse=not minimize
        )

        best = sorted_checkpoints[0]

        self.logger.info(
            "best_checkpoint",
            checkpoint=best["name"],
            metric=metric,
            value=best["metrics"][metric]
        )

        return best["name"]

    def get_latest_checkpoint(self) -> Optional[str]:
        """
        Get latest checkpoint by step number.

        Returns:
            Name of latest checkpoint
        """
        metadata = self._load_metadata()

        if not metadata.get("checkpoints"):
            return None

        checkpoints = metadata["checkpoints"]

        latest = max(checkpoints, key=lambda cp: cp["step"])

        self.logger.info("latest_checkpoint", checkpoint=latest["name"], step=latest["step"])

        return latest["name"]

    def list_checkpoints(self) -> list[dict[str, Any]]:
        """
        List all checkpoints.

        Returns:
            List of checkpoint metadata
        """
        metadata = self._load_metadata()
        return metadata.get("checkpoints", [])

    def delete_checkpoint(self, checkpoint_name: str) -> None:
        """
        Delete a checkpoint.

        Args:
            checkpoint_name: Name of checkpoint to delete
        """
        checkpoint_path = self.checkpoint_dir / checkpoint_name

        if checkpoint_path.exists():
            shutil.rmtree(checkpoint_path)

            # Update metadata
            metadata = self._load_metadata()
            metadata["checkpoints"] = [
                cp for cp in metadata.get("checkpoints", [])
                if cp["name"] != checkpoint_name
            ]
            self._save_metadata(metadata)

            self.logger.info("checkpoint_deleted", checkpoint=checkpoint_name)

    def _update_metadata(
        self,
        checkpoint_name: str,
        step: int,
        metrics: dict[str, Any]
    ) -> None:
        """Update checkpoint metadata"""
        metadata = self._load_metadata()

        if "checkpoints" not in metadata:
            metadata["checkpoints"] = []

        # Remove existing entry for this checkpoint
        metadata["checkpoints"] = [
            cp for cp in metadata["checkpoints"]
            if cp["name"] != checkpoint_name
        ]

        # Add new entry
        metadata["checkpoints"].append({
            "name": checkpoint_name,
            "step": step,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        })

        self._save_metadata(metadata)

    def _cleanup_old_checkpoints(self) -> None:
        """Remove old checkpoints beyond max_checkpoints"""
        metadata = self._load_metadata()

        checkpoints = metadata.get("checkpoints", [])

        if len(checkpoints) <= self.max_checkpoints:
            return

        # Sort by step (keep most recent)
        sorted_checkpoints = sorted(checkpoints, key=lambda cp: cp["step"], reverse=True)

        # Keep only max_checkpoints
        to_keep = sorted_checkpoints[:self.max_checkpoints]
        to_delete = sorted_checkpoints[self.max_checkpoints:]

        for cp in to_delete:
            self.delete_checkpoint(cp["name"])

        self.logger.info(
            "cleaned_up_checkpoints",
            deleted=len(to_delete),
            kept=len(to_keep)
        )

    def _load_metadata(self) -> dict[str, Any]:
        """Load checkpoint metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                return json.load(f)
        else:
            return {"checkpoints": []}

    def _save_metadata(self, metadata: dict[str, Any]) -> None:
        """Save checkpoint metadata"""
        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)
