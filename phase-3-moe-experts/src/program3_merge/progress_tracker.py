"""Progress tracking for merge operations."""

import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class MergeProgress:
    """Track progress of merge operation."""

    stage: str = "initializing"
    progress_percent: float = 0.0
    current_expert: int = 0
    total_experts: int = 0
    start_time: datetime = field(default_factory=datetime.utcnow)
    messages: list[str] = field(default_factory=list)
    is_complete: bool = False
    error: str | None = None

    def update(
        self,
        stage: str | None = None,
        progress: float | None = None,
        message: str | None = None,
    ) -> None:
        """Update progress."""
        if stage:
            self.stage = stage
        if progress is not None:
            self.progress_percent = progress
        if message:
            self.messages.append(f"[{datetime.utcnow().isoformat()}] {message}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "progress_percent": self.progress_percent,
            "current_expert": self.current_expert,
            "total_experts": self.total_experts,
            "start_time": self.start_time.isoformat(),
            "elapsed_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "is_complete": self.is_complete,
            "error": self.error,
            "messages": self.messages[-10:],  # Last 10 messages
        }


class ProgressTracker:
    """Track and report merge progress."""

    def __init__(
        self,
        total_experts: int,
        output_dir: Path | None = None,
        callback: Callable[[MergeProgress], None] | None = None,
    ):
        """
        Initialize progress tracker.

        Args:
            total_experts: Total number of experts being merged
            output_dir: Directory to write progress file
            callback: Optional callback for progress updates
        """
        self.progress = MergeProgress(total_experts=total_experts)
        self.output_dir = output_dir
        self.callback = callback
        self._lock = threading.Lock()

    def start(self) -> None:
        """Mark merge as started."""
        with self._lock:
            self.progress.stage = "starting"
            self.progress.update(message="Merge operation started")
            self._notify()

    def loading_config(self) -> None:
        """Mark config loading stage."""
        with self._lock:
            self.progress.stage = "loading_config"
            self.progress.progress_percent = 5.0
            self.progress.update(message="Loading merge configuration")
            self._notify()

    def loading_base_model(self) -> None:
        """Mark base model loading stage."""
        with self._lock:
            self.progress.stage = "loading_base_model"
            self.progress.progress_percent = 10.0
            self.progress.update(message="Loading base model")
            self._notify()

    def processing_expert(self, expert_num: int, expert_id: str = "") -> None:
        """Mark processing of an expert."""
        with self._lock:
            self.progress.stage = "processing_experts"
            self.progress.current_expert = expert_num

            # Calculate progress (10% config + 10% base + 70% experts + 10% saving)
            expert_progress = (expert_num / self.progress.total_experts) * 70
            self.progress.progress_percent = 20.0 + expert_progress

            msg = f"Processing expert {expert_num}/{self.progress.total_experts}"
            if expert_id:
                msg += f" ({expert_id})"
            self.progress.update(message=msg)
            self._notify()

    def building_router(self) -> None:
        """Mark router building stage."""
        with self._lock:
            self.progress.stage = "building_router"
            self.progress.progress_percent = 92.0
            self.progress.update(message="Building router layer")
            self._notify()

    def saving_model(self) -> None:
        """Mark model saving stage."""
        with self._lock:
            self.progress.stage = "saving_model"
            self.progress.progress_percent = 95.0
            self.progress.update(message="Saving merged model")
            self._notify()

    def complete(self) -> None:
        """Mark merge as complete."""
        with self._lock:
            self.progress.stage = "complete"
            self.progress.progress_percent = 100.0
            self.progress.is_complete = True
            self.progress.update(message="Merge complete!")
            self._notify()
            self._save_final()

    def error(self, error_msg: str) -> None:
        """Mark merge as failed."""
        with self._lock:
            self.progress.stage = "error"
            self.progress.is_complete = True
            self.progress.error = error_msg
            self.progress.update(message=f"Error: {error_msg}")
            self._notify()
            self._save_final()

    def _notify(self) -> None:
        """Notify callback and save progress."""
        if self.callback:
            try:
                self.callback(self.progress)
            except Exception as e:
                logger.warning("callback_error", error=str(e))

        if self.output_dir:
            self._save_progress()

    def _save_progress(self) -> None:
        """Save progress to file."""
        if not self.output_dir:
            return

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            progress_path = self.output_dir / "merge_progress.json"

            with open(progress_path, "w") as f:
                json.dump(self.progress.to_dict(), f, indent=2)
        except Exception as e:
            logger.warning("progress_save_failed", error=str(e))

    def _save_final(self) -> None:
        """Save final progress."""
        if not self.output_dir:
            return

        try:
            final_path = self.output_dir / "merge_result.json"
            with open(final_path, "w") as f:
                json.dump(self.progress.to_dict(), f, indent=2)
        except Exception as e:
            logger.warning("final_save_failed", error=str(e))


def print_progress_bar(progress: MergeProgress) -> None:
    """Print a progress bar to console."""
    bar_width = 40
    filled = int(bar_width * progress.progress_percent / 100)
    bar = "=" * filled + "-" * (bar_width - filled)

    elapsed = (datetime.utcnow() - progress.start_time).total_seconds()

    print(
        f"\r[{bar}] {progress.progress_percent:.1f}% | "
        f"{progress.stage} | "
        f"Expert {progress.current_expert}/{progress.total_experts} | "
        f"{elapsed:.0f}s",
        end="",
        flush=True,
    )

    if progress.is_complete:
        print()  # New line at completion


def watch_progress_file(progress_file: Path, interval: float = 1.0) -> None:
    """Watch a progress file and print updates."""
    last_mtime = 0.0

    while True:
        try:
            if progress_file.exists():
                current_mtime = progress_file.stat().st_mtime
                if current_mtime > last_mtime:
                    with open(progress_file) as f:
                        progress_data = json.load(f)

                    progress = MergeProgress(
                        stage=progress_data.get("stage", "unknown"),
                        progress_percent=progress_data.get("progress_percent", 0),
                        current_expert=progress_data.get("current_expert", 0),
                        total_experts=progress_data.get("total_experts", 0),
                        is_complete=progress_data.get("is_complete", False),
                    )

                    print_progress_bar(progress)

                    if progress.is_complete:
                        break

                    last_mtime = current_mtime

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\nWatch cancelled")
            break
        except Exception as e:
            logger.warning("watch_error", error=str(e))
            time.sleep(interval)
