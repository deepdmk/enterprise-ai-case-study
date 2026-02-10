"""
RLHF Feedback Collection for MoE Interface.

Collects user feedback on MoE model responses for future RLHF training.
Stores feedback in JSONL format for easy processing.
"""

import json
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class InterfaceFeedbackEntry:
    """Single feedback entry for MoE interface interaction."""

    feedback_id: str
    session_id: str
    timestamp: str
    unit_id: str
    prompt: str
    response: str
    activated_experts: list[dict]
    generation_params: dict
    thumbs_up: bool | None = None
    rating: int | None = None
    comment: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class InterfaceFeedbackCollector:
    """
    Collects and stores user feedback on MoE model responses.

    Feedback is stored in monthly JSONL files:
    - data/feedback/interface_feedback_YYYY-MM.jsonl (production)
    - data/feedback/test_interface_feedback_YYYY-MM.jsonl (test mode)
    """

    def __init__(self, feedback_dir: str | Path, test_mode: bool = False):
        """
        Initialize the feedback collector.

        Args:
            feedback_dir: Directory to store feedback files.
            test_mode: If True, use test_ prefix for files.
        """
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self.test_mode = test_mode

        # Track active interactions for feedback
        self._active_interactions: dict[str, dict] = {}

        logger.info(
            "interface_feedback_collector_initialized",
            feedback_dir=str(self.feedback_dir),
            test_mode=test_mode,
        )

    def create_session(self) -> str:
        """
        Create a new session ID.

        Returns:
            UUID session identifier.
        """
        session_id = str(uuid.uuid4())
        logger.info("interface_session_created", session_id=session_id)
        return session_id

    def record_interaction(
        self,
        session_id: str,
        unit_id: str,
        prompt: str,
        response: str,
        activated_experts: list[dict],
        generation_params: dict,
    ) -> str:
        """
        Record an interaction for potential feedback.

        Args:
            session_id: Session identifier.
            unit_id: Unit ID (fundraising, business_development, field_operations).
            prompt: User prompt text.
            response: Model response text.
            activated_experts: List of activated experts with scores.
            generation_params: Generation parameters used.

        Returns:
            Feedback ID for this interaction.
        """
        feedback_id = str(uuid.uuid4())

        # Store interaction context for feedback
        self._active_interactions[feedback_id] = {
            "session_id": session_id,
            "unit_id": unit_id,
            "prompt": prompt,
            "response": response,
            "activated_experts": activated_experts,
            "generation_params": generation_params,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        logger.info(
            "interaction_recorded",
            feedback_id=feedback_id,
            session_id=session_id,
            unit_id=unit_id,
            num_experts=len(activated_experts),
        )

        return feedback_id

    def submit_feedback(
        self,
        feedback_id: str,
        thumbs_up: bool | None = None,
        rating: int | None = None,
        comment: str = "",
    ) -> None:
        """
        Submit feedback for a recorded interaction.

        Args:
            feedback_id: Feedback ID from record_interaction.
            thumbs_up: True for positive, False for negative, None for neutral.
            rating: Optional 1-5 rating.
            comment: Optional text comment.
        """
        if feedback_id not in self._active_interactions:
            logger.warning("feedback_not_found", feedback_id=feedback_id)
            return

        interaction_data = self._active_interactions[feedback_id]

        # Create feedback entry
        entry = InterfaceFeedbackEntry(
            feedback_id=feedback_id,
            session_id=interaction_data["session_id"],
            timestamp=interaction_data["timestamp"],
            unit_id=interaction_data["unit_id"],
            prompt=interaction_data["prompt"],
            response=interaction_data["response"],
            activated_experts=interaction_data["activated_experts"],
            generation_params=interaction_data["generation_params"],
            thumbs_up=thumbs_up,
            rating=rating,
            comment=comment,
        )

        # Append to JSONL file
        self._append_to_file(entry)

        # Remove from active interactions
        del self._active_interactions[feedback_id]

        logger.info(
            "interface_feedback_submitted",
            feedback_id=feedback_id,
            unit_id=interaction_data["unit_id"],
            thumbs_up=thumbs_up,
            rating=rating,
            has_comment=bool(comment),
        )

    def _append_to_file(self, entry: InterfaceFeedbackEntry) -> None:
        """
        Append feedback entry to monthly JSONL file.

        Args:
            entry: Feedback entry to append.
        """
        # Determine file name based on current month
        now = datetime.now(UTC)
        month_str = now.strftime("%Y-%m")

        prefix = "test_interface_feedback" if self.test_mode else "interface_feedback"
        filename = f"{prefix}_{month_str}.jsonl"
        filepath = self.feedback_dir / filename

        # Append entry
        with open(filepath, "a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")

        logger.debug("interface_feedback_written", file=str(filepath))

    def get_stats(self) -> dict:
        """
        Get feedback statistics.

        Returns:
            Dictionary with feedback counts.
        """
        # Count entries across all files
        total = 0
        positive = 0
        negative = 0
        by_unit: dict[str, int] = {}

        pattern = "test_interface_feedback_*.jsonl" if self.test_mode else "interface_feedback_*.jsonl"

        corrupted_lines = 0
        for filepath in self.feedback_dir.glob(pattern):
            with open(filepath) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        corrupted_lines += 1
                        logger.warning(
                            "corrupted_feedback_line_skipped",
                            file=str(filepath),
                            line_num=line_num,
                        )
                        continue

                    total += 1
                    unit_id = entry.get("unit_id", "unknown")
                    by_unit[unit_id] = by_unit.get(unit_id, 0) + 1

                    if entry.get("thumbs_up") is True:
                        positive += 1
                    elif entry.get("thumbs_up") is False:
                        negative += 1

        if corrupted_lines > 0:
            logger.warning(
                "corrupted_feedback_lines_total",
                count=corrupted_lines,
            )

        return {
            "total_feedback": total,
            "positive": positive,
            "negative": negative,
            "neutral": total - positive - negative,
            "by_unit": by_unit,
        }
