"""
Discovery Pipeline Runner

Executes the 90-day adaptive depth discovery experiment.
"""

import random
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import httpx
from datetime import datetime
import uuid

from .phase_config import DiscoveryPhases, WorkflowLibrary, PhaseConfig, WorkflowConfig
from ..shared.a2a_protocol import A2ARequest, A2AResponse, A2AMetadata, ResponseStatus
from ..shared.call_logger import A2ACallLogger


class DiscoveryPipelineRunner:
    """
    Runs the discovery pipeline experiment.

    Simulates realistic workflows across all discovery phases,
    logging all A2A calls for later analysis.
    """

    def __init__(
        self,
        agent_base_url: str = "http://localhost",
        agent_ports: Optional[Dict[str, int]] = None,
        log_directory: Optional[Path] = None,
        test_mode: bool = False
    ):
        """
        Initialize pipeline runner.

        Args:
            agent_base_url: Base URL for agent services
            agent_ports: Dictionary mapping agent IDs to port numbers
            log_directory: Where to store discovery logs
            test_mode: If True, use compressed test schedule
        """
        self.agent_base_url = agent_base_url
        self.agent_ports = agent_ports or {
            "fundraising-agent": 8001,
            "business-development-agent": 8002,
            "field-operations-agent": 8003
        }
        self.test_mode = test_mode

        # Initialize phases
        self.phases = DiscoveryPhases()
        if test_mode:
            self.schedule = self.phases.get_test_schedule()
        else:
            self.schedule = self.phases.get_all_phases()

        # Initialize workflows
        self.workflows = WorkflowLibrary.get_all_workflows()

        # Initialize logger
        log_dir = log_directory or Path("data/logs/discovery")
        self.logger = A2ACallLogger(log_dir)

        # Statistics
        self.stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "by_phase": {}
        }

    def run(self, queries_per_day: int = 10) -> Dict[str, Any]:
        """
        Run the full discovery pipeline.

        Args:
            queries_per_day: Number of queries to run per day

        Returns:
            Summary statistics
        """
        print(f"\n{'='*80}")
        print(f"Discovery Pipeline {'(Test Mode)' if self.test_mode else '(90-Day Experiment)'}")
        print(f"{'='*80}\n")

        # Print schedule
        self.phases.print_schedule(self.test_mode)

        print(f"Running {queries_per_day} queries per day...")
        print(f"Total days: {len(self.schedule)}")
        print(f"Total queries: {len(self.schedule) * queries_per_day}\n")

        # Run each phase
        for phase in self.schedule:
            self._run_phase(phase, queries_per_day)

        # Print final statistics
        self._print_statistics()

        return self.stats

    def _run_phase(self, phase: PhaseConfig, queries_per_day: int) -> None:
        """
        Run a single discovery phase.

        Args:
            phase: Phase configuration
            queries_per_day: Number of queries per day
        """
        print(f"\nPhase {phase.phase_number}: {phase.name}")
        print(f"  Days {phase.start_day}-{phase.end_day}, Depth={phase.max_depth}")
        print(f"  {'-'*60}")

        # Set logger phase
        self.logger.set_phase(phase.phase_number)

        # Initialize phase stats
        phase_stats = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "avg_execution_time": 0
        }

        total_execution_time = 0

        # Run queries for each day in phase
        for day in range(phase.start_day, phase.end_day + 1):
            print(f"  Day {day}: ", end="", flush=True)

            day_successful = 0

            for query_num in range(queries_per_day):
                # Select random workflow
                workflow = random.choice(self.workflows)

                # Determine depth for this query
                if phase.adaptive:
                    # In adaptive phase, use workflow's typical depth
                    max_depth = workflow.typical_depth
                else:
                    # Use phase's fixed depth
                    max_depth = phase.max_depth

                # Generate query
                query = self._generate_query(workflow)

                # Execute query
                result = self._execute_workflow(
                    workflow=workflow,
                    query=query,
                    max_depth=max_depth,
                    phase_number=phase.phase_number
                )

                # Update stats
                phase_stats["total"] += 1
                if result["success"]:
                    phase_stats["successful"] += 1
                    day_successful += 1
                else:
                    phase_stats["failed"] += 1

                total_execution_time += result.get("execution_time_ms", 0)

            print(f"{day_successful}/{queries_per_day} successful")

        # Calculate averages
        if phase_stats["total"] > 0:
            phase_stats["avg_execution_time"] = total_execution_time / phase_stats["total"]

        # Store phase stats
        self.stats["by_phase"][phase.phase_number] = phase_stats

        # Update totals
        self.stats["total_queries"] += phase_stats["total"]
        self.stats["successful_queries"] += phase_stats["successful"]
        self.stats["failed_queries"] += phase_stats["failed"]

        print(f"  Phase complete: {phase_stats['successful']}/{phase_stats['total']} successful")

    def _execute_workflow(
        self,
        workflow: WorkflowConfig,
        query: str,
        max_depth: int,
        phase_number: int
    ) -> Dict[str, Any]:
        """
        Execute a single workflow query.

        Args:
            workflow: Workflow configuration
            query: Query string
            max_depth: Maximum cascade depth
            phase_number: Current phase number

        Returns:
            Execution result
        """
        # Build A2A request
        request = A2ARequest(
            goal=query,
            target=workflow.entry_agent,
            parameters={},
            metadata=A2AMetadata(
                call_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                call_depth=0,
                max_depth=max_depth,
                source_agent="discovery-pipeline",
                target_agent=workflow.entry_agent
            )
        )

        # Get agent URL
        port = self.agent_ports.get(workflow.entry_agent)
        if not port:
            return {
                "success": False,
                "error": f"No port configured for {workflow.entry_agent}"
            }

        url = f"{self.agent_base_url}:{port}/a2a"

        try:
            # Make request
            response = httpx.post(
                url,
                json=request.to_dict(),
                timeout=10.0
            )
            response.raise_for_status()

            # Parse response
            a2a_response = A2AResponse.from_dict(response.json())

            # Log the call (logger will handle it internally)
            # Note: The agent service already logs, but we could double-log here if needed

            return {
                "success": a2a_response.status == ResponseStatus.SUCCESS,
                "status": a2a_response.status.value,
                "execution_time_ms": a2a_response.execution_time_ms,
                "cascaded_calls": len(a2a_response.cascaded_calls)
            }

        except httpx.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _generate_query(self, workflow: WorkflowConfig) -> str:
        """
        Generate a query for a workflow.

        Args:
            workflow: Workflow configuration

        Returns:
            Generated query string
        """
        # Select random query template
        template = random.choice(workflow.queries)

        # Fill in parameters
        params = {
            "id": str(random.randint(100, 999)),
            "country": random.choice(["Kenya", "Ghana", "Nigeria", "Tanzania"])
        }

        query = template.format(**params)
        return query

    def _print_statistics(self) -> None:
        """Print final pipeline statistics"""
        print(f"\n{'='*80}")
        print("Discovery Pipeline Results")
        print(f"{'='*80}\n")

        print(f"Total queries: {self.stats['total_queries']}")
        print(f"Successful: {self.stats['successful_queries']}")
        print(f"Failed: {self.stats['failed_queries']}")

        if self.stats['total_queries'] > 0:
            success_rate = (self.stats['successful_queries'] / self.stats['total_queries']) * 100
            print(f"Success rate: {success_rate:.1f}%")

        print(f"\nBy Phase:")
        print(f"{'Phase':<6} {'Name':<20} {'Total':<8} {'Success':<8} {'Failed':<8} {'Success Rate':<12}")
        print(f"{'-'*80}")

        for phase_num, phase_stats in sorted(self.stats['by_phase'].items()):
            phase = self.phases.get_phase(phase_num)
            if not phase:
                phase_name = f"Phase {phase_num}"
            else:
                phase_name = phase.name

            total = phase_stats['total']
            successful = phase_stats['successful']
            failed = phase_stats['failed']
            success_rate = (successful / total * 100) if total > 0 else 0

            print(f"{phase_num:<6} {phase_name:<20} {total:<8} {successful:<8} {failed:<8} {success_rate:<12.1f}%")

        print()

    def analyze_phase_results(self, phase_number: int) -> Dict[str, Any]:
        """
        Analyze results for a specific phase.

        Args:
            phase_number: Phase to analyze

        Returns:
            Analysis results
        """
        # Get phase stats from logger
        phase_stats = self.logger.get_phase_stats(phase_number)

        return phase_stats

    def export_results(self, output_file: Path) -> None:
        """
        Export all results for analysis.

        Args:
            output_file: Path to output file
        """
        self.logger.export_for_analysis(output_file)
        print(f"\nResults exported to: {output_file}")
