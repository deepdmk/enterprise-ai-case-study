"""Shared modules for Phase 2 Task SLMs.

This module provides lazy loading to avoid heavy import dependencies when
only a subset of functionality is needed. Use direct imports from submodules
when working with specific features.

Example:
    # For lightweight operations (no ML dependencies):
    from src.shared.path_config import configure_paths

    # For full functionality:
    from src.shared import ModelLoader, DataFormatter
"""


def __getattr__(name: str):
    """Lazy loading of module exports to avoid heavy imports at package init."""
    # Data formatting
    if name in (
        "DataFormatter",
        "create_conversation_dataset",
        "format_chatml",
        "format_conversation",
        "format_for_training",
        "load_jsonl",
        "save_jsonl",
        "split_dataset",
    ):
        from src.shared import data_formatter
        return getattr(data_formatter, name)

    # Environment detection
    if name in (
        "ComputeEnvironment",
        "EnvironmentInfo",
        "detect_environment",
        "get_device",
        "get_dtype",
        "print_environment_info",
    ):
        from src.shared import environment_detector
        return getattr(environment_detector, name)

    # Model loading
    if name == "ModelLoader":
        from src.shared.model_loader import ModelLoader
        return ModelLoader

    # Mock data generation
    if name in ("MockDataGenerator", "generate_mock_dataset", "generate_mock_example"):
        from src.shared import mock_data_generator
        return getattr(mock_data_generator, name)

    # Model registry
    if name in ("ModelRegistry", "ModelEntry", "ModelMetrics", "TrainingConfig"):
        from src.shared import model_registry
        return getattr(model_registry, name)

    # Phase 1 integration
    if name == "EmbeddingBridge":
        from src.shared.embedding_bridge import EmbeddingBridge
        return EmbeddingBridge

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


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
