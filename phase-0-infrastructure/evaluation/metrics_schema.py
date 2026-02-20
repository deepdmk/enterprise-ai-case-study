"""
Pydantic models for evaluation metrics.

This module defines the schema for capturing various metrics during model evaluation,
including token usage, costs, performance load, and quality assessments.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class TokenMetrics(BaseModel):
    """Metrics related to token usage during evaluation."""

    input_tokens: int = Field(..., ge=0, description="Number of input tokens processed")
    output_tokens: int = Field(..., ge=0, description="Number of output tokens generated")
    total_tokens: int = Field(..., ge=0, description="Total number of tokens (input + output)")
    tokens_per_second: float | None = Field(
        None, ge=0, description="Token generation rate in tokens per second"
    )

    @field_validator("total_tokens")
    @classmethod
    def validate_total_tokens(cls, v: int, info: ValidationInfo) -> int:
        """Ensure total_tokens matches input_tokens + output_tokens if both are present."""
        if info.data:
            input_tokens = info.data.get("input_tokens", 0)
            output_tokens = info.data.get("output_tokens", 0)
            expected_total = input_tokens + output_tokens
            if v != expected_total:
                raise ValueError(
                    f"total_tokens ({v}) must equal input_tokens ({input_tokens}) + "
                    f"output_tokens ({output_tokens})"
                )
        return v


class CostMetrics(BaseModel):
    """Metrics related to the cost of evaluation."""

    input_cost: float = Field(..., ge=0, description="Cost for processing input tokens")
    output_cost: float = Field(..., ge=0, description="Cost for generating output tokens")
    total_cost: float = Field(..., ge=0, description="Total cost (input + output)")
    currency: str = Field(default="USD", description="Currency code for costs")

    @field_validator("total_cost")
    @classmethod
    def validate_total_cost(cls, v: float, info: ValidationInfo) -> float:
        """Ensure total_cost matches input_cost + output_cost if both are present."""
        if info.data:
            input_cost = info.data.get("input_cost", 0.0)
            output_cost = info.data.get("output_cost", 0.0)
            expected_total = input_cost + output_cost
            # Allow for small floating point errors
            if abs(v - expected_total) > 0.0001:
                raise ValueError(
                    f"total_cost ({v}) must equal input_cost ({input_cost}) + "
                    f"output_cost ({output_cost})"
                )
        return v


class LoadMetrics(BaseModel):
    """Metrics related to system performance and resource utilization."""

    latency_ms: float = Field(..., ge=0, description="Response latency in milliseconds")
    throughput_rps: float | None = Field(
        None, ge=0, description="Throughput in requests per second"
    )
    memory_mb: float | None = Field(
        None, ge=0, description="Memory usage in megabytes"
    )
    gpu_utilization: float | None = Field(
        None, ge=0, le=1, description="GPU utilization as a fraction (0-1)"
    )


class QualityMetrics(BaseModel):
    """Metrics related to output quality and correctness."""

    format_compliance: float = Field(
        ..., ge=0, le=1, description="Format compliance score (0-1)"
    )
    content_coverage: float = Field(
        ..., ge=0, le=1, description="Content coverage score (0-1)"
    )
    factual_accuracy: float | None = Field(
        None, ge=0, le=1, description="Factual accuracy score (0-1)"
    )
    relevance_score: float | None = Field(
        None, ge=0, le=1, description="Relevance score (0-1)"
    )
    human_preference_score: float | None = Field(
        None, ge=0, le=1, description="Human preference score (0-1)"
    )


class EvaluationReport(BaseModel):
    """Comprehensive evaluation report for a model."""

    report_id: str = Field(..., description="Unique identifier for this evaluation report")
    model_id: str = Field(..., description="Identifier for the model being evaluated")
    dataset_id: str | None = Field(
        None, description="Identifier for the dataset used in evaluation"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the report was created",
    )
    token_metrics: TokenMetrics | None = Field(
        None, description="Token usage metrics"
    )
    cost_metrics: CostMetrics | None = Field(
        None, description="Cost metrics"
    )
    load_metrics: LoadMetrics | None = Field(
        None, description="Performance and load metrics"
    )
    quality_metrics: QualityMetrics | None = Field(
        None, description="Quality assessment metrics"
    )
    sample_outputs: list[dict[str, Any]] | None = Field(
        None, description="Sample outputs from the evaluation"
    )
    notes: str | None = Field(
        None, description="Additional notes or observations about the evaluation"
    )
    schema_version: str = Field(
        default="1.0", description="Schema version for this report format"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "report_id": "eval_20260117_001",
                    "model_id": "llama-3.1-8b-instruct",
                    "dataset_id": "medical_qa_v1",
                    "created_at": "2026-01-17T12:00:00Z",
                    "token_metrics": {
                        "input_tokens": 1000,
                        "output_tokens": 500,
                        "total_tokens": 1500,
                        "tokens_per_second": 50.0,
                    },
                    "cost_metrics": {
                        "input_cost": 0.001,
                        "output_cost": 0.002,
                        "total_cost": 0.003,
                        "currency": "USD",
                    },
                    "load_metrics": {
                        "latency_ms": 250.5,
                        "throughput_rps": 4.0,
                        "memory_mb": 2048.0,
                        "gpu_utilization": 0.75,
                    },
                    "quality_metrics": {
                        "format_compliance": 0.95,
                        "content_coverage": 0.88,
                        "factual_accuracy": 0.92,
                        "relevance_score": 0.90,
                    },
                    "sample_outputs": [
                        {
                            "input": "What is the treatment for diabetes?",
                            "output": "Treatment typically includes lifestyle changes...",
                            "score": 0.9,
                        }
                    ],
                    "notes": "Evaluation performed on single GPU setup",
                    "schema_version": "1.0",
                }
            ]
        }
    }
