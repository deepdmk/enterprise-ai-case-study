"""Tests for the embedding model manager."""

from config.settings import EmbeddingConfig
from src.shared.embedding_model import EmbeddingModelManager


class TestEncodeEmpty:
    """encode([]) must return a 2-D array so downstream vstack/iteration works."""

    def test_empty_input_returns_2d_array(self):
        manager = EmbeddingModelManager(EmbeddingConfig())

        result = manager.encode([])

        assert result.shape == (0, EmbeddingConfig().embedding_dimension)

    def test_empty_input_does_not_load_model(self):
        manager = EmbeddingModelManager(EmbeddingConfig())

        manager.encode([])

        assert manager._model is None
