"""
Contrastive Pair Generation.

Generates anchor + positive pairs for contrastive learning from extracted text samples.
Uses various strategies to create semantically similar pairs.
"""

import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

from src.shared.chunking import ChunkResult, TextChunker
from src.shared.database import ExtractedRecord

logger = get_logger(__name__)


@dataclass
class ContrastivePair:
    """A contrastive learning pair with anchor and positive."""

    anchor: str
    positive: str
    source_db: str
    source_table: str
    doc_id: str
    strategy: str


@dataclass
class Triplet:
    """A triplet with anchor, positive, and negative."""

    anchor: str
    positive: str
    negative: str
    source_db: str
    doc_id: str


PairStrategy = Literal["adjacent_chunks", "title_content", "random_positive"]


class ContrastivePairGenerator:
    """
    Generates contrastive pairs for embedding model training.

    Strategies:
    - adjacent_chunks: Adjacent chunks from same document are positive pairs
    - title_content: Title/heading paired with following content
    - random_positive: Random chunks from same document
    """

    def __init__(
        self,
        strategy: PairStrategy = "adjacent_chunks",
        chunker: TextChunker | None = None,
        min_pair_length: int = 50,
    ):
        """
        Initialize the pair generator.

        Args:
            strategy: Pair generation strategy.
            chunker: TextChunker instance (creates default if None).
            min_pair_length: Minimum length for each text in a pair.
        """
        self.strategy = strategy
        self.chunker = chunker or TextChunker(chunk_size=512, chunk_overlap=50)
        self.min_pair_length = min_pair_length

    def generate_pairs_from_chunks(
        self,
        chunks: list[ChunkResult],
        source_db: str,
        source_table: str,
        doc_id: str,
    ) -> list[ContrastivePair]:
        """
        Generate pairs from a list of chunks using the configured strategy.

        Args:
            chunks: List of text chunks from a document.
            source_db: Source database name.
            source_table: Source table name.
            doc_id: Document ID.

        Returns:
            List of contrastive pairs.
        """
        if len(chunks) < 2:
            return []

        pairs = []

        if self.strategy == "adjacent_chunks":
            # Adjacent chunks are positive pairs
            for i in range(len(chunks) - 1):
                anchor = chunks[i].text.strip()
                positive = chunks[i + 1].text.strip()

                if len(anchor) >= self.min_pair_length and len(positive) >= self.min_pair_length:
                    pairs.append(
                        ContrastivePair(
                            anchor=anchor,
                            positive=positive,
                            source_db=source_db,
                            source_table=source_table,
                            doc_id=doc_id,
                            strategy="adjacent_chunks",
                        )
                    )

        elif self.strategy == "random_positive":
            # Random pairs from same document
            for i, chunk in enumerate(chunks):
                # Pick a random other chunk
                other_indices = [j for j in range(len(chunks)) if j != i]
                if other_indices:
                    j = random.choice(other_indices)
                    anchor = chunk.text.strip()
                    positive = chunks[j].text.strip()

                    if (
                        len(anchor) >= self.min_pair_length
                        and len(positive) >= self.min_pair_length
                    ):
                        pairs.append(
                            ContrastivePair(
                                anchor=anchor,
                                positive=positive,
                                source_db=source_db,
                                source_table=source_table,
                                doc_id=doc_id,
                                strategy="random_positive",
                            )
                        )

        return pairs

    def generate_pairs_from_record(self, record: ExtractedRecord) -> list[ContrastivePair]:
        """
        Generate pairs from a single extracted record.

        Args:
            record: Extracted record with combined text.

        Returns:
            List of contrastive pairs.
        """
        # Chunk the text
        chunks = self.chunker.chunk_text(record.combined_text)

        if not chunks:
            return []

        return self.generate_pairs_from_chunks(
            chunks=chunks,
            source_db=record.source_db,
            source_table=record.source_table,
            doc_id=record.doc_id,
        )

    def generate_pairs(self, records: list[ExtractedRecord]) -> list[ContrastivePair]:
        """
        Generate pairs from multiple records.

        Args:
            records: List of extracted records.

        Returns:
            Combined list of all contrastive pairs.
        """
        all_pairs = []

        for record in records:
            pairs = self.generate_pairs_from_record(record)
            all_pairs.extend(pairs)

        logger.info(
            "pairs_generated",
            strategy=self.strategy,
            num_records=len(records),
            num_pairs=len(all_pairs),
        )

        return all_pairs


class TripletGenerator:
    """
    Generates triplets (anchor, positive, negative) for contrastive learning.

    Negatives are sampled from different documents/sources.
    """

    def __init__(
        self,
        pair_generator: ContrastivePairGenerator | None = None,
        negative_strategy: str = "random_different_doc",
    ):
        """
        Initialize the triplet generator.

        Args:
            pair_generator: ContrastivePairGenerator for positive pairs.
            negative_strategy: Strategy for selecting negatives.
        """
        self.pair_generator = pair_generator or ContrastivePairGenerator()
        self.negative_strategy = negative_strategy

    def generate_triplets(
        self,
        records: list[ExtractedRecord],
        num_negatives_per_pair: int = 1,
    ) -> list[Triplet]:
        """
        Generate triplets from records.

        Args:
            records: List of extracted records.
            num_negatives_per_pair: Number of negatives per positive pair.

        Returns:
            List of triplets.
        """
        # First generate positive pairs
        pairs = self.pair_generator.generate_pairs(records)

        if not pairs:
            return []

        # Build a pool of potential negatives (all chunks)
        negative_pool: list[tuple[str, str]] = []  # (text, doc_id)
        for record in records:
            chunks = self.pair_generator.chunker.chunk_text(record.combined_text)
            for chunk in chunks:
                if len(chunk.text.strip()) >= self.pair_generator.min_pair_length:
                    negative_pool.append((chunk.text.strip(), record.doc_id))

        triplets = []
        for pair in pairs:
            # Find negatives from different documents
            available_negatives = [
                (text, doc_id) for text, doc_id in negative_pool if doc_id != pair.doc_id
            ]

            if not available_negatives:
                continue

            # Sample negatives
            sampled = random.sample(
                available_negatives, min(num_negatives_per_pair, len(available_negatives))
            )

            for negative_text, _ in sampled:
                triplets.append(
                    Triplet(
                        anchor=pair.anchor,
                        positive=pair.positive,
                        negative=negative_text,
                        source_db=pair.source_db,
                        doc_id=pair.doc_id,
                    )
                )

        logger.info(
            "triplets_generated",
            num_pairs=len(pairs),
            num_triplets=len(triplets),
        )

        return triplets
