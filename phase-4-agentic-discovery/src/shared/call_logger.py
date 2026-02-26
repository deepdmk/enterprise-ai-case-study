"""
A2A Call Logger for Discovery Analysis
Tracks agent-to-agent calls during the 90-day discovery phase.
"""

import fcntl
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .a2a_protocol import A2ARequest, A2AResponse, ResponseStatus


@dataclass
class A2ACallLog:
    """
    Log entry for an A2A call during discovery.

    Tracks the full lifecycle of a request/response pair plus metadata
    for analyzing adaptive depth effectiveness.
    """
    call_id: str
    timestamp: datetime
    source_agent: str
    target_agent: str
    goal: str
    call_depth: int
    max_depth: int
    status: ResponseStatus
    execution_time_ms: float
    cascaded_calls: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    phase: int = 1  # Which discovery phase (1-7)
    workflow_id: Optional[str] = None  # Optional workflow tracking

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "call_id": self.call_id,
            "timestamp": self.timestamp.isoformat(),
            "source_agent": self.source_agent,
            "target_agent": self.target_agent,
            "goal": self.goal,
            "call_depth": self.call_depth,
            "max_depth": self.max_depth,
            "status": self.status.value,
            "execution_time_ms": self.execution_time_ms,
            "cascaded_calls": self.cascaded_calls,
            "error_message": self.error_message,
            "phase": self.phase,
            "workflow_id": self.workflow_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2ACallLog":
        """Create from dictionary"""
        data = data.copy()
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        data["status"] = ResponseStatus(data["status"])
        return cls(**data)

    @classmethod
    def from_request_response(
        cls,
        request: A2ARequest,
        response: A2AResponse,
        phase: int = 1,
        workflow_id: Optional[str] = None
    ) -> "A2ACallLog":
        """Create log entry from request/response pair"""
        if not request.metadata:
            raise ValueError("Request must have metadata for logging")

        return cls(
            call_id=request.metadata.call_id,
            timestamp=request.metadata.timestamp,
            source_agent=request.metadata.source_agent,
            target_agent=request.metadata.target_agent,
            goal=request.goal,
            call_depth=request.metadata.call_depth,
            max_depth=request.metadata.max_depth,
            status=response.status,
            execution_time_ms=response.execution_time_ms or 0.0,
            cascaded_calls=response.cascaded_calls,
            error_message=response.error_message,
            phase=phase,
            workflow_id=workflow_id
        )


class A2ACallLogger:
    """
    Logger for A2A protocol calls.

    Writes call logs to JSONL files organized by discovery phase.
    Provides analysis utilities for the adaptive depth analyzer.
    """

    def __init__(self, log_directory: Path):
        """
        Initialize call logger.

        Args:
            log_directory: Directory to store log files
        """
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)

        # Track current phase
        self._current_phase = 1

    def set_phase(self, phase: int) -> None:
        """Set the current discovery phase"""
        self._current_phase = phase

    def log_call(
        self,
        request: A2ARequest,
        response: A2AResponse,
        workflow_id: Optional[str] = None
    ) -> None:
        """
        Log an A2A call to disk.

        Args:
            request: The A2A request
            response: The A2A response
            workflow_id: Optional workflow identifier
        """
        log_entry = A2ACallLog.from_request_response(
            request=request,
            response=response,
            phase=self._current_phase,
            workflow_id=workflow_id
        )

        # Write to phase-specific log file with file locking
        log_file = self._get_log_file(self._current_phase)
        with open(log_file, "a") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.write(json.dumps(log_entry.to_dict()) + "\n")
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def iter_logs(self, phase: Optional[int] = None) -> Iterator[A2ACallLog]:
        """
        Stream logs without loading all into memory.

        Args:
            phase: Load logs for a specific phase, or all phases if None

        Yields:
            Call log entries one at a time
        """
        if phase is not None:
            log_files = [self._get_log_file(phase)]
        else:
            # Load all phase logs
            log_files = sorted(self.log_directory.glob("phase_*.jsonl"))

        for log_file in log_files:
            if log_file.exists():
                with open(log_file) as f:
                    for line in f:
                        if line.strip():
                            yield A2ACallLog.from_dict(json.loads(line))

    def load_logs(self, phase: Optional[int] = None) -> List[A2ACallLog]:
        """
        Load call logs from disk.

        Args:
            phase: Load logs for a specific phase, or all phases if None

        Returns:
            List of call logs
        """
        return list(self.iter_logs(phase))

    def get_phase_stats(self, phase: int) -> Dict[str, Any]:
        """
        Get statistics for a specific phase.

        Returns:
            Dictionary with phase statistics
        """
        logs = self.load_logs(phase)

        if not logs:
            return {
                "phase": phase,
                "total_calls": 0,
                "avg_depth": 0.0,
                "max_depth": 0,
                "success_rate": 0.0,
                "avg_execution_time": 0.0
            }

        total_calls = len(logs)
        successful = sum(1 for log in logs if log.status == ResponseStatus.SUCCESS)
        total_depth = sum(log.call_depth for log in logs)
        max_depth = max(log.call_depth for log in logs)
        total_time = sum(log.execution_time_ms for log in logs)

        return {
            "phase": phase,
            "total_calls": total_calls,
            "avg_depth": total_depth / total_calls,
            "max_depth": max_depth,
            "success_rate": successful / total_calls,
            "avg_execution_time": total_time / total_calls,
            "status_breakdown": self._get_status_breakdown(logs)
        }

    def _get_log_file(self, phase: int) -> Path:
        """Get log file path for a phase"""
        return self.log_directory / f"phase_{phase}.jsonl"

    def _get_status_breakdown(self, logs: List[A2ACallLog]) -> Dict[str, int]:
        """Get breakdown of response statuses"""
        breakdown = {}
        for log in logs:
            status = log.status.value
            breakdown[status] = breakdown.get(status, 0) + 1
        return breakdown

    def export_for_analysis(self, output_file: Path) -> None:
        """
        Export all logs to a single file for analysis.

        Args:
            output_file: Path to output file
        """
        all_logs = self.load_logs()

        with open(output_file, "w") as f:
            json.dump(
                [log.to_dict() for log in all_logs],
                f,
                indent=2
            )
