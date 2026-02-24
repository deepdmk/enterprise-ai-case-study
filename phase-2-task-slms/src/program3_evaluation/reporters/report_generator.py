"""Report generators for evaluation results."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Import from Phase 0
from habitat_logging import get_logger

from src.program3_evaluation.evaluators.metrics import EvaluationReport, EvaluationResult

logger = get_logger(__name__)


class Phase0Reporter:
    """Generate phase-0 standardized evaluation reports."""

    def generate(
        self,
        report: EvaluationReport,
        output_path: str | Path,
        report_id: str | None = None,
        dataset_id: str | None = None,
    ) -> Path:
        """
        Generate a phase-0 standardized JSON report.

        Args:
            report: The phase-2 evaluation report
            output_path: Path to save the report
            report_id: Unique identifier for the report (auto-generated if None)
            dataset_id: Identifier for the dataset used in evaluation

        Returns:
            Path to the saved report
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to phase-0 format
        phase0_report = report.to_phase0_report(
            report_id=report_id,
            dataset_id=dataset_id,
        )

        # Serialize using Pydantic's model_dump for proper JSON serialization
        report_data = phase0_report.model_dump(mode="json")

        with open(output_path, "w") as f:
            json.dump(report_data, f, indent=2, default=str)

        logger.info("phase0_report_saved", path=str(output_path), report_id=phase0_report.report_id)
        return output_path


class JSONReporter:
    """Generate JSON evaluation reports."""

    def generate(
        self,
        report: EvaluationReport,
        output_path: str | Path,
        include_examples: bool = True,
    ) -> Path:
        """
        Generate a JSON report.

        Args:
            report: The evaluation report
            output_path: Path to save the report
            include_examples: Whether to include individual examples

        Returns:
            Path to the saved report
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        report_data: dict[str, Any] = {
            "model_id": report.model_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "num_samples": report.num_samples,
                "avg_format_compliance": round(report.avg_format_compliance, 4),
                "avg_content_coverage": round(report.avg_content_coverage, 4),
                "avg_latency_ms": round(report.avg_latency_ms, 2),
                "avg_tokens_per_second": round(report.avg_tokens_per_second, 2),
            },
            "section_coverage": {
                k: round(v, 4) for k, v in report.section_coverage.items()
            },
            "metadata": report.metadata,
        }

        if include_examples:
            report_data["examples"] = [
                self._serialize_result(r) for r in report.results
            ]

        with open(output_path, "w") as f:
            json.dump(report_data, f, indent=2)

        logger.info("json_report_saved", path=str(output_path))
        return output_path

    def _serialize_result(self, result: EvaluationResult) -> dict[str, Any]:
        """Serialize a single evaluation result."""
        return {
            "input": result.input_text[:200] + "..." if len(result.input_text) > 200 else result.input_text,
            "generated_preview": result.generated_output[:500] + "..." if len(result.generated_output) > 500 else result.generated_output,
            "format_compliance": round(result.format_compliance, 4),
            "content_coverage": round(result.content_coverage, 4),
            "latency_ms": round(result.latency_ms, 2),
            "tokens_generated": result.tokens_generated,
            "tokens_per_second": round(result.tokens_per_second, 2),
            "section_scores": result.section_scores,
            "errors": result.errors,
        }


class MarkdownReporter:
    """Generate Markdown evaluation reports."""

    def generate(
        self,
        report: EvaluationReport,
        output_path: str | Path,
        include_examples: int = 3,
    ) -> Path:
        """
        Generate a Markdown report.

        Args:
            report: The evaluation report
            output_path: Path to save the report
            include_examples: Number of example outputs to include

        Returns:
            Path to the saved report
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# Evaluation Report: {report.model_id}",
            "",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Samples Evaluated | {report.num_samples} |",
            f"| Avg Format Compliance | {report.avg_format_compliance:.1%} |",
            f"| Avg Content Coverage | {report.avg_content_coverage:.1%} |",
            f"| Avg Latency | {report.avg_latency_ms:.1f} ms |",
            f"| Avg Tokens/Second | {report.avg_tokens_per_second:.1f} |",
            "",
        ]

        # Section coverage
        if report.section_coverage:
            lines.extend([
                "## Section Coverage",
                "",
                "| Section | Coverage |",
                "|---------|----------|",
            ])
            for section, coverage in report.section_coverage.items():
                lines.append(f"| {section} | {coverage:.1%} |")
            lines.append("")

        # Example outputs
        if include_examples > 0:
            lines.extend([
                "## Example Outputs",
                "",
            ])

            for i, result in enumerate(report.results[:include_examples]):
                lines.extend([
                    f"### Example {i + 1}",
                    "",
                    "**Input:**",
                    "```",
                    result.input_text[:300] + "..." if len(result.input_text) > 300 else result.input_text,
                    "```",
                    "",
                    "**Generated Output:**",
                    "```",
                    result.generated_output[:800] + "..." if len(result.generated_output) > 800 else result.generated_output,
                    "```",
                    "",
                    f"- Format Compliance: {result.format_compliance:.1%}",
                    f"- Content Coverage: {result.content_coverage:.1%}",
                    f"- Latency: {result.latency_ms:.1f} ms",
                    "",
                ])

        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        logger.info("markdown_report_saved", path=str(output_path))
        return output_path


