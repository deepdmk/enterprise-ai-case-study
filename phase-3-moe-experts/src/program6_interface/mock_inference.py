"""
Mock MoE Inference for Test Mode.

Provides canned responses and simulated expert activations
for testing the interface without GPU/model loading.
"""

import json
import random
from dataclasses import dataclass, field
from pathlib import Path

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class ExpertActivation:
    """Represents activation of a single expert."""

    expert_id: int
    task_id: str
    model_id: str
    activation_score: float


@dataclass
class MockInferenceResult:
    """Result from mock inference."""

    response: str
    activations: list[ExpertActivation] = field(default_factory=list)
    tokens_generated: int = 0


# Canned responses by unit and keyword patterns
CANNED_RESPONSES = {
    "fundraising": {
        "investor": """Based on the investor profile analysis, I recommend focusing on foundations with a track record in sustainable development:

1. **Gates Foundation** - Strong alignment with health and agricultural initiatives
2. **Ford Foundation** - Interest in social justice and economic opportunity
3. **Hewlett Foundation** - Focus on education and environmental programs

These investors have historically funded projects with similar scope and objectives.""",
        "funding": """The funding landscape analysis reveals several promising opportunities:

- **USAID Development Innovation Ventures** - Open call, $1M-5M range
- **EU Horizon Europe** - Climate adaptation focus, deadline Q2
- **World Bank Trust Funds** - Infrastructure development grants

Recommend prioritizing applications based on our current capacity and strategic alignment.""",
        "proposal": """Proposal evaluation complete. Key strengths and areas for improvement:

**Strengths:**
- Clear theory of change with measurable outcomes
- Strong local partnership network
- Competitive budget with reasonable overhead

**Areas to Address:**
- Strengthen sustainability plan beyond project period
- Add more detail on risk mitigation strategies
- Include letters of support from key stakeholders""",
        "default": """Fundraising analysis complete. Based on the current portfolio and market conditions, I recommend reviewing the strategic funding priorities and aligning outreach efforts with high-probability opportunities.""",
    },
    "business_development": {
        "rfp": """RFP Analysis Summary:

**Solicitation:** USAID/Kenya Health Systems Strengthening
**Value:** $15-25M over 5 years
**Deadline:** 45 days

**Key Requirements:**
- Prime must have 3+ similar projects in region
- DUNS registration and SAM.gov active
- Cost-share: 10% minimum

**Competitive Landscape:**
- Likely 4-6 bidders based on historical data
- Key competitors: Abt, DAI, Chemonics

Recommend GO decision with teaming strategy.""",
        "competitive": """Competitive landscape analysis for the East Africa market:

**Market Position:**
- We rank #4 in regional presence
- Growing market share in health sector
- Strong local partner network

**Key Competitors:**
1. DAI - Strongest USAID relationship
2. Chemonics - Largest local staff presence
3. RTI - Technical expertise advantage

**Strategic Recommendations:**
- Strengthen teaming partnerships
- Invest in local recruitment
- Develop differentiated technical approach""",
        "proposal": """Proposal scoring assessment:

**Technical Approach:** 85/100
- Strong methodology section
- Clear management plan
- Innovative M&E framework

**Past Performance:** 78/100
- 3 relevant references
- Some gaps in regional experience

**Cost:** 82/100
- Competitive rate structure
- Reasonable LOE assumptions

**Overall:** Strong competitive position, recommend proceeding.""",
        "default": """Business development analysis indicates favorable conditions for expansion in the target sector. Current win rate trends and pipeline analysis support continued investment in proposal development capacity.""",
    },
    "field_operations": {
        "market": """Local market intelligence report:

**Economic Indicators:**
- GDP growth: 5.2% YoY
- Currency stability: Moderate risk
- Inflation: 7.8%

**Operational Environment:**
- Political stability: Green
- Security situation: Yellow (regional variation)
- Infrastructure: Improving, road network expanded 15%

**Recommendations:**
- Proceed with planned expansion
- Maintain currency hedging strategy
- Monitor regional security developments""",
        "project": """Project performance dashboard:

**Program: Community Health Initiative - Kenya**

**Output Indicators:**
- Health workers trained: 450/500 (90%)
- Facilities upgraded: 28/30 (93%)
- Community sessions: 1,200/1,000 (120%)

**Outcome Progress:**
- Service utilization: +35% vs baseline
- Patient satisfaction: 4.2/5.0

**Risk Status:** Green
**Budget Burn Rate:** 72% at month 9 (on track)

Next quarterly review scheduled for March.""",
        "partner": """Partner assessment for proposed subcontractor:

**Organization:** Local Health NGO (LHNO)

**Capacity Scores:**
- Technical expertise: 4/5
- Financial management: 3/5
- M&E systems: 3/5
- Local presence: 5/5

**Due Diligence Findings:**
- Clean audit history (3 years)
- Strong community relationships
- Some gaps in procurement procedures

**Recommendation:** Approve with capacity building plan and enhanced monitoring for first 6 months.""",
        "risk": """Risk assessment summary:

**High Priority Risks:**
1. Currency fluctuation - IMPACT: High, LIKELIHOOD: Medium
   - Mitigation: Forward contracts in place

2. Staff turnover - IMPACT: Medium, LIKELIHOOD: High
   - Mitigation: Retention bonuses, career pathways

3. Supply chain disruption - IMPACT: High, LIKELIHOOD: Low
   - Mitigation: Local sourcing alternatives identified

**Overall Risk Level:** Moderate
**Risk trend:** Stable

Next assessment due in 30 days.""",
        "default": """Field operations analysis indicates stable conditions across active project sites. Key performance indicators are tracking to target, with minor variations requiring attention in logistics and partner coordination.""",
    },
}


