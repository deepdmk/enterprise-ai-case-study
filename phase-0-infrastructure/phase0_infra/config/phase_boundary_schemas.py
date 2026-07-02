"""Pydantic schemas for validating data at phase boundaries.

These schemas define the contracts between phases, ensuring that
exports from one phase match the expected imports of the next phase.

Phase boundaries:
- Phase 2 → Phase 3: Task SLM adapters (LoRA weights + configs)
- Phase 3 → Phase 4: MoE model packages (agent configs + routing metadata)
- Phase 4 → Phase 5: Discovery logs (training data + summaries)
"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

# --- Phase 2 → Phase 3: Task SLM Adapter Export ---


class AdapterExport(BaseModel):
    """Schema for a single Task SLM adapter exported from Phase 2."""

    unit_id: str = Field(description="Organizational unit ID (e.g., 'fundraising')")
    task_id: str = Field(description="Task ID (e.g., 'investor_profiling')")
    base_model: str = Field(description="Base model used for fine-tuning")
    adapter_path: str = Field(description="Path to adapter weights directory")
    lora_config: dict[str, Any] = Field(description="LoRA configuration used")

    @field_validator("adapter_path")
    @classmethod
    def validate_adapter_path(cls, v: str) -> str:
        path = Path(v)
        if path.exists() and not (path / "adapter_config.json").exists():
            raise ValueError(f"adapter_config.json not found in {v}")
        return v


class Phase2ExportManifest(BaseModel):
    """Schema for the complete Phase 2 export manifest."""

    phase: int = Field(default=2, description="Source phase number")
    adapters: list[AdapterExport] = Field(description="List of exported adapters")
    base_model: str = Field(description="Common base model for all adapters")
    total_adapters: int = Field(description="Total number of adapters exported")

    @field_validator("total_adapters")
    @classmethod
    def validate_count(cls, v: int, info) -> int:
        # Only skip when "adapters" itself failed validation (absent from
        # info.data) — an empty list must still be checked.
        if "adapters" in info.data:
            adapters = info.data["adapters"]
            if v != len(adapters):
                raise ValueError(
                    f"total_adapters ({v}) doesn't match adapters list length ({len(adapters)})"
                )
        return v


# --- Phase 3 → Phase 4: MoE Agent Config Export ---


class ExpertInfo(BaseModel):
    """Schema for a single expert in the MoE model."""

    expert_id: int = Field(ge=0, description="Expert index")
    task_id: str = Field(description="Task this expert was trained on")
    positive_prompts: list[str] = Field(default_factory=list, description="Routing prompts")


class AgentModelConfig(BaseModel):
    """Schema for agent model configuration exported from Phase 3."""

    type: str = Field(default="moe", description="Model type")
    architecture: str = Field(default="mixtral", description="MoE architecture")
    path: str = Field(description="Path to model files")
    num_experts: int | None = Field(default=None, ge=1, description="Number of experts in MoE")
    experts_per_token: int | None = Field(default=None, ge=1, le=8, description="Experts activated per token")
    experts: list[ExpertInfo] = Field(default_factory=list, description="Expert configurations")


class AgentRoutingConfig(BaseModel):
    """Schema for agent routing configuration."""

    method: str = Field(default="semantic", description="Routing method")
    gate_mode: str = Field(default="hidden", description="Gate mode for MoE routing")
    embedding_model: str = Field(description="Embedding model for semantic routing")


class Phase3AgentExport(BaseModel):
    """Schema for a single agent package exported from Phase 3."""

    agent: dict[str, str] = Field(description="Agent identity (id, name, description)")
    model: AgentModelConfig = Field(description="Model configuration")
    routing: AgentRoutingConfig = Field(description="Routing configuration")
    tasks: list[str] = Field(description="Task IDs this agent handles")


# --- Phase 4 → Phase 5: Discovery Data Export ---


class CallSequenceEntry(BaseModel):
    """Schema for a single entry in a call sequence."""

    depth: int = Field(ge=0, description="Call depth level")
    target: str = Field(description="Target agent ID")
    goal: str = Field(description="Goal/query for this call")
    status: str | None = Field(default=None, description="Call status")
    execution_time_ms: int | None = Field(default=None, description="Execution time")


class Phase4TrainingExample(BaseModel):
    """Schema for a single training example from Phase 4 discovery."""

    query: str = Field(min_length=1, description="User query")
    entry_agent: str = Field(description="Entry agent ID (e.g., 'fundraising-agent')")
    optimal_depth: int = Field(ge=1, le=4, description="Optimal cascade depth")
    call_sequence: list[dict[str, Any]] = Field(
        default_factory=list, description="Actual call sequence"
    )
    final_response: str = Field(default="", description="Final response")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("entry_agent")
    @classmethod
    def validate_agent_name(cls, v: str) -> str:
        valid_agents = {
            "fundraising-agent",
            "business-development-agent",
            "field-operations-agent",
        }
        if v not in valid_agents:
            raise ValueError(f"Unknown agent: '{v}'. Valid agents: {valid_agents}")
        return v


class WorkflowStats(BaseModel):
    """Schema for workflow statistics in Phase 5 summary."""

    total_calls: int = Field(ge=0, description="Total calls for this workflow")
    avg_depth: float = Field(ge=0, description="Average cascade depth")
    success_rate: float = Field(ge=0.0, le=1.0, description="Success rate")
    avg_latency_ms: float = Field(ge=0, description="Average latency")


class Phase4ExportSummary(BaseModel):
    """Schema for the Phase 5 summary file exported from Phase 4."""

    optimal_depths: dict[str, int] = Field(
        default_factory=dict, description="Mapping of workflow_id to optimal depth"
    )
    workflows: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Workflow statistics"
    )


class Phase4ExportBundle(BaseModel):
    """Schema for the complete Phase 4 export bundle."""

    training_examples: list[Phase4TrainingExample] = Field(description="Training examples")
    summary: Phase4ExportSummary = Field(description="Discovery summary")
    total_examples: int = Field(ge=0, description="Total training examples")

    @field_validator("total_examples")
    @classmethod
    def validate_count(cls, v: int, info) -> int:
        # Only skip when "training_examples" itself failed validation
        # (absent from info.data) — an empty list must still be checked.
        if "training_examples" in info.data:
            examples = info.data["training_examples"]
            if v != len(examples):
                raise ValueError(
                    f"total_examples ({v}) doesn't match training_examples length ({len(examples)})"
                )
        return v


# --- Validation helpers ---


class SchemaValidationResult(BaseModel):
    """Result of schema validation.

    Distinct from ``registries.schemas.ValidationResult`` (a mutable
    dataclass used for dataset path validation) — this model reports the
    outcome of validating records against phase-boundary schemas.
    """

    valid: bool = Field(description="Whether validation passed")
    errors: list[str] = Field(default_factory=list, description="Validation errors")
    warnings: list[str] = Field(default_factory=list, description="Validation warnings")
    records_validated: int = Field(default=0, description="Number of records validated")
    records_skipped: int = Field(default=0, description="Number of records skipped")


def validate_phase4_training_examples(
    examples: list[dict[str, Any]],
) -> tuple[list[Phase4TrainingExample], SchemaValidationResult]:
    """Validate Phase 4 training examples against the schema.

    Args:
        examples: Raw training examples from Phase 4 export

    Returns:
        Tuple of (validated examples, validation result)
    """
    validated = []
    errors = []
    skipped = 0

    for i, raw in enumerate(examples):
        try:
            example = Phase4TrainingExample(**raw)
            validated.append(example)
        except Exception as e:
            errors.append(f"Example {i}: {e}")
            skipped += 1

    result = SchemaValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        records_validated=len(validated),
        records_skipped=skipped,
    )

    return validated, result
