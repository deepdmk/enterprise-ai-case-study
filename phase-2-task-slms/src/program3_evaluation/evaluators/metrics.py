"""Evaluation metrics for Task SLMs."""

import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Import from Phase 0
from habitat_logging import get_logger
from evaluation.metrics_schema import (
    TokenMetrics,
    LoadMetrics,
    QualityMetrics,
    EvaluationReport as Phase0EvaluationReport,
)

logger = get_logger(__name__)


@dataclass
class EvaluationResult:
    """Result of evaluating a single example.

    This class maintains backward compatibility while mapping to phase-0 schemas.
    """

    input_text: str
    expected_output: str
    generated_output: str
    format_compliance: float
    content_coverage: float
    latency_ms: float
    tokens_generated: int
    tokens_per_second: float
    section_scores: dict[str, bool] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_phase0_token_metrics(self, input_tokens: int | None = None) -> TokenMetrics:
        """Convert to phase-0 TokenMetrics schema.

        Args:
            input_tokens: Number of input tokens (if known, otherwise estimated)

        Returns:
            TokenMetrics instance
        """
        # Estimate input tokens if not provided (rough approximation: 1 token ≈ 4 chars)
        if input_tokens is None:
            input_tokens = len(self.input_text) // 4

        return TokenMetrics(
            input_tokens=input_tokens,
            output_tokens=self.tokens_generated,
            total_tokens=input_tokens + self.tokens_generated,
            tokens_per_second=self.tokens_per_second if self.tokens_per_second > 0 else None,
        )

    def to_phase0_load_metrics(self) -> LoadMetrics:
        """Convert to phase-0 LoadMetrics schema.

        Returns:
            LoadMetrics instance
        """
        return LoadMetrics(
            latency_ms=self.latency_ms,
            throughput_rps=None,  # Not tracked at individual result level
            memory_mb=None,  # Not tracked in phase-2
            gpu_utilization=None,  # Not tracked in phase-2
        )

    def to_phase0_quality_metrics(self) -> QualityMetrics:
        """Convert to phase-0 QualityMetrics schema.

        Returns:
            QualityMetrics instance
        """
        return QualityMetrics(
            format_compliance=self.format_compliance,
            content_coverage=self.content_coverage,
            factual_accuracy=None,  # Not tracked in phase-2
            relevance_score=None,  # Not tracked in phase-2
            human_preference_score=None,  # Not tracked in phase-2
        )


@dataclass
class EvaluationReport:
    """Aggregate evaluation report.

    This class maintains backward compatibility while mapping to phase-0 schemas.
    """

    model_id: str
    num_samples: int
    avg_format_compliance: float
    avg_content_coverage: float
    avg_latency_ms: float
    avg_tokens_per_second: float
    section_coverage: dict[str, float]
    results: list[EvaluationResult]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_phase0_report(
        self,
        report_id: str | None = None,
        dataset_id: str | None = None,
    ) -> Phase0EvaluationReport:
        """Convert to phase-0 EvaluationReport schema.

        Args:
            report_id: Unique identifier for the report (auto-generated if None)
            dataset_id: Identifier for the dataset used in evaluation

        Returns:
            Phase0EvaluationReport instance
        """
        # Calculate aggregate token metrics
        total_input_tokens = sum(
            len(r.input_text) // 4 for r in self.results  # Rough approximation
        )
        total_output_tokens = sum(r.tokens_generated for r in self.results)

        avg_token_metrics = TokenMetrics(
            input_tokens=total_input_tokens,
            output_tokens=total_output_tokens,
            total_tokens=total_input_tokens + total_output_tokens,
            tokens_per_second=self.avg_tokens_per_second if self.avg_tokens_per_second > 0 else None,
        )

        # Calculate aggregate load metrics
        avg_load_metrics = LoadMetrics(
            latency_ms=self.avg_latency_ms,
            throughput_rps=None,  # Not tracked in phase-2
            memory_mb=None,  # Not tracked in phase-2
            gpu_utilization=None,  # Not tracked in phase-2
        )

        # Calculate aggregate quality metrics
        avg_quality_metrics = QualityMetrics(
            format_compliance=self.avg_format_compliance,
            content_coverage=self.avg_content_coverage,
            factual_accuracy=None,  # Not tracked in phase-2
            relevance_score=None,  # Not tracked in phase-2
            human_preference_score=None,  # Not tracked in phase-2
        )

        # Convert sample results to phase-0 format
        sample_outputs = [
            {
                "input": r.input_text[:200] + "..." if len(r.input_text) > 200 else r.input_text,
                "output": r.generated_output[:500] + "..." if len(r.generated_output) > 500 else r.generated_output,
                "expected": r.expected_output[:200] + "..." if len(r.expected_output) > 200 else r.expected_output,
                "token_metrics": r.to_phase0_token_metrics().model_dump(),
                "load_metrics": r.to_phase0_load_metrics().model_dump(),
                "quality_metrics": r.to_phase0_quality_metrics().model_dump(),
                "section_scores": r.section_scores,
                "errors": r.errors,
            }
            for r in self.results[:10]  # Limit to first 10 samples
        ]

        # Build notes with phase-2 specific information
        notes = f"Phase-2 Task SLM Evaluation. Section Coverage: {self.section_coverage}"
        if self.metadata:
            notes += f". Metadata: {self.metadata}"

        return Phase0EvaluationReport(
            report_id=report_id or f"phase2_eval_{uuid4().hex[:8]}",
            model_id=self.model_id,
            dataset_id=dataset_id,
            created_at=datetime.now(timezone.utc),
            token_metrics=avg_token_metrics,
            cost_metrics=None,  # Not tracked in phase-2
            load_metrics=avg_load_metrics,
            quality_metrics=avg_quality_metrics,
            sample_outputs=sample_outputs,
            notes=notes,
            schema_version="1.0",
        )


