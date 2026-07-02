"""
Intent Generator

Generates synthetic user intents from workflow patterns to augment training data.
"""

import random
from phase0_infra.habitat_logging import get_logger

from ..shared.routing_schema import TrainingExample, AgentType

logger = get_logger(__name__)


class IntentGenerator:
    """
    Generates synthetic user intents based on discovered workflow patterns.

    Strategy:
    1. Analyze existing queries to identify patterns
    2. Generate variations with different parameters
    3. Create new queries following same patterns
    """

    def __init__(self):
        """Initialize intent generator"""
        self.logger = logger.bind(component="intent_generator")

        # Intent templates by workflow type
        self.intent_templates = {
            AgentType.FUNDRAISING: [
                "What is the investment capacity of {investor}?",
                "Assess investor {investor}'s portfolio performance",
                "Evaluate {investor}'s interest in {sector} investments",
                "Should we pursue partnership with {investor}?",
                "What are {investor}'s current funding priorities?",
                "Analyze {investor}'s historical investment patterns",
                "Is {investor} accepting new proposals in {sector}?",
            ],
            AgentType.BUSINESS_DEVELOPMENT: [
                "What RFPs are currently open in {sector}?",
                "Analyze competitive landscape for {sector} funding",
                "Assess market fit for {sector} opportunities",
                "What funding opportunities exist in {region}?",
                "Evaluate competitive funders for {project_type}",
                "What are the requirements for {rfp_id}?",
                "Should we bid on {rfp_id}?",
            ],
            AgentType.FIELD_OPERATIONS: [
                "Evaluate funding opportunity in {region} for {sector}",
                "Assess local capacity in {region} for {project_type}",
                "What is the project performance in {region}?",
                "Should we pursue {project_type} in {region}?",
                "Analyze regional market dynamics in {region}",
                "Evaluate {region} office capacity for new projects",
                "What are the key challenges in {region}?",
            ]
        }

        # Parameter values for templates
        self.parameters = {
            "investor": ["INV-123", "INV-456", "INV-789", "Angel Foundation", "Impact Fund"],
            "sector": [
                "climate",
                "education",
                "healthcare",
                "renewable energy",
                "agriculture",
                "water sanitation"
            ],
            "region": [
                "Kenya",
                "Tanzania",
                "Uganda",
                "Ethiopia",
                "Rwanda",
                "Ghana"
            ],
            "project_type": [
                "climate project",
                "education initiative",
                "healthcare program",
                "infrastructure development",
                "community development"
            ],
            "rfp_id": ["RFP-2024-001", "RFP-2024-002", "RFP-2024-003"]
        }

    def generate_intents(
        self,
        existing_examples: list[TrainingExample],
        max_per_workflow: int = 5
    ) -> list[TrainingExample]:
        """
        Generate synthetic intents based on existing examples.

        Args:
            existing_examples: Existing training examples to learn from
            max_per_workflow: Maximum intents to generate per agent type

        Returns:
            List of synthetic TrainingExample objects
        """
        self.logger.info(
            "generating_intents",
            existing_count=len(existing_examples),
            max_per_workflow=max_per_workflow
        )

        # Analyze existing patterns
        agent_distribution = self._analyze_agent_distribution(existing_examples)
        depth_distribution = self._analyze_depth_distribution(existing_examples)

        # Generate synthetic examples
        synthetic_examples = []

        for agent in AgentType:
            templates = self.intent_templates.get(agent, [])
            if not templates:
                continue

            # Determine how many to generate (proportional to existing distribution)
            count = min(
                max_per_workflow,
                int(agent_distribution.get(agent, 0.33) * max_per_workflow * 3)
            )

            for _ in range(count):
                example = self._generate_single_intent(agent, depth_distribution)
                if example:
                    synthetic_examples.append(example)

        self.logger.info("intents_generated", count=len(synthetic_examples))
        return synthetic_examples

    def _generate_single_intent(
        self,
        agent: AgentType,
        depth_distribution: dict[int, float]
    ) -> TrainingExample:
        """
        Generate a single synthetic intent.

        Args:
            agent: Target agent type
            depth_distribution: Distribution of depths in existing data

        Returns:
            Synthetic TrainingExample
        """
        # Select random template
        templates = self.intent_templates[agent]
        template = random.choice(templates)

        # Fill in parameters
        query = self._fill_template(template)

        # Select depth based on distribution
        depth = self._sample_depth(depth_distribution)

        # Create example
        example = TrainingExample(
            query=query,
            entry_agent=agent,
            optimal_depth=depth,
            call_sequence=[{
                "depth": 0,
                "target": agent.value,
                "goal": query
            }],
            final_response=f"Synthetic response for: {query}",
            metadata={
                "workflow_id": f"synthetic_{agent.value}",
                "success": True,
                "synthetic": True
            }
        )

        return example

    def _fill_template(self, template: str) -> str:
        """
        Fill in template parameters.

        Args:
            template: Template string with {param} placeholders

        Returns:
            Filled template
        """
        filled = template

        for param_name, param_values in self.parameters.items():
            if f"{{{param_name}}}" in filled:
                filled = filled.replace(
                    f"{{{param_name}}}",
                    random.choice(param_values)
                )

        return filled

    def _analyze_agent_distribution(
        self,
        examples: list[TrainingExample]
    ) -> dict[AgentType, float]:
        """
        Analyze distribution of agents in existing examples.

        Args:
            examples: Existing training examples

        Returns:
            Dictionary mapping agent to proportion
        """
        if not examples:
            return {agent: 0.33 for agent in AgentType}

        counts = {agent: 0 for agent in AgentType}

        for example in examples:
            counts[example.entry_agent] += 1

        total = len(examples)
        distribution = {agent: count / total for agent, count in counts.items()}

        return distribution

    def _analyze_depth_distribution(
        self,
        examples: list[TrainingExample]
    ) -> dict[int, float]:
        """
        Analyze distribution of depths in existing examples.

        Args:
            examples: Existing training examples

        Returns:
            Dictionary mapping depth to proportion
        """
        if not examples:
            return {1: 0.2, 2: 0.5, 3: 0.25, 4: 0.05}

        counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for example in examples:
            depth = min(4, max(1, example.optimal_depth))
            counts[depth] += 1

        total = len(examples)
        distribution = {depth: count / total for depth, count in counts.items()}

        return distribution

    def _sample_depth(self, distribution: dict[int, float]) -> int:
        """
        Sample a depth based on distribution.

        Args:
            distribution: Depth distribution

        Returns:
            Sampled depth
        """
        depths = list(distribution.keys())
        weights = list(distribution.values())

        return random.choices(depths, weights=weights)[0]

    def generate_paraphrases(
        self,
        query: str,
        num_paraphrases: int = 3
    ) -> list[str]:
        """
        Generate paraphrases of a query.

        Simple rule-based paraphrasing (for test mode).
        In production, could use a paraphrasing model.

        Args:
            query: Original query
            num_paraphrases: Number of paraphrases to generate

        Returns:
            List of paraphrased queries
        """
        paraphrases = [query]  # Include original

        # Simple paraphrasing rules
        transformations = [
            lambda q: q.replace("What is", "Can you tell me"),
            lambda q: q.replace("Evaluate", "Please evaluate"),
            lambda q: q.replace("Assess", "Can you assess"),
            lambda q: q.replace("Should we", "Do you recommend that we"),
            lambda q: q.replace("?", " please?"),
        ]

        for _ in range(min(num_paraphrases, len(transformations))):
            transform = random.choice(transformations)
            paraphrased = transform(query)

            if paraphrased != query and paraphrased not in paraphrases:
                paraphrases.append(paraphrased)

        return paraphrases[:num_paraphrases + 1]
