"""
Program 4: Adaptive Analyzer
Main entry point for analyzing discovery results and exporting Phase 5 data.

Usage:
    # Analyze discovery results
    python -m src.program4_adaptive_analyzer.main --analyze

    # Export for Phase 5
    python -m src.program4_adaptive_analyzer.main --export-phase5

    # Full pipeline (analyze + export)
    python -m src.program4_adaptive_analyzer.main --full-pipeline
"""

import argparse
from pathlib import Path
import sys
import json

from .adaptive_depth_analyzer import AdaptiveDepthAnalyzer
from .orchestrator_exporter import OrchestratorExporter
from ..shared.phase0_integration import get_phase0_integration


def analyze_results(log_directory: Path, save_results: bool = True):
    """
    Analyze discovery experiment results.

    Args:
        log_directory: Directory containing discovery logs
        save_results: Whether to save analysis to file

    Returns:
        Analysis results
    """
    print("Starting analysis...")

    # Create analyzer
    analyzer = AdaptiveDepthAnalyzer(log_directory)

    # Run analysis
    results = analyzer.analyze_all_phases()

    # Print results
    analyzer.print_analysis(results)

    # Save if requested
    if save_results:
        output_file = Path("data/exports/analysis_results.json")
        analyzer.export_analysis(output_file)

    return results


def export_phase5_data(
    log_directory: Path,
    optimal_depths: dict,
    output_directory: Path
):
    """
    Export training data for Phase 5 orchestrators.

    Args:
        log_directory: Directory containing discovery logs
        optimal_depths: Optimal depths per workflow
        output_directory: Where to save Phase 5 data

    Returns:
        Number of examples exported
    """
    print("\nExporting Phase 5 training data...")

    # Create exporter
    exporter = OrchestratorExporter(log_directory)

    # Export training data
    num_examples = exporter.export_training_data(
        output_dir=output_directory,
        optimal_depths=optimal_depths
    )

    # Export summary
    summary_file = output_directory / "phase5_summary.json"
    exporter.export_summary(summary_file, optimal_depths)

    # Register with Phase 0
    phase0 = get_phase0_integration(Path("data"), test_mode=False)
    if phase0["available"]:
        train_file = output_directory / "orchestrator_training.json"
        chat_file = output_directory / "orchestrator_chat.jsonl"

        if train_file.exists() and chat_file.exists():
            phase0["data_registry"].register_phase5_export(
                dataset_id="phase-4/discovery/orchestrator-export/v1",
                train_path=train_file,
                chat_path=chat_file,
                num_examples=num_examples,
                optimal_depths=optimal_depths,
                tags=["orchestrator", "phase5-export", "routing"]
            )

    return num_examples


def full_pipeline(
    log_directory: Path,
    output_directory: Path,
    test_mode: bool = False
):
    """
    Run full analysis and export pipeline.

    Args:
        log_directory: Directory containing discovery logs
        output_directory: Where to save outputs
        test_mode: If True, use test mode
    """
    print(f"\n{'='*80}")
    print("Adaptive Depth Analysis & Phase 5 Export Pipeline")
    print(f"{'='*80}\n")

    # Step 1: Analyze results
    print("Step 1/2: Analyzing discovery results...")
    analyzer = AdaptiveDepthAnalyzer(log_directory)
    results = analyzer.analyze_all_phases()
    analyzer.print_analysis(results)

    # Save analysis
    analysis_file = output_directory / "analysis_results.json"
    analyzer.export_analysis(analysis_file)

    # Step 2: Export for Phase 5
    print("\nStep 2/2: Exporting Phase 5 training data...")

    # Get optimal depths from analysis
    optimal_depths = results.get("optimal_depths", {})

    if not optimal_depths:
        print("\nWarning: No optimal depths determined")
        print("Using default depths...")
        optimal_depths = {
            "investor_profile": 2,
            "rfp_analysis": 3,
            "regional_analysis": 2,
            "simple_query": 1
        }

    exporter = OrchestratorExporter(log_directory)
    num_examples = exporter.export_training_data(
        output_dir=output_directory,
        optimal_depths=optimal_depths
    )

    summary_file = output_directory / "phase5_summary.json"
    exporter.export_summary(summary_file, optimal_depths)

    # Register with Phase 0
    phase0 = get_phase0_integration(Path("data"), test_mode=test_mode)
    if phase0["available"]:
        train_file = output_directory / "orchestrator_training.json"
        chat_file = output_directory / "orchestrator_chat.jsonl"

        if train_file.exists() and chat_file.exists():
            phase0["data_registry"].register_phase5_export(
                dataset_id="phase-4/discovery/orchestrator-export/v1",
                train_path=train_file,
                chat_path=chat_file,
                num_examples=num_examples,
                optimal_depths=optimal_depths,
                tags=["orchestrator", "phase5-export", "routing"]
            )

    # Final summary
    print(f"\n{'='*80}")
    print("Pipeline Complete")
    print(f"{'='*80}\n")
    print(f"Analysis results: {analysis_file}")
    print(f"Training examples: {num_examples}")
    print(f"Phase 5 summary: {summary_file}")
    print(f"\nNext steps:")
    print(f"  1. Review analysis results in {analysis_file}")
    print(f"  2. Use orchestrator_chat.jsonl for Phase 5 training")
    print(f"  3. Implement orchestrator with optimal depths: {optimal_depths}")
    print()


