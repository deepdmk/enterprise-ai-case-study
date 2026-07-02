"""
Search Reranker using CrossEncoder models.

Reranks initial retrieval results using a more expensive but more accurate
CrossEncoder model for improved search quality.
"""

from sentence_transformers import CrossEncoder

from src.shared.path_config import configure_paths
configure_paths()

from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


class SearchReranker:
    """
    Reranks search results using a CrossEncoder model.

    CrossEncoders are more accurate than bi-encoders (like sentence-transformers)
    because they jointly encode the query and document, but are too slow for
    initial retrieval over large collections. Use them for reranking top candidates.
    """

    def __init__(self, model_name: str):
        """
        Initialize the reranker.

        Args:
            model_name: Name or path of the CrossEncoder model.
        """
        self.model_name = model_name
        self._model: CrossEncoder | None = None

    def _load_model(self) -> CrossEncoder:
        """Lazy load the CrossEncoder model."""
        if self._model is None:
            logger.info("loading_reranker_model", model=self.model_name)
            self._model = CrossEncoder(self.model_name)
            logger.info("reranker_model_loaded", model=self.model_name)
        return self._model

    def rerank(
        self,
        query: str,
        results: list[dict],
        documents: list[str],
        top_k: int,
    ) -> list[dict]:
        """
        Rerank search results using the CrossEncoder.

        Args:
            query: The search query.
            results: List of result dictionaries from initial retrieval.
            documents: List of document texts corresponding to results.
            top_k: Number of top results to return after reranking.

        Returns:
            Reranked list of result dictionaries, limited to top_k.
        """
        if not results or not documents:
            return results

        if len(results) != len(documents):
            logger.error(
                "rerank_length_mismatch",
                num_results=len(results),
                num_documents=len(documents),
            )
            return results[:top_k]

        # Load model
        model = self._load_model()

        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]

        # Score all pairs
        logger.info("reranking_candidates", num_candidates=len(pairs), top_k=top_k)
        scores = model.predict(pairs)

        # Add scores to results and sort
        for result, score in zip(results, scores):
            result["rerank_score"] = float(score)

        # Sort by rerank score descending
        reranked = sorted(results, key=lambda x: x["rerank_score"], reverse=True)

        logger.info(
            "reranking_complete",
            original_top_score=results[0].get("distance", 0) if results else 0,
            reranked_top_score=reranked[0]["rerank_score"],
        )

        return reranked[:top_k]
