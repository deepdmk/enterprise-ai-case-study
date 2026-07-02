"""
Discovery Converter

Converts Phase 4 discovery logs to training format for orchestrator fine-tuning.
"""

from pathlib import Path
from typing import Any
from phase0_infra.habitat_logging import get_logger

from ..shared.phase4_importer import Phase4Importer
from ..shared.routing_schema import TrainingExample, AgentType

logger = get_logger(__name__)


class DiscoveryConverter:
    """
    Converts Phase 4 orchestrator training data to Phase 5 format.
    """

    def __init__(self, phase4_exports_dir: Path = None):
        """
        Initialize converter.

        Args:
            phase4_exports_dir: Path to Phase 4 exports directory
        """
        self.importer = Phase4Importer(phase4_exports_dir)
        self.logger = logger.bind(component="discovery_converter")

    def convert_training_examples(
        self,
        test_mode: bool = False
    ) -> list[TrainingExample]:
        """
        Convert Phase 4 training examples to TrainingExample objects.

        Args:
            test_mode: If True, limit to small sample

        Returns:
            List of TrainingExample objects
        """
        self.logger.info("converting_training_examples", test_mode=test_mode)

        # Import Phase 4 data
        raw_examples = self.importer.import_training_examples()

        if not raw_examples:
            self.logger.warning("no_examples_found", message="No Phase 4 data to convert")
            return []

        # Limit in test mode
        if test_mode:
            raw_examples = raw_examples[:100]
            self.logger.info("test_mode_limiting", count=100)

        # Convert to TrainingExample objects
        training_examples = []

        for raw in raw_examples:
            try:
                example = self._convert_single_example(raw)
                if example:
                    training_examples.append(example)
            except Exception as e:
                self.logger.warning(
                    "conversion_failed",
                    query=raw.get("query", "unknown"),
                    error=str(e)
                )
                continue

        self.logger.info("conversion_complete", count=len(training_examples))
        return training_examples

    def _convert_single_example(self, raw: dict[str, Any]) -> TrainingExample:
        """
        Convert a single raw example to TrainingExample.

        Args:
            raw: Raw example dict from Phase 4

        Returns:
            TrainingExample object
        """
        # Map agent names to AgentType enum
        entry_agent_str = raw.get("entry_agent", "")
        entry_agent = self._map_agent_name(entry_agent_str)

        return TrainingExample(
            query=raw.get("query", ""),
            entry_agent=entry_agent,
            optimal_depth=raw.get("optimal_depth", 2),
            call_sequence=raw.get("call_sequence", []),
            final_response=raw.get("final_response", ""),
            metadata=raw.get("metadata", {})
        )

    def _map_agent_name(self, agent_name: str) -> AgentType:
        """Map agent name string to AgentType enum"""
        agent_mapping = {
            "fundraising-agent": AgentType.FUNDRAISING,
            "business-development-agent": AgentType.BUSINESS_DEVELOPMENT,
            "field-operations-agent": AgentType.FIELD_OPERATIONS
        }

        return agent_mapping.get(agent_name, AgentType.FIELD_OPERATIONS)

    def convert_to_chat_format(
        self,
        training_examples: list[TrainingExample]
    ) -> list[dict[str, Any]]:
        """
        Convert training examples to ChatML format.

        Args:
            training_examples: List of TrainingExample objects

        Returns:
            List of ChatML formatted examples
        """
        self.logger.info("converting_to_chat_format", count=len(training_examples))

        chat_examples = []
        for example in training_examples:
            try:
                chat_format = example.to_chat_format()
                chat_examples.append(chat_format)
            except Exception as e:
                self.logger.warning(
                    "chat_conversion_failed",
                    query=example.query,
                    error=str(e)
                )
                continue

        self.logger.info("chat_conversion_complete", count=len(chat_examples))
        return chat_examples

    def export_training_data(
        self,
        training_examples: list[TrainingExample],
        output_dir: Path
    ) -> None:
        """
        Export training data to files.

        Args:
            training_examples: Training examples to export
            output_dir: Output directory
        """
        import json

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Export as JSON (list format)
        json_file = output_dir / "converted_examples.json"
        with open(json_file, "w") as f:
            json.dump(
                [ex.model_dump() for ex in training_examples],
                f,
                indent=2
            )
        self.logger.info("exported_json", path=str(json_file), count=len(training_examples))

        # Export as JSONL
        jsonl_file = output_dir / "converted_examples.jsonl"
        with open(jsonl_file, "w") as f:
            for ex in training_examples:
                f.write(json.dumps(ex.model_dump()) + "\n")
        self.logger.info("exported_jsonl", path=str(jsonl_file), count=len(training_examples))

        # Export ChatML format
        chat_examples = self.convert_to_chat_format(training_examples)
        chat_file = output_dir / "chat_format.jsonl"
        with open(chat_file, "w") as f:
            for ex in chat_examples:
                f.write(json.dumps(ex) + "\n")
        self.logger.info("exported_chat", path=str(chat_file), count=len(chat_examples))

    def validate_conversion(
        self,
        training_examples: list[TrainingExample]
    ) -> dict[str, Any]:
        """
        Validate converted training examples.

        Args:
            training_examples: Training examples to validate

        Returns:
            Validation statistics
        """
        stats = {
            "total_examples": len(training_examples),
            "agents": {},
            "depths": {},
            "successful": 0,
            "failed": 0
        }

        for example in training_examples:
            # Count by agent
            agent = example.entry_agent.value
            stats["agents"][agent] = stats["agents"].get(agent, 0) + 1

            # Count by depth
            depth = example.optimal_depth
            stats["depths"][depth] = stats["depths"].get(depth, 0) + 1

            # Count by success
            if example.metadata.get("success", False):
                stats["successful"] += 1
            else:
                stats["failed"] += 1

        self.logger.info("validation_complete", stats=stats)
        return stats

    def create_mock_data(self, count: int = 100) -> list[TrainingExample]:
        """
        Create mock training data for testing.

        Args:
            count: Number of examples to create

        Returns:
            List of mock TrainingExample objects
        """
        self.logger.info("creating_mock_data", count=count)

        mock_examples = []

        queries = [
            ("What is the investment capacity of investor INV-123?", AgentType.FUNDRAISING, 1),
            ("Evaluate funding opportunity in Kenya for climate project", AgentType.FIELD_OPERATIONS, 3),
            ("What RFPs are currently open in the education sector?", AgentType.BUSINESS_DEVELOPMENT, 2),
            ("Should we pursue partnership with INV-456?", AgentType.FUNDRAISING, 2),
            ("Assess competitive landscape for renewable energy funding", AgentType.BUSINESS_DEVELOPMENT, 3),
        ]

        for i in range(count):
            query, agent, depth = queries[i % len(queries)]

            example = TrainingExample(
                query=f"{query} (example {i+1})",
                entry_agent=agent,
                optimal_depth=depth,
                call_sequence=[{
                    "depth": 0,
                    "target": agent.value,
                    "goal": query
                }],
                final_response=f"Mock response for {query}",
                metadata={
                    "workflow_id": f"mock_workflow_{i % 5}",
                    "success": True,
                    "execution_time_ms": 100 + (i % 500)
                }
            )

            mock_examples.append(example)

        self.logger.info("mock_data_created", count=len(mock_examples))
        return mock_examples
