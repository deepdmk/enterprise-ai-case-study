"""
Orchestrator Training Data Exporter

Exports discovery logs as training data for Phase 5 orchestrator models.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from ..shared.call_logger import A2ACallLogger, A2ACallLog
from ..shared.a2a_protocol import ResponseStatus


class OrchestratorTrainingExample:
    """
    Training example for Phase 5 orchestrator.

    Orchestrators learn to:
    1. Decompose complex queries into sub-tasks
    2. Route tasks to appropriate agents
    3. Determine optimal cascade depth
    4. Synthesize multi-agent responses
    """

    def __init__(
        self,
        query: str,
        entry_agent: str,
        optimal_depth: int,
        call_sequence: List[Dict[str, Any]],
        final_response: str,
        metadata: Dict[str, Any]
    ):
        """
        Initialize training example.

        Args:
            query: User query
            entry_agent: Which agent should handle this
            optimal_depth: Optimal cascade depth for this query
            call_sequence: Sequence of agent calls made
            final_response: Final synthesized response
            metadata: Additional metadata (success, timing, etc.)
        """
        self.query = query
        self.entry_agent = entry_agent
        self.optimal_depth = optimal_depth
        self.call_sequence = call_sequence
        self.final_response = final_response
        self.metadata = metadata

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "query": self.query,
            "entry_agent": self.entry_agent,
            "optimal_depth": self.optimal_depth,
            "call_sequence": self.call_sequence,
            "final_response": self.final_response,
            "metadata": self.metadata
        }

    def to_chat_format(self) -> Dict[str, Any]:
        """
        Convert to chat/instruction format for training.

        Returns:
            ChatML-style training example
        """
        # Build system prompt
        system_prompt = """You are an AI orchestrator that coordinates multiple specialized agents.

Your responsibilities:
1. Analyze user queries and determine which agents to call
2. Decide the optimal cascade depth (how many levels of agent calls)
3. Decompose complex queries into sub-tasks
4. Route sub-tasks to appropriate agents
5. Synthesize responses from multiple agents

Available agents:
- fundraising-agent: Investor profiles, capacity, interests
- business-development-agent: RFP data, competitive landscape
- field-operations-agent: Local capacity, project performance

For each query, output:
1. Entry agent (which agent should handle this)
2. Optimal depth (1-4, how many cascade levels needed)
3. Rationale (why this routing and depth)
"""

        # Build user message
        user_message = f"Query: {self.query}"

        # Build expected response
        assistant_response = f"""Entry agent: {self.entry_agent}
Optimal depth: {self.optimal_depth}

Rationale: {self._generate_rationale()}