def show_analysis_summary(log_directory: Path):
    """
    Show quick summary of discovery results.

    Args:
        log_directory: Directory containing discovery logs
    """
    from ..shared.call_logger import A2ACallLogger

    logger = A2ACallLogger(log_directory)

    print(f"\n{'='*80}")
    print("Discovery Results Summary")
    print(f"{'='*80}\n")

    # Get stats for each phase
    for phase in range(1, 8):
        stats = logger.get_phase_stats(phase)

        if stats["total_calls"] > 0:
            print(f"Phase {phase}: {stats['total_calls']} calls, "
                  f"{stats['success_rate']:.1%} success, "
                  f"avg depth {stats['avg_depth']:.1f}")

    print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 4: Adaptive Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick summary
  python -m src.program4_adaptive_analyzer.main --summary

  # Analyze results
  python -m src.program4_adaptive_analyzer.main --analyze

  # Export for Phase 5
  python -m src.program4_adaptive_analyzer.main --export-phase5

  # Full pipeline
  python -m src.program4_adaptive_analyzer.main --full-pipeline
        """
    )

    # Operation mode
    parser.add_argument("--summary", action="store_true",
                       help="Show quick summary of results")
    parser.add_argument("--analyze", action="store_true",
                       help="Analyze discovery results")
    parser.add_argument("--export-phase5", action="store_true",
                       help="Export training data for Phase 5")
    parser.add_argument("--full-pipeline", action="store_true",
                       help="Run full analysis and export pipeline")

    # Optional parameters
    parser.add_argument("--log-dir", type=Path,
                       default=Path("data/logs/discovery"),
                       help="Discovery log directory (default: data/logs/discovery)")
    parser.add_argument("--output-dir", type=Path,
                       default=Path("data/exports"),
                       help="Output directory (default: data/exports)")
    parser.add_argument("--test-mode", action="store_true",
                       help="Use test mode")

    args = parser.parse_args()

    # Validate that at least one operation is specified
    if not any([args.summary, args.analyze, args.export_phase5, args.full_pipeline]):
        parser.error("Must specify at least one operation")

    try:
        # Check if log directory exists
        if not args.log_dir.exists():
            print(f"Error: Log directory not found: {args.log_dir}")
            print("Run discovery pipeline first with:")
            print("  python -m src.program3_discovery_pipeline.main --run --test-mode")
            sys.exit(1)

        # Run operations
        if args.summary:
            show_analysis_summary(args.log_dir)

        if args.analyze:
            results = analyze_results(args.log_dir, save_results=True)

        if args.export_phase5:
            # Load optimal depths if analysis exists
            analysis_file = args.output_dir / "analysis_results.json"
            if analysis_file.exists():
                with open(analysis_file) as f:
                    analysis = json.load(f)
                    optimal_depths = analysis.get("optimal_depths", {})
            else:
                print("Warning: No analysis results found, using defaults")
                optimal_depths = {
                    "investor_profile": 2,
                    "rfp_analysis": 3,
                    "regional_analysis": 2,
                    "simple_query": 1
                }

            export_phase5_data(args.log_dir, optimal_depths, args.output_dir)

        if args.full_pipeline:
            full_pipeline(args.log_dir, args.output_dir, args.test_mode)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        if args.test_mode:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
