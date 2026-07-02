"""Test script to validate phase-0 metrics integration."""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field

import pytest

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

from src.program3_evaluation.evaluators.metrics import EvaluationResult, EvaluationReport


@pytest.fixture
def phase0_report():
    """Fixture providing a phase0 report for testing."""
    results = [
        EvaluationResult(
            input_text=f"Sample input {i}",
            expected_output=f"Expected output {i}",
            generated_output=f"Generated output {i} with some content",
            format_compliance=0.90 + (i * 0.01),
            content_coverage=0.85 + (i * 0.02),
            latency_ms=150.0 + (i * 10),
            tokens_generated=40 + i,
            tokens_per_second=250.0 + (i * 5),
            section_scores={"section_1": True, "section_2": i % 2 == 0},
        )
        for i in range(5)
    ]

    report = EvaluationReport(
        model_id="fundraising/portfolio_analysis_v1",
        num_samples=5,
        avg_format_compliance=0.92,
        avg_content_coverage=0.89,
        avg_latency_ms=170.0,
        avg_tokens_per_second=262.5,
        section_coverage={"section_1": 1.0, "section_2": 0.6},
        results=results,
        metadata={"unit_id": "fundraising", "task_id": "portfolio_analysis"},
    )

    return report.to_phase0_report(
        report_id="test_eval_001",
        dataset_id="fundraising/portfolio_analysis_eval",
    )


def test_evaluation_result_conversion():
    """Test EvaluationResult conversion to phase-0 schemas."""
    print("\n" + "="*60)
    print("Test 1: EvaluationResult Conversion")
    print("="*60)

    # Create sample evaluation result
    result = EvaluationResult(
        input_text="What are the key benefits of SLMs?",
        expected_output="SLMs offer efficiency and specialization.",
        generated_output="Small Language Models (SLMs) provide several benefits:\n1. Efficiency: Lower compute requirements\n2. Specialization: Task-specific optimization\n3. Deployment: Easier to deploy on edge devices",
        format_compliance=0.95,
        content_coverage=0.88,
        latency_ms=156.3,
        tokens_generated=42,
        tokens_per_second=268.7,
        section_scores={"benefits": True, "examples": False},
        errors=[],
    )

    # Convert to phase-0 schemas
    token_metrics = result.to_phase0_token_metrics()
    load_metrics = result.to_phase0_load_metrics()
    quality_metrics = result.to_phase0_quality_metrics()

    print(f"\n✓ TokenMetrics:")
    print(f"  - Input tokens:    {token_metrics.input_tokens}")
    print(f"  - Output tokens:   {token_metrics.output_tokens}")
    print(f"  - Total tokens:    {token_metrics.total_tokens}")
    print(f"  - Tokens/second:   {token_metrics.tokens_per_second}")

    print(f"\n✓ LoadMetrics:")
    print(f"  - Latency:         {load_metrics.latency_ms} ms")

    print(f"\n✓ QualityMetrics:")
    print(f"  - Format compliance: {quality_metrics.format_compliance:.2%}")
    print(f"  - Content coverage:  {quality_metrics.content_coverage:.2%}")

    assert token_metrics.output_tokens == 42
    assert load_metrics.latency_ms == 156.3


