"""
Discovery Phase Configuration

Defines the 7-phase, 90-day adaptive depth discovery experiment.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class PhaseConfig:
    """
    Configuration for a single discovery phase.

    Attributes:
        phase_number: Phase number (1-7)
        name: Phase name
        start_day: Starting day (1-90)
        end_day: Ending day (1-90)
        max_depth: Maximum cascade depth for this phase
        purpose: Purpose/goal of this phase
        adaptive: Whether this phase uses adaptive depth
    """
    phase_number: int
    name: str
    start_day: int
    end_day: int
    max_depth: int
    purpose: str
    adaptive: bool = False

    @property
    def duration_days(self) -> int:
        """Calculate phase duration"""
        return self.end_day - self.start_day + 1

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "phase_number": self.phase_number,
            "name": self.name,
            "start_day": self.start_day,
            "end_day": self.end_day,
            "duration_days": self.duration_days,
            "max_depth": self.max_depth,
            "purpose": self.purpose,
            "adaptive": self.adaptive
        }


class DiscoveryPhases:
    """
    Manages the 7-phase discovery experiment schedule.

    Phase Schedule:
    1. Days 1-7: Depth 1 (Baseline, no cascading)
    2. Days 8-21: Depth 2 (Single cascade)
    3. Days 22-35: Depth 3 (Two-level cascade)
    4. Days 36-49: Depth 2 (Control #1)
    5. Days 50-63: Depth 4 (Outer bounds)
    6. Days 64-75: Depth 2 (Control #2)
    7. Days 76-90: Adaptive (Per-workflow optimization)
    """

    def __init__(self):
        self.phases = self._initialize_phases()

    def _initialize_phases(self) -> list[PhaseConfig]:
        """Initialize all 7 phases"""
        return [
            PhaseConfig(
                phase_number=1,
                name="Baseline",
                start_day=1,
                end_day=7,
                max_depth=1,
                purpose="Establish baseline without cascading calls",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=2,
                name="Single Cascade",
                start_day=8,
                end_day=21,
                max_depth=2,
                purpose="Evaluate single-level cascading effectiveness",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=3,
                name="Two-Level Cascade",
                start_day=22,
                end_day=35,
                max_depth=3,
                purpose="Test two-level cascade depth",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=4,
                name="Control #1",
                start_day=36,
                end_day=49,
                max_depth=2,
                purpose="Validate depth-2 performance consistency",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=5,
                name="Outer Bounds",
                start_day=50,
                end_day=63,
                max_depth=4,
                purpose="Explore maximum cascade depth limits",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=6,
                name="Control #2",
                start_day=64,
                end_day=75,
                max_depth=2,
                purpose="Final depth-2 validation before adaptive",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=7,
                name="Adaptive",
                start_day=76,
                end_day=90,
                max_depth=3,  # Default, will vary by workflow
                purpose="Per-workflow adaptive depth optimization",
                adaptive=True
            )
        ]

    def get_phase(self, phase_number: int) -> Optional[PhaseConfig]:
        """Get phase by number"""
        for phase in self.phases:
            if phase.phase_number == phase_number:
                return phase
        return None

    def get_phase_for_day(self, day: int) -> Optional[PhaseConfig]:
        """Get which phase a given day falls in"""
        for phase in self.phases:
            if phase.start_day <= day <= phase.end_day:
                return phase
        return None

    def get_all_phases(self) -> list[PhaseConfig]:
        """Get all phases"""
        return self.phases

    def get_test_schedule(self) -> list[PhaseConfig]:
        """
        Get compressed test schedule (7 days instead of 90).

        Each phase gets 1 day.
        """
        return [
            PhaseConfig(
                phase_number=1,
                name="Baseline",
                start_day=1,
                end_day=1,
                max_depth=1,
                purpose="Baseline test",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=2,
                name="Single Cascade",
                start_day=2,
                end_day=2,
                max_depth=2,
                purpose="Single cascade test",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=3,
                name="Two-Level Cascade",
                start_day=3,
                end_day=3,
                max_depth=3,
                purpose="Two-level test",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=4,
                name="Control #1",
                start_day=4,
                end_day=4,
                max_depth=2,
                purpose="Control test #1",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=5,
                name="Outer Bounds",
                start_day=5,
                end_day=5,
                max_depth=4,
                purpose="Outer bounds test",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=6,
                name="Control #2",
                start_day=6,
                end_day=6,
                max_depth=2,
                purpose="Control test #2",
                adaptive=False
            ),
            PhaseConfig(
                phase_number=7,
                name="Adaptive",
                start_day=7,
                end_day=7,
                max_depth=3,
                purpose="Adaptive test",
                adaptive=True
            )
        ]

    def print_schedule(self, test_mode: bool = False):
        """Print the phase schedule"""
        phases = self.get_test_schedule() if test_mode else self.phases

        print(f"\n{'='*80}")
        print(f"Discovery Phase Schedule ({'Test Mode' if test_mode else '90-Day Experiment'})")
        print(f"{'='*80}\n")

        print(f"{'Phase':<6} {'Name':<20} {'Days':<12} {'Depth':<7} {'Purpose':<30}")
        print(f"{'-'*80}")

        for phase in phases:
            days_range = f"{phase.start_day}-{phase.end_day}"
            depth = f"{phase.max_depth}{'*' if phase.adaptive else ''}"
            print(f"{phase.phase_number:<6} {phase.name:<20} {days_range:<12} {depth:<7} {phase.purpose:<30}")

        print(f"\n{'*adaptive' if any(p.adaptive for p in phases) else ''}")
        print()


@dataclass
class WorkflowConfig:
    """
    Configuration for a test workflow.

    Workflows are used to generate realistic agent interaction patterns
    during the discovery experiment.
    """
    workflow_id: str
    name: str
    description: str
    entry_agent: str  # Which agent starts this workflow
    typical_depth: int  # Expected cascade depth for this workflow
    queries: list[str]  # Example queries for this workflow

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "entry_agent": self.entry_agent,
            "typical_depth": self.typical_depth,
            "queries": self.queries
        }


class WorkflowLibrary:
    """
    Library of test workflows for discovery experiments.
    """

    @staticmethod
    def get_all_workflows() -> list[WorkflowConfig]:
        """Get all test workflows"""
        return [
            WorkflowConfig(
                workflow_id="investor_profile",
                name="Investor Profile",
                description="Get comprehensive investor profile",
                entry_agent="fundraising-agent",
                typical_depth=2,
                queries=[
                    "Profile investor INV-{id} including competitive landscape",
                    "Analyze investor INV-{id} with local presence data",
                    "Comprehensive analysis of investor INV-{id}"
                ]
            ),
            WorkflowConfig(
                workflow_id="rfp_analysis",
                name="RFP Analysis",
                description="Analyze RFP with investor and capacity data",
                entry_agent="business-development-agent",
                typical_depth=3,
                queries=[
                    "Analyze RFP-{id} including potential investors and local capacity",
                    "Full competitive analysis for RFP-{id}",
                    "Match RFP-{id} with investors and regional capabilities"
                ]
            ),
            WorkflowConfig(
                workflow_id="regional_analysis",
                name="Regional Analysis",
                description="Regional capacity with funding opportunities",
                entry_agent="field-operations-agent",
                typical_depth=2,
                queries=[
                    "Regional analysis for {country} including investors and RFPs",
                    "Comprehensive capacity assessment for {country}",
                    "Analyze {country} office with funding landscape"
                ]
            ),
            WorkflowConfig(
                workflow_id="simple_query",
                name="Simple Query",
                description="Direct query without cascading",
                entry_agent="fundraising-agent",
                typical_depth=1,
                queries=[
                    "What is the capacity of investor INV-{id}?",
                    "List sectors for investor INV-{id}",
                    "Show recent activity for investor INV-{id}"
                ]
            )
        ]

    @staticmethod
    def get_workflow(workflow_id: str) -> Optional[WorkflowConfig]:
        """Get specific workflow by ID"""
        for workflow in WorkflowLibrary.get_all_workflows():
            if workflow.workflow_id == workflow_id:
                return workflow
        return None
