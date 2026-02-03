# Phase-0 Metrics Schema Integration

## Overview

Phase-2 evaluation metrics have been integrated with phase-0-infrastructure standardized schemas to enable cross-phase comparison and analysis.

## Key Changes

### 1. Metrics Mapping

Phase-2 metrics are mapped to phase-0 schemas as follows:

| Phase-2 Metric | Phase-0 Schema | Field |
|----------------|----------------|-------|
| `format_compliance` | `QualityMetrics` | `format_compliance` |
| `content_coverage` | `QualityMetrics` | `content_coverage` |
| `latency_ms` | `LoadMetrics` | `latency_ms` |
| `tokens_generated` | `TokenMetrics` | `output_tokens` |
| `tokens_per_second` | `TokenMetrics` | `tokens_per_second` |

### 2. New Conversion Methods

#### EvaluationResult
- `to_phase0_token_metrics()`: Converts to `TokenMetrics` schema
- `to_phase0_load_metrics()`: Converts to `LoadMetrics` schema
- `to_phase0_quality_metrics()`: Converts to `QualityMetrics` schema

#### EvaluationReport
- `to_phase0_report()`: Converts entire report to `EvaluationReport` schema

### 3. Report Generation

A new `Phase0Reporter` class generates standardized reports:

```python
from src.program3_evaluation.reporters.report_generator import generate_evaluation_report

# Generate all formats including phase-0
report_paths = generate_evaluation_report(
    report,
    output_dir,
    formats=["json", "md", "phase0"],  # phase0 now included by default
    dataset_id="unit_id/task_id_eval_set",
)
```

## Usage Examples

### Basic Evaluation with Phase-0 Export

```python
from src.program3_evaluation.evaluators.metrics import TaskSLMEvaluator

# Run evaluation as normal
evaluator = TaskSLMEvaluator(model, tokenizer)
report = evaluator.evaluate_batch(examples)

# Convert to phase-0 format
phase0_report = report.to_phase0_report(
    report_id="eval_20260117_001",
    dataset_id="fundraising/portfolio_analysis_eval",
)

# Access standardized metrics
print(f"Format Compliance: {phase0_report.quality_metrics.format_compliance}")
print(f"Latency: {phase0_report.load_metrics.latency_ms}ms")
print(f"Tokens/sec: {phase0_report.token_metrics.tokens_per_second}")
```

### Individual Result Conversion

```python
# Convert individual evaluation result
result = evaluator.evaluate_single(input_text, expected_output)

# Get standardized metrics
token_metrics = result.to_phase0_token_metrics()
load_metrics = result.to_phase0_load_metrics()
quality_metrics = result.to_phase0_quality_metrics()
```

### Command Line Usage

```bash
# Evaluation now automatically generates phase-0 reports
python -m src.program3_evaluation.main \
    --unit fundraising \
    --task portfolio_analysis

# Output includes:
# - evaluation_report.json (phase-2 format)
# - evaluation_report.md (markdown)
# - evaluation_report_phase0.json (phase-0 standardized format)
```

## Schema Compatibility

### Phase-0 Fields Used
- **TokenMetrics**: All fields populated (input/output tokens, total, tokens_per_second)
- **LoadMetrics**: `latency_ms` only (memory/GPU metrics not tracked in phase-2)
- **QualityMetrics**: `format_compliance`, `content_coverage` (factual_accuracy/relevance not tracked)
- **EvaluationReport**: Full schema with sample outputs

### Phase-2 Specific Data
Phase-2 specific data (section_coverage, section_scores) is preserved in:
- The `notes` field of EvaluationReport
- The `sample_outputs` field with custom structure

### Backward Compatibility
All existing phase-2 code continues to work:
- Original `EvaluationResult` and `EvaluationReport` dataclasses unchanged
- All existing methods and attributes preserved
- Conversion to phase-0 is optional via `.to_phase0_*()` methods

## Cross-Phase Comparison

Phase-0 standardized reports enable comparison across phases:

```python
# Compare phase-2 Task SLM with phase-3 MoE
from evaluation.metrics_schema import EvaluationReport

# Load reports
phase2_report = EvaluationReport.model_validate_json(
    Path("evaluations/phase2_eval.json").read_text()
)
phase3_report = EvaluationReport.model_validate_json(
    Path("evaluations/phase3_eval.json").read_text()
)

# Compare using standardized metrics
print(f"Phase-2 Quality: {phase2_report.quality_metrics.format_compliance}")
print(f"Phase-3 Quality: {phase3_report.quality_metrics.format_compliance}")
print(f"Latency Delta: {phase3_report.load_metrics.latency_ms - phase2_report.load_metrics.latency_ms}ms")
```

## Data Flow

```
┌─────────────────────┐
│  TaskSLMEvaluator   │
│  (evaluate_batch)   │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  EvaluationReport   │
│  (Phase-2 format)   │
└──────────┬──────────┘
           │
           ├─→ JSONReporter → evaluation_report.json
           ├─→ MarkdownReporter → evaluation_report.md
           └─→ Phase0Reporter → evaluation_report_phase0.json
                      │
                      v
           ┌──────────────────────┐
           │ Phase0               │
           │ EvaluationReport     │
           │ (Standardized)       │
           └──────────────────────┘
```

## Notes

- **Input Token Estimation**: Phase-2 doesn't track input tokens separately. We estimate using `len(input_text) // 4` (rough approximation: 1 token ≈ 4 chars). For more accurate tracking, consider using the tokenizer to count actual input tokens.

- **Missing Metrics**: Some phase-0 metrics are not tracked in phase-2:
  - `CostMetrics`: Not applicable for local inference
  - `LoadMetrics.memory_mb/gpu_utilization`: Not currently tracked
  - `QualityMetrics.factual_accuracy/relevance_score`: Not evaluated in phase-2

- **Report IDs**: Auto-generated as `phase2_eval_{random_8_chars}` if not provided. For production use, provide explicit IDs for tracking.

## Future Enhancements

1. **Enhanced Token Tracking**: Use tokenizer for accurate input token counts
2. **Resource Monitoring**: Add GPU utilization and memory tracking
3. **Quality Metrics**: Add factual accuracy evaluation (requires ground truth)
4. **Cost Estimation**: Optional cost calculation based on token counts
