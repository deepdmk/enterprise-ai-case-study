"""Routing metadata utilities for Phase 4 integration."""

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

from src.shared.phase2_importer import AdapterInfo

logger = get_logger(__name__)


@dataclass
class ExpertMetadata:
    """Metadata for a single expert in the MoE."""

    expert_id: int
    model_id: str
    unit_id: str
    task_id: str
    version: str
    positive_prompts: list[str] = field(default_factory=list)
    negative_prompts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "expert_id": self.expert_id,
            "model_id": self.model_id,
            "unit_id": self.unit_id,
            "task_id": self.task_id,
            "version": self.version,
            "positive_prompts": self.positive_prompts,
            "negative_prompts": self.negative_prompts,
        }


@dataclass
class RoutingMetadata:
    """Complete routing metadata for the MoE model."""

    experts: list[ExpertMetadata]
    num_experts: int
    experts_per_token: int
    gate_mode: str
    embedding_model: str | None = None

    @classmethod
    def from_adapters(
        cls,
        adapters: list[AdapterInfo],
        experts_per_token: int = 2,
        gate_mode: str = "hidden",
        embedding_model: str | None = None,
    ) -> "RoutingMetadata":
        """Create routing metadata from adapter list."""
        experts = [
            ExpertMetadata(
                expert_id=idx,
                model_id=adapter.model_id,
                unit_id=adapter.unit_id,
                task_id=adapter.task_id,
                version=adapter.version,
                positive_prompts=adapter.positive_prompts,
                negative_prompts=adapter.negative_prompts,
            )
            for idx, adapter in enumerate(adapters)
        ]

        return cls(
            experts=experts,
            num_experts=len(experts),
            experts_per_token=experts_per_token,
            gate_mode=gate_mode,
            embedding_model=embedding_model,
        )

    def get_expert(self, expert_id: int) -> ExpertMetadata | None:
        """Get expert by ID."""
        for expert in self.experts:
            if expert.expert_id == expert_id:
                return expert
        return None

    def get_experts_for_unit(self, unit_id: str) -> list[ExpertMetadata]:
        """Get all experts for a unit."""
        return [e for e in self.experts if e.unit_id == unit_id]

    def get_experts_for_task(self, task_id: str) -> list[ExpertMetadata]:
        """Get all experts for a task."""
        return [e for e in self.experts if e.task_id == task_id]

    def to_dict(self) -> dict[str, Any]:
        return {
            "num_experts": self.num_experts,
            "experts_per_token": self.experts_per_token,
            "gate_mode": self.gate_mode,
            "embedding_model": self.embedding_model,
            "experts": [e.to_dict() for e in self.experts],
        }

    def save(self, output_path: Path) -> None:
        """Save routing metadata to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

        logger.info("routing_metadata_saved", path=str(output_path))

    @classmethod
    def load(cls, input_path: Path) -> "RoutingMetadata":
        """Load routing metadata from file."""
        with open(input_path) as f:
            data = json.load(f)

        experts = [
            ExpertMetadata(**e) for e in data.get("experts", [])
        ]

        return cls(
            experts=experts,
            num_experts=data.get("num_experts", len(experts)),
            experts_per_token=data.get("experts_per_token", 2),
            gate_mode=data.get("gate_mode", "hidden"),
            embedding_model=data.get("embedding_model"),
        )


class RoutingEmbeddings:
    """Manage routing embeddings for fast expert selection."""

    def __init__(self, routing_dir: Path):
        """
        Initialize routing embeddings.

        Args:
            routing_dir: Directory containing routing files
        """
        self.routing_dir = Path(routing_dir)
        self._positive_embeddings = None
        self._negative_embeddings = None
        self._prompt_mapping = None

    def load(self) -> bool:
        """Load embeddings from disk."""
        try:
            import numpy as np

            pos_path = self.routing_dir / "positive_embeddings.npy"
            neg_path = self.routing_dir / "negative_embeddings.npy"
            mapping_path = self.routing_dir / "prompt_mapping.json"

            if pos_path.exists():
                self._positive_embeddings = np.load(pos_path)

            if neg_path.exists():
                self._negative_embeddings = np.load(neg_path)

            if mapping_path.exists():
                with open(mapping_path) as f:
                    self._prompt_mapping = json.load(f)

            logger.info("routing_embeddings_loaded", path=str(self.routing_dir))
            return True

        except ImportError:
            logger.warning("numpy_not_available")
            return False
        except Exception as e:
            logger.error("embeddings_load_failed", error=str(e))
            return False

    def find_relevant_experts(
        self,
        query: str,
        top_k: int = 2,
        embedding_model: str = "BAAI/bge-base-en-v1.5",
    ) -> list[tuple[int, float]]:
        """
        Find most relevant experts for a query.

        Args:
            query: Input query
            top_k: Number of experts to return
            embedding_model: Model for encoding query

        Returns:
            List of (expert_id, similarity_score) tuples
        """
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np

            if self._positive_embeddings is None:
                self.load()

            if self._positive_embeddings is None:
                return []

            # Encode query
            model = SentenceTransformer(embedding_model)
            query_embedding = model.encode([query])[0]

            # Compute similarities to positive prompts
            similarities = np.dot(self._positive_embeddings, query_embedding)

            # Map similarities to experts
            prompt_to_expert = self._prompt_mapping.get("prompt_to_expert", {})
            positive_prompts = self._prompt_mapping.get("positive_prompts", [])

            expert_scores: dict[int, float] = {}
            for idx, similarity in enumerate(similarities):
                if idx < len(positive_prompts):
                    prompt = positive_prompts[idx]
                    expert_ids = prompt_to_expert.get(prompt, [])
                    for expert_id in expert_ids:
                        if expert_id not in expert_scores:
                            expert_scores[expert_id] = 0.0
                        expert_scores[expert_id] = max(
                            expert_scores[expert_id], float(similarity)
                        )

            # Sort and return top_k
            sorted_experts = sorted(
                expert_scores.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            return sorted_experts[:top_k]

        except ImportError:
            logger.warning("dependencies_not_available")
            return []
        except Exception as e:
            logger.error("expert_search_failed", error=str(e))
            return []


def export_a2a_routing_config(
    metadata: RoutingMetadata,
    output_dir: Path,
) -> Path:
    """
    Export routing configuration for A2A protocol.

    Args:
        metadata: Routing metadata
        output_dir: Output directory

    Returns:
        Path to generated config
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build A2A-compatible routing config
    config = {
        "version": "1.0",
        "model_type": "moe",
        "routing": {
            "method": metadata.gate_mode,
            "experts_per_token": metadata.experts_per_token,
            "embedding_model": metadata.embedding_model,
        },
        "experts": {
            str(e.expert_id): {
                "unit": e.unit_id,
                "task": e.task_id,
                "capabilities": e.positive_prompts,
            }
            for e in metadata.experts
        },
        "unit_mapping": {},
    }

    # Add unit mapping
    for expert in metadata.experts:
        if expert.unit_id not in config["unit_mapping"]:
            config["unit_mapping"][expert.unit_id] = []
        config["unit_mapping"][expert.unit_id].append(expert.expert_id)

    config_path = output_dir / "a2a_routing_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    logger.info("a2a_routing_config_exported", path=str(config_path))

    return config_path