Call sequence:
{json.dumps(self.call_sequence, indent=2)}
"""

        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_response}
            ],
            "metadata": {
                "query": self.query,
                "optimal_depth": self.optimal_depth,
                "success": self.metadata.get("success", False)
            }
        }

    def _generate_rationale(self) -> str:
        """Generate rationale for the routing decision"""
        rationales = {
            "fundraising-agent": "This query requires investor-specific information",
            "business-development-agent": "This query focuses on funding opportunities and RFPs",
            "field-operations-agent": "This query requires regional or local capacity information"
        }

        agent_rationale = rationales.get(
            self.entry_agent,
            f"Best handled by {self.entry_agent}"
        )

        depth_rationale = ""
        if self.optimal_depth == 1:
            depth_rationale = "Direct answer without cascading needed"
        elif self.optimal_depth == 2:
            depth_rationale = "Requires one level of cascading to related agent"
        elif self.optimal_depth >= 3:
            depth_rationale = "Complex query requiring multi-agent coordination"

        return f"{agent_rationale}. {depth_rationale}."


class OrchestratorExporter:
    """
    Exports discovery logs as training data for Phase 5 orchestrators.
    """

    def __init__(self, log_directory: Path):
        """
        Initialize exporter.

        Args:
            log_directory: Directory containing discovery logs
        """
        self.log_directory = Path(log_directory)
        self.logger = A2ACallLogger(log_directory)

    def export_training_data(
        self,
        output_dir: Path,
        optimal_depths: Dict[str, int],
        min_success_rate: float = 0.8
    ) -> int:
        """
        Export training data for orchestrators.

        Args:
            output_dir: Where to save training data
            optimal_depths: Optimal depths per workflow
            min_success_rate: Minimum success rate to include example

        Returns:
            Number of examples exported
        """
        print(f"\n{'='*80}")
        print("Exporting Orchestrator Training Data")
        print(f"{'='*80}\n")

        # Load all logs
        all_logs = self.logger.load_logs()
        print(f"Loaded {len(all_logs)} call logs")

        # Group by workflow
        workflow_logs = self._group_by_workflow(all_logs)
        print(f"Found {len(workflow_logs)} workflows\n")

        # Generate training examples
        examples = []

        for workflow_id, logs in workflow_logs.items():
            print(f"Processing workflow: {workflow_id}")

            # Filter successful calls
            successful_logs = [
                log for log in logs
                if log.status == ResponseStatus.SUCCESS
            ]

            if not successful_logs:
                print(f"  No successful calls, skipping")
                continue

            # Get optimal depth for this workflow
            optimal_depth = optimal_depths.get(workflow_id, 2)

            # Generate examples
            workflow_examples = self._generate_examples(
                successful_logs,
                workflow_id,
                optimal_depth
            )

            examples.extend(workflow_examples)
            print(f"  Generated {len(workflow_examples)} examples")

        print(f"\nTotal examples: {len(examples)}")

        # Export in multiple formats
        self._export_json(examples, output_dir / "orchestrator_training.json")
        self._export_jsonl(examples, output_dir / "orchestrator_training.jsonl")
        self._export_chat_format(examples, output_dir / "orchestrator_chat.jsonl")

        print(f"\n✓ Export complete")
        return len(examples)

    def _group_by_workflow(
        self,
        logs: List[A2ACallLog]
    ) -> Dict[str, List[A2ACallLog]]:
        """Group logs by workflow ID"""
        from collections import defaultdict

        workflow_logs = defaultdict(list)
        for log in logs:
            if log.workflow_id:
                workflow_logs[log.workflow_id].append(log)

        return dict(workflow_logs)

    def _generate_examples(
        self,
        logs: List[A2ACallLog],
        workflow_id: str,
        optimal_depth: int
    ) -> List[OrchestratorTrainingExample]:
        """
        Generate training examples from logs.

        Args:
            logs: Call logs for this workflow
            workflow_id: Workflow identifier
            optimal_depth: Optimal depth for this workflow

        Returns:
            List of training examples
        """
        examples = []

        # Group logs by trace_id to reconstruct full call chains
        # For now, create one example per successful call
        for log in logs:
            if log.status != ResponseStatus.SUCCESS:
                continue

            # Build call sequence
            call_sequence = [{
                "depth": log.call_depth,
                "target": log.target_agent,
                "goal": log.goal,
                "cascaded_to": log.cascaded_calls
            }]

            # Create example
            example = OrchestratorTrainingExample(
                query=log.goal,
                entry_agent=log.target_agent,
                optimal_depth=optimal_depth,
                call_sequence=call_sequence,
                final_response=f"Successfully processed via {log.target_agent}",
                metadata={
                    "workflow_id": workflow_id,
                    "success": True,
                    "execution_time_ms": log.execution_time_ms,
                    "phase": log.phase,
                    "actual_depth": log.call_depth
                }
            )

            examples.append(example)

        return examples

    def _export_json(self, examples: List[OrchestratorTrainingExample], output_file: Path) -> None:
        """Export examples as JSON"""
        output_file.parent.mkdir(parents=True, exist_ok=True)

        data = [ex.to_dict() for ex in examples]

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"  Exported JSON: {output_file}")

    def _export_jsonl(self, examples: List[OrchestratorTrainingExample], output_file: Path) -> None:
        """Export examples as JSONL"""
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            for ex in examples:
                f.write(json.dumps(ex.to_dict()) + "\n")

        print(f"  Exported JSONL: {output_file}")

    def _export_chat_format(self, examples: List[OrchestratorTrainingExample], output_file: Path) -> None:
        """Export examples in chat/instruction format"""
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            for ex in examples:
                chat_format = ex.to_chat_format()
                f.write(json.dumps(chat_format) + "\n")

        print(f"  Exported Chat Format: {output_file}")

    def export_summary(self, output_file: Path, optimal_depths: Dict[str, int]) -> None:
        """
        Export summary of discovery experiment.

        Args:
            output_file: Path to summary file
            optimal_depths: Optimal depths determined by analyzer
        """
        summary = {
            "export_timestamp": datetime.now().isoformat(),
            "optimal_depths": optimal_depths,
            "workflows": {},
            "phase_5_recommendations": self._generate_phase5_recommendations(optimal_depths)
        }

        # Get workflow stats
        all_logs = self.logger.load_logs()
        workflow_logs = self._group_by_workflow(all_logs)

        for workflow_id, logs in workflow_logs.items():
            successful = sum(1 for log in logs if log.status == ResponseStatus.SUCCESS)
            summary["workflows"][workflow_id] = {
                "total_calls": len(logs),
                "successful_calls": successful,
                "success_rate": successful / len(logs) if logs else 0,
                "optimal_depth": optimal_depths.get(workflow_id, 2)
            }

        # Export
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\nSummary exported: {output_file}")

    def _generate_phase5_recommendations(self, optimal_depths: Dict[str, int]) -> List[str]:
        """Generate recommendations for Phase 5"""
        recommendations = [
            "Use exported orchestrator_chat.jsonl for instruction fine-tuning",
            "Train orchestrator to predict optimal_depth based on query analysis",
            "Implement adaptive routing based on discovered patterns",
            f"Default depths: {optimal_depths}",
            "Monitor Phase 5 performance against Phase 4 baselines"
        ]
        return recommendations
