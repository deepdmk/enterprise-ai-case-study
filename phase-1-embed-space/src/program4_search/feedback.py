"""
RLHF Feedback Collection.

Collects user feedback on search results for future RLHF training.
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
class FeedbackEntry:
    """Single feedback entry."""

    feedback_id: str
    session_id: str
    timestamp: str
    query: str
    results: list[dict]
    thumbs_up: bool | None = None
    rating: int | None = None
    comment: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class FeedbackCollector:
    """
    Collects and stores user feedback on search results.

    Feedback is stored in monthly JSONL files:
    - data/feedback/feedback_YYYY-MM.jsonl (production)
    - data/feedback/test_feedback_YYYY-MM.jsonl (test mode)
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

        # Track active searches for feedback
        self._active_searches: dict[str, dict] = {}

        logger.info(
            "feedback_collector_initialized",
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
        logger.info("session_created", session_id=session_id)
        return session_id

    def record_search(
        self,
        session_id: str,
        query: str,
        results: list[dict],
    ) -> str:
        """
        Record a search for potential feedback.

        Args:
            session_id: Session identifier.
            query: Search query text.
            results: List of search results (as dicts).

        Returns:
            Feedback ID for this search.
        """
        feedback_id = str(uuid.uuid4())

        # Store search context for feedback
        self._active_searches[feedback_id] = {
            "session_id": session_id,
            "query": query,
            "results": results,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        logger.info(
            "search_recorded",
            feedback_id=feedback_id,
            session_id=session_id,
            num_results=len(results),
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
        Submit feedback for a recorded search.

        Args:
            feedback_id: Feedback ID from record_search.
            thumbs_up: True for positive, False for negative, None for neutral.
            rating: Optional 1-5 rating.
            comment: Optional text comment.
        """
        if feedback_id not in self._active_searches:
            logger.warning("feedback_not_found", feedback_id=feedback_id)
            return

        search_data = self._active_searches[feedback_id]

        # Create feedback entry
        entry = FeedbackEntry(
            feedback_id=feedback_id,
            session_id=search_data["session_id"],
            timestamp=search_data["timestamp"],
            query=search_data["query"],
            results=search_data["results"],
            thumbs_up=thumbs_up,
            rating=rating,
            comment=comment,
        )

        # Append to JSONL file
        self._append_to_file(entry)

        # Remove from active searches
        del self._active_searches[feedback_id]

        logger.info(
            "feedback_submitted",
            feedback_id=feedback_id,
            thumbs_up=thumbs_up,
            rating=rating,
            has_comment=bool(comment),
        )

    def _append_to_file(self, entry: FeedbackEntry) -> None:
        """
        Append feedback entry to monthly JSONL file.

        Args:
            entry: Feedback entry to append.
        """
        # Determine file name based on current month
        now = datetime.now(UTC)
        month_str = now.strftime("%Y-%m")

        prefix = "test_feedback" if self.test_mode else "feedback"
        filename = f"{prefix}_{month_str}.jsonl"
        filepath = self.feedback_dir / filename

        # Append entry
        with open(filepath, "a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")

        logger.debug("feedback_written", file=str(filepath))

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

        pattern = "test_feedback_*.jsonl" if self.test_mode else "feedback_*.jsonl"

        for filepath in self.feedback_dir.glob(pattern):
            with open(filepath) as f:
                for line in f:
                    total += 1
                    entry = json.loads(line)
                    if entry.get("thumbs_up") is True:
                        positive += 1
                    elif entry.get("thumbs_up") is False:
                        negative += 1

        return {
            "total_feedback": total,
            "positive": positive,
            "negative": negative,
            "neutral": total - positive - negative,
        }
