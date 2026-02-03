"""Shared modules for Phase 2 Task SLMs."""

from src.shared.data_formatter import (
    DataFormatter,
    create_conversation_dataset,
    format_chatml,
    format_conversation,
    format_for_training,
    load_jsonl,
    save_jsonl,
    split_dataset,
)
from src.shared.embedding_bridge import EmbeddingBridge
from src.shared.environment_detector import (
    ComputeEnvironment,
    EnvironmentInfo,
    detect_environment,
    get_device,
    get_dtype,
    print_environment_info,
)
from src.shared.mock_data_generator import (
    MockDataGenerator,
    generate_mock_dataset,
    generate_mock_example,
)
from src.shared.model_loader import ModelLoader
from src.shared.model_registry import (
    ModelEntry,
    ModelMetrics,
    ModelRegistry,
    TrainingConfig,
)

__all__ = [
    # Environment
    "ComputeEnvironment",
    "EnvironmentInfo",
    "detect_environment",
    "get_device",
    "get_dtype",
    "print_environment_info",
    # Model loading
    "ModelLoader",
    # Data formatting
    "DataFormatter",
    "format_chatml",
    "format_conversation",
    "format_for_training",
    "create_conversation_dataset",
    "load_jsonl",
    "save_jsonl",
    "split_dataset",
    # Mock data
    "MockDataGenerator",
    "generate_mock_dataset",
    "generate_mock_example",
    # Registry
    "ModelRegistry",
    "ModelEntry",
    "ModelMetrics",
    "TrainingConfig",
    # Phase 1 integration
    "EmbeddingBridge",
]
