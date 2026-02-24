"""Mock data generator for test mode training.

WARNING: This module generates synthetic data for pipeline verification ONLY.
Do NOT use mock data for production model training. Models trained on synthetic
data will not perform well on real tasks.

For production training, prepare real domain data and place it in:
    data/raw/{unit}/{task}/*.jsonl

Then run without --test-mode flag:
    python -m src.program1_data_preparation.main --unit <unit_id>
"""

import random
from pathlib import Path
from typing import Any

# Configure paths - centralizes sys.path manipulation
from src.shared.path_config import configure_paths

configure_paths()

# Now import from both local config and phase-0-infrastructure
from config.settings import TaskDefinition
from habitat_logging import get_logger

logger = get_logger(__name__)

# Domain-specific templates for each unit/task combination
MOCK_TEMPLATES = {
    # Fundraising Unit
    "fundraising": {
        "investor_profiling": {
            "inputs": [
                "Profile investor {name} who focuses on {sector} startups",
                "Create a comprehensive profile for {name}, an angel investor in {location}",
                "Analyze the investment history of {name}",
                "What is the investment thesis of {name}?",
                "Provide background on angel investor {name} who has invested in {num} companies",
            ],
            "output_template": """## Investment Thesis
{name} focuses on {sector} investments, typically at the {stage} stage.

## Historical Patterns
- Average check size: ${check_size}
- Investments per year: {investments_per_year}
- Preferred sectors: {sector}, {secondary_sector}

## Preferences
- Stage: {stage}
- Geography: {location}
- Team requirements: Technical founders preferred

## Key Insights
{name} shows strong preference for {sector} with proven traction. Co-invests frequently with {coinvestor}.""",
            "variables": {
                "name": [
                    "John Smith",
                    "Sarah Chen",
                    "Michael Johnson",
                    "Emily Rodriguez",
                    "David Kim",
                    "Lisa Wang",
                    "Robert Taylor",
                    "Jennifer Lee",
                ],
                "sector": [
                    "fintech",
                    "healthtech",
                    "cleantech",
                    "edtech",
                    "enterprise SaaS",
                    "consumer apps",
                    "AI/ML",
                    "biotech",
                ],
                "secondary_sector": [
                    "sustainability",
                    "digital health",
                    "marketplaces",
                    "developer tools",
                    "infrastructure",
                ],
                "location": [
                    "San Francisco",
                    "New York",
                    "Boston",
                    "Austin",
                    "Seattle",
                    "London",
                    "Singapore",
                ],
                "stage": ["pre-seed", "seed", "Series A"],
                "check_size": [
                    "25,000-50,000",
                    "50,000-100,000",
                    "100,000-250,000",
                    "250,000-500,000",
                ],
                "investments_per_year": ["3-5", "5-8", "8-12", "10-15"],
                "num": ["15", "25", "40", "60", "100"],
                "coinvestor": ["Sequoia scouts", "YC alumni network", "local angel groups"],
            },
        },
        "fit_assessment": {
            "inputs": [
                "Assess fit between {investor} and {company} in {sector}",
                "Is {investor} a good match for our {stage} {sector} startup?",
                "Evaluate alignment between {investor} and {company}",
                "Would {investor} be interested in {company}'s {sector} opportunity?",
            ],
            "output_template": """## Fit Score: {score}/100

## Alignment Analysis
- Sector alignment: {sector_fit}
- Stage alignment: {stage_fit}
- Check size compatibility: {check_fit}
- Geographic fit: {geo_fit}

## Potential Concerns
- {concern}

## Recommendation
{recommendation}""",
            "variables": {
                "investor": ["John Smith", "Sarah Chen", "Michael Johnson", "Emily Rodriguez"],
                "company": ["TechCo", "HealthStart", "GreenFuture", "EduLearn", "DataFlow"],
                "sector": ["fintech", "healthtech", "cleantech", "edtech", "enterprise SaaS"],
                "stage": ["pre-seed", "seed", "Series A"],
                "score": ["45", "62", "78", "85", "92"],
                "sector_fit": ["Strong - direct thesis match", "Moderate - adjacent interest", "Weak - outside focus"],
                "stage_fit": ["Excellent - preferred stage", "Good - within range", "Marginal - typically later"],
                "check_fit": ["Compatible", "Below typical range", "Above typical range"],
                "geo_fit": ["Strong local presence", "Remote but engaged", "No prior presence"],
                "concern": [
                    "Portfolio conflict with existing investment",
                    "Limited bandwidth currently",
                    "Check size may be too small",
                    "Geographic distance for board involvement",
                ],
                "recommendation": [
                    "Strong fit - prioritize outreach",
                    "Good potential - worth pursuing with warm intro",
                    "Moderate fit - include in broader list",
                    "Low priority - focus elsewhere first",
                ],
            },
        },
        "capacity_analysis": {
            "inputs": [
                "Analyze investment capacity for {investor}",
                "Can {investor} make new investments currently?",
                "Assess {investor}'s availability for new deals",
                "What is {investor}'s current investment capacity?",
            ],
            "output_template": """## Capacity Assessment: {capacity}

## Supporting Signals
- Recent activity: {recent_activity}
- Portfolio load: {portfolio_load}
- Market engagement: {engagement}

## Confidence Level: {confidence}

## Timing Recommendation
{timing}""",
            "variables": {
                "investor": ["John Smith", "Sarah Chen", "Michael Johnson"],
                "capacity": ["High", "Moderate", "Limited", "Uncertain"],
                "recent_activity": [
                    "3 investments in past 6 months",
                    "No new investments this quarter",
                    "Active at conferences",
                ],
                "portfolio_load": ["Light - 8 active companies", "Moderate - 15 companies", "Heavy - 25+ companies"],
                "engagement": ["Very active on LinkedIn", "Quiet recently", "Seeking new deals publicly"],
                "confidence": ["High (85%)", "Medium (65%)", "Low (40%)"],
                "timing": [
                    "Approach now - good window",
                    "Wait 2-3 months for current deal flow to settle",
                    "Proceed with caution - unclear bandwidth",
                ],
            },
        },
        "engagement_strategy": {
            "inputs": [
                "How should we approach {investor}?",
                "Generate engagement strategy for {investor}",
                "Best way to reach {investor} for our {sector} startup",
                "Create outreach plan for {investor}",
            ],
            "output_template": """## Approach Strategy
{approach}

## Key Messages
1. {message1}
2. {message2}
3. {message3}

## Timing
{timing}

## Action Items
- [ ] {action1}
- [ ] {action2}
- [ ] {action3}""",
            "variables": {
                "investor": ["John Smith", "Sarah Chen", "Michael Johnson"],
                "sector": ["fintech", "healthtech", "cleantech"],
                "approach": [
                    "Warm introduction via YC network",
                    "Direct LinkedIn outreach with portfolio reference",
                    "Conference meeting at upcoming event",
                ],
                "message1": [
                    "Reference their successful exit in similar space",
                    "Highlight shared connection through portfolio company",
                ],
                "message2": ["Emphasize traction metrics", "Share unique technical moat", "Discuss market timing"],
                "message3": ["Propose specific ask and timeline", "Offer demo/product walkthrough"],
                "timing": ["Reach out next week - quiet period for them", "Wait until after their board meetings"],
                "action1": ["Identify warm introduction path", "Prepare tailored deck"],
                "action2": ["Draft personalized email", "Research recent investments"],
                "action3": ["Schedule follow-up cadence", "Prepare for likely questions"],
            },
        },
        "portfolio_synthesis": {
            "inputs": [
                "Analyze portfolio patterns for {investor}",
                "What themes emerge from {investor}'s portfolio?",
                "Portfolio synthesis for {investor}",
                "Investment pattern analysis for {investor}",
            ],
            "output_template": """## Key Patterns
- Primary focus: {primary_focus}
- Secondary themes: {secondary_theme}
- Evolution: {evolution}

## Theme Analysis
{theme_analysis}

## Evolution Over Time
{evolution_detail}

## Strategic Insights
{insights}""",
            "variables": {
                "investor": ["John Smith", "Sarah Chen", "Michael Johnson"],
                "primary_focus": ["B2B SaaS with PLG motion", "Healthcare infrastructure", "Climate tech hardware"],
                "secondary_theme": [
                    "Developer tools",
                    "Data infrastructure",
                    "Vertical AI applications",
                ],
                "evolution": ["Expanding into adjacent markets", "Deepening sector focus", "Moving earlier stage"],
                "theme_analysis": [
                    "Strong preference for technical founding teams with prior startup experience",
                    "Focus on capital-efficient businesses with path to profitability",
                ],
                "evolution_detail": [
                    "Started in consumer, shifted to B2B in 2020",
                    "Consistently focused on healthcare since 2018",
                ],
                "insights": [
                    "Best approached with clear technical differentiation and strong unit economics",
                    "Values board involvement - prefers local companies",
                ],
            },
        },
    },
    # Field Operations Unit
    "field_operations": {
        "market_assessment": {
            "inputs": [
                "Assess market readiness in {country}",
                "Is {country} ready for {program_type} implementation?",
                "Market feasibility study for {country}",
                "Local market conditions in {country} for {program_type}",
            ],
            "output_template": """## Market Overview
{country} presents {overall_assessment} conditions for {program_type} implementation.

## Readiness Assessment
- Regulatory: {regulatory}
- Infrastructure: {infrastructure}
- Human capital: {human_capital}

## Key Enablers
- {enabler1}
- {enabler2}

## Key Barriers
- {barrier1}
- {barrier2}

## Recommendations
{recommendation}""",
            "variables": {
                "country": ["Kenya", "Nigeria", "Indonesia", "Philippines", "Colombia", "Egypt", "Bangladesh"],
                "program_type": ["microfinance", "agricultural extension", "digital health", "skills training"],
                "overall_assessment": ["favorable", "moderate", "challenging", "mixed"],
                "regulatory": ["Supportive framework", "Neutral environment", "Restrictive regulations"],
                "infrastructure": ["Strong digital infrastructure", "Limited connectivity", "Improving rapidly"],
                "human_capital": ["Skilled workforce available", "Training needs identified", "Partner capacity strong"],
                "enabler1": ["Mobile money penetration", "Government support", "Strong NGO ecosystem"],
                "enabler2": ["Youth population", "Growing middle class", "Technology adoption"],
                "barrier1": ["Political instability", "Currency volatility", "Infrastructure gaps"],
                "barrier2": ["Limited local partners", "Regulatory uncertainty", "Competition for talent"],
                "recommendation": [
                    "Proceed with pilot program",
                    "Delay until regulatory clarity",
                    "Partner with established local organization",
                ],
            },
        },
        "project_performance": {
            "inputs": [
                "Analyze performance of {project} in {country}",
                "How is {project} performing?",
                "Performance review for {project}",
                "Evaluate outcomes of {project}",
            ],
            "output_template": """## Performance Summary
{project} in {country}: {overall_status}

## Key Metrics
- Beneficiaries reached: {beneficiaries}
- Budget utilization: {budget}
- Timeline status: {timeline}

## Trend Analysis
{trend}

## Recommendations
{recommendation}""",
            "variables": {
                "project": ["Digital Skills Program", "Agricultural Support Initiative", "Health Access Project"],
                "country": ["Kenya", "Nigeria", "Indonesia", "Philippines"],
                "overall_status": ["On track", "Behind schedule", "Exceeding targets", "At risk"],
                "beneficiaries": ["12,500 of 15,000 target", "8,200 of 10,000 target", "25,000 of 20,000 target"],
                "budget": ["78% utilized", "92% utilized", "65% utilized"],
                "timeline": ["On schedule", "2 months delayed", "Ahead by 1 month"],
                "trend": ["Accelerating in Q4", "Slowdown due to seasonal factors", "Steady growth"],
                "recommendation": ["Maintain current approach", "Increase partner support", "Reallocate resources"],
            },
        },
        "capacity_mapping": {
            "inputs": [
                "Map local capacity in {country}",
                "What implementation capacity exists in {country}?",
                "Partner landscape analysis for {country}",
                "Resource mapping in {country}",
            ],
            "output_template": """## Capacity Overview
{country} has {overall_capacity} implementation capacity.

## Partner Analysis
- NGOs: {ngos}
- Government: {government}
- Private sector: {private_sector}

## Resource Inventory
{resources}

## Gaps and Needs
- {gap1}
- {gap2}

## Recommendations
{recommendation}""",
            "variables": {
                "country": ["Kenya", "Nigeria", "Indonesia", "Philippines", "Colombia"],
                "overall_capacity": ["strong", "moderate", "limited", "developing"],
                "ngos": ["15 qualified partners identified", "5 potential partners", "Limited NGO presence"],
                "government": ["Active ministry engagement", "Bureaucratic challenges", "Strong local government"],
                "private_sector": ["Growing social enterprise sector", "Limited CSR engagement", "Active impact investors"],
                "resources": ["Technical training centers available", "Limited rural infrastructure", "Strong urban presence"],
                "gap1": ["M&E expertise", "Financial management capacity", "Technical specialists"],
                "gap2": ["Rural reach", "Youth engagement", "Digital infrastructure"],
                "recommendation": ["Build local partner capacity", "Import expertise initially", "Partner with regional hub"],
            },
        },
        "demand_forecasting": {
            "inputs": [
                "Forecast demand for {program_type} in {country}",
                "What is expected demand in {country}?",
                "Demand projection for {region}",
                "Predict program uptake in {country}",
            ],
            "output_template": """## Demand Forecast
{program_type} in {country}: {forecast}

## Methodology
{methodology}

## Key Drivers
- {driver1}
- {driver2}

## Scenarios
- Optimistic: {optimistic}
- Base case: {base_case}
- Conservative: {conservative}

## Confidence Assessment
{confidence}""",
            "variables": {
                "program_type": ["microfinance", "agricultural extension", "digital health", "skills training"],
                "country": ["Kenya", "Nigeria", "Indonesia", "Philippines"],
                "region": ["East Africa", "West Africa", "Southeast Asia", "Latin America"],
                "forecast": ["25,000 beneficiaries in Year 1", "50,000 by 2025", "100,000 over 3 years"],
                "methodology": ["Historical uptake analysis with demographic adjustment", "Peer country comparison"],
                "driver1": ["Population growth in target segment", "Government policy support", "Mobile penetration"],
                "driver2": ["Economic conditions", "Competitor activity", "Seasonal factors"],
                "optimistic": ["35,000 (+40%)", "75,000", "150,000"],
                "base_case": ["25,000", "50,000", "100,000"],
                "conservative": ["18,000 (-28%)", "35,000", "70,000"],
                "confidence": ["High confidence (80%)", "Medium confidence (65%)", "Low confidence (45%)"],
            },
        },
    },
    # Business Development Unit
    "business_development": {
        "rfp_analysis": {
            "inputs": [
                "Analyze RFP from {funder} for {program_type}",
                "What are the requirements for {funder}'s RFP?",
                "Extract criteria from {funder} opportunity",
                "RFP analysis for {opportunity_name}",
            ],
            "output_template": """## Eligibility Requirements
- Organization type: {org_type}
- Geographic presence: {geography}
- Prior experience: {experience}

## Technical Requirements
- {tech_req1}
- {tech_req2}

## Evaluation Criteria
| Criterion | Weight |
|-----------|--------|
| Technical approach | {weight1}% |
| Past performance | {weight2}% |
| Cost | {weight3}% |

## Key Dates
- Questions due: {questions_date}
- Submission deadline: {deadline}

## Compliance Checklist
- [ ] {checklist1}
- [ ] {checklist2}
- [ ] {checklist3}""",
            "variables": {
                "funder": ["USAID", "World Bank", "Gates Foundation", "DFID", "EU", "GIZ"],
                "program_type": ["health systems", "agricultural development", "education", "climate adaptation"],
                "opportunity_name": ["Global Health Initiative", "Rural Development Program", "Digital Inclusion"],
                "org_type": ["501(c)(3) or equivalent", "International NGO", "Consortium eligible"],
                "geography": ["Must have presence in target countries", "Headquarters in DAC country"],
                "experience": ["5+ years in sector", "Prior USAID experience preferred", "$10M+ similar projects"],
                "tech_req1": ["Evidence-based methodology", "M&E framework required", "Gender integration"],
                "tech_req2": ["Local partner involvement", "Sustainability plan", "Innovation component"],
                "weight1": ["40", "50", "35"],
                "weight2": ["30", "25", "35"],
                "weight3": ["30", "25", "30"],
                "questions_date": ["January 15", "February 1", "March 10"],
                "deadline": ["February 28", "March 15", "April 30"],
                "checklist1": ["SAM.gov registration", "DUNS number", "Audit reports"],
                "checklist2": ["Past performance references", "Key personnel CVs", "Budget template"],
                "checklist3": ["Technical narrative (20 pages)", "Management plan", "Cost proposal"],
            },
        },
        "competitive_positioning": {
            "inputs": [
                "Analyze competitors for {opportunity}",
                "Who are we competing against for {funder} opportunity?",
                "Competitive landscape for {program_type} bid",
                "Competition assessment for {opportunity}",
            ],
            "output_template": """## Competitor Overview
{num_competitors} likely competitors identified for {opportunity}.

## Comparative Analysis
| Competitor | Strength | Weakness |
|------------|----------|----------|
| {comp1} | {strength1} | {weakness1} |
| {comp2} | {strength2} | {weakness2} |

## Competitive Advantages
- {advantage1}
- {advantage2}

## Vulnerabilities
- {vulnerability}

## Positioning Recommendations
{positioning}""",
            "variables": {
                "opportunity": ["USAID Health Program", "World Bank Education Grant", "Gates Foundation Initiative"],
                "funder": ["USAID", "World Bank", "Gates Foundation"],
                "program_type": ["health systems", "education", "agriculture"],
                "num_competitors": ["3-5", "5-7", "2-3"],
                "comp1": ["JSI", "Chemonics", "DAI", "Abt Associates"],
                "comp2": ["FHI 360", "RTI", "Palladium", "MSI"],
                "strength1": ["Strong funder relationship", "Technical expertise", "Local presence"],
                "strength2": ["Cost competitive", "Innovation track record", "Similar past performance"],
                "weakness1": ["Limited geographic coverage", "Recent performance issues", "Key staff departed"],
                "weakness2": ["Higher cost structure", "Less relevant experience", "No local partner"],
                "advantage1": ["Unique technical approach", "Stronger local partnerships", "Cost efficiency"],
                "advantage2": ["Key personnel advantage", "Better past performance", "Innovation edge"],
                "vulnerability": [
                    "Less direct funder relationship",
                    "Smaller portfolio in region",
                    "New to this specific sector",
                ],
                "positioning": [
                    "Lead with technical innovation and local expertise",
                    "Emphasize cost efficiency and past performance",
                    "Focus on partnership strength and sustainability",
                ],
            },
        },
        "proposal_drafting": {
            "inputs": [
                "Draft technical approach section for {program_type}",
                "Write management section for {opportunity}",
                "Create proposal content for {section}",
                "Draft {section} for {funder} proposal",
            ],
            "output_template": """## Section Content

{content}

## Compliance Notes
- Addresses requirement: {requirement}
- Word count: {word_count}

## Enhancement Suggestions
- {suggestion1}
- {suggestion2}""",
            "variables": {
                "program_type": ["health systems strengthening", "agricultural development", "education access"],
                "opportunity": ["USAID Health Program", "World Bank Grant", "Foundation Initiative"],
                "section": ["Technical Approach", "Management Plan", "Monitoring & Evaluation", "Sustainability"],
                "funder": ["USAID", "World Bank", "Gates Foundation"],
                "content": [
                    "Our technical approach leverages evidence-based methodologies proven in similar contexts...",
                    "The management structure ensures efficient coordination across all implementation sites...",
                    "Our M&E framework tracks both output and outcome indicators with rigorous data quality...",
                ],
                "requirement": ["Technical Approach (Section C.1)", "Management (Section C.2)", "M&E (Section C.3)"],
                "word_count": ["1,850 of 2,000 limit", "950 of 1,000 limit", "1,200 of 1,500 limit"],
                "suggestion1": [
                    "Add specific metrics from past performance",
                    "Include organizational chart",
                    "Reference funder priorities",
                ],
                "suggestion2": ["Strengthen sustainability section", "Add risk mitigation detail", "Include timeline"],
            },
        },
        "win_probability": {
            "inputs": [
                "What is our win probability for {opportunity}?",
                "Should we bid on {funder}'s {program_type} opportunity?",
                "Assess win likelihood for {opportunity}",
                "Go/no-go assessment for {opportunity}",
            ],
            "output_template": """## Win Probability Score: {score}%

## Factor Analysis
| Factor | Assessment | Impact |
|--------|------------|--------|
| Technical fit | {tech_fit} | {tech_impact} |
| Past performance | {past_perf} | {perf_impact} |
| Price position | {price} | {price_impact} |
| Relationship | {relationship} | {rel_impact} |

## Key Risks
- {risk1}
- {risk2}

## Go/No-Go Recommendation: {recommendation}

## Improvement Actions
- {action1}
- {action2}""",
            "variables": {
                "opportunity": ["USAID Health Program", "World Bank Education Grant", "Foundation Initiative"],
                "funder": ["USAID", "World Bank", "Gates Foundation"],
                "program_type": ["health systems", "education", "agriculture"],
                "score": ["35", "55", "72", "85"],
                "tech_fit": ["Strong", "Moderate", "Weak"],
                "tech_impact": ["High positive", "Neutral", "Negative"],
                "past_perf": ["Excellent references", "Good but limited", "No direct experience"],
                "perf_impact": ["High positive", "Moderate positive", "Neutral"],
                "price": ["Competitive", "Above market", "Below market"],
                "price_impact": ["Positive", "Negative", "Neutral"],
                "relationship": ["Strong existing", "Some contacts", "No relationship"],
                "rel_impact": ["High positive", "Moderate positive", "Negative"],
                "risk1": ["Incumbent advantage", "Budget constraints", "Timeline challenges"],
                "risk2": ["Key personnel availability", "Partner capacity", "Cost competitiveness"],
                "recommendation": ["GO - Strong opportunity", "CONDITIONAL GO - Address gaps", "NO-GO - Low probability"],
                "action1": ["Strengthen technical team", "Develop funder relationship", "Reduce cost structure"],
                "action2": ["Secure key personnel commitments", "Identify stronger partners", "Gather additional references"],
            },
        },
        "funder_priorities": {
            "inputs": [
                "Analyze {funder}'s priorities",
                "What does {funder} want in proposals?",
                "Understand {funder}'s preferences",
                "Donor priorities for {funder}",
            ],
            "output_template": """## Strategic Priorities
{funder}'s current focus areas:
- {priority1}
- {priority2}
- {priority3}

## Funding Patterns
- Average award size: {avg_award}
- Typical duration: {duration}
- Geographic focus: {geography}

## Decision Factors
- {factor1}
- {factor2}

## Relationship Insights
{relationship_insight}

## Positioning Recommendations
{positioning}""",
            "variables": {
                "funder": ["USAID", "World Bank", "Gates Foundation", "DFID", "EU"],
                "priority1": ["Climate adaptation", "Gender equality", "Digital transformation", "Health equity"],
                "priority2": ["Local ownership", "Sustainability", "Innovation", "Scale"],
                "priority3": ["Evidence-based approaches", "Private sector engagement", "Youth focus"],
                "avg_award": ["$5-15M", "$10-50M", "$2-10M", "$1-5M"],
                "duration": ["3-5 years", "5-7 years", "2-4 years"],
                "geography": ["Sub-Saharan Africa priority", "Global with Asia focus", "Fragile states"],
                "factor1": ["Strong M&E framework", "Cost efficiency", "Innovation track record"],
                "factor2": ["Local partner involvement", "Sustainability plan", "Co-funding leverage"],
                "relationship_insight": [
                    "Key decision maker is new - relationship building opportunity",
                    "Strong existing relationship through past projects",
                    "Limited direct contact - need warm introduction",
                ],
                "positioning": [
                    "Emphasize innovation and evidence-based approach",
                    "Lead with sustainability and local ownership",
                    "Focus on cost efficiency and scale potential",
                ],
            },
        },
    },
}