class FormatComplianceEvaluator:
    """Evaluate format compliance of generated outputs."""

    def __init__(self, required_sections: list[str] | None = None):
        """
        Initialize format evaluator.

        Args:
            required_sections: List of sections that should appear in output
        """
        self.required_sections = required_sections or []

    def evaluate(self, generated: str, expected: str | None = None) -> tuple[float, dict[str, bool]]:
        """
        Evaluate format compliance.

        Args:
            generated: Generated output
            expected: Expected output (optional, for structure comparison)

        Returns:
            Tuple of (compliance_score, section_scores)
        """
        section_scores = {}

        # Check required sections
        for section in self.required_sections:
            # Check for markdown headers or section names
            patterns = [
                rf"^#+\s*{re.escape(section)}",  # Markdown header
                rf"\*\*{re.escape(section)}\*\*",  # Bold
                rf"^{re.escape(section)}:",  # Colon-style
            ]
            found = any(
                re.search(pattern, generated, re.IGNORECASE | re.MULTILINE)
                for pattern in patterns
            )
            section_scores[section] = found

        # Check basic formatting
        format_checks = {
            "has_structure": bool(re.search(r"^#+\s|\*\*|^-\s|\d+\.", generated, re.MULTILINE)),
            "reasonable_length": len(generated) > 50,
            "no_repetition": not self._has_repetition(generated),
            "complete_sentences": self._has_complete_sentences(generated),
        }

        # Calculate score
        section_score = sum(section_scores.values()) / len(section_scores) if section_scores else 1.0
        format_score = sum(format_checks.values()) / len(format_checks)

        # Weighted average
        compliance_score = 0.6 * section_score + 0.4 * format_score

        return compliance_score, section_scores

    def _has_repetition(self, text: str, threshold: int = 3) -> bool:
        """Check for excessive repetition."""
        sentences = text.split(". ")
        if len(sentences) < threshold:
            return False

        # Check for repeated sentences
        seen = set()
        for sent in sentences:
            normalized = sent.strip().lower()
            if len(normalized) > 20:
                if normalized in seen:
                    return True
                seen.add(normalized)
        return False

    def _has_complete_sentences(self, text: str) -> bool:
        """Check if text has complete sentences."""
        # Simple heuristic: ends with punctuation or has multiple sentences
        return text.strip().endswith((".", "!", "?", "```")) or ". " in text


class ContentCoverageEvaluator:
    """Evaluate content coverage of generated outputs."""

    def __init__(self, key_concepts: list[str] | None = None):
        """
        Initialize content evaluator.

        Args:
            key_concepts: Key concepts that should appear in output
        """
        self.key_concepts = key_concepts or []

    def evaluate(self, generated: str, expected: str | None = None) -> float:
        """
        Evaluate content coverage.

        Args:
            generated: Generated output
            expected: Expected output for comparison

        Returns:
            Coverage score (0-1)
        """
        scores = []

        # Check key concepts
        if self.key_concepts:
            concept_score = sum(
                1 for concept in self.key_concepts
                if concept.lower() in generated.lower()
            ) / len(self.key_concepts)
            scores.append(concept_score)

        # Compare to expected if available
        if expected:
            # Simple overlap measure
            expected_words = set(expected.lower().split())
            generated_words = set(generated.lower().split())

            if expected_words:
                overlap = len(expected_words & generated_words) / len(expected_words)
                scores.append(min(overlap * 1.5, 1.0))  # Cap at 1.0

        # Check for substantive content
        substantive_score = self._evaluate_substantive_content(generated)
        scores.append(substantive_score)

        return sum(scores) / len(scores) if scores else 0.0

    def _evaluate_substantive_content(self, text: str) -> float:
        """Evaluate if content is substantive."""
        # Check for various quality indicators
        indicators = [
            len(text) > 100,  # Minimum length
            len(text.split()) > 30,  # Minimum words
            re.search(r"\d+", text) is not None,  # Contains numbers
            re.search(r"[A-Z][a-z]+", text) is not None,  # Contains proper nouns
            text.count(".") > 2,  # Multiple sentences
        ]
        return sum(indicators) / len(indicators)