class ComparisonReporter:
    """Generate comparison reports between models."""

    def generate(
        self,
        reports: list[EvaluationReport],
        output_path: str | Path,
    ) -> Path:
        """
        Generate a comparison report.

        Args:
            reports: List of evaluation reports to compare
            output_path: Path to save the report

        Returns:
            Path to the saved report
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "# Model Comparison Report",
            "",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Performance Comparison",
            "",
            "| Model | Format | Content | Latency (ms) | Tokens/s |",
            "|-------|--------|---------|--------------|----------|",
        ]

        for report in reports:
            lines.append(
                f"| {report.model_id} | {report.avg_format_compliance:.1%} | "
                f"{report.avg_content_coverage:.1%} | {report.avg_latency_ms:.1f} | "
                f"{report.avg_tokens_per_second:.1f} |"
            )

        lines.append("")

        # Section coverage comparison
        all_sections: set[str] = set()
        for report in reports:
            all_sections.update(report.section_coverage.keys())

        if all_sections:
            lines.extend([
                "## Section Coverage Comparison",
                "",
                "| Section | " + " | ".join(r.model_id for r in reports) + " |",
                "|---------|" + "|".join("-" * (len(r.model_id) + 2) for r in reports) + "|",
            ])

            for section in sorted(all_sections):
                values = [
                    f"{r.section_coverage.get(section, 0):.1%}"
                    for r in reports
                ]
                lines.append(f"| {section} | " + " | ".join(values) + " |")

        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        logger.info("comparison_report_saved", path=str(output_path))
        return output_path


def generate_evaluation_report(
    report: EvaluationReport,
    output_dir: str | Path,
    formats: list[str] | None = None,
    report_id: str | None = None,
    dataset_id: str | None = None,
) -> dict[str, Path]:
    """
    Generate evaluation reports in multiple formats.

    Args:
        report: The evaluation report
        output_dir: Directory for reports
        formats: List of formats to generate (default: ["json", "md", "phase0"])
        report_id: Unique identifier for phase-0 report (auto-generated if None)
        dataset_id: Identifier for the dataset used in evaluation

    Returns:
        Dictionary mapping format to output path
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    formats = formats or ["json", "md", "phase0"]
    paths: dict[str, Path] = {}

    if "json" in formats:
        json_reporter = JSONReporter()
        paths["json"] = json_reporter.generate(
            report,
            output_dir / "evaluation_report.json",
        )

    if "md" in formats:
        md_reporter = MarkdownReporter()
        paths["md"] = md_reporter.generate(
            report,
            output_dir / "evaluation_report.md",
        )

    if "phase0" in formats:
        phase0_reporter = Phase0Reporter()
        paths["phase0"] = phase0_reporter.generate(
            report,
            output_dir / "evaluation_report_phase0.json",
            report_id=report_id,
            dataset_id=dataset_id,
        )

    return paths
