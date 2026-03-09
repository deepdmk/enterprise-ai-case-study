"""
Program 3: Discovery Pipeline
Main entry point for the 90-day adaptive depth discovery experiment.

Usage:
    # Run full 90-day experiment
    python -m src.program3_discovery_pipeline.main --run

    # Run compressed test (7 days)
    python -m src.program3_discovery_pipeline.main --run --test-mode

    # Show schedule
    python -m src.program3_discovery_pipeline.main --show-schedule

    # Analyze specific phase
    python -m src.program3_discovery_pipeline.main --analyze-phase 3
"""

import argparse
from pathlib import Path
import sys

from .pipeline_runner import DiscoveryPipelineRunner
from .phase_config import DiscoveryPhases, WorkflowLibrary


def show_schedule(test_mode: bool = False):
    """
    Display the discovery phase schedule.

    Args:
        test_mode: If True, show test schedule
    """
    phases = DiscoveryPhases()
    phases.print_schedule(test_mode)


def show_workflows():
    """Display available workflows"""
    print(f"\n{'='*80}")
    print("Discovery Workflows")
    print(f"{'='*80}\n")

    workflows = WorkflowLibrary.get_all_workflows()

    for workflow in workflows:
        print(f"{workflow.name} ({workflow.workflow_id})")
        print(f"  Description: {workflow.description}")
        print(f"  Entry agent: {workflow.entry_agent}")
        print(f"  Typical depth: {workflow.typical_depth}")
        print(f"  Example queries:")
        for query in workflow.queries[:2]:
            print(f"    - {query}")
        print()


def run_pipeline(
    test_mode: bool = False,
    queries_per_day: int = 10,
    agent_base_url: str = "http://localhost"
):
    """
    Run the discovery pipeline.

    Args:
        test_mode: If True, run compressed test
        queries_per_day: Number of queries per day
        agent_base_url: Base URL for agent services
    """
    print("Initializing discovery pipeline...")

    # Create runner
    runner = DiscoveryPipelineRunner(
        agent_base_url=agent_base_url,
        test_mode=test_mode
    )

    # Check if agent services are running
    print("\nChecking agent services...")
    try:
        import httpx
        for agent_id, port in runner.agent_ports.items():
            url = f"{agent_base_url}:{port}/health"
            try:
                response = httpx.get(url, timeout=2.0)
                if response.status_code == 200:
                    print(f"  ✓ {agent_id} (port {port})")
                else:
                    print(f"  ✗ {agent_id} (port {port}) - returned {response.status_code}")
            except httpx.HTTPError:
                print(f"  ✗ {agent_id} (port {port}) - not responding")
                if not test_mode:
                    print("\nError: Agent services must be running before starting discovery pipeline")
                    print("Start them with: python -m src.program2_agent_services.main --start-all")
                    sys.exit(1)
                else:
                    print("  (Continuing in test mode)")

    except ImportError:
        print("Warning: httpx not installed, skipping health check")

    print()

    # Run pipeline
    try:
        stats = runner.run(queries_per_day=queries_per_day)

        # Export results
        output_file = Path("data/logs/discovery/all_results.json")
        runner.export_results(output_file)

        return stats

    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        if test_mode:
            print("(Running in test mode)")
        sys.exit(1)


def analyze_phase(phase_number: int):
    """
    Analyze results from a specific phase.

    Args:
        phase_number: Phase to analyze
    """
    print(f"\n{'='*80}")
    print(f"Analyzing Phase {phase_number} Results")
    print(f"{'='*80}\n")

    # Create runner just to access logger
    runner = DiscoveryPipelineRunner()

    # Get phase info
    phases = DiscoveryPhases()
    phase = phases.get_phase(phase_number)

    if not phase:
        print(f"Error: Invalid phase number {phase_number}")
        sys.exit(1)

    print(f"Phase: {phase.name}")
    print(f"Days: {phase.start_day}-{phase.end_day}")
    print(f"Max Depth: {phase.max_depth}")
    print(f"Purpose: {phase.purpose}\n")

    # Get statistics
    stats = runner.analyze_phase_results(phase_number)

    print("Statistics:")
    print(f"  Total calls: {stats['total_calls']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Average depth: {stats['avg_depth']:.2f}")
    print(f"  Max depth: {stats['max_depth']}")
    print(f"  Average execution time: {stats['avg_execution_time']:.2f}ms")

    if stats.get('status_breakdown'):
        print(f"\nStatus breakdown:")
        for status, count in stats['status_breakdown'].items():
            percentage = (count / stats['total_calls'] * 100) if stats['total_calls'] > 0 else 0
            print(f"  {status}: {count} ({percentage:.1f}%)")

    print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 3: Discovery Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show schedule
  python -m src.program3_discovery_pipeline.main --show-schedule

  # Show workflows
  python -m src.program3_discovery_pipeline.main --show-workflows

  # Run test (7 days)
  python -m src.program3_discovery_pipeline.main --run --test-mode

  # Run full experiment (90 days)
  python -m src.program3_discovery_pipeline.main --run

  # Analyze phase results
  python -m src.program3_discovery_pipeline.main --analyze-phase 3
        """
    )

    # Operation mode
    parser.add_argument("--show-schedule", action="store_true",
                       help="Show discovery phase schedule")
    parser.add_argument("--show-workflows", action="store_true",
                       help="Show available workflows")
    parser.add_argument("--run", action="store_true",
                       help="Run discovery pipeline")
    parser.add_argument("--analyze-phase", type=int,
                       help="Analyze specific phase results")

    # Optional parameters
    parser.add_argument("--test-mode", action="store_true",
                       help="Use test mode (7 days instead of 90)")
    parser.add_argument("--queries-per-day", type=int, default=10,
                       help="Number of queries per day (default: 10)")
    parser.add_argument("--agent-base-url", type=str, default="http://localhost",
                       help="Base URL for agent services (default: http://localhost)")

    args = parser.parse_args()

    # Validate that at least one operation is specified
    if not any([args.show_schedule, args.show_workflows, args.run, args.analyze_phase]):
        parser.error("Must specify at least one operation")

    try:
        if args.show_schedule:
            show_schedule(test_mode=args.test_mode)

        if args.show_workflows:
            show_workflows()

        if args.run:
            run_pipeline(
                test_mode=args.test_mode,
                queries_per_day=args.queries_per_day,
                agent_base_url=args.agent_base_url
            )

        if args.analyze_phase is not None:
            analyze_phase(args.analyze_phase)

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
