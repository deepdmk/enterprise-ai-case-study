"""
Pydantic settings for type-safe configuration management.
Supports environment variable overrides and YAML config loading.
"""

import os
import sys
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from pydantic import BaseModel, Field

# Import HabitatBaseSettings from phase-0-infrastructure's phase0_infra package
# (namespaced, so it no longer conflicts with this local config package)
_phase0_root = Path(__file__).parent.parent.parent / "phase-0-infrastructure"
if str(_phase0_root) not in sys.path:
    sys.path.insert(0, str(_phase0_root))
from phase0_infra.config.base_settings import HabitatBaseSettings  # noqa: E402


class TableConfig(BaseModel):
    """Configuration for a database table."""

    name: str
    text_columns: list[str]
    id_column: str
    timestamp_column: str
    additional_metadata: list[str] = Field(default_factory=list)


class DatabaseConfig(BaseModel):
    """Configuration for a PostgreSQL database connection."""

    host: str = "localhost"
    port: str = "5432"
    name: str
    user: str = "postgres"
    password: str = ""
    pool_size: int = 5
    tables: list[TableConfig] = Field(default_factory=list)

    @property
    def connection_string(self) -> str:
        """Generate PostgreSQL connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def async_connection_string(self) -> str:
        """Generate async PostgreSQL connection string for asyncpg."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class ChromaDBConfig(BaseModel):
    """Configuration for ChromaDB connection."""

    host: str = "localhost"
    port: str = "8000"
    collection_name: str = "enterprise_embeddings"
    hnsw: dict[str, Any] = Field(
        default_factory=lambda: {"space": "cosine", "ef_construction": 200, "ef_search": 40}
    )


class EmbeddingConfig(BaseModel):
    """Configuration for embedding model."""

    base_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    fine_tuned_model_path: str = "data/models/enterprise-embed-v1"
    embedding_dimension: int = 384
    batch_size: int = 32
    device: str = "auto"


class ChunkingConfig(BaseModel):
    """Configuration for text chunking."""

    chunk_size: int = 512
    chunk_overlap: int = 50
    strategy: str = "recursive"


class PairGenerationConfig(BaseModel):
    """Configuration for training pair generation."""

    strategy: str = "adjacent_chunks"
    min_chunk_length: int = 50


class DatasetGeneratorConfig(BaseModel):
    """Configuration for Program 1: Dataset Generator."""

    output_dir: str = "data/training_datasets"
    samples_per_table: int = 10000
    pair_generation: PairGenerationConfig = Field(default_factory=PairGenerationConfig)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    train_val_split: float = 0.9
    random_seed: int = 42


class TrainingParamsConfig(BaseModel):
    """Training parameters for fine-tuning."""

    epochs: int = 3
    batch_size: int = 64
    learning_rate: float = 2e-5
    warmup_ratio: float = 0.1
    fp16: bool = True
    save_strategy: str = "epoch"
    logging_steps: int = 100
    evaluation_strategy: str = "steps"
    eval_steps: int = 500


class LossConfig(BaseModel):
    """Loss function configuration."""

    type: str = "MultipleNegativesRankingLoss"
    scale: float = 20.0


class FineTuningConfig(BaseModel):
    """Configuration for Program 2: Fine-Tuning."""

    output_dir: str = "data/models"
    model_name: str = "enterprise-embed-v1"
    training: TrainingParamsConfig = Field(default_factory=TrainingParamsConfig)
    loss: LossConfig = Field(default_factory=LossConfig)


class IncrementalConfig(BaseModel):
    """Configuration for incremental ingestion."""

    enabled: bool = True
    state_file: str = "data/sync_state.json"


class IngestionConfig(BaseModel):
    """Configuration for Program 3: Ingestion Pipeline."""

    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    batch_size: int = 100
    incremental: IncrementalConfig = Field(default_factory=IncrementalConfig)


class GradioConfig(BaseModel):
    """Configuration for Gradio UI."""

    host: str = "0.0.0.0"
    port: int = 7860
    share: bool = False
    title: str = "Enterprise Document Search"
    description: str = "Semantic search across unified enterprise data"


class RerankingConfig(BaseModel):
    """Configuration for search reranking."""

    # Opt-in by design: config.yaml enables it explicitly. Reranking runs
    # after the parent-document fetch (the index stores no chunk text).
    enabled: bool = False
    model: str | None = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    candidate_multiplier: int = 3  # Retrieve N*k candidates before reranking


class FeedbackConfig(BaseModel):
    """Configuration for RLHF feedback collection."""

    enabled: bool = True
    feedback_dir: str = "data/feedback"


class SearchConfig(BaseModel):
    """Configuration for Program 4: Search."""

    default_k: int = 5
    max_k: int = 20
    reranking: RerankingConfig = Field(default_factory=RerankingConfig)
    feedback: FeedbackConfig = Field(default_factory=FeedbackConfig)
    gradio: GradioConfig = Field(default_factory=GradioConfig)


class AppConfig(BaseModel):
    """Application-level configuration."""

    name: str = "enterprise-embedding-space"
    version: str = "1.0.0"
    log_dir: str = "data/logs"


class Settings(HabitatBaseSettings):  # type: ignore[misc, valid-type]
    """Main settings class that loads from YAML config file."""

    app: AppConfig = Field(default_factory=AppConfig)
    databases: dict[str, DatabaseConfig] = Field(default_factory=dict)
    chromadb: ChromaDBConfig = Field(default_factory=ChromaDBConfig)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    dataset_generator: DatasetGeneratorConfig = Field(default_factory=DatasetGeneratorConfig)
    fine_tuning: FineTuningConfig = Field(default_factory=FineTuningConfig)
    ingestion: IngestionConfig = Field(default_factory=IngestionConfig)
    search: SearchConfig = Field(default_factory=SearchConfig)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def from_yaml(cls, config_path: str | Path) -> "Settings":
        """Load settings from a YAML configuration file."""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path) as f:
            config_data = yaml.safe_load(f)

        # Expand environment variables in config
        config_data = cls._expand_env_vars(config_data)

        return cls(**config_data)

    @classmethod
    def _expand_env_vars(cls, data: Any) -> Any:
        """Recursively expand environment variables in config data."""
        if isinstance(data, dict):
            return {k: cls._expand_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls._expand_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Handle ${VAR:-default} pattern
            if data.startswith("${") and "}" in data:
                # Extract variable name and default
                inner = data[2 : data.index("}")]
                if ":-" in inner:
                    var_name, default = inner.split(":-", 1)
                else:
                    var_name, default = inner, ""
                return os.environ.get(var_name, default)
            return data
        return data


def load_settings(config_path: str | Path | None = None) -> Settings:
    """
    Load settings from config file.

    Args:
        config_path: Path to config.yaml. If None, looks for config/config.yaml
                     relative to the package root.

    Returns:
        Settings instance with loaded configuration.
    """
    if config_path is None:
        # Default to config/config.yaml relative to this file
        config_path = Path(__file__).parent / "config.yaml"

    return Settings.from_yaml(config_path)
