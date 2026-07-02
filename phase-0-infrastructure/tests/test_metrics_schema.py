"""Tests for evaluation.metrics_schema module."""

from datetime import UTC, datetime

import pytest

from phase0_infra.evaluation.metrics_schema import (
    CostMetrics,
    EvaluationReport,
    LoadMetrics,
    QualityMetrics,
    TokenMetrics,
)


class TestTokenMetrics:
    """Tests for TokenMetrics model."""

    def test_valid_token_metrics(self):
        """Test creating valid TokenMetrics."""
        metrics = TokenMetrics(
            input_tokens=100,
            output_tokens=50,
            total_tokens=150
        )
        assert metrics.input_tokens == 100
        assert metrics.output_tokens == 50
        assert metrics.total_tokens == 150
        assert metrics.tokens_per_second is None

    def test_with_tokens_per_second(self):
        """Test TokenMetrics with tokens_per_second."""
        metrics = TokenMetrics(
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            tokens_per_second=25.5
        )
        assert metrics.tokens_per_second == 25.5

    def test_total_tokens_validation_correct(self):
        """Test total_tokens validation passes when sum is correct."""
        metrics = TokenMetrics(
            input_tokens=1000,
            output_tokens=500,
            total_tokens=1500
        )
        assert metrics.total_tokens == 1500

    def test_total_tokens_validation_incorrect(self):
        """Test total_tokens validation fails when sum is incorrect."""
        with pytest.raises(ValueError, match="total_tokens.*must equal"):
            TokenMetrics(
                input_tokens=100,
                output_tokens=50,
                total_tokens=200  # Should be 150
            )

    def test_negative_tokens_rejected(self):
        """Test negative token values are rejected."""
        with pytest.raises(Exception):  # ValidationError
            TokenMetrics(
                input_tokens=-10,
                output_tokens=50,
                total_tokens=40
            )

    def test_zero_tokens_accepted(self):
        """Test zero tokens are accepted."""
        metrics = TokenMetrics(
            input_tokens=0,
            output_tokens=0,
            total_tokens=0
        )
        assert metrics.total_tokens == 0


class TestCostMetrics:
    """Tests for CostMetrics model."""

    def test_valid_cost_metrics(self):
        """Test creating valid CostMetrics."""
        metrics = CostMetrics(
            input_cost=0.001,
            output_cost=0.002,
            total_cost=0.003
        )
        assert metrics.input_cost == 0.001
        assert metrics.output_cost == 0.002
        assert metrics.total_cost == 0.003
        assert metrics.currency == "USD"

    def test_custom_currency(self):
        """Test CostMetrics with custom currency."""
        metrics = CostMetrics(
            input_cost=1.0,
            output_cost=2.0,
            total_cost=3.0,
            currency="EUR"
        )
        assert metrics.currency == "EUR"

    def test_total_cost_validation_correct(self):
        """Test total_cost validation passes when sum is correct."""
        metrics = CostMetrics(
            input_cost=0.10,
            output_cost=0.20,
            total_cost=0.30
        )
        assert metrics.total_cost == 0.30

    def test_total_cost_validation_incorrect(self):
        """Test total_cost validation fails when sum is incorrect."""
        with pytest.raises(ValueError, match="total_cost.*must equal"):
            CostMetrics(
                input_cost=0.10,
                output_cost=0.20,
                total_cost=0.50  # Should be 0.30
            )

    def test_total_cost_floating_point_tolerance(self):
        """Test total_cost allows small floating point errors."""
        # This should pass due to the 0.0001 tolerance
        metrics = CostMetrics(
            input_cost=0.1,
            output_cost=0.2,
            total_cost=0.30000001  # Very close to 0.3
        )
        assert metrics.total_cost == pytest.approx(0.3, abs=0.0001)

    def test_negative_cost_rejected(self):
        """Test negative cost values are rejected."""
        with pytest.raises(Exception):  # ValidationError
            CostMetrics(
                input_cost=-0.01,
                output_cost=0.02,
                total_cost=0.01
            )


class TestLoadMetrics:
    """Tests for LoadMetrics model."""

    def test_valid_load_metrics_minimal(self):
        """Test creating LoadMetrics with only required field."""
        metrics = LoadMetrics(latency_ms=100.5)
        assert metrics.latency_ms == 100.5
        assert metrics.throughput_rps is None
        assert metrics.memory_mb is None
        assert metrics.gpu_utilization is None

    def test_valid_load_metrics_full(self):
        """Test creating LoadMetrics with all fields."""
        metrics = LoadMetrics(
            latency_ms=250.5,
            throughput_rps=4.0,
            memory_mb=2048.0,
            gpu_utilization=0.75
        )
        assert metrics.latency_ms == 250.5
        assert metrics.throughput_rps == 4.0
        assert metrics.memory_mb == 2048.0
        assert metrics.gpu_utilization == 0.75

    def test_gpu_utilization_bounds(self):
        """Test gpu_utilization accepts values between 0 and 1."""
        # Valid boundary values
        metrics_zero = LoadMetrics(latency_ms=100, gpu_utilization=0.0)
        assert metrics_zero.gpu_utilization == 0.0

        metrics_one = LoadMetrics(latency_ms=100, gpu_utilization=1.0)
        assert metrics_one.gpu_utilization == 1.0

    def test_gpu_utilization_out_of_bounds(self):
        """Test gpu_utilization rejects values outside 0-1."""
        with pytest.raises(Exception):  # ValidationError
            LoadMetrics(latency_ms=100, gpu_utilization=1.5)

        with pytest.raises(Exception):  # ValidationError
            LoadMetrics(latency_ms=100, gpu_utilization=-0.1)

    def test_negative_latency_rejected(self):
        """Test negative latency is rejected."""
        with pytest.raises(Exception):  # ValidationError
            LoadMetrics(latency_ms=-10.0)