def test_evaluation_report_conversion():
    """Test EvaluationReport conversion to phase-0 schema."""
    print("\n" + "="*60)
    print("Test 2: EvaluationReport Conversion")
    print("="*60)

    # Create sample results
    results = [
        EvaluationResult(
            input_text=f"Sample input {i}",
            expected_output=f"Expected output {i}",
            generated_output=f"Generated output {i} with some content",
            format_compliance=0.90 + (i * 0.01),
            content_coverage=0.85 + (i * 0.02),
            latency_ms=150.0 + (i * 10),
            tokens_generated=40 + i,
            tokens_per_second=250.0 + (i * 5),
            section_scores={"section_1": True, "section_2": i % 2 == 0},
        )
        for i in range(5)
    ]

    # Create report
    report = EvaluationReport(
        model_id="fundraising/portfolio_analysis_v1",
        num_samples=5,
        avg_format_compliance=0.92,
        avg_content_coverage=0.89,
        avg_latency_ms=170.0,
        avg_tokens_per_second=262.5,
        section_coverage={"section_1": 1.0, "section_2": 0.6},
        results=results,
        metadata={"unit_id": "fundraising", "task_id": "portfolio_analysis"},
    )

    # Convert to phase-0 format
    phase0_report = report.to_phase0_report(
        report_id="test_eval_001",
        dataset_id="fundraising/portfolio_analysis_eval",
    )

    print(f"\n✓ Report ID:       {phase0_report.report_id}")
    print(f"✓ Model ID:        {phase0_report.model_id}")
    print(f"✓ Dataset ID:      {phase0_report.dataset_id}")
    print(f"✓ Created at:      {phase0_report.created_at}")

    print(f"\n✓ Token Metrics:")
    print(f"  - Total tokens:   {phase0_report.token_metrics.total_tokens}")
    print(f"  - Tokens/second:  {phase0_report.token_metrics.tokens_per_second}")

    print(f"\n✓ Load Metrics:")
    print(f"  - Latency:        {phase0_report.load_metrics.latency_ms} ms")

    print(f"\n✓ Quality Metrics:")
    print(f"  - Format:         {phase0_report.quality_metrics.format_compliance:.2%}")
    print(f"  - Coverage:       {phase0_report.quality_metrics.content_coverage:.2%}")

    print(f"\n✓ Sample outputs:  {len(phase0_report.sample_outputs)} samples")

    assert phase0_report.report_id == "test_eval_001"
    assert phase0_report.model_id == "fundraising/portfolio_analysis_v1"


def test_json_serialization(phase0_report):
    """Test JSON serialization of phase-0 report."""
    print("\n" + "="*60)
    print("Test 3: JSON Serialization")
    print("="*60)

    # Serialize to JSON
    report_dict = phase0_report.model_dump(mode="json")
    json_str = json.dumps(report_dict, indent=2, default=str)

    print(f"\n✓ Serialized to JSON ({len(json_str)} bytes)")

    # Show sample of JSON
    lines = json_str.split("\n")
    print(f"\nFirst 20 lines of JSON output:")
    print("\n".join(lines[:20]))
    print("...")

    # Validate can be deserialized
    from phase0_infra.evaluation.metrics_schema import EvaluationReport as Phase0EvaluationReport

    reloaded = Phase0EvaluationReport.model_validate(report_dict)
    print(f"\n✓ Successfully deserialized")
    print(f"  - Report ID matches: {reloaded.report_id == phase0_report.report_id}")

    assert reloaded.report_id == phase0_report.report_id


