"""Environment detector for determining available compute resources."""

import os
import platform
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Import from Phase 0
from habitat_logging import get_logger

logger = get_logger(__name__)


class ComputeEnvironment(Enum):
    """Available compute environments."""

    COLAB_GPU = "colab_gpu"
    LINUX_CUDA = "linux_cuda"
    MAC_MPS = "mac_mps"
    CPU_ONLY = "cpu_only"


@dataclass
class EnvironmentInfo:
    """Information about the detected environment."""

    environment: ComputeEnvironment
    is_colab: bool
    has_cuda: bool
    has_mps: bool
    cuda_version: str | None
    gpu_name: str | None
    gpu_memory_gb: float | None
    can_use_unsloth: bool
    recommended_backend: str
    platform: str
    python_version: str


def detect_colab() -> bool:
    """Detect if running in Google Colab."""
    try:
        import google.colab  # noqa: F401

        return True
    except ImportError:
        return False


def detect_cuda() -> tuple[bool, str | None, str | None, float | None]:
    """Detect CUDA availability and GPU info."""
    try:
        import torch

        if torch.cuda.is_available():
            cuda_version = torch.version.cuda
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            return True, cuda_version, gpu_name, gpu_memory_gb
    except ImportError:
        pass
    return False, None, None, None


def detect_mps() -> bool:
    """Detect Apple MPS availability."""
    try:
        import torch

        return bool(torch.backends.mps.is_available())
    except (ImportError, AttributeError):
        return False


def check_unsloth_available() -> bool:
    """Check if Unsloth can be imported."""
    try:
        import unsloth  # noqa: F401

        return True
    except ImportError:
        return False


def detect_environment() -> EnvironmentInfo:
    """Detect the current compute environment and capabilities."""
    is_colab = detect_colab()
    has_cuda, cuda_version, gpu_name, gpu_memory = detect_cuda()
    has_mps = detect_mps()

    # Determine environment type
    if is_colab and has_cuda:
        env = ComputeEnvironment.COLAB_GPU
    elif has_cuda:
        env = ComputeEnvironment.LINUX_CUDA
    elif has_mps:
        env = ComputeEnvironment.MAC_MPS
    else:
        env = ComputeEnvironment.CPU_ONLY

    # Unsloth requires Linux + CUDA
    can_use_unsloth = has_cuda and platform.system() == "Linux"
    if is_colab:
        can_use_unsloth = has_cuda

    # Determine recommended backend
    if can_use_unsloth:
        recommended_backend = "unsloth"
    elif has_cuda or has_mps:
        recommended_backend = "transformers"
    else:
        recommended_backend = "transformers_cpu"

    info = EnvironmentInfo(
        environment=env,
        is_colab=is_colab,
        has_cuda=has_cuda,
        has_mps=has_mps,
        cuda_version=cuda_version,
        gpu_name=gpu_name,
        gpu_memory_gb=gpu_memory,
        can_use_unsloth=can_use_unsloth,
        recommended_backend=recommended_backend,
        platform=platform.system(),
        python_version=platform.python_version(),
    )

    logger.info(
        "environment_detected",
        environment=env.value,
        can_use_unsloth=can_use_unsloth,
        recommended_backend=recommended_backend,
        gpu_name=gpu_name,
    )

    return info


def get_device() -> str:
    """Get the appropriate torch device string."""
    env = detect_environment()
    if env.has_cuda:
        return "cuda"
    elif env.has_mps:
        return "mps"
    return "cpu"


def get_dtype() -> Any:
    """Get the appropriate dtype for the environment."""
    import torch

    env = detect_environment()
    if env.has_cuda:
        return torch.float16
    elif env.has_mps:
        return torch.float32  # MPS has limited float16 support
    return torch.float32


def print_environment_info() -> None:
    """Print formatted environment information."""
    info = detect_environment()

    print("\n" + "=" * 60)
    print("Environment Detection Results")
    print("=" * 60)
    print(f"Platform:           {info.platform}")
    print(f"Python:             {info.python_version}")
    print(f"Environment:        {info.environment.value}")
    print(f"Is Colab:           {info.is_colab}")
    print(f"Has CUDA:           {info.has_cuda}")
    if info.has_cuda:
        print(f"  CUDA Version:     {info.cuda_version}")
        print(f"  GPU:              {info.gpu_name}")
        print(f"  GPU Memory:       {info.gpu_memory_gb:.1f} GB")
    print(f"Has MPS:            {info.has_mps}")
    print(f"Can Use Unsloth:    {info.can_use_unsloth}")
    print(f"Recommended Backend: {info.recommended_backend}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    print_environment_info()
