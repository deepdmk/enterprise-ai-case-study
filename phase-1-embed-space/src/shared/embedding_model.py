"""
Embedding Model Manager.

Handles loading and inference for embedding models (base and fine-tuned).
Uses Sentence-Transformers library for model management.
"""

import sys
from pathlib import Path
from typing import Literal

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Import local config BEFORE adding phase-0 to path
from config.settings import EmbeddingConfig

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

logger = get_logger(__name__)


class EmbeddingModelManager:
    """
    Manages embedding model loading and inference.

    Supports:
    - Loading base models from HuggingFace
    - Loading fine-tuned models from local paths
    - Batch encoding with configurable batch size
    - Automatic device selection (CUDA, MPS, CPU)
    """

    def __init__(self, config: EmbeddingConfig):
        """
        Initialize the embedding model manager.

        Args:
            config: Embedding configuration with model paths and settings.
        """
        self.config = config
        self._model: SentenceTransformer | None = None
        self._device: str | None = None

    def _select_device(self) -> str:
        """Select the best available device."""
        if self.config.device != "auto":
            return self.config.device

        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def load_model(self, use_fine_tuned: bool = True) -> SentenceTransformer:
        """
        Load the embedding model.

        Args:
            use_fine_tuned: If True, try to load fine-tuned model first.
                           Falls back to base model if not available.

        Returns:
            Loaded SentenceTransformer model.
        """
        if self._model is not None:
            return self._model

        self._device = self._select_device()
        model_path = None

        # Try fine-tuned model first if requested
        if use_fine_tuned:
            fine_tuned_path = Path(self.config.fine_tuned_model_path)
            if fine_tuned_path.exists():
                model_path = str(fine_tuned_path)
                logger.info("loading_fine_tuned_model", path=model_path)

        # Fall back to base model
        if model_path is None:
            model_path = self.config.base_model
            logger.info("loading_base_model", model=model_path)

        try:
            self._model = SentenceTransformer(model_path, device=self._device)
            logger.info(
                "embedding_model_loaded",
                model=model_path,
                device=self._device,
                dimension=self._model.get_sentence_embedding_dimension(),
            )
        except Exception as e:
            logger.error("model_loading_failed", model=model_path, error=str(e))
            raise

        return self._model

    @property
    def model(self) -> SentenceTransformer:
        """Get the loaded model, loading if necessary."""
        if self._model is None:
            self.load_model()
        return self._model

    @property
    def device(self) -> str:
        """Get the device the model is running on."""
        if self._device is None:
            self._device = self._select_device()
        return self._device

    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension of the model."""
        return self.model.get_sentence_embedding_dimension()

    def encode(
        self,
        texts: list[str],
        batch_size: int | None = None,
        show_progress: bool = False,
        normalize: bool = True,
    ) -> np.ndarray:
        """
        Encode texts into embeddings.

        Args:
            texts: List of texts to encode.
            batch_size: Batch size for encoding (uses config default if None).
            show_progress: Show progress bar during encoding.
            normalize: Normalize embeddings to unit length.

        Returns:
            NumPy array of embeddings with shape (len(texts), embedding_dim).
        """
        if not texts:
            return np.array([])

        batch_size = batch_size or self.config.batch_size

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=normalize,
            convert_to_numpy=True,
        )

        return embeddings

    def encode_queries(
        self,
        queries: list[str],
        batch_size: int | None = None,
    ) -> np.ndarray:
        """
        Encode search queries.

        Some models have different encoding for queries vs documents.
        This method can be overridden for such models.

        Args:
            queries: List of query texts.
            batch_size: Batch size for encoding.

        Returns:
            NumPy array of query embeddings.
        """
        return self.encode(queries, batch_size=batch_size)

    def encode_documents(
        self,
        documents: list[str],
        batch_size: int | None = None,
        show_progress: bool = True,
    ) -> np.ndarray:
        """
        Encode documents for indexing.

        Args:
            documents: List of document texts.
            batch_size: Batch size for encoding.
            show_progress: Show progress bar.

        Returns:
            NumPy array of document embeddings.
        """
        return self.encode(documents, batch_size=batch_size, show_progress=show_progress)

    def encode_single(self, text: str) -> list[float]:
        """
        Encode a single text and return as list.

        Convenient for single queries where list format is needed.

        Args:
            text: Text to encode.

        Returns:
            Embedding as list of floats.
        """
        embedding = self.encode([text])[0]
        return embedding.tolist()

    def similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.

        Args:
            text1: First text.
            text2: Second text.

        Returns:
            Cosine similarity score (0-1 for normalized embeddings).
        """
        embeddings = self.encode([text1, text2])
        # Cosine similarity for normalized vectors is just dot product
        return float(np.dot(embeddings[0], embeddings[1]))

    def batch_similarity(
        self, queries: list[str], documents: list[str]
    ) -> np.ndarray:
        """
        Compute similarity matrix between queries and documents.

        Args:
            queries: List of query texts.
            documents: List of document texts.

        Returns:
            Similarity matrix with shape (len(queries), len(documents)).
        """
        query_embeddings = self.encode_queries(queries)
        doc_embeddings = self.encode_documents(documents, show_progress=False)

        # Matrix multiplication for all pairwise similarities
        return np.matmul(query_embeddings, doc_embeddings.T)

    def unload(self) -> None:
        """Unload the model to free memory."""
        if self._model is not None:
            del self._model
            self._model = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.info("embedding_model_unloaded")


def create_embedding_manager(config: EmbeddingConfig) -> EmbeddingModelManager:
    """
    Create an embedding model manager from configuration.

    Args:
        config: Embedding configuration.

    Returns:
        Configured EmbeddingModelManager instance.
    """
    return EmbeddingModelManager(config)
