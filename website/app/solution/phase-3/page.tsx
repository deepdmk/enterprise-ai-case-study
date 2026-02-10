import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { CodeBlock } from "@/components/ui/CodeBlock";
import { PhaseNav } from "@/components/phases/PhaseNav";
import { PhaseNavTop } from "@/components/phases/PhaseNavTop";
import { PhaseTabs } from "@/components/phases/PhaseTabs";
import { Phase3ArchitectureDiagram } from "@/components/phases/Phase3ArchitectureDiagram";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Phase 3: MoE Expert Routing",
  description: "Division-level AI agents with emergent multi-step intelligence. Three MoE agents consolidate fourteen task models into specialized division intelligence trained on proprietary organizational patterns.",
};

export default function Phase3() {
  return (
    <>
      <PageHeader
        title="Phase 3: MoE Expert Routing"
        subtitle="Division-level agents with emergent capabilities—intelligence patterns trained on organizational knowledge that competitors cannot replicate."
      >
        <div className="flex gap-4 mt-4">
          <div className="text-base">
            <span className="text-white/60">Direct Investment:</span>
            <span className="ml-2 font-semibold">$31,200</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Architecture:</span>
            <span className="ml-2 font-semibold">Mixture of Experts (MoE)</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Consolidation:</span>
            <span className="ml-2 font-semibold">14 task models → 3 division agents</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Value Stage:</span>
            <span className="ml-2 font-semibold">Competitive Differentiation</span>
          </div>
        </div>
      </PageHeader>

      <PhaseNavTop currentPhase={3} />

      <section className="py-12">
        <Container>
          <PhaseTabs
            vision={
              <>
                {/* The Problem */}
                <h3 className="text-xl font-bold text-navy mb-3">The Problem</h3>
                <p className="text-lg text-gray-700 leading-relaxed mb-6">
                  Task-based models add value, but only in the form of efficiencies. They make existing work faster, not fundamentally different. Isolated models cannot combine their intelligence to produce capabilities that none possess individually. Managing 14 separate task models also creates complexity: users must know which model to query, orchestrators must coordinate 14 APIs. Linking models together unlocks innovative and emergent capabilities that transform what becomes possible.
                </p>

                {/* The Solution */}
                <h3 className="text-xl font-bold text-navy mb-3">The Solution</h3>
                <p className="text-lg text-gray-700 leading-relaxed mb-6">
                  Consolidate task models into 3 division-level MoE (Mixture-of-Experts) agents, where each task model becomes an expert within the agent. These agents are more sophisticated than individual small models: they can be trained to handle chain of thought reasoning, tool calls, and multi-step logical workflows. The Fundraising agent contains 5 task experts, Business Development contains 5 experts, Field Operations contains 4 experts. Users interact with one agent per division; the agent routes to its appropriate expert automatically.
                </p>

                {/* The Value */}
                <h3 className="text-xl font-bold text-navy mb-3">The Value</h3>
                <p className="text-lg text-gray-700 leading-relaxed">
                  Division-level intelligence with emergent multi-step capabilities. Intelligence patterns trained on proprietary data that competitors cannot replicate. The Fundraising agent knows relationship-building sequences your team has refined over years. The Business Development agent understands your bidding strategies. The Field Operations agent captures local market intelligence and operational rhythms. Three production-ready division agents replacing fourteen separate task models: users gain single access points per division capable of complex, multi-step workflows with accuracy trained on organizational knowledge. Full optionality maintained: can stop here with three specialized agents delivering immediate differentiation value, or continue to cross-division orchestration in Phase 4.
                </p>
              </>
            }
            approach={
              <>
                <Card className="mb-12 bg-magenta/5 border-magenta/20 border-t-4 border-t-magenta">
                  <h3 className="text-xl text-gray-700 mb-6">Consolidating task expertise into division-level intelligence through Mixture of Experts architecture</h3>

                  <p className="text-lg text-gray-700 leading-relaxed mb-8">
                    Phase 3 used model consolidation and Mixture-of-Experts architecture to create division-level intelligence that preserved task-specific precision while enabling emergent multi-step capabilities. The strategic approach prioritized operational simplicity, bounded experimentation cost, and foundation-building for enterprise-wide orchestration.
                  </p>

                  {/* Subsection 2.1: Consolidating Fourteen Models Into Three Division Agents */}
                  <h3 className="text-2xl font-bold text-navy mb-4">Consolidating Fourteen Models Into Three Division Agents</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 2 delivers immediate value: fourteen working task models with a combined Phase 2 Direct Investment of $43,600. Teams have AI capabilities they own and control. But this also creates both operational and architectural complexity that would compound in later phases.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The immediate problem was user experience. When a fundraiser needed to profile an investor, assess fit, analyze capacity, design engagement strategy, and synthesize portfolio patterns, they queried five separate models. Each task required a separate API call, different prompts, and manual integration of results. This worked for single-task queries but became cumbersome for complex workflows.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The deeper problem was agentic orchestration. Future phases would train an orchestrator to coordinate AI capabilities across divisions. Teaching an orchestrator to manage fourteen separate models creates exponential complexity—it must learn which model handles which task, how to call each one, how to consolidate outputs, and how to use intermediate results in subsequent calls. Each model becomes a separate API with its own interface, prompt format, and output structure. The orchestrator&apos;s job becomes managing fourteen different tools rather than reasoning about three division-level capabilities.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Division-level consolidation addressed both problems. Instead of managing five Fundraising models, teams interact with one Fundraising agent that internally routes to the appropriate expert. The user experience shifts from &quot;which model do I need?&quot; to &quot;ask the division agent.&quot; This consolidation doesn&apos;t sacrifice the precision of task-specific models—it preserves them as internal experts while simplifying the interface.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    More importantly, consolidation creates quality control points at the division level. The router within each MoE agent can adjust intermediate outputs before passing them to subsequent experts, apply division-specific standards, and ensure consistency across multi-step workflows. These quality gates live inside the division agent rather than requiring orchestrator-level intervention. When Phase 5&apos;s orchestrator coordinates division agents, it reasons about three high-level capabilities (Fundraising, Business Development, Field Operations) rather than orchestrating fourteen granular tasks.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    The economics reinforced this decision. Three division agents require $31,200 Direct Investment for Phase 3 while consolidating the fourteen task models from Phase 2. Each division agent becomes a building block for enterprise-wide capabilities rather than an isolated endpoint. The organization maintains optionality—can stop at division-level agents or continue building—while reducing both operational and architectural complexity.
                  </p>

                  {/* Subsection 2.2: Choosing Mixture-of-Experts Architecture */}
                  <h3 className="text-2xl font-bold text-navy mb-4 mt-8">Choosing Mixture-of-Experts Architecture</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The consolidation strategy required choosing an architecture that preserved task-specific precision while enabling multi-step intelligence. Three approaches were considered:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Option 1: Single Large Model Per Division</strong> - Utilize transfer learning to build and train one model on all division tasks. This creates simplicity (one model) but loses the precision of task-specific fine-tuning. A general &quot;Fundraising model&quot; trained on investor profiling plus capacity analysis plus engagement strategy becomes mediocre at everything rather than excellent at each task.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Option 2: Orchestration Layer</strong> - Build custom routing logic or an agentic system at the division level that sends queries to the right task model. This preserves precision but creates compounding problems. These task models are too small to handle much self-coordination—they lack the reasoning capacity for complex agent-to-agent negotiation. Custom routing logic requires brittle if-then rules that break when tasks overlap or evolve. Every new query type requires code changes. Worse, this complexity would compound in future phases when the enterprise orchestrator tries to coordinate multiple division-level orchestration systems. The orchestration layer becomes a maintenance burden that multiplies across architectural layers.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Option 3: Mixture-of-Experts (MoE)</strong> - Merge task models into a unified architecture where a trained router learns which expert to activate. This preserves task-specific precision (each expert is the original fine-tuned model) while creating emergent intelligence (the router learns patterns not explicitly programmed). The router handles ambiguous queries, multi-step workflows, and edge cases without manual coding.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 3 chose MoE because it was the only architecture that preserved precision, enabled emergence, and avoided technical debt. The router becomes an artifact of organizational intelligence—it learned how tasks actually combine in real workflows rather than following predetermined rules.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    MoE architecture also enabled continuous experimentation and improvement. The modular expert structure made it possible to swap individual models without rebuilding the entire agent. If a team improved their RFP analysis model, they could substitute the new version into the Business Development MoE and test results. The Phase 0 ModelRegistry tracked these experiments—which expert versions worked best, which combinations improved performance, which models could be shared across divisions. In later phases, this flexibility could enable cross-divisional model sharing. A Field Operations forecasting expert might prove more effective for Business Development&apos;s resource planning than the original expert. The MoE structure made these discoveries testable without architectural changes.
                  </p>

                  {/* Subsection 2.3: Emergent Capabilities From Expert Combination */}
                  <h3 className="text-2xl font-bold text-navy mb-4 mt-8">Emergent Capabilities From Expert Combination</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    MoE architecture creates capabilities that weren&apos;t designed upfront. When the Business Development agent combines RFP analysis with competitive positioning with proposal drafting, it develops understanding of how these tasks connect. A query like &quot;analyze this RFP and recommend our positioning strategy&quot; activates multiple experts in sequence, with the router learning which combinations work for which scenarios.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    This emergence matters strategically. The division agent doesn&apos;t just execute predefined workflows—it discovers effective patterns through use. A Fundraising agent might learn that capacity analysis should precede engagement strategy for certain donor types, even though no one explicitly programmed that sequence. These emergent patterns become organizational knowledge encoded in the router&apos;s weights, captured and refined over time.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    The bounded infrastructure cost ($1,200, accommodating multiple iterations) made this experimentation practical. If a router configuration didn&apos;t work, retraining required minimal time and compute. The organization could try different expert combinations, test routing strategies, and iterate based on real usage patterns. This learning-by-doing approach built institutional knowledge about how AI capabilities should combine for their specific business model.
                  </p>

                  {/* Subsection 2.4: Building on Previous Phases and Enabling Future Intelligence */}
                  <h3 className="text-2xl font-bold text-navy mb-4 mt-8">Building on Previous Phases and Enabling Future Intelligence</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 3 represents an inflection point where previous investments compound into new capabilities while creating the foundation for enterprise-wide intelligence. The design decisions prioritized leveraging existing infrastructure, avoiding premature optimization, and preserving optionality for future phases.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Leveraging Phase 0 Infrastructure:</strong> The ModelRegistry and ExperimentTracker built in Phase 0 made Phase 3 practical. Without the registry, managing three MoE agents (each containing 5-4 expert models) would require custom tracking infrastructure. The registry provided immediate versioning, metadata management, and performance monitoring. The file-based architecture kept overhead minimal—no database dependencies, no complex deployment. Phase 0&apos;s infrastructure investment paid dividends in Phase 3&apos;s execution speed. Each division agent registers with the ModelRegistry as a single unit with metadata describing its scope and capabilities. This abstraction creates flexibility—Phase 4&apos;s discovery system and Phase 5&apos;s orchestrator interact with &quot;division agents&quot; without needing to understand internal MoE structure. A Business Development agent registers capabilities like opportunity analysis, proposal development, and compliance checking. The registry doesn&apos;t track the five internal expert models; it sees one intelligent agent with broad division-level skills. This design decision avoided premature optimization. Phase 3 didn&apos;t build cross-division routing or orchestration logic. It built three working division agents and registered them in a way that made future orchestration possible while keeping infrastructure lightweight.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Building on Phase 1&apos;s Semantic Foundation:</strong> Phase 1&apos;s unified embedding space enabled Phase 3 division agents to access knowledge across all organizational data. When a Business Development agent analyzes an RFP, it queries the embedding space for relevant historical proposals, competitive intelligence, and successful strategies—regardless of which division originally created that content. The semantic search capability became a tool available to all expert models within each MoE agent, amplifying their effectiveness beyond their training data.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Inheriting Phase 2&apos;s Proven Capabilities:</strong> Phase 3 didn&apos;t build models from scratch—it inherited fourteen proven, production-tested expert models. Each task SLM had been refined by teams, tested in real workflows, and validated through actual use. The Fundraising portfolio analysis expert had analyzed hundreds of investments. The Business Development proposal expert had drafted dozens of winning proposals. Phase 3 merged battle-tested capabilities, not theoretical ones. This de-risked the entire phase—the experts worked, the question was whether the router could orchestrate them effectively.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Enabling Phase 4&apos;s Discovery:</strong> Phase 3 division agents become the actors in Phase 4&apos;s experimental environment. Phase 4 connects the three division agents and observes how they collaborate when given complex cross-divisional queries. A Fundraising agent might consult the Field Operations agent for local market intelligence, then coordinate with Business Development on partnership opportunities. These emergent collaboration patterns get captured and become training data for Phase 5&apos;s orchestrator. Phase 3 created the intelligent agents that Phase 4 would connect and observe.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Preparing Phase 5&apos;s Orchestration:</strong> The Phase 0 registry abstraction means Phase 5&apos;s orchestrator sees three division-level capabilities, not fourteen task-level models. This simplification makes orchestrator training tractable—learning to coordinate three agents is fundamentally different from coordinating fourteen models. Phase 3&apos;s consolidation decision directly enabled Phase 5&apos;s feasibility. The router training approach in Phase 3 also provided the template for Phase 5&apos;s orchestrator training—both learn coordination patterns from observed workflows rather than predetermined rules.
                  </p>

                  <p className="text-gray-700 leading-relaxed">
                    <strong>Learning Without Lock-In:</strong> The registry enabled learning without creating dependencies. Each division agent logged performance metrics and usage patterns. Teams could see which experts got activated most frequently, which queries caused routing uncertainty, which workflows emerged in practice. This data informed Phase 4&apos;s discovery experiments and Phase 5&apos;s orchestrator training. The organization was building institutional knowledge about how AI capabilities should combine, captured in registry data rather than tribal knowledge. If the organization stopped at Phase 3, the registry overhead was minimal. If they continued to Phase 4, the foundation was ready.
                  </p>
                </Card>

                <Card className="mb-12 bg-white/50 border border-gray-200">
                  <h3 className="text-lg font-bold text-navy mb-2">
                    Skip the Technical Details?
                  </h3>
                  <p className="text-gray-700 mb-4">
                    The Technical Implementation section below provides complete code examples, architecture diagrams, and deployment instructions for building Phase 3&apos;s MoE division agents. If you&apos;d prefer to explore the next phase first, you can skip ahead:
                  </p>
                  <p className="text-gray-700 mb-4">
                    Phase 4 introduces cross-division discovery, where the three division agents collaborate and reveal enterprise-wide patterns. This experimental phase captures how organizational intelligence should coordinate across divisions.
                  </p>
                  <a
                    href="/solution/phase-4"
                    className="inline-block px-6 py-3 bg-navy text-white font-medium rounded-md hover:bg-navy/90 transition-colors"
                  >
                    Continue to Phase 4: Agentic Discovery →
                  </a>
                  <p className="text-base text-gray-600 mt-4">
                    Otherwise, scroll down for the full technical breakdown of Phase 3&apos;s implementation.
                  </p>
                </Card>
              </>
            }
            technical={
              <>
                <h3 className="text-xl text-gray-700 mb-8">Building production MoE division agents through model merging, router training, and registry integration</h3>

                {/* Architecture Diagram */}
                <div className="mb-12 bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                  <Phase3ArchitectureDiagram />
                </div>

                {/* Architecture Overview */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Architecture Overview</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Six-Program Pipeline</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 3 implements a six-program pipeline that transforms 14 task-specific models into 3 division-level MoE agents with staff interaction capabilities:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 1: Import</strong> organizes Phase 2&apos;s task models by division, validating adapter compatibility and preparing expert pools for merging.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 2: Config Generation</strong> creates MergeKit YAML configurations for each division, specifying expert sources and routing hints through positive/negative prompts.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 3: MergeKit Execution</strong> runs three separate merges, combining task adapters into Mixtral-style MoE models with trained routers.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 4: Optional Fine-tuning</strong> refines router behavior through LoRA adaptation on division-specific query patterns when needed.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 5: Export</strong> packages merged models for Phase 4 A2A agents, including routing embeddings and agent configurations.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    <strong>Program 6: Staff Interface</strong> provides a Gradio web interface for staff to interact with MoE models, view expert activations, and submit feedback for RLHF.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Technology Stack</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Merging:</strong> MergeKit with Mixtral-style MoE architecture</li>
                    <li><strong>Router:</strong> Hidden gate mode using sentence-transformer embeddings</li>
                    <li><strong>Expert selection:</strong> 2-of-N per token (within each division pool)</li>
                    <li><strong>Base model:</strong> Llama 3.1 8B (same as Phase 2 task models)</li>
                    <li><strong>Integration:</strong> Phase 0 registries for versioning and lineage tracking</li>
                  </ul>
                </div>

                {/* Part 1: MoE Architecture Design */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">1. MoE Architecture Design</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 3 creates three independent Mixture-of-Experts models, not one unified MoE architecture. Each division receives its own specialized MoE agent with isolated expert pools, enabling division-specific intelligence while maintaining clean separation of capabilities.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The architecture uses Mixtral&apos;s MoE design with hidden gate mode routing. Each division agent selects two experts per token from its isolated pool. Fundraising selects 2-of-5 experts, Business Development selects 2-of-4, and Field Operations selects 2-of-5. This top-2 activation strategy balances precision (leveraging multiple specialized experts) with efficiency (avoiding unnecessary computation).
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/settings.py:3-6
"""Creates 3 separate MoE models, one per organizational unit:
- Fundraising MoE (5 experts)
- Business Development MoE (4 experts)
- Field Operations MoE (5 experts)
"""`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    The separation decision prioritizes deployment independence and failure isolation. Each division agent operates as a standalone service—if Business Development&apos;s MoE needs retraining or experiences issues, Fundraising and Field Operations continue operating without disruption. This architecture also simplifies Phase 4&apos;s discovery experiments, where agents collaborate as independent actors rather than shared components of a monolithic system.
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/settings.py:25-31
class MoEArchitectureConfig(BaseModel):
    architecture: str = "mixtral"
    gate_mode: Literal["hidden", "cheap_embed", "random"] = "hidden"
    dtype: Literal["float16", "bfloat16", "float32"] = "float16"
    experts_per_token: int = 2  # Within each unit's MoE`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mt-6">
                    The <code>gate_mode: hidden</code> configuration means the router learns from prompt embeddings during the merge process rather than requiring separate training. This approach reduces complexity—no router training pipeline, no training data curation, no hyperparameter tuning for routing logic. The router weights initialize based on positive and negative prompt embeddings provided in the MergeKit configuration, creating routing intelligence without explicit training loops.
                  </p>
                </div>

                {/* Part 2: Expert Model Preparation */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">2. Expert Model Preparation</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 3 imports Phase 2&apos;s fourteen task-specific models and organizes them into division-aligned expert pools. The production configuration defines precise task-to-division mappings that reflect organizational structure:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/config.yaml:12-40
units:
  fundraising:
    tasks:
      - investor_profiling
      - funding_opportunity_analysis
      - proposal_evaluation
      - portfolio_matching
      - engagement_recommendation                 # 5 tasks

  business_development:
    tasks:
      - rfp_analysis
      - competitive_landscape
      - proposal_scoring
      - funding_trends                            # 4 tasks

  field_operations:
    tasks:
      - market_intelligence
      - project_performance
      - partner_assessment
      - regulatory_compliance
      - risk_assessment                           # 5 tasks`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    This 5+4+5 distribution reflects actual organizational needs, not arbitrary balancing. Fundraising handles the most complex relationship-building workflows (five distinct tasks), Business Development focuses on competitive positioning (four tasks), and Field Operations manages local intelligence and compliance (five tasks).
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The import pipeline validates model compatibility and standardizes formats for MergeKit consumption. Phase 2 exports each task model with adapter weights, metadata, and performance logs. Phase 3&apos;s import process verifies base model alignment (all experts must derive from the same foundation model), extracts adapter weights, and organizes files into unit-specific directories:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/src/program1_import/main.py (import logic)
# Imports Phase 2 exports, validates compatibility, organizes by unit
python -m src.program1_import.main --phase2-export ../phase-2-task-slms/exports`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    For development and testing, the system supports mock mode with reduced expert counts (2 experts per unit) to enable rapid iteration without GPU requirements:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/config.yaml:75-76
test_mode:
  num_experts_per_unit: 2  # 2 mock experts per unit = 6 total`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mt-6">
                    This test mode generates synthetic adapter weights with realistic structure, allowing developers to verify merge logic, routing configuration, and export pipelines before committing to full-scale GPU merges with production models.
                  </p>
                </div>

                {/* Part 3: MergeKit Configuration & Execution */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">3. MergeKit Configuration & Execution</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The configuration generation system creates three separate MergeKit YAML files, one per division agent. Each configuration specifies the base model, architecture parameters, expert sources, and routing hints through positive and negative prompts.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Here&apos;s the generated configuration for the Fundraising division agent:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/data/configs/fundraising_moe.yaml:1-22
base_model: HuggingFaceTB/SmolLM-135M
architecture: mixtral
gate_mode: hidden
dtype: float16
experts_per_token: 2
experts:
- source_model: /path/to/fundraising/investor_profiling/v1/model
  positive_prompts:
  - Profile this investor
  - Create investor profile
  - Analyze investor background
  negative_prompts:
  - Analyze RFP
  - Assess market conditions
- source_model: /path/to/fundraising/funding_opportunity/v1/model
  positive_prompts:
  - Evaluate funding opportunity
  - Assess investment potential
  negative_prompts:
  - Profile investor
  - Analyze competition`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    The configuration generator programmatically constructs these files from imported expert metadata:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/src/program2_config_gen/mergekit_config.py:126-133
config = {
    "base_model": base_model,
    "architecture": self.settings.moe.architecture,
    "gate_mode": self.settings.moe.gate_mode,
    "dtype": self.settings.moe.dtype,
    "experts_per_token": experts_per_token,
    "experts": experts,
}`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Positive and negative prompts provide routing hints without requiring separate training. When a query matches &quot;Profile this investor,&quot; the router learns to favor the investor profiling expert. Negative prompts (&quot;Analyze RFP&quot;) tell the router when NOT to activate that expert. This prompt-based routing initialization eliminates the need for curated training datasets while still producing intelligent routing behavior.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The merge process executes sequentially for each division, running MergeKit three times with division-specific configurations:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/src/program3_merge/main.py:162-179
for config_path in sorted(config_files):
    unit_id = config_path.stem.replace("_moe", "")
    output_dir = merged_dir / f"{unit_id}_moe"

    config = load_mergekit_config(config_path)
    num_experts = len(config.get("experts", []))

    result = merger.merge(
        config_path=config_path,
        output_dir=output_dir,
        use_cuda=cuda,
        dry_run=dry_run,
    )`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Each merge operation combines expert adapter weights with the base model, initializes the router gate based on prompt embeddings, and outputs a unified MoE model ready for inference. The process configuration balances safety with GPU utilization:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/config.yaml:43-50
merge:
  use_cuda: true
  lazy_unpickle: true
  allow_crimes: false
  trust_remote_code: true
  timeout_minutes: 60  # Per-unit merge time
  copy_tokenizer: true
  out_shard_size: 5000000000  # 5GB shards`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mt-6">
                    The sequential merge approach (versus one massive merge) enables incremental validation. After merging Fundraising&apos;s MoE, teams can test it immediately while Business Development and Field Operations merges continue. This de-risks deployment—if one division&apos;s merge produces unexpected behavior, the other divisions remain unaffected and investigation can focus on that specific expert pool.
                  </p>
                </div>

                {/* Part 4: Router Initialization Through Prompt Embeddings */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">4. Router Initialization Through Prompt Embeddings</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 3&apos;s routing infrastructure uses semantic embeddings rather than explicit training loops. The <code>gate_mode: hidden</code> configuration means MergeKit initializes router weights from prompt embeddings computed during configuration generation, eliminating the need for separate router training infrastructure.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The routing configuration system computes embeddings for each expert&apos;s positive and negative prompts using a pre-trained sentence transformer:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/src/program2_config_gen/routing_config.py:87-102
def _compute_prompt_embeddings(self, adapter: AdapterInfo) -> dict[str, Any]:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(self.settings.export_config.embedding_model)

    result = {}
    if adapter.positive_prompts:
        pos_embeddings = model.encode(adapter.positive_prompts)
        result["positive_embeddings"] = pos_embeddings.tolist()

    if adapter.negative_prompts:
        neg_embeddings = model.encode(adapter.negative_prompts)
        result["negative_embeddings"] = neg_embeddings.tolist()

    return result`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    The embedding model choice balances quality and deployment simplicity:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/config.yaml:60-64
export_config:
  generate_agent_configs: true
  generate_routing_embeddings: true
  embedding_model: "BAAI/bge-base-en-v1.5"
  export_format: safetensors`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    BAAI&apos;s BGE model produces 768-dimensional embeddings that capture semantic intent without requiring specialized infrastructure. The router uses these embeddings to initialize gate weights—queries semantically similar to positive prompts receive higher activation scores for that expert, while queries similar to negative prompts receive lower scores.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    This embedding-based approach creates routing intelligence without the operational complexity of training pipelines. No training data curation, no hyperparameter tuning, no convergence monitoring. The router&apos;s initial weights come directly from prompt semantics, and those weights remain fixed during inference unless teams choose optional post-merge fine-tuning (covered in Part 5).
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The routing embeddings export alongside the merged model, enabling Phase 4&apos;s discovery environment to analyze which semantic patterns activate which experts:
                  </p>

                  <CodeBlock
                    code={`# Generated routing outputs exported for Phase 4 analysis
data/exports/phase4/{unit_id}/routing/
├── expert_registry.json         # Expert ID → task mapping
├── routing_embeddings.npy       # Pre-computed prompt embeddings
├── intent_mapping.json          # Intent → expert IDs
└── a2a_routing_config.json      # A2A protocol config`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mt-6">
                    This export structure supports both runtime inference (which expert to activate) and observability (why was this expert chosen). Teams can examine routing decisions, identify patterns where router confidence is low, and optionally refine prompt sets for specific experts without retraining models.
                  </p>
                </div>

                {/* Part 5: Optional Post-Merge Fine-Tuning */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">5. Optional Post-Merge Fine-Tuning</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The base Phase 3 pipeline produces working MoE agents without additional training—the prompt embedding approach initializes functional routers during merge. However, teams can optionally fine-tune merged models to refine routing behavior or adapt experts to specific deployment contexts.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The fine-tuning implementation uses LoRA (Low-Rank Adaptation) to efficiently update model weights without full retraining:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/finetune_moe.py:29-36
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "up_proj", "down_proj", "gate_proj"],
)`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    This configuration targets all projection layers including the gate projection that controls expert routing. The rank-16 LoRA adapters add minimal parameters (~1-2% of base model size) while enabling effective fine-tuning on division-specific query patterns.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Training hyperparameters balance convergence speed with stability:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/finetune_moe.py:69-82
args=TrainingArguments(
    learning_rate=3e-4,
    lr_scheduler_type="linear",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=4,
    fp16=True,
    logging_steps=1,
    optim="adamw_8bit",
    weight_decay=0.01,
    warmup_steps=10,
    output_dir=OUTPUT_DIR,
    seed=0,
)`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    The 8-bit AdamW optimizer reduces memory requirements, enabling fine-tuning on consumer GPUs. Four epochs with small batch sizes (effective batch size 16 via gradient accumulation) provide sufficient exposure to training data without overfitting.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Configuration settings make fine-tuning opt-in with conservative defaults:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/config.yaml:82-89
finetune:
  enabled: false
  epochs: 2
  batch_size: 4
  learning_rate: 0.00001
  lora_r: 8
  lora_alpha: 16
  max_samples: 1000`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mt-6">
                    By default, fine-tuning is disabled—most deployments achieve sufficient routing accuracy from prompt embeddings alone. Teams enable fine-tuning when they have division-specific query logs showing routing ambiguities or when deploying to specialized contexts where prompt-based initialization underperforms.
                  </p>

                  <p className="text-gray-700 leading-relaxed">
                    The optional nature of this step reinforces Phase 3&apos;s bounded cost approach. The base pipeline delivers working agents immediately. Fine-tuning becomes an optimization lever teams can pull if needed, not a required complexity for initial deployment.
                  </p>
                </div>

                {/* Part 6: Testing & Export Pipeline for Phase 4 Integration */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">6. Testing & Export Pipeline for Phase 4 Integration</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 3&apos;s testing strategy enables rapid iteration through test mode before committing to GPU-intensive production merges. The test mode generates mock experts and executes the entire pipeline with minimal resource requirements:
                  </p>

                  <CodeBlock
                    code={`# Generate mock adapters (2 per unit)
python -m src.program1_import.main --test-mode

# Generate 3 mock MoE configs
python -m src.program2_config_gen.main --test-mode

# Create 3 mock merged models
python -m src.program3_merge.main --test-mode

# Export 3 mock packages
python -m src.program5_export.main --test-mode`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Test mode uses 2 experts per division (6 total) instead of production&apos;s 14 experts. This reduced scope runs on CPU without GPU acceleration, enabling developers to verify configuration generation logic, routing initialization, and export packaging without hardware dependencies. Teams validate the complete workflow—import, config generation, merge, export—in minutes rather than hours.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The export pipeline packages each division agent for Phase 4 consumption. Each export contains the merged model, routing configuration, expert registry, and Agent-to-Agent (A2A) protocol specifications:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/README.md:219-231
data/exports/phase4/{unit_id}/
├── model/                           # MoE model files
├── routing/
│   ├── expert_registry.json         # Expert ID → task mapping
│   ├── routing_embeddings.npy       # Pre-computed embeddings
│   ├── intent_mapping.json          # Intent → expert IDs
│   └── a2a_routing_config.json      # A2A protocol config
├── agent_config/
│   └── {unit_id}_agent.yaml         # A2A agent configuration
└── export_manifest.json`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Phase 4&apos;s discovery environment imports these packages to instantiate three independent agents. The routing metadata enables observability—Phase 4 can analyze which experts activate for cross-divisional queries, identify collaboration patterns, and capture routing decisions as training data for Phase 5&apos;s orchestrator.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Single-unit export operations support incremental deployment and testing:
                  </p>

                  <CodeBlock
                    code={`# Export specific unit for isolated testing
python -m src.program5_export.main --unit fundraising`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mt-6">
                    This granular export capability allows teams to deploy one division agent to production while continuing development on others. If Fundraising&apos;s MoE performs well in validation, it can go live immediately while Business Development and Field Operations undergo additional refinement. The independent export structure eliminates coordination dependencies between divisions.
                  </p>
                </div>

                {/* Part 7: Production Pipeline & Deployment */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">7. Production Pipeline & Deployment</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The full production pipeline executes four sequential programs to transform Phase 2&apos;s task models into Phase 4-ready division agents:
                  </p>

                  <CodeBlock
                    code={`# Import Phase 2 exports
python -m src.program1_import.main --phase2-export ../phase-2-task-slms/exports

# Generate 3 MoE configs (fundraising, business_development, field_operations)
python -m src.program2_config_gen.main

# Merge all 3 units (requires GPU with 24GB+ VRAM)
python -m src.program3_merge.main --cuda

# Export all 3 packages for Phase 4
python -m src.program5_export.main --generate-agent-configs --generate-embeddings`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    The merge step requires GPU acceleration for production-scale operations. Each division merge processes 4-5 expert models, combining adapter weights and initializing router gates:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/README.md:298-302
# Test Mode: CPU only, minimal memory
# Full Merge: GPU with 24GB+ VRAM (per unit merge)
# Disk Space: ~30GB per unit merged (3 units = ~90GB total)`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    The 60-minute timeout per unit provides buffer for larger base models or higher expert counts:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/config.yaml:48
timeout_minutes: 60  # Per-unit merge time`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    This generous timeout enables experimentation with different base models. While test mode uses SmolLM-135M for rapid iteration, production deployments might use Llama 3.1 8B or similar models depending on capability requirements and infrastructure constraints.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Single-unit operations support targeted merges and incremental deployment:
                  </p>

                  <CodeBlock
                    code={`# Merge specific unit only
python -m src.program3_merge.main --unit fundraising --cuda

# Export specific unit package
python -m src.program5_export.main --unit fundraising`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    These unit-specific commands enable teams to iterate on one division&apos;s configuration without reprocessing all three agents. If Fundraising needs router refinement or expert rebalancing, developers can re-merge just that unit and export an updated package while Business Development and Field Operations remain unchanged.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The Phase 0 ModelRegistry integration happens at export time. Each division agent registers as a single model entry with metadata describing its division scope and capabilities:
                  </p>

                  <CodeBlock
                    code={`# Registry entry structure (conceptual - abstracts MoE complexity)
{
  "model_id": "fundraising_division_agent",
  "version": "1.0.0",
  "type": "moe_agent",
  "capabilities": [
    "investor_profiling",
    "funding_opportunity_analysis",
    "proposal_evaluation",
    "portfolio_matching",
    "engagement_recommendation"
  ],
  "division": "fundraising",
  "base_model": "HuggingFaceTB/SmolLM-135M",
  "num_experts": 5,
  "architecture": "mixtral"
}`}
                    language="json"
                  />

                  <p className="text-gray-700 leading-relaxed mt-6">
                    This abstraction means downstream systems (Phase 4 discovery, Phase 5 orchestrator) interact with &quot;division agents&quot; without needing to understand internal MoE structure. The registry sees three intelligent agents with division-level capabilities, not fourteen underlying task experts. This design decision simplifies future orchestration—Phase 5&apos;s orchestrator learns to coordinate three agents rather than fourteen models, directly enabled by Phase 3&apos;s consolidation and registry abstraction strategy.
                  </p>
                </div>

                {/* Part 8: Staff Interface for Model Interaction */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">8. Staff Interface for Model Interaction</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Program 6 provides a Gradio web interface enabling staff to interact directly with division MoE agents. This interface serves dual purposes: immediate utility for staff needing AI assistance, and feedback collection for continuous model improvement through RLHF (Reinforcement Learning from Human Feedback).
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The interface architecture separates inference engines for test and production modes:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/src/program6_interface/gradio_app.py:421-432
# Initialize inference engine
if test_mode:
    inference_engine = MockMoEInference(
        exports_dir=exports_dir,
        experts_per_token=settings.moe.experts_per_token,
    )
else:
    inference_engine = MoEModelLoader(
        exports_dir=exports_dir,
        device="auto",
    )`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Test mode uses mock inference with canned responses and simulated expert activations, enabling UI development and workflow testing without GPU requirements. Production mode loads actual MoE models and tracks real expert activations through forward hooks on the router layer.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The interface displays which experts were activated for each query, providing transparency into model behavior:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/src/program6_interface/model_loader.py:70-88
def router_hook(self, module: Any, input: Any, output: Any) -> None:
    """Hook function for router layer - captures expert selection weights."""
    try:
        if isinstance(output, tuple):
            router_logits = output[0]
        else:
            router_logits = output

        # Get top-k selections and their weights
        router_probs = torch.softmax(router_logits, dim=-1)

        # Aggregate across batch and sequence
        mean_probs = router_probs.mean(dim=[0, 1])

        # Update activation scores
        for expert_id, score in enumerate(mean_probs.tolist()):
            self.activations[expert_id] = self.activations.get(expert_id, 0) + score
    except Exception as e:
        logger.warning("router_hook_error", error=str(e))`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Expert activation tracking enables teams to understand which task experts respond to which queries. This observability helps identify routing patterns, detect ambiguous queries where router confidence is low, and validate that expert selection aligns with query intent.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    The feedback collection system captures staff ratings for future RLHF training:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/src/program6_interface/feedback.py:81-116
def record_interaction(
    self,
    session_id: str,
    unit_id: str,
    prompt: str,
    response: str,
    activated_experts: list[dict],
    generation_params: dict,
) -> str:
    """Record an interaction for potential feedback."""
    feedback_id = str(uuid.uuid4())

    self._active_interactions[feedback_id] = {
        "session_id": session_id,
        "unit_id": unit_id,
        "prompt": prompt,
        "response": response,
        "activated_experts": activated_experts,
        "generation_params": generation_params,
        "timestamp": datetime.now(UTC).isoformat(),
    }
    return feedback_id`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Each interaction records the complete context: which division agent was queried, what prompt was submitted, which experts activated, and the response generated. When staff provide feedback (thumbs up/down or detailed ratings), this context enables targeted model improvement—teams can identify which expert combinations produce unsatisfactory results and refine accordingly.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    Interface configuration integrates with the existing settings infrastructure:
                  </p>

                  <CodeBlock
                    code={`# phase-3-moe-experts/config/config.yaml:97-110
interface:
  gradio:
    host: "0.0.0.0"
    port: 7861
    share: false
    title: "Phase 3 MoE Staff Interface"
    description: "Interact with organizational unit MoE models"
  generation:
    max_new_tokens: 256
    temperature: 0.7
    top_p: 0.9
  feedback:
    enabled: true
    feedback_dir: "data/feedback"`}
                    language="yaml"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    Launching the interface requires a single command:
                  </p>

                  <CodeBlock
                    code={`# Test mode (no GPU required, mock responses)
python -m src.program6_interface.main --test-mode

# Production mode (requires GPU, real model inference)
python -m src.program6_interface.main

# Custom configuration
python -m src.program6_interface.main --port 7862 --share`}
                    language="bash"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    The <code>--share</code> flag creates a public Gradio link, enabling remote staff access without VPN configuration. This simplifies pilot deployments where teams across locations need to evaluate division agents before full infrastructure deployment.
                  </p>

                  <p className="text-gray-700 leading-relaxed">
                    Feedback data accumulates in monthly JSONL files, creating training datasets for future model refinement. This feedback loop closes the gap between deployment and improvement—staff interactions directly inform which experts need attention, which routing patterns cause confusion, and where division agents excel or struggle. The collected data becomes input for Phase 5&apos;s orchestrator training, capturing real-world usage patterns that synthetic data cannot replicate.
                  </p>
                </div>
              </>
            }
          />

          {/* Next Steps CTA */}
          <div className="bg-navy text-white p-8 rounded-lg mt-12">
            <h3 className="text-2xl font-bold mb-4">Next: Phase 4 - Agentic Discovery</h3>
            <p className="text-white/90 mb-4">
              Phase 3 delivers three division-level agents with specialized intelligence. Phase 4 opens cross-division experimentation, enabling agents to discover collaboration patterns and identify opportunities spanning multiple divisions. This discovery phase generates the training data that powers Phase 5&apos;s orchestrated system.
            </p>
            <p className="text-white/90 mb-6">
              Where Phase 3 consolidates division expertise, Phase 4 explores enterprise-wide potential. The sandboxed discovery environment captures emergent collaboration patterns while maintaining production stability. This learning becomes the foundation for orchestrated intelligence in Phase 5.
            </p>
            <a
              href="/solution/phase-4"
              className="inline-block px-6 py-3 bg-teal text-white font-medium rounded-md hover:bg-teal/90 transition-colors"
            >
              Continue to Phase 4 →
            </a>
          </div>
        </Container>
      </section>

      <PhaseNav currentPhase={3} />
    </>
  );
}
