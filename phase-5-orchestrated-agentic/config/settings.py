"""
Phase 5 Configuration Settings
Pydantic-based settings for all programs.
"""

from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class DataConversionSettings(BaseModel):
    """Program 1: Data Conversion configuration"""
    test_mode_samples: int = Field(default=100, description="Number of samples in test mode")
    full_mode_samples: int = Field(
        default=71000, description="Expected number of samples in full mode"
    )
    train_split: float = Field(default=0.7, description="Training set split ratio")
    val_split: float = Field(default=0.15, description="Validation set split ratio")
    test_split: float = Field(default=0.15, description="Test set split ratio")
    augmentation_factor: int = Field(default=3, description="Number of augmented variants per example")
    max_synthetic_intents: int = Field(default=5, description="Max synthetic intents per workflow")


class SLMFineTuningSettings(BaseModel):
    """Program 2: SLM Fine-tuning configuration"""
    base_model: str = Field(default="Qwen/Qwen2.5-7B", description="Base model to fine-tune")
    alternative_model: str = Field(default="microsoft/phi-4", description="Alternative base model")

    # LoRA configuration
    lora_rank: int = Field(default=16, description="LoRA rank")
    lora_alpha: int = Field(default=32, description="LoRA alpha")
    lora_dropout: float = Field(default=0.05, description="LoRA dropout")
    target_modules: List[str] = Field(
        default=["q_proj", "v_proj"],
        description="Target modules for LoRA"
    )

    # Training configuration
    learning_rate: float = Field(default=2e-4, description="Learning rate")
    num_epochs: int = Field(default=3, description="Number of training epochs")
    batch_size: int = Field(default=4, description="Training batch size")
    gradient_accumulation_steps: int = Field(default=4, description="Gradient accumulation steps")
    max_seq_length: int = Field(default=2048, description="Maximum sequence length")
    warmup_steps: int = Field(default=100, description="Warmup steps")

    # Evaluation
    eval_steps: int = Field(default=100, description="Evaluation frequency")
    save_steps: int = Field(default=500, description="Checkpoint save frequency")
    target_accuracy: float = Field(default=0.94, description="Target accuracy on known workflows")
    target_latency_ms: int = Field(default=150, description="Target inference latency in ms")


class InferenceServerSettings(BaseModel):
    """Program 3: Inference Server configuration"""
    server_type: str = Field(default="vllm", description="Server type (vllm or tgi)")
    host: str = Field(default="0.0.0.0", description="Host to bind to")
    port: int = Field(default=8100, description="Inference server port")

    # vLLM settings
    vllm_gpu_memory_utilization: float = Field(default=0.9, description="GPU memory utilization")
    vllm_max_model_len: int = Field(default=2048, description="Max model length")
    vllm_tensor_parallel_size: int = Field(default=1, description="Tensor parallel size")

    # TGI settings
    tgi_max_concurrent_requests: int = Field(default=128, description="Max concurrent requests")
    tgi_max_batch_total_tokens: int = Field(default=16384, description="Max batch total tokens")

    # Health monitoring
    health_check_interval_seconds: int = Field(default=30, description="Health check interval")
    max_latency_ms: int = Field(default=200, description="Maximum acceptable latency")


class OrchestratorServiceSettings(BaseModel):
    """Program 4: Orchestrator Service configuration"""
    host: str = Field(default="0.0.0.0", description="Host to bind to")
    port: int = Field(default=8000, description="Orchestrator service port")

    # Agent registry (runtime connection to Phase 4 agents)
    agent_registry: Dict[str, str] = Field(
        default={
            "fundraising-agent": "http://localhost:8001",
            "business-development-agent": "http://localhost:8002",
            "field-operations-agent": "http://localhost:8003"
        },
        description="Agent service URLs"
    )

    # Inference server connection
    inference_server_url: str = Field(
        default="http://localhost:8100/generate",
        description="Inference server URL"
    )

    # Request settings
    max_concurrent_agent_calls: int = Field(default=5, description="Max concurrent agent calls")
    agent_timeout_ms: int = Field(default=10000, description="Agent call timeout in ms")
    routing_timeout_ms: int = Field(default=500, description="Routing decision timeout in ms")

    # Response synthesis
    enable_response_synthesis: bool = Field(
        default=True,
        description="Enable multi-agent response synthesis"
    )


class PathSettings(BaseModel):
    """Path configuration"""
    data_dir: Path = Field(default=Path("data"), description="Data directory")
    models_dir: Path = Field(default=Path("data/models"), description="Models directory")
    training_dir: Path = Field(default=Path("data/training"), description="Training data directory")
    checkpoints_dir: Path = Field(
        default=Path("data/checkpoints"),
        description="Checkpoints directory"
    )
    exports_dir: Path = Field(default=Path("data/exports"), description="Exports directory")
    phase4_imports_dir: Path = Field(
        default=Path("data/phase4_imports"),
        description="Phase 4 imports directory"
    )

    # Phase 4 integration
    phase4_path: Optional[Path] = Field(
        default=None,
        description="Path to phase-4-agentic-discovery"
    )
    phase4_exports_dir: Optional[Path] = Field(
        default=None,
        description="Path to Phase 4 exports directory"
    )


class Settings(BaseSettings):
    """
    Main settings for Phase 5.

    Can be configured via:
    1. config.yaml file
    2. Environment variables (prefixed with PHASE5_)
    3. Direct instantiation
    """

    # Sub-settings
    data_conversion: DataConversionSettings = Field(default_factory=DataConversionSettings)
    slm_finetuning: SLMFineTuningSettings = Field(default_factory=SLMFineTuningSettings)
    inference_server: InferenceServerSettings = Field(default_factory=InferenceServerSettings)
    orchestrator_service: OrchestratorServiceSettings = Field(
        default_factory=OrchestratorServiceSettings
    )
    paths: PathSettings = Field(default_factory=PathSettings)

    # General settings
    test_mode: bool = Field(default=False, description="Global test mode flag")
    device: Optional[str] = Field(default=None, description="Device for training (cuda/cpu/mps)")
    log_level: str = Field(default="INFO", description="Logging level")

    class Config:
        env_prefix = "PHASE5_"
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
