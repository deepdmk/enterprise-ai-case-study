# Phase-2 to Phase-0 Schema Mapping Quick Reference

## Metric Mappings

### EvaluationResult → Phase-0 Schemas

```python
result = EvaluationResult(...)

# TokenMetrics
token_metrics = result.to_phase0_token_metrics()
# - input_tokens: estimated from len(input_text) // 4
# - output_tokens: result.tokens_generated
# - total_tokens: input_tokens + output_tokens
# - tokens_per_second: result.tokens_per_second

# LoadMetrics
load_metrics = result.to_phase0_load_metrics()
# - latency_ms: result.latency_ms
# - throughput_rps: None
# - memory_mb: None
# - gpu_utilization: None

# QualityMetrics
quality_metrics = result.to_phase0_quality_metrics()
# - format_compliance: result.format_compliance
# - content_coverage: result.content_coverage
# - factual_accuracy: None
# - relevance_score: None
# - human_preference_score: None
```

### EvaluationReport → Phase-0 Report

```python
report = EvaluationReport(...)

phase0_report = report.to_phase0_report(
    report_id="eval_001",  # Auto-generated if None
    dataset_id="unit/task_eval_set"
)

# Aggregated metrics from all results:
# - token_metrics: Sum of all tokens, average tokens/sec
# - load_metrics: Average latency
# - quality_metrics: Average format compliance & content coverage
# - sample_outputs: First 10 results with full details
# - notes: Section coverage + metadata
```

## Field Reference

### Phase-2 Fields → Phase-0 Location

| Phase-2 Field | Phase-0 Schema.Field | Transformation |
|---------------|----------------------|----------------|
| `input_text` | `sample_outputs[i].input` | Truncated to 200 chars |
| `expected_output` | `sample_outputs[i].expected` | Truncated to 200 chars |
| `generated_output` | `sample_outputs[i].output` | Truncated to 500 chars |
| `format_compliance` | `quality_metrics.format_compliance` | Direct (0-1 float) |
| `content_coverage` | `quality_metrics.content_coverage` | Direct (0-1 float) |
| `latency_ms` | `load_metrics.latency_ms` | Direct (float) |
| `tokens_generated` | `token_metrics.output_tokens` | Direct (int) |
| `tokens_per_second` | `token_metrics.tokens_per_second` | Direct (float) |
| `section_scores` | `sample_outputs[i].section_scores` | Dict preserved |
| `errors` | `sample_outputs[i].errors` | List preserved |
| `section_coverage` | `notes` | Serialized to string |
| `metadata` | `notes` | Serialized to string |

### Phase-0 Only Fields (Not in Phase-2)

Set to `None` or omitted:

**TokenMetrics:**
- `input_tokens` - Estimated only

**LoadMetrics:**
- `throughput_rps`
- `memory_mb`
- `gpu_utilization`

**QualityMetrics:**
- `factual_accuracy`
- `relevance_score`
- `human_preference_score`

**CostMetrics:**
- Entire schema (not applicable)

**EvaluationReport:**
- `cost_metrics` - Set to None

## Code Examples

### Convert Single Result

```python
from src.program3_evaluation.evaluators.metrics import EvaluationResult

result = EvaluationResult(
    input_text="Analyze this portfolio",
    expected_output="Expected analysis",
    generated_output="Generated analysis with details",
    format_compliance=0.95,
    content_coverage=0.88,
    latency_ms=156.3,
    tokens_generated=42,
    tokens_per_second=268.7,
)

# Get phase-0 schemas
tokens = result.to_phase0_token_metrics()
load = result.to_phase0_load_metrics()
quality = result.to_phase0_quality_metrics()

print(f"Tokens: {tokens.total_tokens}")
print(f"Latency: {load.latency_ms}ms")
print(f"Quality: {quality.format_compliance:.1%}")
```

### Convert Full Report

```python
from src.program3_evaluation.evaluators.metrics import EvaluationReport

report = EvaluationReport(
    model_id="unit/task_v1",
    num_samples=100,
    avg_format_compliance=0.92,
    avg_content_coverage=0.89,
    avg_latency_ms=170.0,
    avg_tokens_per_second=262.5,
    section_coverage={"intro": 0.95, "body": 0.88},
    results=[...],
)

# Convert to phase-0
phase0 = report.to_phase0_report(
    report_id="eval_20260117_001",
    dataset_id="unit/task_eval_v1",
)

# Access standardized fields
print(f"Report ID: {phase0.report_id}")
print(f"Model: {phase0.model_id}")
print(f"Dataset: {phase0.dataset_id}")
print(f"Quality: {phase0.quality_metrics.format_compliance:.1%}")
print(f"Latency: {phase0.load_metrics.latency_ms:.1f}ms")
```

