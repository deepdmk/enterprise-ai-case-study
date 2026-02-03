"""
A2A Training Data Generator

Generates synthetic training examples to teach MoE models:
1. When to call other agents
2. How to generate A2A protocol calls
3. How to handle responses
4. Depth limit awareness
"""

import random
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json


@dataclass
class A2ATrainingExample:
    """
    Single training example for A2A fine-tuning.

    Attributes:
        category: Type of example (direct_task, single_call, multi_call, etc.)
        context: Setup/background information
        user_query: What the user is asking for
        expected_action: What the model should do (call agent, respond directly, etc.)
        expected_output: The actual expected response/call
        depth: Current call depth
        max_depth: Maximum allowed depth
    """
    category: str
    context: str
    user_query: str
    expected_action: str
    expected_output: str
    depth: int = 0
    max_depth: int = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "category": self.category,
            "context": self.context,
            "user_query": self.user_query,
            "expected_action": self.expected_action,
            "expected_output": self.expected_output,
            "depth": self.depth,
            "max_depth": self.max_depth
        }


class A2ADataGenerator:
    """
    Generates A2A training examples for different unit types.

    Training Data Distribution:
    - Direct Task: 40% - Model knows when NOT to call agents
    - Single Agent Call: 30% - Generate correct A2A requests
    - Multi-Agent Orchestration: 15% - Coordinate multiple calls
    - Depth Limit Handling: 10% - Graceful degradation
    - Error Handling: 5% - Timeouts, not_found, errors
    """

    def __init__(self, unit_name: str):
        """
        Initialize data generator for a specific unit.

        Args:
            unit_name: Unit name (fundraising, business_development, field_operations)
        """
        self.unit_name = unit_name
        self.unit_configs = self._get_unit_configs()

    def generate_dataset(
        self,
        num_examples: int = 1000,
        test_mode: bool = False
    ) -> List[A2ATrainingExample]:
        """
        Generate complete training dataset.

        Args:
            num_examples: Total number of examples to generate
            test_mode: If True, generate smaller dataset for testing

        Returns:
            List of training examples
        """
        if test_mode:
            num_examples = 100

        examples = []

        # Calculate distribution
        num_direct = int(num_examples * 0.40)
        num_single = int(num_examples * 0.30)
        num_multi = int(num_examples * 0.15)
        num_depth = int(num_examples * 0.10)
        num_error = num_examples - (num_direct + num_single + num_multi + num_depth)

        # Generate each category
        examples.extend(self.generate_direct_task_examples(num_direct))
        examples.extend(self.generate_single_call_examples(num_single))
        examples.extend(self.generate_multi_call_examples(num_multi))
        examples.extend(self.generate_depth_limit_examples(num_depth))
        examples.extend(self.generate_error_handling_examples(num_error))

        # Shuffle
        random.shuffle(examples)

        return examples

    def generate_direct_task_examples(self, count: int) -> List[A2ATrainingExample]:
        """
        Generate examples where the model should handle the task directly.

        These teach the model when NOT to call other agents.
        """
        examples = []
        config = self.unit_configs[self.unit_name]

        for _ in range(count):
            query_template = random.choice(config["direct_queries"])
            query = query_template.format(**self._random_params())

            example = A2ATrainingExample(
                category="direct_task",
                context=f"You are the {config['name']} agent. Handle queries about {', '.join(config['domains'])}.",
                user_query=query,
                expected_action="respond_directly",
                expected_output=f"[Direct response based on {self.unit_name} knowledge]",
                depth=0,
                max_depth=3
            )
            examples.append(example)

        return examples

    def generate_single_call_examples(self, count: int) -> List[A2ATrainingExample]:
        """
        Generate examples requiring a single A2A call.

        These teach the model to recognize when it needs another agent.
        """
        examples = []
        config = self.unit_configs[self.unit_name]

        for _ in range(count):
            # Pick a dependency to call
            if not config.get("dependencies"):
                continue

            target_agent = random.choice(config["dependencies"])
            query_template = random.choice(config["call_queries"].get(target_agent, []))
            query = query_template.format(**self._random_params())

            # Generate A2A call
            a2a_call = {
                "goal": query,
                "target": target_agent,
                "parameters": {}
            }

            example = A2ATrainingExample(
                category="single_agent_call",
                context=f"You are the {config['name']} agent at depth 0/3.",
                user_query=query,
                expected_action="call_agent",
                expected_output=f"<a2a_call>\n{json.dumps(a2a_call, indent=2)}\n</a2a_call>",
                depth=0,
                max_depth=3
            )
            examples.append(example)

        return examples

    def generate_multi_call_examples(self, count: int) -> List[A2ATrainingExample]:
        """
        Generate examples requiring coordination of multiple agents.

        These teach orchestration skills.
        """
        examples = []
        config = self.unit_configs[self.unit_name]

        for _ in range(count):
            if not config.get("dependencies") or len(config["dependencies"]) < 2:
                continue

            # Pick 2-3 agents to coordinate
            num_agents = random.randint(2, min(3, len(config["dependencies"])))
            target_agents = random.sample(config["dependencies"], num_agents)

            query = random.choice(config["multi_queries"])

            # Generate sequence of calls
            calls = []
            for i, agent in enumerate(target_agents):
                calls.append({
                    "step": i + 1,
                    "goal": f"Get information from {agent}",
                    "target": agent,
                    "parameters": {}
                })

            example = A2ATrainingExample(
                category="multi_agent_orchestration",
                context=f"You are the {config['name']} agent. This requires information from multiple sources.",
                user_query=query,
                expected_action="orchestrate_calls",
                expected_output=json.dumps(calls, indent=2),
                depth=0,
                max_depth=3
            )
            examples.append(example)

        return examples

    def generate_depth_limit_examples(self, count: int) -> List[A2ATrainingExample]:
        """
        Generate examples at or near depth limits.

        These teach graceful degradation when depth limits are reached.
        """
        examples = []
        config = self.unit_configs[self.unit_name]

        for _ in range(count):
            # Vary the depth limit scenario
            depth = random.choice([2, 3, 3])  # Mostly at limit
            max_depth = 3

            query = random.choice(config.get("direct_queries", ["General query"]))

            if depth >= max_depth:
                expected_action = "respond_directly"
                expected_output = "[Response without making additional calls - depth limit reached]"
            else:
                expected_action = "respond_directly"
                expected_output = "[Carefully consider if call is necessary given depth={}/{}]".format(depth, max_depth)

            example = A2ATrainingExample(
                category="depth_limit_handling",
                context=f"You are the {config['name']} agent at depth {depth}/{max_depth}.",
                user_query=query,
                expected_action=expected_action,
                expected_output=expected_output,
                depth=depth,
                max_depth=max_depth
            )
            examples.append(example)

        return examples

    def generate_error_handling_examples(self, count: int) -> List[A2ATrainingExample]:
        """
        Generate examples with error scenarios.

        These teach handling of timeouts, not_found, and errors.
        """
        examples = []
        config = self.unit_configs[self.unit_name]

        error_types = [
            ("timeout", "The agent took too long to respond"),
            ("not_found", "The requested agent doesn't exist"),
            ("error", "An error occurred during the call")
        ]

        for _ in range(count):
            error_type, error_msg = random.choice(error_types)

            example = A2ATrainingExample(
                category="error_handling",
                context=f"You made an A2A call but received an error: {error_msg}",
                user_query="How should you handle this?",
                expected_action="handle_error",
                expected_output=f"[Gracefully handle {error_type} and provide alternative response]",
                depth=1,
                max_depth=3
            )
            examples.append(example)

        return examples

    def _get_unit_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get configuration for each unit type"""
        return {
            "fundraising": {
                "name": "Fundraising",
                "domains": ["investor profiles", "investment capacity", "sector interests"],
                "dependencies": ["business-development-agent", "field-operations-agent"],
                "direct_queries": [
                    "What is the investment capacity of {investor_id}?",
                    "Which sectors does {investor_id} focus on?",
                    "List all angel investors in the {sector} sector"
                ],
                "call_queries": {
                    "business-development-agent": [
                        "Compare angel investor {investor_id} with competitive funders",
                        "What RFPs might interest investor {investor_id}?"
                    ],
                    "field-operations-agent": [
                        "What local capacity exists for investor {investor_id}?",
                        "Which country offices work with investor {investor_id}?"
                    ]
                },
                "multi_queries": [
                    "Create a comprehensive profile for investor {investor_id} including competitive landscape and local presence"
                ]
            },
            "business_development": {
                "name": "Business Development",
                "domains": ["RFP data", "competitive landscape", "funding opportunities"],
                "dependencies": ["fundraising-agent", "field-operations-agent"],
                "direct_queries": [
                    "What RFPs are available in {sector}?",
                    "Show competitive landscape for {sector}",
                    "List recent funding opportunities"
                ],
                "call_queries": {
                    "fundraising-agent": [
                        "Which angel investors might be interested in RFP {rfp_id}?",
                        "Find investors matching this RFP profile"
                    ],
                    "field-operations-agent": [
                        "What local capacity is needed for RFP {rfp_id}?",
                        "Which country offices can support this RFP?"
                    ]
                },
                "multi_queries": [
                    "Analyze RFP {rfp_id} including potential investors and local capacity"
                ]
            },
            "field_operations": {
                "name": "Field Operations",
                "domains": ["local capacity", "project performance", "regional data"],
                "dependencies": ["fundraising-agent", "business-development-agent"],
                "direct_queries": [
                    "What is the capacity of {country} office?",
                    "Show project performance in {country}",
                    "List active projects in {region}"
                ],
                "call_queries": {
                    "fundraising-agent": [
                        "Which investors are active in {country}?",
                        "Find investors interested in {region}"
                    ],
                    "business-development-agent": [
                        "What RFPs are relevant for {country}?",
                        "Show funding opportunities in {region}"
                    ]
                },
                "multi_queries": [
                    "Create regional analysis for {country} including investors and opportunities"
                ]
            }
        }

    def _random_params(self) -> Dict[str, str]:
        """Generate random parameters for query templates"""
        return {
            "investor_id": f"INV-{random.randint(100, 999)}",
            "sector": random.choice(["health", "education", "agriculture", "technology"]),
            "rfp_id": f"RFP-{random.randint(1000, 9999)}",
            "country": random.choice(["Kenya", "Ghana", "Nigeria", "Tanzania"]),
            "region": random.choice(["East Africa", "West Africa", "Southern Africa"])
        }

    def save_dataset(self, examples: List[A2ATrainingExample], output_path: str) -> None:
        """Save dataset to JSON file"""
        import json
        from pathlib import Path

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump([ex.to_dict() for ex in examples], f, indent=2)

        print(f"Saved {len(examples)} examples to {output_path}")