def generate_mock_example(
    unit_id: str,
    task_id: str,
    seed: int | None = None,
) -> dict[str, str]:
    """
    Generate a single mock training example.

    Args:
        unit_id: The unit identifier
        task_id: The task identifier
        seed: Optional random seed

    Returns:
        Dictionary with 'input' and 'output' keys
    """
    if seed is not None:
        random.seed(seed)

    templates = MOCK_TEMPLATES.get(unit_id, {}).get(task_id)
    if not templates:
        raise ValueError(f"No templates found for {unit_id}/{task_id}")

    # Select random input template
    input_template = random.choice(templates["inputs"])

    # Generate variables
    variables = {}
    for var_name, var_options in templates["variables"].items():
        variables[var_name] = random.choice(var_options)

    # Format input and output
    try:
        input_text = input_template.format(**variables)
        output_text = templates["output_template"].format(**variables)
    except KeyError as e:
        logger.warning("template_format_error", unit=unit_id, task=task_id, error=str(e))
        # Fall back to simpler generation
        input_text = input_template
        output_text = templates["output_template"]

    return {"input": input_text, "output": output_text}


def generate_mock_dataset(
    unit_id: str,
    task_id: str,
    num_samples: int = 50,
    seed: int = 42,
) -> list[dict[str, str]]:
    """
    Generate a mock dataset for a specific task.

    Args:
        unit_id: The unit identifier
        task_id: The task identifier
        num_samples: Number of samples to generate
        seed: Random seed for reproducibility

    Returns:
        List of training examples
    """
    random.seed(seed)
    examples = []

    for i in range(num_samples):
        example = generate_mock_example(unit_id, task_id, seed=seed + i)
        examples.append(example)

    logger.info(
        "generated_mock_dataset",
        unit=unit_id,
        task=task_id,
        num_samples=len(examples),
    )

    return examples


