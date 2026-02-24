"""Bridge to Phase 1 embedding space for RAG integration."""

from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Import from Phase 0
from habitat_logging import get_logger

logger = get_logger(__name__)


class EmbeddingBridge:
    """Bridge to Phase 1 embedding space for retrieving relevant context."""

    def __init__(self, phase1_config_path: str | Path | None = None):
        """
        Initialize the embedding bridge.

        Args:
            phase1_config_path: Path to Phase 1 config.yaml
        """
        self.config_path = Path(phase1_config_path) if phase1_config_path else None
        self._initialized = False
        self._collection = None
        self._embed_model = None

    def initialize(self) -> bool:
        """
        Initialize connection to Phase 1 embedding space.

        Returns:
            True if initialization successful, False otherwise
        """
        if self._initialized:
            return True

        if not self.config_path or not self.config_path.exists():
            logger.warning("phase1_config_not_found", path=str(self.config_path))
            return False

        try:
            import yaml

            with open(self.config_path) as f:
                config = yaml.safe_load(f)

            # Load ChromaDB collection
            import chromadb

            persist_dir = self.config_path.parent / config.get("chroma", {}).get(
                "persist_directory", "data/chroma"
            )

            if not persist_dir.exists():
                logger.warning("chroma_directory_not_found", path=str(persist_dir))
                return False

            client = chromadb.PersistentClient(path=str(persist_dir))
            collection_name = config.get("chroma", {}).get(
                "collection_name", "enterprise_embeddings"
            )
            self._collection = client.get_collection(name=collection_name)

            # Load embedding model
            from sentence_transformers import SentenceTransformer

            model_name = config.get("embedding", {}).get(
                "model_name", "BAAI/bge-base-en-v1.5"
            )
            self._embed_model = SentenceTransformer(model_name)

            self._initialized = True
            logger.info(
                "embedding_bridge_initialized",
                collection=collection_name,
                model=model_name,
            )
            return True

        except Exception as e:
            logger.error("embedding_bridge_init_failed", error=str(e))
            return False

    def get_relevant_context(
        self,
        query: str,
        k: int = 3,
        unit_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve relevant context from Phase 1 embedding space.

        Args:
            query: The query text
            k: Number of results to return
            unit_filter: Optional filter by unit ID

        Returns:
            List of relevant context documents
        """
        if not self._initialized:
            if not self.initialize():
                return []

        try:
            # Generate query embedding
            query_embedding = self._embed_model.encode(query).tolist()

            # Build filter
            where_filter = None
            if unit_filter:
                where_filter = {"unit_id": unit_filter}

            # Query collection
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=where_filter,
            )

            # Format results
            context_docs = []
            if results and results.get("documents"):
                for i, doc in enumerate(results["documents"][0]):
                    metadata = (
                        results["metadatas"][0][i] if results.get("metadatas") else {}
                    )
                    distance = (
                        results["distances"][0][i] if results.get("distances") else None
                    )
                    context_docs.append(
                        {
                            "content": doc,
                            "metadata": metadata,
                            "distance": distance,
                        }
                    )

            logger.info(
                "context_retrieved",
                query_length=len(query),
                num_results=len(context_docs),
            )

            return context_docs

        except Exception as e:
            logger.error("context_retrieval_failed", error=str(e))
            return []

    def format_context_for_prompt(
        self,
        context_docs: list[dict[str, Any]],
        max_tokens: int = 1000,
    ) -> str:
        """
        Format retrieved context for inclusion in a prompt.

        Args:
            context_docs: List of context documents
            max_tokens: Maximum approximate tokens for context

        Returns:
            Formatted context string
        """
        if not context_docs:
            return ""

        parts = ["Relevant context:"]
        total_length = 0
        char_per_token = 4  # Rough approximation

        for i, doc in enumerate(context_docs):
            content = doc.get("content", "")
            if total_length + len(content) > max_tokens * char_per_token:
                # Truncate remaining content
                remaining_chars = max_tokens * char_per_token - total_length
                if remaining_chars > 100:
                    content = content[:remaining_chars] + "..."
                else:
                    break

            parts.append(f"\n[{i + 1}] {content}")
            total_length += len(content)

        return "\n".join(parts)

    def augment_prompt(
        self,
        prompt: str,
        k: int = 3,
        unit_filter: str | None = None,
        max_context_tokens: int = 1000,
    ) -> str:
        """
        Augment a prompt with relevant context from Phase 1.

        Args:
            prompt: The original prompt
            k: Number of context documents
            unit_filter: Optional filter by unit
            max_context_tokens: Maximum tokens for context

        Returns:
            Augmented prompt with context
        """
        context_docs = self.get_relevant_context(
            query=prompt,
            k=k,
            unit_filter=unit_filter,
        )

        if not context_docs:
            return prompt

        context_str = self.format_context_for_prompt(
            context_docs=context_docs,
            max_tokens=max_context_tokens,
        )

        return f"{context_str}\n\n{prompt}"

    @property
    def is_available(self) -> bool:
        """Check if the bridge is available."""
        return self._initialized or (
            self.config_path is not None and self.config_path.exists()
        )