class LatencyEvaluator:
    """Evaluate generation latency."""

    def __init__(self, model, tokenizer, device: str = "cuda"):
        """
        Initialize latency evaluator.

        Args:
            model: The model to evaluate
            tokenizer: The tokenizer
            device: Device to run on
        """
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def evaluate(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
    ) -> tuple[str, float, int, float]:
        """
        Generate output and measure latency.

        Args:
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Tuple of (generated_text, latency_ms, tokens_generated, tokens_per_second)
        """
        import torch

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        input_length = inputs["input_ids"].shape[1]

        # Time generation
        start_time = time.perf_counter()

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.pad_token_id,
            )

        end_time = time.perf_counter()

        # Calculate metrics
        latency_ms = (end_time - start_time) * 1000
        output_length = outputs.shape[1]
        tokens_generated = output_length - input_length
        tokens_per_second = tokens_generated / (latency_ms / 1000) if latency_ms > 0 else 0

        # Decode output
        generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove prompt from output
        if generated.startswith(prompt):
            generated = generated[len(prompt):].strip()

        return generated, latency_ms, tokens_generated, tokens_per_second


class TaskSLMEvaluator:
    """Main evaluator for Task SLMs."""

    def __init__(
        self,
        model,
        tokenizer,
        required_sections: list[str] | None = None,
        key_concepts: list[str] | None = None,
        device: str = "cuda",
    ):
        """
        Initialize the evaluator.

        Args:
            model: The model to evaluate
            tokenizer: The tokenizer
            required_sections: Required output sections
            key_concepts: Key concepts to check for
            device: Device to run on
        """
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

        self.format_evaluator = FormatComplianceEvaluator(required_sections)
        self.content_evaluator = ContentCoverageEvaluator(key_concepts)
        self.latency_evaluator = LatencyEvaluator(model, tokenizer, device)

    def evaluate_single(
        self,
        input_text: str,
        expected_output: str | None = None,
        system_prompt: str = "",
        max_new_tokens: int = 512,
    ) -> EvaluationResult:
        """
        Evaluate a single example.

        Args:
            input_text: The input prompt
            expected_output: Expected output (optional)
            system_prompt: System prompt to prepend
            max_new_tokens: Maximum tokens to generate

        Returns:
            EvaluationResult
        """
        # Format prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {input_text}\n\nAssistant:"
        else:
            full_prompt = f"User: {input_text}\n\nAssistant:"

        # Generate and measure latency
        generated, latency_ms, tokens_generated, tokens_per_second = (
            self.latency_evaluator.evaluate(full_prompt, max_new_tokens)
        )

        # Evaluate format
        format_score, section_scores = self.format_evaluator.evaluate(
            generated, expected_output
        )

        # Evaluate content
        content_score = self.content_evaluator.evaluate(generated, expected_output)

        return EvaluationResult(
            input_text=input_text,
            expected_output=expected_output or "",
            generated_output=generated,
            format_compliance=format_score,
            content_coverage=content_score,
            latency_ms=latency_ms,
            tokens_generated=tokens_generated,
            tokens_per_second=tokens_per_second,
            section_scores=section_scores,
        )

    def evaluate_batch(
        self,
        examples: list[dict[str, str]],
        system_prompt: str = "",
        max_new_tokens: int = 512,
        model_id: str = "unknown",
    ) -> EvaluationReport:
        """
        Evaluate a batch of examples.

        Args:
            examples: List of {"input": ..., "output": ...} dicts
            system_prompt: System prompt to use
            max_new_tokens: Maximum tokens per generation
            model_id: Model identifier for the report

        Returns:
            EvaluationReport
        """
        results = []

        for i, ex in enumerate(examples):
            logger.info("evaluating_example", index=i, total=len(examples))

            result = self.evaluate_single(
                input_text=ex.get("input", ""),
                expected_output=ex.get("output"),
                system_prompt=system_prompt,
                max_new_tokens=max_new_tokens,
            )
            results.append(result)

        # Aggregate metrics
        avg_format = sum(r.format_compliance for r in results) / len(results)
        avg_content = sum(r.content_coverage for r in results) / len(results)
        avg_latency = sum(r.latency_ms for r in results) / len(results)
        avg_tps = sum(r.tokens_per_second for r in results) / len(results)

        # Section coverage
        all_sections: set[str] = set()
        for r in results:
            all_sections.update(r.section_scores.keys())

        section_coverage = {
            section: sum(1 for r in results if r.section_scores.get(section, False)) / len(results)
            for section in all_sections
        }

        return EvaluationReport(
            model_id=model_id,
            num_samples=len(examples),
            avg_format_compliance=avg_format,
            avg_content_coverage=avg_content,
            avg_latency_ms=avg_latency,
            avg_tokens_per_second=avg_tps,
            section_coverage=section_coverage,
            results=results,
        )