class MockMoEInference:
    """
    Mock MoE inference engine for test mode.

    Loads expert registries and returns canned responses
    with simulated expert activations.
    """

    def __init__(self, exports_dir: Path, experts_per_token: int = 2):
        """
        Initialize mock inference engine.

        Args:
            exports_dir: Path to phase4_test exports directory.
            experts_dir: Number of experts activated per token.
        """
        self.exports_dir = Path(exports_dir)
        self.experts_per_token = experts_per_token
        self.expert_registries: dict[str, dict] = {}

        self._load_expert_registries()

        logger.info(
            "mock_inference_initialized",
            exports_dir=str(self.exports_dir),
            units_loaded=list(self.expert_registries.keys()),
        )

    def _load_expert_registries(self) -> None:
        """Load expert registries for all units."""
        for unit_dir in self.exports_dir.iterdir():
            if not unit_dir.is_dir():
                continue

            registry_path = unit_dir / "routing" / "expert_registry.json"
            if registry_path.exists():
                with open(registry_path) as f:
                    self.expert_registries[unit_dir.name] = json.load(f)
                logger.debug(
                    "expert_registry_loaded",
                    unit=unit_dir.name,
                    num_experts=len(self.expert_registries[unit_dir.name].get("experts", {})),
                )

    def get_available_units(self) -> list[str]:
        """Get list of available units."""
        return list(self.expert_registries.keys())

    def generate(
        self,
        unit_id: str,
        prompt: str,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> MockInferenceResult:
        """
        Generate a mock response with simulated expert activations.

        Args:
            unit_id: Unit to use for generation.
            prompt: User prompt.
            max_new_tokens: Maximum tokens (used for simulation).
            temperature: Temperature (used for activation variance).
            top_p: Top-p (unused in mock).

        Returns:
            MockInferenceResult with response and activations.
        """
        if unit_id not in self.expert_registries:
            return MockInferenceResult(
                response=f"Error: Unit '{unit_id}' not found. Available units: {self.get_available_units()}",
                activations=[],
                tokens_generated=0,
            )

        # Select response based on keywords in prompt
        response = self._select_response(unit_id, prompt)

        # Simulate expert activations
        activations = self._simulate_activations(unit_id, prompt, temperature)

        # Estimate tokens generated
        tokens_generated = min(len(response.split()) * 1.3, max_new_tokens)

        logger.info(
            "mock_generation_complete",
            unit_id=unit_id,
            prompt_length=len(prompt),
            response_length=len(response),
            num_activations=len(activations),
        )

        return MockInferenceResult(
            response=response,
            activations=activations,
            tokens_generated=int(tokens_generated),
        )

    def _select_response(self, unit_id: str, prompt: str) -> str:
        """Select appropriate canned response based on prompt keywords."""
        prompt_lower = prompt.lower()
        unit_responses = CANNED_RESPONSES.get(unit_id, {})

        # Check for keyword matches
        for keyword, response in unit_responses.items():
            if keyword != "default" and keyword in prompt_lower:
                return response

        # Return default response for unit
        return unit_responses.get(
            "default",
            f"Analysis complete for {unit_id}. Please provide more specific requirements for detailed recommendations.",
        )

    def _simulate_activations(
        self,
        unit_id: str,
        prompt: str,
        temperature: float,
    ) -> list[ExpertActivation]:
        """Simulate expert activations based on prompt."""
        registry = self.expert_registries.get(unit_id, {})
        experts = registry.get("experts", {})

        if not experts:
            return []

        # Convert experts dict to list
        expert_list = list(experts.values())

        # Select top-k experts (simulate MoE routing)
        num_to_activate = min(self.experts_per_token, len(expert_list))
        activated = random.sample(expert_list, num_to_activate)

        # Generate activation scores with some variance based on temperature
        activations = []
        base_score = 0.7
        for i, expert in enumerate(activated):
            # Higher scores for first expert, add temperature-based variance
            score = base_score + (0.2 * (num_to_activate - i) / num_to_activate)
            score += random.uniform(-0.1 * temperature, 0.1 * temperature)
            score = max(0.1, min(1.0, score))

            activations.append(
                ExpertActivation(
                    expert_id=expert["expert_id"],
                    task_id=expert["task_id"],
                    model_id=expert["model_id"],
                    activation_score=round(score, 4),
                )
            )

        # Sort by activation score descending
        activations.sort(key=lambda x: x.activation_score, reverse=True)

        return activations
