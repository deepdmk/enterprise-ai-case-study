"""
Adaptive Depth Analyzer

Analyzes discovery logs to determine optimal cascade depths per workflow.
"""

from pathlib import Path
from typing import Any, Optional
from collections import defaultdict
import statistics

from ..shared.call_logger import A2ACallLogger, A2ACallLog
from ..shared.a2a_protocol import ResponseStatus


class AdaptiveDepthAnalyzer:
    """
    Analyzes discovery experiment logs to determine optimal depths.

    Compares performance across phases to identify:
    1. Which workflows benefit from deeper cascades
    2. Optimal depth for each workflow type
    3. Patterns in successful vs failed calls
    4. Performance vs depth trade-offs
    """

    def __init__(self, log_directory: Path):
        """
        Initialize analyzer.

        Args:
            log_directory: Directory containing discovery logs
        """
        self.log_directory = Path(log_directory)
        self.logger = A2ACallLogger(log_directory)
        self.analysis_results = {}

    def analyze_all_phases(self) -> dict[str, Any]:
        """
        Analyze all discovery phases.

        Returns:
            Comprehensive analysis results
        """
        print(f"\n{'='*80}")
        print("Analyzing Discovery Experiment Results")
        print(f"{'='*80}\n")

        # Load all logs
        all_logs = self.logger.load_logs()
        print(f"Loaded {len(all_logs)} call logs\n")

        # Analyze by phase
        phase_analysis = self._analyze_by_phase(all_logs)

        # Analyze by depth
        depth_analysis = self._analyze_by_depth(all_logs)

        # Analyze by workflow
        workflow_analysis = self._analyze_by_workflow(all_logs)

        # Compare control phases
        control_comparison = self._compare_control_phases(all_logs)

        # Determine optimal depths
        optimal_depths = self._determine_optimal_depths(all_logs)

        # Compile results
        results = {
            "total_calls": len(all_logs),
            "phase_analysis": phase_analysis,
            "depth_analysis": depth_analysis,
            "workflow_analysis": workflow_analysis,
            "control_comparison": control_comparison,
            "optimal_depths": optimal_depths,
            "recommendations": self._generate_recommendations(optimal_depths)
        }

        self.analysis_results = results
        return results

    def _analyze_by_phase(self, logs: list[A2ACallLog]) -> dict[int, dict[str, Any]]:
        """Analyze performance by discovery phase"""
        print("Analyzing by phase...")

        phase_data = defaultdict(list)
        for log in logs:
            phase_data[log.phase].append(log)

        results = {}
        for phase, phase_logs in sorted(phase_data.items()):
            stats = self._compute_phase_stats(phase_logs)
            results[phase] = stats

        return results

    def _analyze_by_depth(self, logs: list[A2ACallLog]) -> dict[int, dict[str, Any]]:
        """Analyze performance by cascade depth"""
        print("Analyzing by depth...")

        depth_data = defaultdict(list)
        for log in logs:
            depth_data[log.call_depth].append(log)

        results = {}
        for depth, depth_logs in sorted(depth_data.items()):
            stats = self._compute_depth_stats(depth_logs)
            results[depth] = stats

        return results

    def _analyze_by_workflow(self, logs: list[A2ACallLog]) -> dict[str, dict[str, Any]]:
        """Analyze performance by workflow"""
        print("Analyzing by workflow...")

        workflow_data = defaultdict(list)
        for log in logs:
            if log.workflow_id:
                workflow_data[log.workflow_id].append(log)

        results = {}
        for workflow_id, workflow_logs in workflow_data.items():
            stats = self._compute_workflow_stats(workflow_logs)
            results[workflow_id] = stats

        return results

    def _compare_control_phases(self, logs: list[A2ACallLog]) -> dict[str, Any]:
        """
        Compare control phases (2, 4, 6) to validate consistency.

        All three phases use depth=2, so should have similar performance.
        """
        print("Comparing control phases...")

        control_phases = [2, 4, 6]
        control_data = {}

        for phase in control_phases:
            phase_logs = [log for log in logs if log.phase == phase]
            if phase_logs:
                control_data[phase] = self._compute_phase_stats(phase_logs)

        # Calculate variance
        if len(control_data) >= 2:
            success_rates = [stats["success_rate"] for stats in control_data.values()]
            variance = statistics.variance(success_rates) if len(success_rates) > 1 else 0
            mean_success_rate = statistics.mean(success_rates)

            return {
                "phases": control_data,
                "mean_success_rate": mean_success_rate,
                "variance": variance,
                "consistent": variance < 0.01  # Less than 1% variance
            }

        return {"phases": control_data, "insufficient_data": True}

    def _determine_optimal_depths(self, logs: list[A2ACallLog]) -> dict[str, int]:
        """
        Determine optimal cascade depth for each workflow type.

        Analyzes success rate and execution time vs depth.
        """
        print("Determining optimal depths...")

        # Group by workflow and depth
        workflow_depth_data = defaultdict(lambda: defaultdict(list))

        for log in logs:
            if log.workflow_id:
                workflow_depth_data[log.workflow_id][log.call_depth].append(log)

        optimal_depths = {}

        for workflow_id, depth_data in workflow_depth_data.items():
            best_depth = None
            best_score = -1

            for depth, depth_logs in depth_data.items():
                if len(depth_logs) < 5:  # Need minimum sample size
                    continue

                # Calculate score: balance success rate and execution time
                successful = sum(1 for log in depth_logs if log.status == ResponseStatus.SUCCESS)
                success_rate = successful / len(depth_logs)

                avg_time = statistics.mean([log.execution_time_ms for log in depth_logs])
                time_penalty = avg_time / 1000  # Convert to seconds

                # Score formula: success_rate - (time_penalty * 0.1)
                # Prioritize success but penalize very slow responses
                score = success_rate - (time_penalty * 0.1)

                if score > best_score:
                    best_score = score
                    best_depth = depth

            if best_depth is not None:
                optimal_depths[workflow_id] = best_depth

        return optimal_depths

    def _generate_recommendations(self, optimal_depths: dict[str, int]) -> list[str]:
        """Generate recommendations based on analysis"""
        recommendations = []

        if not optimal_depths:
            recommendations.append(
                "Insufficient data to make depth recommendations. "
                "Run discovery pipeline first."
            )
            return recommendations

        # General recommendations
        depths = list(optimal_depths.values())
        if depths:
            avg_optimal_depth = statistics.mean(depths)
            recommendations.append(
                f"Average optimal depth across workflows: {avg_optimal_depth:.1f}"
            )

        # Per-workflow recommendations
        for workflow_id, depth in optimal_depths.items():
            recommendations.append(
                f"Workflow '{workflow_id}': Optimal depth = {depth}"
            )

        # Phase 5 orchestrator training
        recommendations.append(
            "Use these optimal depths for Phase 5 orchestrator training"
        )

        return recommendations

    def _compute_phase_stats(self, logs: list[A2ACallLog]) -> dict[str, Any]:
        """Compute statistics for a phase"""
        if not logs:
            return {"error": "No logs"}

        successful = sum(1 for log in logs if log.status == ResponseStatus.SUCCESS)
        total = len(logs)

        return {
            "total_calls": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0,
            "avg_execution_time": statistics.mean([log.execution_time_ms for log in logs]),
            "avg_depth": statistics.mean([log.call_depth for log in logs]),
            "max_depth": max([log.max_depth for log in logs])
        }

    def _compute_depth_stats(self, logs: list[A2ACallLog]) -> dict[str, Any]:
        """Compute statistics for a specific depth"""
        return self._compute_phase_stats(logs)

    def _compute_workflow_stats(self, logs: list[A2ACallLog]) -> dict[str, Any]:
        """Compute statistics for a workflow"""
        stats = self._compute_phase_stats(logs)

        # Add workflow-specific stats
        depths = [log.call_depth for log in logs]
        stats["depth_distribution"] = {
            "min": min(depths) if depths else 0,
            "max": max(depths) if depths else 0,
            "mean": statistics.mean(depths) if depths else 0
        }

        return stats

    def print_analysis(self, results: Optional[dict[str, Any]] = None) -> None:
        """
        Print analysis results.

        Args:
            results: Analysis results (uses self.analysis_results if None)
        """
        results = results or self.analysis_results

        if not results:
            print("No analysis results available")
            return

        print(f"\n{'='*80}")
        print("Analysis Results")
        print(f"{'='*80}\n")

        print(f"Total calls analyzed: {results['total_calls']}\n")

        # Phase analysis
        print("Performance by Phase:")
        print(f"{'Phase':<8} {'Calls':<8} {'Success':<10} {'Avg Time':<12} {'Avg Depth':<10}")
        print("-" * 60)

        for phase, stats in sorted(results['phase_analysis'].items()):
            if "error" not in stats:
                print(f"{phase:<8} {stats['total_calls']:<8} "
                      f"{stats['success_rate']:<10.1%} "
                      f"{stats['avg_execution_time']:<12.2f}ms "
                      f"{stats['avg_depth']:<10.2f}")

        # Optimal depths
        print(f"\nOptimal Depths by Workflow:")
        for workflow_id, depth in results['optimal_depths'].items():
            print(f"  {workflow_id}: depth={depth}")

        # Recommendations
        print(f"\nRecommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")

        print()

    def export_analysis(self, output_file: Path) -> None:
        """
        Export analysis results to JSON.

        Args:
            output_file: Path to output file
        """
        import json

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(self.analysis_results, f, indent=2, default=str)

        print(f"Analysis exported to: {output_file}")
