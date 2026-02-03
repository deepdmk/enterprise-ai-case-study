"""
Evaluation metrics and reporting infrastructure.

This module provides standardized schemas for capturing evaluation metrics:
- Token usage metrics
- Cost metrics
- Performance and load metrics
- Quality assessment metrics
- Comprehensive evaluation reports

Basic usage:
    >>> from phase_0_infrastructure.evaluation import TokenMetrics, QualityMetrics, EvaluationReport
    >>>
    >>> # Create token metrics
    >>> token_metrics = TokenMetrics(
    ...     input_tokens=1000,
    ...     output_tokens=500,
    ...     total_tokens=1500,
    ...     tokens_per_second=50.0,
    ... )
    >>>
    >>> # Create quality metrics
    >>> quality_metrics = QualityMetrics(
    ...     format_compliance=0.95,
    ...     content_coverage=0.88,
    ...     factual_accuracy=0.92,
    ... )
    >>>
    >>> # Create evaluation report
    >>> report = EvaluationReport(
    ...     report_id="eval_001",
    ...     model_id="llama-3.1-8b-instruct",
    ...     token_metrics=token_metrics,
    ...     quality_metrics=quality_metrics,
    ... )
"""

from .metrics_schema import (
    TokenMetrics,
    CostMetrics,
    LoadMetrics,
    QualityMetrics,
    EvaluationReport,
)

__all__ = [
    "TokenMetrics",
    "CostMetrics",
    "LoadMetrics",
    "QualityMetrics",
    "EvaluationReport",
]