def generate_mock_data_for_task(
    task: TaskDefinition,
    unit_id: str,
    num_samples: int = 50,
    seed: int = 42,
) -> list[dict[str, str]]:
    """
    Generate mock data for a task definition.

    Args:
        task: The task definition
        unit_id: The unit identifier
        num_samples: Number of samples to generate
        seed: Random seed

    Returns:
        List of training examples
    """
    return generate_mock_dataset(
        unit_id=unit_id,
        task_id=task.id,
        num_samples=num_samples,
        seed=seed,
    )


class MockDataGenerator:
    """Generator for creating synthetic training data."""

    def __init__(self, seed: int = 42):
        """
        Initialize the generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.generated_count = 0

    def generate_for_unit(
        self,
        unit_id: str,
        tasks: list[TaskDefinition],
        samples_per_task: int = 50,
    ) -> dict[str, list[dict[str, str]]]:
        """
        Generate mock data for all tasks in a unit.

        Args:
            unit_id: The unit identifier
            tasks: List of task definitions
            samples_per_task: Number of samples per task

        Returns:
            Dictionary mapping task_id to list of examples
        """
        all_data = {}

        for task in tasks:
            try:
                examples = generate_mock_data_for_task(
                    task=task,
                    unit_id=unit_id,
                    num_samples=samples_per_task,
                    seed=self.seed + self.generated_count,
                )
                all_data[task.id] = examples
                self.generated_count += samples_per_task
            except ValueError as e:
                logger.warning(
                    "skipping_task_no_templates",
                    unit=unit_id,
                    task=task.id,
                    error=str(e),
                )

        return all_data

    def generate_all(
        self,
        units: dict[str, list[TaskDefinition]],
        samples_per_task: int = 50,
    ) -> dict[str, dict[str, list[dict[str, str]]]]:
        """
        Generate mock data for all units and tasks.

        Args:
            units: Dictionary mapping unit_id to list of task definitions
            samples_per_task: Number of samples per task

        Returns:
            Nested dictionary: unit_id -> task_id -> examples
        """
        all_data = {}

        for unit_id, tasks in units.items():
            all_data[unit_id] = self.generate_for_unit(
                unit_id=unit_id,
                tasks=tasks,
                samples_per_task=samples_per_task,
            )

        return all_data
