"""
Phase 4 Configuration Settings
Pydantic-based settings for all programs.
"""

from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class A2AProtocolSettings(BaseModel):
    """A2A Protocol configuration"""
    default_max_depth: int = Field(default=3, description="Default maximum cascade depth")
    default_timeout_ms: int = Field(default=5000, description="Default timeout in milliseconds")
    max_cascade_depth: int = Field(default=4, description="Maximum allowed cascade depth")


class A2AFineTuningSettings(BaseModel):
    """Program 1: A2A Fine-Tuning configuration"""
    num_training_examples: int = Field(default=1000, description="Number of training examples")
    lora_rank: int = Field(default=16, description="LoRA rank")
    lora_alpha: int = Field(default=32, description="LoRA alpha")
    learning_rate: float = Field(default=2e-4, description="Learning rate")
    num_epochs: int = Field(default=3, description="Number of training epochs")
    batch_size: int = Field(default=4, description="Training batch size")
    gradient_accumulation_steps: int = Field(default=4, description="Gradient accumulation")
    max_seq_length: int = Field(default=512, description="Maximum sequence length")


class AgentServiceSettings(BaseModel):
    """Program 2: Agent Services configuration"""
    base_port: int = Field(default=8000, description="Base port for agent services")
    host: str = Field(default="0.0.0.0", description="Host to bind to")
    agent_ports: Dict[str, int] = Field(
        default={
            "fundraising-agent": 8001,
            "business-development-agent": 8002,
            "field-operations-agent": 8003
        },
        description="Port mapping for each agent"
    )


class DiscoveryPipelineSettings(BaseModel):
    """Program 3: Discovery Pipeline configuration"""
    queries_per_day: int = Field(default=10, description="Queries to run per day")
    test_mode_days: int = Field(default=7, description="Number of days in test mode")
    full_experiment_days: int = Field(default=90, description="Number of days in full experiment")


class AdaptiveAnalyzerSettings(BaseModel):
    """Program 4: Adaptive Analyzer configuration"""
    min_success_rate: float = Field(default=0.8, description="Minimum success rate for export")
    min_sample_size: int = Field(default=5, description="Minimum samples for analysis")


class PathSettings(BaseModel):
    """Path configuration"""
    data_dir: Path = Field(default=Path("data"), description="Data directory")
    models_dir: Path = Field(default=Path("data/models"), description="Models directory")
    training_dir: Path = Field(default=Path("data/training"), description="Training data directory")
    logs_dir: Path = Field(default=Path("data/logs"), description="Logs directory")
    exports_dir: Path = Field(default=Path("data/exports"), description="Exports directory")
    phase3_path: Optional[Path] = Field(default=None, description="Path to phase-3-moe-experts")
    phase1_path: Optional[Path] = Field(default=None, description="Path to phase-1-embed-space")


class Settings(BaseSettings):
    """
    Main settings for Phase 4.

    Can be configured via:
    1. config.yaml file
    2. Environment variables (prefixed with PHASE4_)
    3. Direct instantiation
    """

    # Sub-settings
    a2a_protocol: A2AProtocolSettings = Field(default_factory=A2AProtocolSettings)
    a2a_finetuning: A2AFineTuningSettings = Field(default_factory=A2AFineTuningSettings)
    agent_services: AgentServiceSettings = Field(default_factory=AgentServiceSettings)
    discovery_pipeline: DiscoveryPipelineSettings = Field(default_factory=DiscoveryPipelineSettings)
    adaptive_analyzer: AdaptiveAnalyzerSettings = Field(default_factory=AdaptiveAnalyzerSettings)
    paths: PathSettings = Field(default_factory=PathSettings)

    # General settings
    test_mode: bool = Field(default=False, description="Global test mode flag")
    device: Optional[str] = Field(default=None, description="Device for training (cuda/cpu/mps)")

    class Config:
        env_prefix = "PHASE4_"
        env_nested_delimiter = "__"


def load_settings(config_file: Optional[Path] = None) -> Settings:
    """
    Load settings from config file and environment.

    Args:
        config_file: Path to config.yaml (optional)

    Returns:
        Settings instance
    """
    if config_file and config_file.exists():
        import yaml

        with open(config_file) as f:
            config_data = yaml.safe_load(f)

        return Settings(**config_data)
    else:
        return Settings()


# Global settings instance (lazy loaded)
_settings: Optional[Settings] = None


def get_settings(config_file: Optional[Path] = None) -> Settings:
    """
    Get global settings instance.

    Args:
        config_file: Path to config.yaml (optional)

    Returns:
        Settings instance
    """
    global _settings

    if _settings is None:
        _settings = load_settings(config_file)

    return _settings
