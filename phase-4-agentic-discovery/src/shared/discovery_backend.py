"""
Discovery Backend for Agent Capability Discovery
Integrates with Phase 1 ChromaDB for semantic agent matching.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any
import sys

from .a2a_protocol import A2ACapability


class DiscoveryBackend(ABC):
    """Abstract base class for agent discovery backends"""

    @abstractmethod
    def register_agent(self, capability: A2ACapability) -> None:
        """Register an agent's capabilities"""
        pass

    @abstractmethod
    def discover_agents(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.5
    ) -> List[tuple[A2ACapability, float]]:
        """
        Discover agents that can handle a query.

        Args:
            query: Natural language query describing needed capability
            top_k: Maximum number of agents to return
            min_score: Minimum similarity score threshold

        Returns:
            List of (capability, score) tuples, sorted by score descending
        """
        pass

    @abstractmethod
    def get_agent(self, agent_id: str) -> Optional[A2ACapability]:
        """Get a specific agent's capability by ID"""
        pass

    @abstractmethod
    def list_agents(self) -> List[A2ACapability]:
        """List all registered agents"""
        pass


class ChromaDBDiscoveryBackend(DiscoveryBackend):
    """
    ChromaDB-based discovery backend.
    Integrates with Phase 1 embedding infrastructure.
    """

    def __init__(
        self,
        collection_name: str = "agent_capabilities",
        persist_directory: Optional[Path] = None,
        phase1_path: Optional[Path] = None
    ):
        """
        Initialize ChromaDB discovery backend.

        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Where to persist ChromaDB data
            phase1_path: Path to phase-1-embed-space for ChromaDB client
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory or Path.cwd() / "data" / "chromadb"
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Import ChromaDB client from Phase 1
        if phase1_path:
            sys.path.insert(0, str(phase1_path / "src"))

        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            raise ImportError(
                "chromadb not installed. Install with: pip install chromadb"
            )

        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=str(self.persist_directory),
            anonymized_telemetry=False
        ))

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Agent capability discovery"}
        )

        # In-memory cache for quick lookups
        self._agent_cache: Dict[str, A2ACapability] = {}

    def register_agent(self, capability: A2ACapability) -> None:
        """Register an agent's capabilities in ChromaDB"""
        # Create embedding text from capability
        embedding_text = self._capability_to_text(capability)

        # Add to ChromaDB
        self.collection.add(
            documents=[embedding_text],
            metadatas=[capability.to_dict()],
            ids=[capability.agent_id]
        )

        # Update cache
        self._agent_cache[capability.agent_id] = capability

    def discover_agents(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.5
    ) -> List[tuple[A2ACapability, float]]:
        """
        Discover agents using semantic search in ChromaDB.

        Returns agents ranked by similarity to the query.
        """
        # Query ChromaDB
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        # Parse results
        agents_with_scores = []
        if results["ids"] and results["ids"][0]:
            for i, agent_id in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i]
                capability = A2ACapability.from_dict(metadata)

                # ChromaDB returns distances, convert to similarity score
                # Cosine distance is in [0, 2], convert to similarity in [0, 1]
                distance = results["distances"][0][i] if results.get("distances") else 0.5
                score = 1.0 - (distance / 2.0)

                if score >= min_score:
                    agents_with_scores.append((capability, score))

        return sorted(agents_with_scores, key=lambda x: x[1], reverse=True)

    def get_agent(self, agent_id: str) -> Optional[A2ACapability]:
        """Get a specific agent by ID"""
        # Check cache first
        if agent_id in self._agent_cache:
            return self._agent_cache[agent_id]

        # Query ChromaDB
        try:
            result = self.collection.get(ids=[agent_id])
            if result["ids"]:
                metadata = result["metadatas"][0]
                capability = A2ACapability.from_dict(metadata)
                self._agent_cache[agent_id] = capability
                return capability
        except Exception:
            pass

        return None

    def list_agents(self) -> List[A2ACapability]:
        """List all registered agents"""
        result = self.collection.get()
        agents = []
        for metadata in result["metadatas"]:
            agents.append(A2ACapability.from_dict(metadata))
        return agents

    def _capability_to_text(self, capability: A2ACapability) -> str:
        """Convert capability to text for embedding"""
        parts = [
            f"Agent: {capability.name}",
            f"Description: {capability.description}",
            f"Domains: {', '.join(capability.domains)}"
        ]

        if capability.example_queries:
            parts.append(f"Examples: {' | '.join(capability.example_queries)}")

        return "\n".join(parts)


class InMemoryDiscoveryBackend(DiscoveryBackend):
    """
    Simple in-memory discovery backend for testing.
    Uses basic string matching instead of embeddings.
    """

    def __init__(self):
        self._agents: Dict[str, A2ACapability] = {}

    def register_agent(self, capability: A2ACapability) -> None:
        """Register an agent in memory"""
        self._agents[capability.agent_id] = capability

    def discover_agents(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.5
    ) -> List[tuple[A2ACapability, float]]:
        """Discover agents using basic string matching"""
        query_lower = query.lower()
        scored_agents = []

        for capability in self._agents.values():
            # Simple scoring based on keyword matching
            score = 0.0
            searchable_text = (
                f"{capability.name} {capability.description} "
                f"{' '.join(capability.domains)} {' '.join(capability.example_queries)}"
            ).lower()

            # Count keyword matches
            keywords = query_lower.split()
            matches = sum(1 for kw in keywords if kw in searchable_text)
            score = matches / len(keywords) if keywords else 0.0

            if score >= min_score:
                scored_agents.append((capability, score))

        # Sort by score and return top_k
        scored_agents.sort(key=lambda x: x[1], reverse=True)
        return scored_agents[:top_k]

    def get_agent(self, agent_id: str) -> Optional[A2ACapability]:
        """Get agent by ID"""
        return self._agents.get(agent_id)

    def list_agents(self) -> List[A2ACapability]:
        """List all agents"""
        return list(self._agents.values())
