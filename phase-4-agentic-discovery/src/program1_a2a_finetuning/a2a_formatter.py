"""
A2A Data Formatter

Formats A2A training examples into ChatML format.
Extends Phase 2's data formatting with A2A-specific system prompts.
"""

from typing import Any, Optional
from .data_generator import A2ATrainingExample


# A2A System Prompt Template
A2A_SYSTEM_PROMPT = """You are a {unit_name} agent with A2A protocol capabilities.

Your primary responsibilities:
{responsibilities}

When you need information outside your capabilities, call other agents:
{available_agents}

Current context: Call depth: {depth}/{max_depth}

To call another agent, use this format:
<a2a_call>
{{"goal": "what you need", "target": "agent-id", "parameters": {{}}}}
</a2a_call>

Important rules:
1. Only call agents when necessary - prefer direct responses when you have the information
2. Respect depth limits - at depth {max_depth}/{max_depth}, respond directly without calls
3. Be specific in your agent calls - clearly state what you need
4. Handle errors gracefully - if a call fails, provide the best answer you can
"""


class A2ADataFormatter:
    """
    Formats A2A training data into ChatML format.

    Compatible with Phase 2's instruction fine-tuning format but adds
    A2A-specific context and protocols.
    """

    def __init__(self, unit_name: str):
        """
        Initialize formatter for a specific unit.

        Args:
            unit_name: Unit name (fundraising, business_development, field_operations)
        """
        self.unit_name = unit_name
        self.unit_configs = self._get_unit_configs()

    def format_examples(
        self,
        examples: list[A2ATrainingExample]
    ) -> list[dict[str, Any]]:
        """
        Format training examples into ChatML format.

        Args:
            examples: List of A2A training examples

        Returns:
            List of formatted examples ready for training
        """
        formatted = []

        for example in examples:
            formatted_example = self.format_single_example(example)
            formatted.append(formatted_example)

        return formatted

    def format_single_example(
        self,
        example: A2ATrainingExample
    ) -> dict[str, Any]:
        """
        Format a single example into ChatML format.

        Args:
            example: Single training example

        Returns:
            ChatML formatted example
        """
        config = self.unit_configs[self.unit_name]

        # Build system prompt
        system_prompt = A2A_SYSTEM_PROMPT.format(
            unit_name=config["name"],
            responsibilities="\n".join(f"- {r}" for r in config["responsibilities"]),
            available_agents=self._format_available_agents(config.get("dependencies", [])),
            depth=example.depth,
            max_depth=example.max_depth
        )

        # Build messages
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": self._format_user_message(example)
            },
            {
                "role": "assistant",
                "content": example.expected_output
            }
        ]

        return {
            "messages": messages,
            "metadata": {
                "category": example.category,
                "unit": self.unit_name,
                "depth": example.depth,
                "max_depth": example.max_depth,
                "expected_action": example.expected_action
            }
        }

    def _format_user_message(self, example: A2ATrainingExample) -> str:
        """Format the user message with context"""
        parts = []

        if example.context:
            parts.append(f"Context: {example.context}")

        parts.append(example.user_query)

        return "\n\n".join(parts)

    def _format_available_agents(self, dependencies: list[str]) -> str:
        """Format the list of available agents"""
        if not dependencies:
            return "- No other agents available (handle all queries directly)"

        agent_descriptions = {
            "fundraising-agent": "Investor profiles, interests, capacity",
            "business-development-agent": "RFP data, competitive landscape",
            "field-operations-agent": "Local capacity, project performance"
        }

        lines = []
        for agent_id in dependencies:
            desc = agent_descriptions.get(agent_id, "General assistance")
            lines.append(f"- {agent_id}: {desc}")

        return "\n".join(lines)

    def _get_unit_configs(self) -> dict[str, dict[str, Any]]:
        """Get unit configurations"""
        return {
            "fundraising": {
                "name": "Fundraising",
                "responsibilities": [
                    "Maintain investor profiles and track investment capacity",
                    "Analyze investor sector interests and preferences",
                    "Match investors to opportunities",
                    "Provide comprehensive investor intelligence"
                ],
                "dependencies": ["business-development-agent", "field-operations-agent"]
            },
            "business_development": {
                "name": "Business Development",
                "responsibilities": [
                    "Track and analyze RFP opportunities",
                    "Monitor competitive funding landscape",
                    "Identify funding trends and patterns",
                    "Match opportunities to capabilities"
                ],
                "dependencies": ["fundraising-agent", "field-operations-agent"]
            },
            "field_operations": {
                "name": "Field Operations",
                "responsibilities": [
                    "Track local capacity and resources",
                    "Monitor project performance by region",
                    "Provide regional insights and context",
                    "Coordinate local implementation"
                ],
                "dependencies": ["fundraising-agent", "business-development-agent"]
            }
        }

    def to_jsonl(self, formatted_examples: list[dict[str, Any]], output_path: str) -> None:
        """
        Save formatted examples to JSONL file.

        Args:
            formatted_examples: List of formatted examples
            output_path: Path to output JSONL file
        """
        import json
        from pathlib import Path

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            for example in formatted_examples:
                # Only save the messages for training
                f.write(json.dumps({"messages": example["messages"]}) + "\n")

        print(f"Saved {len(formatted_examples)} formatted examples to {output_path}")

    def to_hf_dataset(self, formatted_examples: list[dict[str, Any]]) -> Any:
        """
        Convert formatted examples to HuggingFace dataset.

        Args:
            formatted_examples: List of formatted examples

        Returns:
            HuggingFace Dataset object
        """
        try:
            from datasets import Dataset
        except ImportError:
            raise ImportError("datasets required. Install with: pip install datasets")

        # Extract just the messages for the dataset
        data = {
            "messages": [ex["messages"] for ex in formatted_examples]
        }

        return Dataset.from_dict(data)


def format_a2a_response(
    content: str,
    is_agent_call: bool = False,
    target_agent: Optional[str] = None,
    goal: Optional[str] = None,
    parameters: Optional[dict[str, Any]] = None
) -> str:
    """
    Helper function to format A2A responses during inference.

    Args:
        content: The main content/response
        is_agent_call: Whether this is an agent call
        target_agent: Target agent ID if making a call
        goal: Goal for the agent call
        parameters: Additional parameters

    Returns:
        Formatted response string
    """
    if is_agent_call and target_agent and goal:
        import json
        a2a_call = {
            "goal": goal,
            "target": target_agent,
            "parameters": parameters or {}
        }
        return f"<a2a_call>\n{json.dumps(a2a_call, indent=2)}\n</a2a_call>"
    else:
        return content
