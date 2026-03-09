"""
Training Data Logger

Captures orchestration interactions for future SLM fine-tuning.
Logs routing decisions, agent responses, and user feedback.
"""

from typing import Any, Optional
import json
import time
from pathlib import Path
from habitat_logging import get_logger

from ...shared.routing_schema import OrchestratedResponse, TrainingExample

logger = get_logger(__name__)


class TrainingLogger:
    """
    Logs orchestration interactions for future fine-tuning cycles.

    This enables continuous improvement of the orchestrator SLM by
    capturing real-world usage patterns and routing decisions.
    """

    def __init__(
        self,
        log_dir: str = "data/training/agno_logs",
        enabled: bool = True
    ):
        """
        Initialize training logger.

        Args:
            log_dir: Directory to store training logs
            enabled: Whether to enable logging
        """
        self.log_dir = Path(log_dir)
        self.enabled = enabled
        self.log_file = None

        if self.enabled:
            self.log_dir.mkdir(parents=True, exist_ok=True)

            # Create log file with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.log_file = self.log_dir / f"orchestration_log_{timestamp}.jsonl"

            logger.info(
                "training_logger_initialized",
                log_file=str(self.log_file),
                enabled=enabled
            )
        else:
            logger.info("training_logger_disabled")

    def log_orchestration(
        self,
        response: OrchestratedResponse,
        feedback: Optional[dict[str, Any]] = None
    ) -> None:
        """
        Log an orchestration interaction.

        Args:
            response: OrchestratedResponse from the orchestrator
            feedback: Optional user feedback (e.g., thumbs up/down, corrections)
        """
        if not self.enabled:
            return

        try:
            # Build training example
            log_entry = {
                "timestamp": time.time(),
                "query": response.query,
                "routing_decision": {
                    "entry_agent": response.routing_decision.entry_agent,
                    "optimal_depth": response.routing_decision.optimal_depth,
                    "workflow": response.routing_decision.workflow,
                    "reasoning": response.routing_decision.reasoning
                },
                "agent_responses": [
                    {
                        "agent": ar.agent,
                        "operation": ar.operation,
                        "success": ar.success,
                        "latency_ms": ar.latency_ms,
                        "cascaded_calls": ar.cascaded_calls
                    }
                    for ar in response.agent_responses
                ],
                "synthesized_response": response.synthesized_response,
                "total_latency_ms": response.total_latency_ms,
                "success": response.success,
                "feedback": feedback or {},
                "metadata": response.metadata or {}
            }

            # Append to JSONL file
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            logger.debug(
                "orchestration_logged",
                query=response.query[:50],
                success=response.success
            )

        except Exception as e:
            logger.error("training_log_failed", error=str(e))

    def log_routing_only(
        self,
        query: str,
        entry_agent: str,
        optimal_depth: int,
        reasoning: str
    ) -> None:
        """
        Log a routing decision only (no agent execution).

        Useful for capturing lightweight routing-only calls.

        Args:
            query: User query
            entry_agent: Selected entry agent
            optimal_depth: Optimal cascade depth
            reasoning: Routing reasoning
        """
        if not self.enabled:
            return

        try:
            log_entry = {
                "timestamp": time.time(),
                "query": query,
                "routing_only": True,
                "routing_decision": {
                    "entry_agent": entry_agent,
                    "optimal_depth": optimal_depth,
                    "reasoning": reasoning
                }
            }

            # Append to JSONL file
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            logger.debug("routing_logged", query=query[:50])

        except Exception as e:
            logger.error("routing_log_failed", error=str(e))

    def export_training_data(
        self,
        output_file: Optional[str] = None,
        filter_successful: bool = True
    ) -> str:
        """
        Export logged data to training format (ChatML JSONL).

        Args:
            output_file: Output file path (if None, auto-generate)
            filter_successful: Only include successful orchestrations

        Returns:
            Path to exported file
        """
        if output_file is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = str(self.log_dir / f"training_data_{timestamp}.jsonl")

        # Read all log entries
        log_entries = []
        if self.log_file.exists():
            with open(self.log_file, "r") as f:
                for line in f:
                    if line.strip():
                        log_entries.append(json.loads(line))

        # Convert to training examples
        training_count = 0
        with open(output_file, "w") as f:
            for entry in log_entries:
                # Skip routing-only entries
                if entry.get("routing_only"):
                    continue

                # Filter by success if requested
                if filter_successful and not entry.get("success", False):
                    continue

                # Convert to TrainingExample format
                training_example = self._convert_to_training_example(entry)

                if training_example:
                    # Write ChatML format
                    f.write(json.dumps(training_example.to_chat_format()) + "\n")
                    training_count += 1

        logger.info(
            "training_data_exported",
            output_file=output_file,
            count=training_count
        )

        return output_file

    def _convert_to_training_example(self, log_entry: dict[str, Any]) -> Optional[TrainingExample]:
        """
        Convert log entry to TrainingExample.

        Args:
            log_entry: Log entry dictionary

        Returns:
            TrainingExample or None
        """
        try:
            routing = log_entry.get("routing_decision", {})

            # Build call sequence
            call_sequence = []
            for ar in log_entry.get("agent_responses", []):
                call_sequence.append({
                    "agent": ar["agent"],
                    "operation": ar["operation"],
                    "success": ar["success"],
                    "latency_ms": ar["latency_ms"]
                })

            example = TrainingExample(
                query=log_entry["query"],
                entry_agent=routing.get("entry_agent", "field-operations-agent"),
                optimal_depth=routing.get("optimal_depth", 2),
                call_sequence=call_sequence,
                final_response=log_entry.get("synthesized_response", ""),
                metadata={
                    "timestamp": log_entry.get("timestamp"),
                    "success": log_entry.get("success", False),
                    "total_latency_ms": log_entry.get("total_latency_ms", 0),
                    "feedback": log_entry.get("feedback", {}),
                    "workflow": routing.get("workflow", "unknown")
                }
            )

            return example

        except Exception as e:
            logger.error("training_example_conversion_failed", error=str(e))
            return None

    def get_stats(self) -> dict[str, Any]:
        """
        Get logging statistics.

        Returns:
            Statistics dictionary
        """
        if not self.enabled or self.log_file is None or not self.log_file.exists():
            return {
                "total_logs": 0,
                "successful": 0,
                "failed": 0,
                "log_file": str(self.log_file)
            }

        total_logs = 0
        successful = 0
        failed = 0

        with open(self.log_file, "r") as f:
            for line in f:
                if line.strip():
                    total_logs += 1
                    entry = json.loads(line)
                    if entry.get("success", False):
                        successful += 1
                    else:
                        failed += 1

        return {
            "total_logs": total_logs,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total_logs if total_logs > 0 else 0,
            "log_file": str(self.log_file)
        }
