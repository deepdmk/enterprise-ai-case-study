"""
Data Augmenter

Augments training data through paraphrasing and variations.
"""

import random
from phase0_infra.habitat_logging import get_logger

from ..shared.routing_schema import TrainingExample
from .intent_generator import IntentGenerator

logger = get_logger(__name__)


class DataAugmenter:
    """
    Augments training data to increase diversity.

    Techniques:
    1. Query paraphrasing
    2. Parameter variation
    3. Synonym substitution
    """

    def __init__(self):
        """Initialize data augmenter"""
        self.logger = logger.bind(component="data_augmenter")
        self.intent_generator = IntentGenerator()

        # Synonym mappings for simple substitution
        self.synonyms = {
            "evaluate": ["assess", "analyze", "review"],
            "opportunity": ["possibility", "prospect", "option"],
            "capacity": ["capability", "ability", "resources"],
            "project": ["initiative", "program", "endeavor"],
            "funding": ["financing", "investment", "financial support"],
            "region": ["area", "territory", "location"],
        }

    def augment_examples(
        self,
        examples: list[TrainingExample],
        augmentation_factor: int = 3,
        test_mode: bool = False
    ) -> list[TrainingExample]:
        """
        Augment training examples.

        Args:
            examples: Original training examples
            augmentation_factor: Number of augmented variants per example
            test_mode: If True, use faster/simpler augmentation

        Returns:
            List including original + augmented examples
        """
        self.logger.info(
            "augmenting_examples",
            original_count=len(examples),
            augmentation_factor=augmentation_factor,
            test_mode=test_mode
        )

        if test_mode:
            # In test mode, just use simple paraphrasing
            augmentation_factor = min(augmentation_factor, 1)

        augmented = list(examples)  # Include originals

        for example in examples:
            # Generate augmented variants
            variants = self._create_variants(example, augmentation_factor)
            augmented.extend(variants)

        self.logger.info("augmentation_complete", total_count=len(augmented))
        return augmented

    def _create_variants(
        self,
        example: TrainingExample,
        count: int
    ) -> list[TrainingExample]:
        """
        Create augmented variants of an example.

        Args:
            example: Original example
            count: Number of variants to create

        Returns:
            List of variant examples
        """
        variants = []

        for i in range(count):
            # Choose augmentation technique
            technique = random.choice([
                self._paraphrase_query,
                self._substitute_synonyms,
                self._vary_parameters
            ])

            augmented_query = technique(example.query)

            # Create variant example
            variant = TrainingExample(
                query=augmented_query,
                entry_agent=example.entry_agent,
                optimal_depth=example.optimal_depth,
                call_sequence=example.call_sequence,
                final_response=example.final_response,
                metadata={
                    **example.metadata,
                    "augmented": True,
                    "augmentation_technique": technique.__name__
                }
            )

            variants.append(variant)

        return variants

    def _paraphrase_query(self, query: str) -> str:
        """
        Paraphrase a query using simple rules.

        Args:
            query: Original query

        Returns:
            Paraphrased query
        """
        paraphrases = self.intent_generator.generate_paraphrases(query, num_paraphrases=1)
        return paraphrases[-1] if len(paraphrases) > 1 else query

    def _substitute_synonyms(self, query: str) -> str:
        """
        Substitute words with synonyms.

        Args:
            query: Original query

        Returns:
            Query with synonyms substituted
        """
        words = query.lower().split()
        new_words = []

        for word in words:
            # Check if we have synonyms for this word
            clean_word = word.strip("?.,!")
            if clean_word in self.synonyms:
                # 50% chance to substitute
                if random.random() < 0.5:
                    synonym = random.choice(self.synonyms[clean_word])
                    # Preserve capitalization
                    if word[0].isupper():
                        synonym = synonym.capitalize()
                    new_words.append(synonym + word[len(clean_word):])
                else:
                    new_words.append(word)
            else:
                new_words.append(word)

        return " ".join(new_words)

    def _vary_parameters(self, query: str) -> str:
        """
        Vary parameters in the query (IDs, names, etc.).

        Args:
            query: Original query

        Returns:
            Query with varied parameters
        """
        # Simple parameter variations
        variations = [
            # Investor IDs
            ("INV-123", "INV-456"),
            ("INV-456", "INV-789"),
            ("INV-789", "INV-123"),

            # Regions
            ("Kenya", "Tanzania"),
            ("Tanzania", "Uganda"),
            ("Uganda", "Ethiopia"),
            ("Ethiopia", "Rwanda"),
            ("Rwanda", "Ghana"),

            # Sectors
            ("climate", "education"),
            ("education", "healthcare"),
            ("healthcare", "renewable energy"),
            ("renewable energy", "agriculture"),

            # RFP IDs
            ("RFP-2024-001", "RFP-2024-002"),
            ("RFP-2024-002", "RFP-2024-003"),
        ]

        varied_query = query

        for old_param, new_param in variations:
            if old_param in varied_query:
                varied_query = varied_query.replace(old_param, new_param)
                break  # Only vary one parameter per augmentation

        return varied_query

    def balance_dataset(
        self,
        examples: list[TrainingExample],
        target_per_agent: int = None
    ) -> list[TrainingExample]:
        """
        Balance dataset across agents.

        Args:
            examples: Training examples
            target_per_agent: Target number per agent. If None, use max count.

        Returns:
            Balanced dataset
        """
        from collections import defaultdict

        self.logger.info("balancing_dataset", original_count=len(examples))

        # Group by agent
        by_agent = defaultdict(list)
        for example in examples:
            by_agent[example.entry_agent].append(example)

        # Determine target
        if target_per_agent is None:
            target_per_agent = max(len(exs) for exs in by_agent.values())

        # Balance
        balanced = []

        for agent, agent_examples in by_agent.items():
            current_count = len(agent_examples)

            if current_count >= target_per_agent:
                # Downsample
                balanced.extend(random.sample(agent_examples, target_per_agent))
            else:
                # Upsample through augmentation
                balanced.extend(agent_examples)

                shortage = target_per_agent - current_count
                for _ in range(shortage):
                    # Randomly duplicate and augment
                    original = random.choice(agent_examples)
                    variants = self._create_variants(original, count=1)
                    balanced.extend(variants)

        random.shuffle(balanced)

        self.logger.info(
            "balancing_complete",
            balanced_count=len(balanced),
            target_per_agent=target_per_agent
        )

        return balanced
