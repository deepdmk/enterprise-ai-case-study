"""
Agno Framework Integration for Phase 5 Orchestrator

This module implements the Agno framework integration, replacing the custom
routing engine with Agno's Team coordination mode.

Components:
- model_provider: Built-in VLLM model provider for fine-tuned SLM inference
- members: RemoteAgent wrappers for Phase 4 A2A agents
- coordinator: Coordinator agent configuration and instructions
- team: Team orchestration setup
- legacy_adapter: Adapts Agno responses to legacy API format
- agui_interface: Optional AG-UI streaming interface
- training_logger: Captures interaction data for future fine-tuning
"""

from .model_provider import create_vllm_model
from .members import (
    create_fundraising_member,
    create_business_dev_member,
    create_field_ops_member,
    create_all_members
)
from .coordinator import create_coordinator_instructions
from .team import create_orchestrator_team
from .legacy_adapter import LegacyAdapter
from .agui_interface import create_agui_interface
from .training_logger import TrainingLogger

__all__ = [
    # Model Provider
    "create_vllm_model",

    # Members
    "create_fundraising_member",
    "create_business_dev_member",
    "create_field_ops_member",
    "create_all_members",

    # Coordinator
    "create_coordinator_instructions",

    # Team
    "create_orchestrator_team",

    # Adapters
    "LegacyAdapter",

    # AG-UI
    "create_agui_interface",

    # Training
    "TrainingLogger"
]
