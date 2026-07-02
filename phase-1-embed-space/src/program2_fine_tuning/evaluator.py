"""
Evaluation Metrics for Embedding Models.

Provides evaluation metrics for assessing embedding quality including
cosine similarity, retrieval metrics (NDCG, MRR), and comparison tools.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

from src.shared.path_config import configure_paths
configure_paths()

from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class SimilarityResult:
    """Result of similarity evaluation."""

    mean_similarity: float
    std_similarity: float
    min_similarity: float
    max_similarity: float
    num_pairs: int


@dataclass
class RetrievalMetrics:
    """Retrieval evaluation metrics."""

    ndcg_at_5: float
    ndcg_at_10: float
    mrr: float
    precision_at_5: float
    num_queries: int


@dataclass
class ComparisonResult:
    """Result of comparing two models."""

    base_similarity: SimilarityResult
    finetuned_similarity: SimilarityResult
    improvement: float  # Percentage improvement


class EmbeddingEvaluator:
    """
    Evaluator for embedding model quality.

    Provides methods for:
    - Cosine similarity evaluation on positive pairs
    - Retrieval metrics (NDCG, MRR)
    - Model comparison (base vs fine-tuned)
    """

    def __init__(self, model: SentenceTransformer):
        """
        Initialize the evaluator.

        Args:
            model: SentenceTransformer model to evaluate.
        """
        self.model = model

    def evaluate_similarity(
        self,
        pairs: list[tuple[str, str]],
        batch_size: int = 32,
    ) -> SimilarityResult:
        """
        Evaluate cosine similarity on text pairs.

        For positive pairs, higher similarity indicates better model.

        Args:
            pairs: List of (text1, text2) tuples.
            batch_size: Batch size for encoding.

        Returns:
            SimilarityResult with statistics.
        """
        if not pairs:
            return SimilarityResult(
                mean_similarity=0.0,
                std_similarity=0.0,
                min_similarity=0.0,
                max_similarity=0.0,
                num_pairs=0,
            )

        texts1 = [p[0] for p in pairs]
        texts2 = [p[1] for p in pairs]

        # Encode both sets
        embeddings1 = self.model.encode(
            texts1, batch_size=batch_size, normalize_embeddings=True
        )
        embeddings2 = self.model.encode(
            texts2, batch_size=batch_size, normalize_embeddings=True
        )

        # Compute cosine similarities (dot product for normalized vectors)
        similarities = np.sum(embeddings1 * embeddings2, axis=1)

        return SimilarityResult(
            mean_similarity=float(np.mean(similarities)),
            std_similarity=float(np.std(similarities)),
            min_similarity=float(np.min(similarities)),
            max_similarity=float(np.max(similarities)),
            num_pairs=len(pairs),
        )

    def evaluate_retrieval(
        self,
        queries: list[str],
        corpus: list[str],
        relevance: list[list[int]],
        k_values: list[int] = [5, 10],
    ) -> RetrievalMetrics:
        """
        Evaluate retrieval performance.

        Args:
            queries: List of query texts.
            corpus: List of document texts.
            relevance: List of relevant document indices for each query.
            k_values: K values for NDCG/precision calculations.

        Returns:
            RetrievalMetrics with NDCG, MRR, and precision.
        """
        # Encode queries and corpus
        query_embeddings = self.model.encode(queries, normalize_embeddings=True)
        corpus_embeddings = self.model.encode(corpus, normalize_embeddings=True)

        # Compute similarity matrix
        similarity_matrix = np.matmul(query_embeddings, corpus_embeddings.T)

        # Calculate metrics
        ndcg_scores: dict[int, list[float]] = {k: [] for k in k_values}
        mrr_scores: list[float] = []
        precision_scores: dict[int, list[float]] = {k: [] for k in k_values}

        for i, (scores, relevant_docs) in enumerate(zip(similarity_matrix, relevance)):
            # Get ranking
            ranking = np.argsort(-scores)  # Descending order

            # MRR: position of first relevant document
            for rank, doc_idx in enumerate(ranking):
                if doc_idx in relevant_docs:
                    mrr_scores.append(1.0 / (rank + 1))
                    break
            else:
                mrr_scores.append(0.0)

            # NDCG and Precision at K
            for k in k_values:
                top_k = ranking[:k]

                # Precision@K
                relevant_in_top_k = sum(1 for idx in top_k if idx in relevant_docs)
                precision_scores[k].append(relevant_in_top_k / k)

                # NDCG@K
                dcg = 0.0
                for rank, doc_idx in enumerate(top_k):
                    if doc_idx in relevant_docs:
                        dcg += 1.0 / np.log2(rank + 2)

                ideal_dcg = sum(1.0 / np.log2(r + 2) for r in range(min(k, len(relevant_docs))))
                ndcg = dcg / ideal_dcg if ideal_dcg > 0 else 0.0
                ndcg_scores[k].append(ndcg)

        return RetrievalMetrics(
            ndcg_at_5=float(np.mean(ndcg_scores.get(5, [0.0]))),
            ndcg_at_10=float(np.mean(ndcg_scores.get(10, [0.0]))),
            mrr=float(np.mean(mrr_scores)),
            precision_at_5=float(np.mean(precision_scores.get(5, [0.0]))),
            num_queries=len(queries),
        )

    @staticmethod
    def compare_models(
        base_model: SentenceTransformer,
        finetuned_model: SentenceTransformer,
        pairs: list[tuple[str, str]],
        batch_size: int = 32,
    ) -> ComparisonResult:
        """
        Compare base model with fine-tuned model on similarity task.

        Args:
            base_model: Original base model.
            finetuned_model: Fine-tuned model.
            pairs: Test pairs for evaluation.
            batch_size: Batch size for encoding.

        Returns:
            ComparisonResult with both results and improvement.
        """
        base_evaluator = EmbeddingEvaluator(base_model)
        finetuned_evaluator = EmbeddingEvaluator(finetuned_model)

        base_result = base_evaluator.evaluate_similarity(pairs, batch_size)
        finetuned_result = finetuned_evaluator.evaluate_similarity(pairs, batch_size)

        # Calculate improvement
        if base_result.mean_similarity > 0:
            improvement = (
                (finetuned_result.mean_similarity - base_result.mean_similarity)
                / base_result.mean_similarity
                * 100
            )
        else:
            improvement = 0.0

        logger.info(
            "model_comparison",
            base_similarity=base_result.mean_similarity,
            finetuned_similarity=finetuned_result.mean_similarity,
            improvement_pct=improvement,
        )

        return ComparisonResult(
            base_similarity=base_result,
            finetuned_similarity=finetuned_result,
            improvement=improvement,
        )


def evaluate_model_on_dataset(
    model_path: str,
    eval_dataset_path: str,
    batch_size: int = 32,
) -> dict[str, Any]:
    """
    Evaluate a model on a dataset file.

    Args:
        model_path: Path to the model.
        eval_dataset_path: Path to evaluation dataset (Parquet with anchor/positive).
        batch_size: Batch size for encoding.

    Returns:
        Dictionary with evaluation metrics.
    """
    from datasets import load_dataset

    # Load model and dataset
    model = SentenceTransformer(model_path)
    dataset = load_dataset("parquet", data_files=eval_dataset_path, split="train")

    # Create pairs
    pairs = [(row["anchor"], row["positive"]) for row in dataset]

    # Evaluate
    evaluator = EmbeddingEvaluator(model)
    result = evaluator.evaluate_similarity(pairs, batch_size)

    return {
        "model_path": model_path,
        "mean_similarity": result.mean_similarity,
        "std_similarity": result.std_similarity,
        "min_similarity": result.min_similarity,
        "max_similarity": result.max_similarity,
        "num_pairs": result.num_pairs,
    }