### Generate Phase-0 Report

```python
from src.program3_evaluation.reporters.report_generator import Phase0Reporter

reporter = Phase0Reporter()
output_path = reporter.generate(
    report=report,
    output_path="evaluations/report_phase0.json",
    report_id="custom_eval_001",
    dataset_id="my_dataset_v1",
)

print(f"Phase-0 report saved to: {output_path}")
```

### Use in Evaluation Pipeline

```python
from src.program3_evaluation.reporters.report_generator import generate_evaluation_report

# Generate all formats including phase-0
paths = generate_evaluation_report(
    report=report,
    output_dir="evaluations/unit/model",
    formats=["json", "md", "phase0"],  # All three formats
    report_id="eval_001",
    dataset_id="unit/task_eval",
)

print(f"JSON: {paths['json']}")
print(f"Markdown: {paths['md']}")
print(f"Phase-0: {paths['phase0']}")  # Standardized format
```

## Validation

All phase-0 reports use Pydantic validation:

```python
from evaluation.metrics_schema import EvaluationReport as Phase0Report

# Load and validate
with open("evaluation_report_phase0.json") as f:
    report_data = json.load(f)

report = Phase0Report.model_validate(report_data)

# Automatic validation ensures:
# - total_tokens == input_tokens + output_tokens
# - All required fields present
# - Types match schema
# - Numeric constraints (e.g., 0 <= format_compliance <= 1)
```

## Schema Versions

**Current version**: `1.0`

Phase-0 reports include `schema_version` field for future compatibility:

```json
{
  "schema_version": "1.0",
  ...
}
```

When loading reports, check version:

```python
if report.schema_version != "1.0":
    print(f"Warning: Report uses schema version {report.schema_version}")
```

## Common Patterns

### Compare Two Reports

```python
from evaluation.metrics_schema import EvaluationReport

def compare_reports(report1: EvaluationReport, report2: EvaluationReport):
    """Compare two phase-0 reports."""
    print(f"\nModel 1: {report1.model_id}")
    print(f"Model 2: {report2.model_id}")

    quality1 = report1.quality_metrics.format_compliance
    quality2 = report2.quality_metrics.format_compliance
    print(f"Quality: {quality1:.1%} vs {quality2:.1%} ({quality2-quality1:+.1%})")

    latency1 = report1.load_metrics.latency_ms
    latency2 = report2.load_metrics.latency_ms
    print(f"Latency: {latency1:.1f}ms vs {latency2:.1f}ms ({latency2-latency1:+.1f}ms)")
```

### Extract Key Metrics

```python
def extract_metrics(report: EvaluationReport) -> dict:
    """Extract key metrics from phase-0 report."""
    return {
        "model": report.model_id,
        "quality": report.quality_metrics.format_compliance,
        "coverage": report.quality_metrics.content_coverage,
        "latency": report.load_metrics.latency_ms,
        "tokens_per_sec": report.token_metrics.tokens_per_second,
    }
```

### Aggregate Across Evaluations

```python
from pathlib import Path
from evaluation.metrics_schema import EvaluationReport

def aggregate_evaluations(eval_dir: Path) -> dict:
    """Aggregate metrics across multiple evaluations."""
    reports = []
    for path in eval_dir.glob("**/evaluation_report_phase0.json"):
        report = EvaluationReport.model_validate_json(path.read_text())
        reports.append(report)

    return {
        "count": len(reports),
        "avg_quality": sum(r.quality_metrics.format_compliance for r in reports) / len(reports),
        "avg_latency": sum(r.load_metrics.latency_ms for r in reports) / len(reports),
    }
```

## Tips

1. **Always provide dataset_id**: Helps track which evaluation set was used
2. **Use consistent report_id format**: Consider timestamp-based IDs
3. **Check sample_outputs**: Contains detailed per-result information
4. **Read notes field**: Contains phase-2 specific info (section coverage, metadata)
5. **Validate after loading**: Use Pydantic's validation for data integrity

## See Also

- Full integration guide: `PHASE0_INTEGRATION.md`
- Test examples: `test_phase0_integration.py`
- Phase-0 schema: `../../phase-0-infrastructure/evaluation/metrics_schema.py`