class TestQualityMetrics:
    """Tests for QualityMetrics model."""

    def test_valid_quality_metrics_minimal(self):
        """Test creating QualityMetrics with only required fields."""
        metrics = QualityMetrics(
            format_compliance=0.95,
            content_coverage=0.88
        )
        assert metrics.format_compliance == 0.95
        assert metrics.content_coverage == 0.88
        assert metrics.factual_accuracy is None
        assert metrics.relevance_score is None
        assert metrics.human_preference_score is None

    def test_valid_quality_metrics_full(self):
        """Test creating QualityMetrics with all fields."""
        metrics = QualityMetrics(
            format_compliance=0.95,
            content_coverage=0.88,
            factual_accuracy=0.92,
            relevance_score=0.90,
            human_preference_score=0.85
        )
        assert metrics.factual_accuracy == 0.92
        assert metrics.relevance_score == 0.90
        assert metrics.human_preference_score == 0.85

    def test_score_bounds(self):
        """Test all scores accept values between 0 and 1."""
        metrics = QualityMetrics(
            format_compliance=0.0,
            content_coverage=1.0
        )
        assert metrics.format_compliance == 0.0
        assert metrics.content_coverage == 1.0

    def test_score_out_of_bounds(self):
        """Test scores reject values outside 0-1."""
        with pytest.raises(Exception):  # ValidationError
            QualityMetrics(
                format_compliance=1.5,  # Invalid
                content_coverage=0.5
            )

        with pytest.raises(Exception):  # ValidationError
            QualityMetrics(
                format_compliance=0.5,
                content_coverage=-0.1  # Invalid
            )


class TestEvaluationReport:
    """Tests for EvaluationReport model."""

    def test_minimal_report(self):
        """Test creating EvaluationReport with only required fields."""
        report = EvaluationReport(
            report_id="eval_001",
            model_id="model_v1"
        )
        assert report.report_id == "eval_001"
        assert report.model_id == "model_v1"
        assert report.dataset_id is None
        assert report.schema_version == "1.0"
        assert isinstance(report.created_at, datetime)

    def test_full_report(self):
        """Test creating EvaluationReport with all fields."""
        token_metrics = TokenMetrics(
            input_tokens=1000,
            output_tokens=500,
            total_tokens=1500
        )
        cost_metrics = CostMetrics(
            input_cost=0.001,
            output_cost=0.002,
            total_cost=0.003
        )
        load_metrics = LoadMetrics(
            latency_ms=250.5,
            throughput_rps=4.0
        )
        quality_metrics = QualityMetrics(
            format_compliance=0.95,
            content_coverage=0.88
        )

        report = EvaluationReport(
            report_id="eval_full",
            model_id="model_v1",
            dataset_id="dataset_v1",
            token_metrics=token_metrics,
            cost_metrics=cost_metrics,
            load_metrics=load_metrics,
            quality_metrics=quality_metrics,
            sample_outputs=[{"input": "test", "output": "result"}],
            notes="Test evaluation"
        )

        assert report.token_metrics is not None
        assert report.token_metrics.total_tokens == 1500
        assert report.cost_metrics is not None
        assert report.load_metrics is not None
        assert report.quality_metrics is not None
        assert len(report.sample_outputs) == 1
        assert report.notes == "Test evaluation"

    def test_created_at_default_is_utc(self):
        """Test created_at defaults to UTC timezone."""
        before = datetime.now(UTC)
        report = EvaluationReport(report_id="eval_001", model_id="model_v1")
        after = datetime.now(UTC)

        assert before <= report.created_at <= after

    def test_custom_created_at(self):
        """Test custom created_at value."""
        custom_time = datetime(2026, 1, 15, 12, 0, 0, tzinfo=UTC)
        report = EvaluationReport(
            report_id="eval_001",
            model_id="model_v1",
            created_at=custom_time
        )
        assert report.created_at == custom_time

    def test_nested_metrics_validation(self):
        """Test nested metrics are validated."""
        # Invalid token metrics should fail
        with pytest.raises(Exception):  # ValidationError
            EvaluationReport(
                report_id="eval_001",
                model_id="model_v1",
                token_metrics=TokenMetrics(
                    input_tokens=100,
                    output_tokens=50,
                    total_tokens=999  # Wrong total
                )
            )

    def test_model_dump(self):
        """Test EvaluationReport can be serialized."""
        report = EvaluationReport(
            report_id="eval_001",
            model_id="model_v1",
            token_metrics=TokenMetrics(
                input_tokens=100,
                output_tokens=50,
                total_tokens=150
            )
        )

        data = report.model_dump()
        assert data["report_id"] == "eval_001"
        assert data["model_id"] == "model_v1"
        assert data["token_metrics"]["total_tokens"] == 150
