"""Pydantic settings for Phase 3 MoE Experts.

Creates 3 separate MoE models, one per organizational unit:
- Fundraising MoE (5 experts)
- Business Development MoE (4 experts)
- Field Operations MoE (5 experts)
"""

import importlib.util
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Import HabitatBaseSettings from phase-0-infrastructure using direct file import
_phase0_config_path = Path(__file__).parent.parent.parent / "phase-0-infrastructure" / "config" / "base_settings.py"
_spec = importlib.util.spec_from_file_location("phase0_base_settings", _phase0_config_path)
_phase0_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_phase0_module)
HabitatBaseSettings = _phase0_module.HabitatBaseSettings


class MoEArchitectureConfig(BaseModel):
    """MoE architecture configuration (applied to each unit's MoE)."""

    architecture: str = "mixtral"
    gate_mode: Literal["hidden", "cheap_embed", "random"] = "hidden"
    dtype: Literal["float16", "bfloat16", "float32"] = "float16"
    experts_per_token: int = 2  # Within each unit's MoE


class UnitDefinition(BaseModel):
    """Definition of an organizational unit and its tasks."""

    model_config = {"protected_namespaces": ()}

    name: str
    description: str = ""
    tasks: list[str] = Field(default_factory=list)


class MergeConfig(BaseModel):
    """Merge execution configuration."""

    use_cuda: bool = True
    lazy_unpickle: bool = True
    allow_crimes: bool = False
    trust_remote_code: bool = False
    timeout_minutes: int = 60  # Per-unit merge time
    copy_tokenizer: bool = True
    out_shard_size: int = Field(default=5_000_000_000, description="Output shard size in bytes")


class ImportConfig(BaseModel):
    """Phase 2 import configuration."""

    phase2_export_dir: str = "../phase-2-task-slms/exports"
    validate_adapters: bool = True
    required_files: list[str] = Field(
        default_factory=lambda: [
            "adapter_config.json",
        ]
    )


class ExportConfig(BaseModel):
    """Phase 4 export configuration."""

    generate_agent_configs: bool = True
    generate_routing_embeddings: bool = True
    embedding_model: str = "BAAI/bge-base-en-v1.5"
    export_format: str = "safetensors"
    embedding_timeout: int = Field(default=300, description="Timeout in seconds for embedding model download")


class PathsConfig(BaseModel):
    """Path configuration."""

    data_dir: Path = Path("data")
    imports_dir: Path = Path("data/imports")
    configs_dir: Path = Path("data/configs")
    merged_dir: Path = Path("data/merged")
    exports_dir: Path = Path("data/exports")


class TestModeConfig(BaseModel):
    """Test mode configuration for quick validation."""

    num_experts_per_unit: int = 2  # 2 mock experts per unit
    mock_base_model: str = "HuggingFaceTB/SmolLM-135M"
    skip_actual_merge: bool = True
    generate_mock_exports: bool = True


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    format: Literal["json", "text"] = "json"


class FineTuneConfig(BaseModel):
    """Optional MoE fine-tuning configuration (per-unit)."""

    enabled: bool = False
    epochs: int = 2
    batch_size: int = 4
    learning_rate: float = 1e-5
    lora_r: int = 8
    lora_alpha: int = 16
    max_samples: int = 1000


class InterfaceGradioConfig(BaseModel):
    """Gradio interface configuration."""

    host: str = "0.0.0.0"
    port: int = 7861
    share: bool = False
    title: str = "Phase 3 MoE Staff Interface"
    description: str = "Interact with organizational unit MoE models"


class GenerationConfig(BaseModel):
    """Text generation configuration."""

    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9


class InterfaceFeedbackConfig(BaseModel):
    """Interface feedback collection configuration."""

    enabled: bool = True
    feedback_dir: str = "data/feedback"


class InterfaceConfig(BaseModel):
    """Staff interface configuration."""

    gradio: InterfaceGradioConfig = Field(default_factory=InterfaceGradioConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    feedback: InterfaceFeedbackConfig = Field(default_factory=InterfaceFeedbackConfig)


class ExpertDefinition(BaseModel):
    """Definition of a single expert in a unit's MoE."""

    model_config = {"protected_namespaces": ()}

    model_id: str
    unit_id: str
    task_id: str
    source_model: str
    positive_prompts: list[str] = Field(default_factory=list)
    negative_prompts: list[str] = Field(default_factory=list)


class Settings(HabitatBaseSettings):
    """Main settings class combining all configurations."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=(),
    )

    # Environment variables
    hf_token: str | None = Field(default=None, alias="HF_TOKEN")
    hf_home: str | None = Field(default=None, alias="HF_HOME")
    # test_mode and log_level inherited from HabitatBaseSettings

    # Nested configurations (loaded from YAML)
    moe: MoEArchitectureConfig = Field(default_factory=MoEArchitectureConfig)
    units: dict[str, UnitDefinition] = Field(default_factory=dict)
    merge: MergeConfig = Field(default_factory=MergeConfig)
    import_config: ImportConfig = Field(default_factory=ImportConfig)
    export_config: ExportConfig = Field(default_factory=ExportConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    test_mode_config: TestModeConfig = Field(default_factory=TestModeConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    finetune: FineTuneConfig = Field(default_factory=FineTuneConfig)
    interface: InterfaceConfig = Field(default_factory=InterfaceConfig)

    @classmethod
    def from_yaml(cls, config_path: str | Path) -> "Settings":
        """Load settings from YAML configuration file."""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path) as f:
            config_data = yaml.safe_load(f)

        # Map YAML keys to Pydantic field names
        if "test_mode" in config_data and isinstance(config_data["test_mode"], dict):
            config_data["test_mode_config"] = config_data.pop("test_mode")

        # Convert units dict to UnitDefinition objects
        if "units" in config_data:
            units_dict = {}
            for unit_id, unit_data in config_data["units"].items():
                units_dict[unit_id] = UnitDefinition(**unit_data)
            config_data["units"] = units_dict

        return cls(**config_data)

    def get_unit_ids(self) -> list[str]:
        """Get list of unit IDs."""
        return list(self.units.keys())

    def get_unit(self, unit_id: str) -> UnitDefinition | None:
        """Get unit definition by ID."""
        return self.units.get(unit_id)

    def get_tasks_for_unit(self, unit_id: str) -> list[str]:
        """Get task list for a unit."""
        unit = self.units.get(unit_id)
        return unit.tasks if unit else []

    def get_base_model_for_merge(self) -> str:
        """Get base model path for merging."""
        if self.test_mode:
            return self.test_mode_config.mock_base_model
        return ""  # Will be determined from imported adapters

    def resolve_path(self, path: Path) -> Path:
        """Resolve a path relative to the project root."""
        if path.is_absolute():
            return path
        return Path(__file__).parent.parent / path


def get_settings(config_path: str | Path | None = None) -> Settings:
    """Get settings instance, optionally loading from YAML."""
    if config_path:
        return Settings.from_yaml(config_path)
    return Settings()