def test_cross_phase_comparison():
    """Test comparing metrics across phases."""
    print("\n" + "="*60)
    print("Test 4: Cross-Phase Comparison Simulation")
    print("="*60)

    # Simulate phase-2 report
    phase2_results = [
        EvaluationResult(
            input_text=f"Input {i}",
            expected_output=f"Expected {i}",
            generated_output=f"Generated {i}",
            format_compliance=0.85,
            content_coverage=0.80,
            latency_ms=200.0,
            tokens_generated=50,
            tokens_per_second=250.0,
        )
        for i in range(3)
    ]

    phase2_report = EvaluationReport(
        model_id="phase2/task_slm",
        num_samples=3,
        avg_format_compliance=0.85,
        avg_content_coverage=0.80,
        avg_latency_ms=200.0,
        avg_tokens_per_second=250.0,
        section_coverage={},
        results=phase2_results,
    ).to_phase0_report(report_id="phase2_eval")

    # Simulate phase-3 MoE report (improved metrics)
    phase3_results = [
        EvaluationResult(
            input_text=f"Input {i}",
            expected_output=f"Expected {i}",
            generated_output=f"Generated {i}",
            format_compliance=0.92,
            content_coverage=0.88,
            latency_ms=180.0,
            tokens_generated=50,
            tokens_per_second=277.8,
        )
        for i in range(3)
    ]

    phase3_report = EvaluationReport(
        model_id="phase3/moe_expert",
        num_samples=3,
        avg_format_compliance=0.92,
        avg_content_coverage=0.88,
        avg_latency_ms=180.0,
        avg_tokens_per_second=277.8,
        section_coverage={},
        results=phase3_results,
    ).to_phase0_report(report_id="phase3_eval")

    # Compare
    print(f"\n{'Metric':<25} {'Phase-2':<15} {'Phase-3':<15} {'Delta':<15}")
    print("-" * 70)

    format_delta = phase3_report.quality_metrics.format_compliance - phase2_report.quality_metrics.format_compliance
    print(f"{'Format Compliance':<25} {phase2_report.quality_metrics.format_compliance:<15.2%} {phase3_report.quality_metrics.format_compliance:<15.2%} {format_delta:+.2%}")

    coverage_delta = phase3_report.quality_metrics.content_coverage - phase2_report.quality_metrics.content_coverage
    print(f"{'Content Coverage':<25} {phase2_report.quality_metrics.content_coverage:<15.2%} {phase3_report.quality_metrics.content_coverage:<15.2%} {coverage_delta:+.2%}")

    latency_delta = phase3_report.load_metrics.latency_ms - phase2_report.load_metrics.latency_ms
    print(f"{'Latency (ms)':<25} {phase2_report.load_metrics.latency_ms:<15.1f} {phase3_report.load_metrics.latency_ms:<15.1f} {latency_delta:+.1f}")

    tps_delta = phase3_report.token_metrics.tokens_per_second - phase2_report.token_metrics.tokens_per_second
    print(f"{'Tokens/Second':<25} {phase2_report.token_metrics.tokens_per_second:<15.1f} {phase3_report.token_metrics.tokens_per_second:<15.1f} {tps_delta:+.1f}")

    print(f"\n✓ Standardized schemas enable direct cross-phase comparison")

    # Verify improvements (phase-3 should be better)
    assert phase3_report.quality_metrics.format_compliance > phase2_report.quality_metrics.format_compliance
    assert phase3_report.load_metrics.latency_ms < phase2_report.load_metrics.latency_ms


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Phase-0 Metrics Integration Test Suite")
    print("="*60)

    try:
        # Run tests
        test_evaluation_result_conversion()
        test_evaluation_report_conversion()

        # Create phase0_report for json serialization test
        from src.program3_evaluation.evaluators.metrics import EvaluationResult, EvaluationReport
        results = [
            EvaluationResult(
                input_text=f"Sample input {i}",
                expected_output=f"Expected output {i}",
                generated_output=f"Generated output {i} with some content",
                format_compliance=0.90 + (i * 0.01),
                content_coverage=0.85 + (i * 0.02),
                latency_ms=150.0 + (i * 10),
                tokens_generated=40 + i,
                tokens_per_second=250.0 + (i * 5),
                section_scores={"section_1": True, "section_2": i % 2 == 0},
            )
            for i in range(5)
        ]
        report = EvaluationReport(
            model_id="fundraising/portfolio_analysis_v1",
            num_samples=5,
            avg_format_compliance=0.92,
            avg_content_coverage=0.89,
            avg_latency_ms=170.0,
            avg_tokens_per_second=262.5,
            section_coverage={"section_1": 1.0, "section_2": 0.6},
            results=results,
            metadata={"unit_id": "fundraising", "task_id": "portfolio_analysis"},
        )
        phase0_report = report.to_phase0_report(
            report_id="test_eval_001",
            dataset_id="fundraising/portfolio_analysis_eval",
        )
        test_json_serialization(phase0_report)
        test_cross_phase_comparison()

        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        print("\nIntegration Summary:")
        print("- Phase-2 metrics successfully map to phase-0 schemas")
        print("- Conversion methods work correctly")
        print("- JSON serialization/deserialization functional")
        print("- Cross-phase comparison enabled")
        print("\nNext Steps:")
        print("- Run actual evaluation: python -m src.program3_evaluation.main --unit <unit> --task <task>")
        print("- Check output: evaluations/<unit>/<model>/evaluation_report_phase0.json")
        print("="*60 + "\n")

        return 0

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
