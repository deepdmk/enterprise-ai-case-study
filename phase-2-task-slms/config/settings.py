"""Pydantic settings for Phase 2 Task SLMs."""

import sys
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

# Import HabitatBaseSettings from phase-0-infrastructure's phase0_infra package
# (namespaced, so it no longer conflicts with this local config package)
_phase0_root = Path(__file__).parent.parent.parent / "phase-0-infrastructure"
if str(_phase0_root) not in sys.path:
    sys.path.insert(0, str(_phase0_root))
from phase0_infra.config.base_settings import HabitatBaseSettings  # noqa: E402


class LoRAConfig(BaseModel):
    """LoRA configuration for fine-tuning."""

    r: int = 16
    lora_alpha: int = 16
    lora_dropout: float = 0
    target_modules: list[str] = Field(
        default_factory=lambda: [
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "up_proj",
            "down_proj",
            "gate_proj",
        ]
    )
    use_rslora: bool = True
    bias: str = "none"
    task_type: str = "CAUSAL_LM"


class ModelConfig(BaseModel):
    """Base model configuration.

    Security Note:
        The `trust_remote_code` setting allows models to execute custom Python
        code from the Hugging Face Hub. This is required for some models but
        poses security risks. Only enable for trusted model sources.
    """

    base_model: str = "unsloth/Meta-Llama-3.1-8B-bnb-4bit"
    max_seq_length: int = 2048
    dtype: str | None = None
    load_in_4bit: bool = True
    # SECURITY: Only enable for trusted model sources (e.g., official HuggingFace repos)
    trust_remote_code: bool = Field(
        default=False,
        description="Allow executing custom code from model repos. SECURITY RISK - only enable for trusted sources."
    )


class TrainingConfig(BaseModel):
    """Training configuration."""

    epochs: int = 3
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 3e-4
    warmup_steps: int = 10
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    lr_scheduler_type: str = "linear"
    logging_steps: int = 10
    save_steps: int = 100
    eval_steps: int = 100
    fp16: bool = True
    bf16: bool = False
    seed: int = 42


class TestModeConfig(BaseModel):
    """Test mode configuration for quick validation."""

    samples: int = 50
    epochs: int = 1
    batch_size: int = 2
    gradient_accumulation_steps: int = 1
    logging_steps: int = 1


class DataConfig(BaseModel):
    """Data processing configuration."""

    train_split: float = 0.9
    val_split: float = 0.1
    max_samples_per_task: int = 500
    min_samples_per_task: int = 200
    shuffle: bool = True


class PathsConfig(BaseModel):
    """Path configuration."""

    data_dir: Path = Path("data")
    raw_dir: Path = Path("data/raw")
    processed_dir: Path = Path("data/processed")
    models_dir: Path = Path("data/models")
    evaluations_dir: Path = Path("data/evaluations")
    rlhf_dir: Path = Path("data/rlhf")
    registry_dir: Path = Path("data/registry")


class Phase1Config(BaseModel):
    """Phase 1 integration configuration."""

    config_path: str = "../phase-1-embed-space/config/config.yaml"
    enabled: bool = False


class EvaluationConfig(BaseModel):
    """Evaluation configuration."""

    metrics: list[str] = Field(
        default_factory=lambda: ["format_compliance", "content_coverage", "generation_latency"]
    )
    num_eval_samples: int = 20
    max_new_tokens: int = 512
    temperature: float = 0.7


class RegistryConfig(BaseModel):
    """Model registry configuration."""

    registry_file: str = "model_registry.json"
    export_merged: bool = True
    export_format: str = "safetensors"


class UnitConfig(BaseModel):
    """Unit configuration."""

    id: str
    name: str
    tasks_file: str


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    format: Literal["json", "text"] = "json"


class TaskDefinition(BaseModel):
    """Task definition for a specific SLM."""

    id: str
    name: str
    description: str = ""
    system_prompt: str
    positive_prompts: list[str] = Field(default_factory=list)
    negative_prompts: list[str] = Field(default_factory=list)
    examples_required: int = 300
    output_format: str = "text"
    required_sections: list[str] = Field(default_factory=list)


class UnitDefinition(BaseModel):
    """Unit definition with its tasks."""

    id: str
    name: str
    description: str = ""
    tasks: list[TaskDefinition] = Field(default_factory=list)


class Settings(HabitatBaseSettings):
    """Main settings class combining all configurations."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Environment variables
    hf_token: str | None = Field(default=None, alias="HF_TOKEN")
    hf_home: str | None = Field(default=None, alias="HF_HOME")
    # test_mode and log_level inherited from HabitatBaseSettings

    # Nested configurations (loaded from YAML)
    model: ModelConfig = Field(default_factory=ModelConfig)
    lora: LoRAConfig = Field(default_factory=LoRAConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    test_mode_config: TestModeConfig = Field(default_factory=TestModeConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    phase1: Phase1Config = Field(default_factory=Phase1Config)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    registry: RegistryConfig = Field(default_factory=RegistryConfig)
    units: list[UnitConfig] = Field(default_factory=list)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @classmethod
    def from_yaml(cls, config_path: str | Path) -> "Settings":
        """Load settings from YAML configuration file."""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path) as f:
            config_data = yaml.safe_load(f)

        # Map YAML keys to Pydantic field names
        if "test_mode" in config_data:
            config_data["test_mode_config"] = config_data.pop("test_mode")

        return cls(**config_data)

    def get_effective_training_config(self) -> TrainingConfig:
        """Get training config adjusted for test mode."""
        if self.test_mode:
            return TrainingConfig(
                epochs=self.test_mode_config.epochs,
                batch_size=self.test_mode_config.batch_size,
                gradient_accumulation_steps=self.test_mode_config.gradient_accumulation_steps,
                learning_rate=self.training.learning_rate,
                warmup_steps=self.training.warmup_steps,
                weight_decay=self.training.weight_decay,
                max_grad_norm=self.training.max_grad_norm,
                lr_scheduler_type=self.training.lr_scheduler_type,
                logging_steps=self.test_mode_config.logging_steps,
                save_steps=self.training.save_steps,
                eval_steps=self.training.eval_steps,
                fp16=self.training.fp16,
                bf16=self.training.bf16,
                seed=self.training.seed,
            )
        return self.training

    def get_effective_samples(self) -> int:
        """Get number of samples adjusted for test mode."""
        if self.test_mode:
            return self.test_mode_config.samples
        return self.data.max_samples_per_task


def load_task_definitions(tasks_file: str | Path, base_path: Path | None = None) -> UnitDefinition:
    """Load task definitions from YAML file."""
    if base_path:
        tasks_path = base_path / tasks_file
    else:
        tasks_path = Path(tasks_file)

    if not tasks_path.exists():
        raise FileNotFoundError(f"Tasks file not found: {tasks_path}")

    with open(tasks_path) as f:
        data = yaml.safe_load(f)

    return UnitDefinition(
        id=data.get("unit", {}).get("id", ""),
        name=data.get("unit", {}).get("name", ""),
        description=data.get("unit", {}).get("description", ""),
        tasks=[TaskDefinition(**task) for task in data.get("tasks", [])],
    )


def get_settings(config_path: str | Path | None = None) -> Settings:
    """Get settings instance, optionally loading from YAML."""
    if config_path:
        return Settings.from_yaml(config_path)
    return Settings()
