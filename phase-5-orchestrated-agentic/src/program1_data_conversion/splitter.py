"""
Data Splitter

Splits training data into train/validation/test sets with stratification.
"""

from pathlib import Path
from typing import Any
import json
import random
from phase0_infra.habitat_logging import get_logger

from ..shared.routing_schema import TrainingExample

logger = get_logger(__name__)


class DataSplitter:
    """
    Splits training data into train/val/test sets.

    Uses stratified splitting to ensure balanced distribution across:
    - Agent types
    - Depth levels
    """

    def __init__(
        self,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_seed: int = 42
    ):
        """
        Initialize data splitter.

        Args:
            train_ratio: Proportion for training set
            val_ratio: Proportion for validation set
            test_ratio: Proportion for test set
            random_seed: Random seed for reproducibility
        """
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.01, \
            "Ratios must sum to 1.0"

        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.random_seed = random_seed

        self.logger = logger.bind(component="data_splitter")

        # Set random seed
        random.seed(random_seed)

    def split(
        self,
        examples: list[TrainingExample],
        stratify_by: str = "agent"
    ) -> tuple[list[TrainingExample], list[TrainingExample], list[TrainingExample]]:
        """
        Split examples into train/val/test sets.

        Args:
            examples: Training examples to split
            stratify_by: Stratification key ("agent", "depth", or "both")

        Returns:
            (train, val, test) tuple of example lists
        """
        self.logger.info(
            "splitting_data",
            total_count=len(examples),
            train_ratio=self.train_ratio,
            val_ratio=self.val_ratio,
            test_ratio=self.test_ratio,
            stratify_by=stratify_by
        )

        if stratify_by == "agent":
            return self._split_by_agent(examples)
        elif stratify_by == "depth":
            return self._split_by_depth(examples)
        elif stratify_by == "both":
            return self._split_by_agent_and_depth(examples)
        else:
            return self._split_random(examples)

    def _split_by_agent(
        self,
        examples: list[TrainingExample]
    ) -> tuple[list[TrainingExample], list[TrainingExample], list[TrainingExample]]:
        """Split stratified by agent type"""
        from collections import defaultdict

        # Group by agent
        by_agent = defaultdict(list)
        for example in examples:
            by_agent[example.entry_agent].append(example)

        # Split each group
        train, val, test = [], [], []

        for agent, agent_examples in by_agent.items():
            random.shuffle(agent_examples)

            n = len(agent_examples)
            train_end = int(n * self.train_ratio)
            val_end = train_end + int(n * self.val_ratio)

            train.extend(agent_examples[:train_end])
            val.extend(agent_examples[train_end:val_end])
            test.extend(agent_examples[val_end:])

        # Shuffle final splits
        random.shuffle(train)
        random.shuffle(val)
        random.shuffle(test)

        self._log_split_stats(train, val, test)
        return train, val, test

    def _split_by_depth(
        self,
        examples: list[TrainingExample]
    ) -> tuple[list[TrainingExample], list[TrainingExample], list[TrainingExample]]:
        """Split stratified by depth level"""
        from collections import defaultdict

        # Group by depth
        by_depth = defaultdict(list)
        for example in examples:
            by_depth[example.optimal_depth].append(example)

        # Split each group
        train, val, test = [], [], []

        for depth, depth_examples in by_depth.items():
            random.shuffle(depth_examples)

            n = len(depth_examples)
            train_end = int(n * self.train_ratio)
            val_end = train_end + int(n * self.val_ratio)

            train.extend(depth_examples[:train_end])
            val.extend(depth_examples[train_end:val_end])
            test.extend(depth_examples[val_end:])

        # Shuffle final splits
        random.shuffle(train)
        random.shuffle(val)
        random.shuffle(test)

        self._log_split_stats(train, val, test)
        return train, val, test

    def _split_by_agent_and_depth(
        self,
        examples: list[TrainingExample]
    ) -> tuple[list[TrainingExample], list[TrainingExample], list[TrainingExample]]:
        """Split stratified by both agent and depth"""
        from collections import defaultdict

        # Group by (agent, depth) tuple
        by_agent_depth = defaultdict(list)
        for example in examples:
            key = (example.entry_agent, example.optimal_depth)
            by_agent_depth[key].append(example)

        # Split each group
        train, val, test = [], [], []

        for (agent, depth), group_examples in by_agent_depth.items():
            random.shuffle(group_examples)

            n = len(group_examples)
            train_end = int(n * self.train_ratio)
            val_end = train_end + int(n * self.val_ratio)

            train.extend(group_examples[:train_end])
            val.extend(group_examples[train_end:val_end])
            test.extend(group_examples[val_end:])

        # Shuffle final splits
        random.shuffle(train)
        random.shuffle(val)
        random.shuffle(test)

        self._log_split_stats(train, val, test)
        return train, val, test

    def _split_random(
        self,
        examples: list[TrainingExample]
    ) -> tuple[list[TrainingExample], list[TrainingExample], list[TrainingExample]]:
        """Random split (no stratification)"""
        shuffled = list(examples)
        random.shuffle(shuffled)

        n = len(shuffled)
        train_end = int(n * self.train_ratio)
        val_end = train_end + int(n * self.val_ratio)

        train = shuffled[:train_end]
        val = shuffled[train_end:val_end]
        test = shuffled[val_end:]

        self._log_split_stats(train, val, test)
        return train, val, test

    def export_splits(
        self,
        train: list[TrainingExample],
        val: list[TrainingExample],
        test: list[TrainingExample],
        output_dir: Path
    ) -> None:
        """
        Export splits to files.

        Args:
            train: Training examples
            val: Validation examples
            test: Test examples
            output_dir: Output directory
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        splits = {
            "train": train,
            "val": val,
            "test": test
        }

        for split_name, examples in splits.items():
            # Export as JSONL
            jsonl_path = output_dir / f"{split_name}.jsonl"
            with open(jsonl_path, "w") as f:
                for example in examples:
                    f.write(json.dumps(example.model_dump()) + "\n")

            # Export ChatML format
            chat_path = output_dir / f"{split_name}_chat.jsonl"
            with open(chat_path, "w") as f:
                for example in examples:
                    chat_format = example.to_chat_format()
                    f.write(json.dumps(chat_format) + "\n")

            self.logger.info(
                "exported_split",
                split=split_name,
                count=len(examples),
                jsonl_path=str(jsonl_path),
                chat_path=str(chat_path)
            )

        # Export split statistics
        stats = self._compute_split_statistics(train, val, test)
        stats_path = output_dir / "split_statistics.json"
        with open(stats_path, "w") as f:
            json.dump(stats, f, indent=2)

        self.logger.info("exported_statistics", path=str(stats_path))

    def _log_split_stats(
        self,
        train: list[TrainingExample],
        val: list[TrainingExample],
        test: list[TrainingExample]
    ) -> None:
        """Log split statistics"""
        self.logger.info(
            "split_complete",
            train_count=len(train),
            val_count=len(val),
            test_count=len(test),
            total=len(train) + len(val) + len(test)
        )

    def _compute_split_statistics(
        self,
        train: list[TrainingExample],
        val: list[TrainingExample],
        test: list[TrainingExample]
    ) -> dict[str, Any]:
        """Compute detailed split statistics"""
        stats = {
            "counts": {
                "train": len(train),
                "val": len(val),
                "test": len(test),
                "total": len(train) + len(val) + len(test)
            },
            "ratios": {
                "train": self.train_ratio,
                "val": self.val_ratio,
                "test": self.test_ratio
            },
            "distribution_by_agent": {},
            "distribution_by_depth": {}
        }

        for split_name, examples in [("train", train), ("val", val), ("test", test)]:
            # Agent distribution
            agent_counts = {}
            for example in examples:
                agent = example.entry_agent.value if hasattr(example.entry_agent, 'value') else example.entry_agent
                agent_counts[agent] = agent_counts.get(agent, 0) + 1

            stats["distribution_by_agent"][split_name] = agent_counts

            # Depth distribution
            depth_counts = {}
            for example in examples:
                depth = example.optimal_depth
                depth_counts[depth] = depth_counts.get(depth, 0) + 1

            stats["distribution_by_depth"][split_name] = depth_counts

        return stats
