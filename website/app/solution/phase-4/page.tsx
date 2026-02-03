import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { CodeBlock } from "@/components/ui/CodeBlock";
import { PhaseNav } from "@/components/phases/PhaseNav";
import { PhaseNavTop } from "@/components/phases/PhaseNavTop";
import { PhaseTabs } from "@/components/phases/PhaseTabs";
import { Phase4ArchitectureDiagram } from "@/components/phases/Phase4ArchitectureDiagram";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Phase 4: Agentic Discovery",
  description: "Capturing years of cross-divisional learning in 90 days through agent discovery rather than workflow design. Three division agents, adaptive depth limiting, and autonomous collaboration patterns generating training data for orchestrator development.",
};

export default function Phase4() {
  return (
    <>
      <PageHeader
        title="Phase 4: Agentic Discovery"
        subtitle="Capturing years of cross-divisional learning in 90 days through agent discovery rather than workflow design"
      >
        <div className="flex flex-wrap gap-4 mt-4">
          <div className="text-base">
            <span className="text-white/60">Direct Investment:</span>
            <span className="ml-2 font-semibold">$15,500</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Time:</span>
            <span className="ml-2 font-semibold">90 days</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Agents:</span>
            <span className="ml-2 font-semibold">3 division services</span>
          </div>
        </div>
        <div className="mt-6">
          <p className="text-base text-white/80 font-semibold mb-2">Deliverables:</p>
          <ul className="text-base text-white/70 space-y-1">
            <li>• 3 division agent services (Fundraising, Field Operations, Business Development)</li>
            <li>• 7-phase adaptive depth limiting experiment (depth 1→2→3→2→4→2→adaptive)</li>
            <li>• 900 A2A interaction logs generating Phase 5 orchestrator training data</li>
            <li>• Validated collaboration patterns with quantified cost-value tradeoffs</li>
          </ul>
        </div>
      </PageHeader>

      <PhaseNavTop currentPhase={4} />

      <section className="py-12">
        <Container>
          <PhaseTabs
            vision={
              <>
                <p className="text-lg text-gray-700 mb-8">
                  Capturing years of cross-divisional learning in 90 days through agent discovery rather than workflow design
                </p>

                <div className="prose prose-lg max-w-none">
                  <p>
                    This Phase generates strategic intelligence no planning session can produce. For $6,000, the organization deploys three division agents (Fundraising, Field Operations, Business Development) as independent services and observes which collaboration patterns emerge organically over 90 days. This isn&apos;t about connecting systems. It&apos;s about capturing the relational intelligence that normally lives in people&apos;s heads: which teams should coordinate on what tasks, when division handoffs add value, where cross-functional workflows emerge naturally through actual work rather than theoretical design.
                  </p>

                  <h3 className="text-2xl font-semibold mt-8 mb-4">Strategic Value:</h3>
                  <p>
                    The 90-day discovery phase compresses years of organizational learning into structured training data. Traditional enterprises spend years discovering which cross-functional collaborations work, which create overhead, and which patterns deliver consistent value. This knowledge accumulates through informal networks, tribal knowledge, and incremental adjustments to who coordinates with whom. This Phase automates that discovery by letting agents experiment with collaboration patterns, logging every pathway, measuring every handoff, and testing workflow depths from simple (1-level delegation) to complex (4-level cascades). The result is quantified evidence—not opinions—about what collaboration patterns deliver value and which create coordination overhead without commensurate return.
                  </p>

                  <h3 className="text-2xl font-semibold mt-8 mb-4">What&apos;s Delivered:</h3>
                  <p>
                    Three division agents running as sandboxed services using A2A (Agent-to-Agent) protocol for autonomous collaboration discovery. 90 days of structured experimentation testing depth limits from 1 to 4 with control phases detecting drift. Comprehensive call logs capturing every delegation decision, synthesis pattern, and workflow outcome. Training dataset for Phase 5&apos;s orchestrator showing discovered collaboration patterns grounded in real usage. Validated insights about cross-divisional coordination that can stand alone or feed forward. Complete optionality: $6,000 investment delivers proprietary intelligence about optimal workflows whether the organization continues to Phase 5 or stops with validated collaboration insights.
                  </p>
                </div>
              </>
            }
            approach={
              <>
                <Card className="bg-gradient-to-br from-teal/5 to-navy/5 border-teal/20 border-t-4 border-t-teal p-12">
                  <p className="text-lg text-gray-700 mb-8">
                    Autonomous agent discovery with adaptive depth limiting generates collaboration intelligence grounded in actual organizational workflows rather than aspirational process designs
                  </p>

                  <div className="prose prose-lg max-w-none">
                    <p className="mb-8">
                      This Phase chose agent-driven discovery over designed orchestration because no planning session can predict which cross-divisional collaborations deliver value in practice. Traditional enterprise integration projects diagram ideal workflows that fail because they represent aspirational processes, not actual work patterns shaped by availability bottlenecks, informal coordination channels, and timing dependencies that only emerge under real conditions. This approach acknowledges that cross-divisional coordination patterns can&apos;t be designed upfront—they must be discovered through experimentation in environments where failure costs nothing beyond logging and success generates validated intelligence for future optimization.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">Discovery Through Experimentation Rather Than Designed Orchestration</h3>
                    <p>
                      This Phase chose agent-driven discovery over designed orchestration because no planning session can predict which cross-divisional collaborations deliver value in practice. Traditional enterprise integration projects diagram ideal workflows that fail because they represent aspirational processes, not actual work patterns shaped by availability bottlenecks, informal coordination channels, and timing dependencies that only emerge under real conditions. This Phase deployed three division agents (Fundraising, Field Operations, Business Development) as independent services using the A2A protocol, then observed which collaboration patterns emerged organically through experimentation.
                    </p>
                    <p>
                      Every A2A interaction generated structured logs showing which agent initiated, which responded, what triggered the collaboration, and whether results improved outcomes. Over 90 days, thousands of interactions accumulated into a dataset showing which collaboration patterns worked consistently, which were context-dependent, and which created coordination overhead without commensurate value. The organization ran a structured experiment in a sandboxed environment where discovery was encouraged and failure cost nothing beyond logging, acknowledging that cross-divisional coordination patterns can&apos;t be designed upfront.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">Adaptive Depth Limiting to Understand Workflow Complexity</h3>
                    <p>
                      This Phase used adaptive depth limiting rather than unrestricted agent cascading because uncontrolled multi-agent systems create coordination overhead that quickly exceeds delivered value. Depth limiting controlled this by restricting how many levels deep an agent cascade could go—depth 1 meant no delegation, depth 2 allowed one level of coordination, depth 3 enabled three-level cascades. The 90-day schedule systematically explored different configurations: days 1-7 at depth 1 (baseline), days 8-21 at depth 2 (control phase one), days 22-35 at depth 3 (exploration), days 36-49 back to depth 2 (detecting drift), days 50-63 at depth 4 (complex cascades), days 64-75 at depth 2 again (control phase three), and days 76-90 running adaptive depth where a router chose depth dynamically.
                    </p>
                    <p>
                      This alternating pattern of exploration and control phases let the organization measure whether deeper workflows delivered proportional value or just created coordination overhead. The final adaptive period tested whether automated routing could learn to choose appropriate depth based on query patterns, preparing the groundwork for Phase 5&apos;s orchestrator training while generating empirical data about where the complexity-value tradeoff fell for this organization&apos;s specific workflows.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">Building on Phase 0 Registries for Agent Capability Discovery</h3>
                    <p>
                      This Phase leveraged Phase 0&apos;s model and training data registries rather than hardcoding agent capabilities because static configurations break as organizational capabilities evolve. The agents consulted registries at runtime to discover available capabilities dynamically—the Model Registry tracked which task models existed from Phase 2, how they consolidated into Phase 3&apos;s division agents, and what capabilities each offered. The agents also leveraged Phase 1&apos;s unified embedding space for semantic capability matching, using the fine-tuned embedding model to understand query semantics and match them to relevant capabilities across divisions rather than relying on hardcoded keyword routing.
                    </p>
                    <p>
                      This registry-driven approach created a self-describing system where capabilities were documented in the same place they were discovered, aligning with the discovery philosophy: agents learned which collaborations were valuable by experimenting with what the registry made available rather than following predetermined routing rules.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">Generating Training Data for Phase 5&apos;s Orchestrator</h3>
                    <p>
                      This Phase prioritized comprehensive logging because the real deliverable wasn&apos;t a working multi-agent production system but rather training data for Phase 5&apos;s orchestrator. Every A2A call generated a structured log entry capturing source agent, destination agent, original query, delegation decision rationale, responses received, synthesis approach, final output, latency, cost, workflow depth, and whether the multi-agent result improved outcomes. This training data provided positive examples of successful workflows, negative examples teaching when to keep queries single-agent, synthesis patterns across query types, and quantified cost-value tradeoffs.
                    </p>
                    <p>
                      The 90-day timeline balanced data quantity, diversity, and project duration while the adaptive depth schedule ensured training data included all complexity levels—simple single-agent responses, two-level coordination, deeper cascades, and learned adaptive routing. The architecture was explicitly designed as a learning phase with elevated instrumentation, not a production deployment. The $6,000 investment purchased both the infrastructure to run the experiment and the resulting proprietary intelligence about optimal collaboration patterns.
                    </p>
                  </div>
                </Card>

                <Card className="bg-teal/5 border-teal/20 p-8 mt-8">
                  <div className="flex items-start gap-6">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 rounded-full bg-teal/10 flex items-center justify-center">
                        <svg className="w-6 h-6 text-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                        </svg>
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold mb-2">Ready for Orchestrated Intelligence?</h3>
                      <p className="text-gray-600 mb-4">
                        The 90-day discovery experiment generates training data showing which collaboration patterns deliver value. Phase 5 transforms these insights into a production-ready orchestrator that routes queries intelligently, manages multi-agent workflows, and optimizes for cost-value tradeoffs based on empirically validated patterns.
                      </p>
                      <Link
                        href="/solution/phase-5"
                        className="inline-flex items-center text-teal hover:text-teal/80 font-medium focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2 rounded transition-colors"
                      >
                        Continue to Phase 5: Orchestrated Intelligence
                        <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </Link>
                    </div>
                  </div>
                </Card>
              </>
            }
            technical={
              <>
                {/* Architecture Diagram */}
                <div className="mb-12 bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                  <Phase4ArchitectureDiagram />
                </div>

                {/* Architecture Overview */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Architecture Overview</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Four-Program Pipeline</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 4 implements a four-program architecture that deploys MoE agents and orchestrates the 90-day discovery experiment:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 1: Import</strong> loads Phase 3&apos;s merged MoE models and prepares them for A2A agent wrapping, validating model compatibility and extracting capability metadata.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 2: Agent Services</strong> deploys three FastAPI services (ports 8001-8003) wrapping each division&apos;s MoE with A2A protocol capabilities, depth limiting, and call logging.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 3: Discovery Pipeline</strong> orchestrates the seven-phase experiment schedule, varying depth limits across 90 days while routing queries to simulate real-world usage patterns.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    <strong>Program 4: Training Data Preparation</strong> converts accumulated JSONL call logs into fine-tuning datasets for Phase 5&apos;s orchestrator, extracting routing decisions and workflow patterns.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Technology Stack</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Services:</strong> FastAPI with async request handling, independent scaling</li>
                    <li><strong>Protocol:</strong> Custom A2A with depth tracking, trace IDs, and status codes</li>
                    <li><strong>Discovery:</strong> Semantic peer matching using Phase 1&apos;s embedding space</li>
                    <li><strong>Logging:</strong> JSONL files organized by experiment phase (phase_1.jsonl - phase_7.jsonl)</li>
                    <li><strong>Integration:</strong> Phase 0 registries tracking agent deployments and experiment metadata</li>
                  </ul>
                </div>

                <div className="space-y-16">
                  {/* Part 1: System Architecture */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">1. Agent Network Details</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        This Phase deploys three specialized agents (Fundraising, Business Development, Field Operations) as independent FastAPI services communicating through a custom A2A (Agent-to-Agent) protocol. Each agent runs on a separate port (8001-8003), enabling horizontal scaling, independent deployment, and fault isolation. The agents wrap Phase 3&apos;s MoE models with A2A protocol capabilities, adding depth-limited cascading, semantic peer discovery, and comprehensive call logging.
                      </p>
                      <p>
                        The architecture prioritizes autonomous collaboration over centralized orchestration. Agents self-describe their capabilities through structured metadata, discover relevant peers through semantic search against Phase 1&apos;s embedding space, and independently decide when to cascade requests based on their own assessment of whether they need complementary expertise. The discovery pipeline orchestrates the 90-day experiment, systematically varying depth limits while the call logger captures every interaction to JSONL files for Phase 5 training data.
                      </p>
                      <p className="text-base text-gray-600 mt-4">
                        <strong>Files:</strong> <code>phase-4-agentic-discovery/src/shared/a2a_protocol.py</code>, <code>phase-4-agentic-discovery/src/program2_agent_services/service_factory.py</code>
                      </p>
                    </div>
                  </div>

                  {/* Part 2: A2A Protocol Implementation */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">2. A2A Protocol Implementation</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        The A2A protocol enables autonomous multi-agent collaboration through structured request/response messaging with depth tracking. Each A2A request carries metadata specifying the current call depth, maximum allowed depth, source agent, target agent, and a trace ID linking related calls into reconstructable chains. The protocol defines status codes including <code>DEPTH_EXCEEDED</code> to signal when cascade limits prevent query completion, enabling the system to detect when workflows require deeper collaboration than the current experiment phase allows.
                      </p>
                    </div>

                    <CodeBlock language="python" code={`@dataclass
class A2AMetadata:
    call_id: str
    timestamp: datetime
    call_depth: int          # Current depth in cascade chain
    max_depth: int           # Maximum allowed depth
    source_agent: str
    target_agent: str
    trace_id: Optional[str]  # Links full call chains`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        Agents process requests by first checking depth limits. If <code>call_depth &gt;= max_depth</code>, they immediately return <code>DEPTH_EXCEEDED</code> without wasting computation. Otherwise, they generate responses using their MoE models, extract any embedded A2A calls (marked with XML tags containing JSON), execute cascading calls to peer agents with incremented depth, and synthesize final responses. Every completed call gets logged to JSONL with full metadata, creating the training corpus for Phase 5.
                      </p>
                      <p className="text-base text-gray-600 mt-4">
                        <strong>File:</strong> <code>phase-4-agentic-discovery/src/program2_agent_services/agent_wrapper.py:79-150</code>
                      </p>
                    </div>
                  </div>

                  {/* Part 3: Adaptive Depth Limiting Schedule */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">3. Adaptive Depth Limiting Schedule</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        The 90-day discovery experiment follows a seven-phase schedule systematically varying depth limits: Phase 1 (days 1-7, depth=1) establishes baseline single-agent performance. Phase 2 (days 8-21, depth=2) tests single-level cascading. Phase 3 (days 22-35, depth=3) explores two-level collaboration. Phase 4 (days 36-49, depth=2) returns to the control configuration to detect system drift. Phase 5 (days 50-63, depth=4) tests complex multi-level cascades. Phase 6 (days 64-75, depth=2) provides final drift validation. Phase 7 (days 76-90, adaptive) uses workflow-specific depth limits where a router chooses depth dynamically based on query characteristics.
                      </p>
                      <p>
                        The alternating exploration and control phases generate empirical evidence about the complexity-value tradeoff. Control phases returning to depth=2 serve as benchmarks detecting whether agent behavior drifts over time or remains stable under repeated use. The final adaptive period tests whether learned routing can choose appropriate depth based on query patterns, preparing the groundwork for Phase 5&apos;s orchestrator while validating that depth selection can be learned rather than manually configured. Logs are organized by phase (<code>phase_1.jsonl</code> through <code>phase_7.jsonl</code>), enabling depth-stratified analysis and comparison across experimental conditions.
                      </p>
                    </div>

                    <div className="mt-6 bg-gray-50 rounded-lg border border-gray-200 p-6">
                      <h4 className="text-lg font-semibold mb-4">Test Workflows</h4>
                      <div className="space-y-4">
                        <div>
                          <p className="font-medium text-gray-900">investor_profile (depth=2)</p>
                          <p className="text-base text-gray-600">&quot;Profile investor INV-{'{id}'} including competitive landscape&quot;</p>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">rfp_analysis (depth=3)</p>
                          <p className="text-base text-gray-600">&quot;Analyze RFP-{'{id}'} including potential investors and local capacity&quot;</p>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">regional_analysis (depth=2)</p>
                          <p className="text-base text-gray-600">&quot;Regional analysis for {'{country}'} including investors and RFPs&quot;</p>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">simple_query (depth=1)</p>
                          <p className="text-base text-gray-600">&quot;What is the capacity of investor INV-123?&quot;</p>
                        </div>
                      </div>
                    </div>

                    <p className="text-base text-gray-600 mt-4">
                      <strong>Files:</strong> <code>phase-4-agentic-discovery/src/program3_discovery_pipeline/phase_config.py:52-135</code>, <code>phase-4-agentic-discovery/src/program3_discovery_pipeline/pipeline_runner.py:104-146</code>
                    </p>
                  </div>

                  {/* Part 4: Semantic Agent Discovery */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">4. Semantic Agent Discovery</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        Agents discover relevant peers through semantic search powered by Phase 1&apos;s embedding infrastructure. Each agent registers its capabilities (domains, example queries, dependencies) with a ChromaDB-backed discovery backend. When an agent receives a query requiring external expertise, it can query the discovery backend with a natural language description to find the most relevant peer agents based on semantic similarity rather than hardcoded routing rules.
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Agent capability registration
capability = A2ACapability(
    agent_id="fundraising-agent",
    name="Fundraising",
    description="Provides investor profiles, investment capacity analysis",
    domains=["investor profiles", "investment capacity", "sector interests"],
    example_queries=["What is the investment capacity of INV-123?", ...],
    dependencies=["business-development-agent", "field-operations-agent"]
)

# Semantic discovery
results = discovery_backend.discover_agents(
    query="I need local market intelligence and regional capacity data",
    top_k=2
)
# Returns: [(FieldOperationsCapability, 0.87), (BusinessDevelopmentCapability, 0.62)]`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        The current implementation uses static dependency lists from capability definitions, but the discovery infrastructure enables future versions to activate fully autonomous agent networks where agents dynamically discover new peers as capabilities evolve. An in-memory discovery backend provides keyword-based matching for testing without ChromaDB dependencies.
                      </p>
                      <p className="text-base text-gray-600 mt-4">
                        <strong>File:</strong> <code>phase-4-agentic-discovery/src/shared/discovery_backend.py:53-243</code>
                      </p>
                    </div>
                  </div>

                  {/* Part 5: Call Chain Logging */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">5. Call Chain Logging</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        Every A2A interaction generates a structured log entry capturing source agent, target agent, original query, call depth, max depth configured for that phase, response status, execution time, which agents were cascaded to, and the workflow identifier. These logs accumulate into phase-specific JSONL files creating a comprehensive dataset showing which collaboration patterns worked consistently, which were context-dependent, and which created coordination overhead without commensurate value.
                      </p>
                    </div>

                    <CodeBlock language="json" code={`{
  "call_id": "a7f3c2e1-4b5d-6a8e-9f0b-1c2d3e4f5a6b",
  "timestamp": "2026-01-21T10:30:45.123456",
  "source_agent": "discovery-pipeline",
  "target_agent": "fundraising-agent",
  "goal": "Profile investor INV-456 including competitive landscape",
  "call_depth": 0,
  "max_depth": 2,
  "status": "success",
  "execution_time_ms": 234.56,
  "cascaded_calls": ["business-development-agent"],
  "phase": 2,
  "workflow_id": "investor_profile"
}`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        The call logger provides phase-specific statistics (success rates, average depth utilization, timing analysis) and exports unified datasets for external analysis. After the 90-day experiment completes, the orchestrator exporter transforms these logs into training data formatted for Phase 5&apos;s instruction fine-tuning, including positive examples of successful multi-agent workflows, negative examples teaching when to keep queries single-agent, synthesis patterns across query types, and quantified cost-value tradeoffs.
                      </p>
                      <p className="text-base text-gray-600 mt-4">
                        <strong>Files:</strong> <code>phase-4-agentic-discovery/src/shared/call_logger.py:92-231</code>, <code>phase-4-agentic-discovery/src/program4_adaptive_analyzer/orchestrator_exporter.py:158-224</code>
                      </p>
                    </div>
                  </div>

                  {/* Part 6: Agent Specializations */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">6. Agent Specializations</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        Each of the three agents wraps a unit-specific MoE model from Phase 3 with A2A protocol capabilities. The Fundraising agent handles investor profiles, investment capacity analysis, and sector interest matching, typically cascading to Business Development for competitive landscape data. The Business Development agent tracks RFPs, funding opportunities, and competitive analysis, cascading to Fundraising for investor matching or Field Operations for capacity checks. The Field Operations agent provides local market intelligence, project performance data, and regional capacity assessment, cascading to other agents for funding or strategic context.
                      </p>
                      <p>
                        All three agents can cascade to each other, creating a fully connected agent network. The dependency lists in their capability definitions specify which peers each can call, while their MoE models (Llama 3.1 8B with 4-5 experts per unit) handle domain-specific reasoning. An additional A2A adapter (LoRA fine-tuning) teaches each agent the protocol syntax and delegation patterns. The agent registry maps agent IDs to service URLs (<code>fundraising-agent: http://localhost:8001</code>), enabling HTTP-based cascading calls.
                      </p>
                      <p className="text-base text-gray-600 mt-4">
                        <strong>Files:</strong> <code>phase-4-agentic-discovery/src/program2_agent_services/agents/fundraising.py:9-33</code>, <code>phase-4-agentic-discovery/src/program2_agent_services/agents/business_development.py</code>, <code>phase-4-agentic-discovery/src/program2_agent_services/agents/field_operations.py</code>
                      </p>
                    </div>
                  </div>

                  {/* Part 7: Phase 0 Registry Integration */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">7. Phase 0 Registry Integration</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        This Phase integrates with Phase 0&apos;s infrastructure registries to track datasets, models, and experiments. The <code>Phase4DataRegistry</code> registers A2A training datasets (protocol fine-tuning data per unit), discovery logs (phase-specific call logs with depth and success metrics), and Phase 5 export datasets (orchestrator training data with optimal depth recommendations). The <code>Phase4ModelRegistry</code> tracks A2A adapters (LoRA adapters adding protocol capabilities to MoE models) with metadata linking them to source datasets and training configurations. The <code>Phase4ExperimentTracker</code> logs fine-tuning experiments and discovery runs for reproducibility.
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Register discovery logs as tracked dataset
registry.register_discovery_logs(
    dataset_id="phase-4/discovery/phase3-logs/v1",
    logs_path=Path("data/logs/discovery/phase_3.jsonl"),
    discovery_phase=3,
    max_depth=3,
    total_calls=140,
    success_rate=0.936
)

# Register Phase 5 export
registry.register_phase5_export(
    dataset_id="phase-4/discovery/orchestrator-export/v1",
    train_path=Path("data/exports/orchestrator_training.jsonl"),
    num_examples=2800,
    optimal_depths={
        "investor_profile": 2,
        "rfp_analysis": 3,
        "regional_analysis": 2,
        "simple_query": 1
    }
)`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        This integration enables tracing which datasets trained which models, comparing performance across experimental phases, versioning log datasets for reproducibility, and providing Phase 5 with structured metadata about optimal collaboration patterns discovered during the experiment.
                      </p>
                      <p className="text-base text-gray-600 mt-4">
                        <strong>File:</strong> <code>phase-4-agentic-discovery/src/shared/phase0_integration.py:41-445</code>
                      </p>
                    </div>
                  </div>

                  {/* Part 8: Deployment & Operations */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">8. Deployment & Operations</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        Agents deploy as independent FastAPI services exposing health check, capability metadata, A2A protocol, and simplified query endpoints. For production, each agent runs in a separate process or container enabling horizontal scaling and fault isolation. The CLI provides multiple deployment modes: <code>--start-all</code> runs all three agents from a single process for development, <code>--start &lt;agent-id&gt;</code> runs a specific agent, and <code>--test-mode</code> uses mock models without GPU requirements for testing and development.
                      </p>
                    </div>

                    <CodeBlock language="bash" code={`# Production deployment (3 terminals)
python -m src.program2_agent_services.main --start fundraising-agent --port 8001
python -m src.program2_agent_services.main --start business-development-agent --port 8002
python -m src.program2_agent_services.main --start field-operations-agent --port 8003

# Discovery pipeline execution
python -m src.program3_discovery_pipeline.main --queries-per-day 10

# Orchestrator export after 90 days
python -m src.program4_adaptive_analyzer.main --export-orchestrator`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        Configuration uses Pydantic-based settings with environment variable support (<code>PHASE4_TEST_MODE=true</code>, <code>PHASE4_AGENT_SERVICES__BASE_PORT=9000</code>), YAML config files for deployment profiles, and direct instantiation for programmatic control. The discovery pipeline runs unattended for 90 days, generating 900 queries (10 per day) distributed across four test workflows with varying depth requirements. The adaptive analyzer processes logs after completion to determine optimal depths per workflow and export Phase 5 training data in ChatML format.
                      </p>
                    </div>

                    <div className="mt-6 bg-gray-50 rounded-lg border border-gray-200 p-6">
                      <h4 className="text-lg font-semibold mb-4">Production vs Test Mode</h4>
                      <div className="grid md:grid-cols-2 gap-6">
                        <div>
                          <p className="font-medium text-gray-900 mb-2">Production Mode</p>
                          <ul className="text-base text-gray-600 space-y-1">
                            <li>• 90 days duration</li>
                            <li>• 10 queries per day = 900 total queries</li>
                            <li>• Real MoE models with GPU requirements</li>
                            <li>• Full agent cascading and collaboration</li>
                          </ul>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900 mb-2">Test Mode</p>
                          <ul className="text-base text-gray-600 space-y-1">
                            <li>• 7 days duration</li>
                            <li>• 5 queries per day = 35 total queries</li>
                            <li>• Mock models without GPU</li>
                            <li>• Validates infrastructure and logging</li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <p className="text-base text-gray-600 mt-4">
                      <strong>Files:</strong> <code>phase-4-agentic-discovery/src/program2_agent_services/main.py:175-236</code>, <code>phase-4-agentic-discovery/config/settings.py:69-136</code>
                    </p>
                  </div>

                  {/* Part 9: Expected Performance & Discovery Insights */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">9. Expected Performance & Discovery Insights</h3>
                    <div className="prose prose-lg max-w-none">
                      <p>
                        The 90-day experiment generates quantifiable insights about multi-agent collaboration effectiveness across different workflow depths. Expected performance improves as the system learns optimal delegation patterns, with baseline single-agent performance (Phase 1, depth=1) showing 60-70% success rates on complex queries requiring cross-divisional information. Enabling single-level cascading (Phase 2, depth=2) increases success to 85-90% as agents access complementary expertise. Deeper cascades (Phase 3-5) test whether additional coordination layers deliver proportional value or create overhead. The final adaptive period (Phase 7) validates whether learned routing can achieve 94-97% success by dynamically selecting appropriate depths.
                      </p>
                    </div>

                    <div className="mt-6 bg-gray-50 rounded-lg border border-gray-200 p-6">
                      <h4 className="text-lg font-semibold mb-4">Phase-by-Phase Performance Expectations</h4>
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-gray-300">
                            <th className="text-left py-2 font-semibold">Phase</th>
                            <th className="text-left py-2 font-semibold">Depth</th>
                            <th className="text-left py-2 font-semibold">Expected Success Rate</th>
                            <th className="text-left py-2 font-semibold">Key Insight</th>
                          </tr>
                        </thead>
                        <tbody className="text-gray-700">
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Phase 1</td>
                            <td className="py-2">1</td>
                            <td className="py-2">60-70%</td>
                            <td className="py-2">Baseline single-agent performance</td>
                          </tr>
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Phase 2</td>
                            <td className="py-2">2</td>
                            <td className="py-2">85-90%</td>
                            <td className="py-2">Single-level delegation adds significant value</td>
                          </tr>
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Phase 3</td>
                            <td className="py-2">3</td>
                            <td className="py-2">88-92%</td>
                            <td className="py-2">Two-level cascades help complex queries</td>
                          </tr>
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Phase 4</td>
                            <td className="py-2">2</td>
                            <td className="py-2">85-90%</td>
                            <td className="py-2">Control phase validates consistency</td>
                          </tr>
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Phase 5</td>
                            <td className="py-2">4</td>
                            <td className="py-2">86-90%</td>
                            <td className="py-2">Deeper cascades show diminishing returns</td>
                          </tr>
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Phase 6</td>
                            <td className="py-2">2</td>
                            <td className="py-2">85-90%</td>
                            <td className="py-2">Final drift detection</td>
                          </tr>
                          <tr>
                            <td className="py-2 font-medium">Phase 7</td>
                            <td className="py-2">Adaptive</td>
                            <td className="py-2 font-medium">94-97%</td>
                            <td className="py-2 font-medium">Learned routing optimizes per-query</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <div className="prose prose-lg max-w-none mt-6">
                      <p>
                        These performance metrics inform Phase 5&apos;s orchestrator training by demonstrating that single-level delegation (depth=2) delivers strong performance for most queries, deeper cascades help specific complex workflows but show diminishing returns, and adaptive routing can optimize dynamically. The cost analysis reveals that depth=2 workflows typically complete in 2-3 seconds at $0.02-0.04 per query while depth=4 cascades take 5-8 seconds at $0.08-0.12 per query, providing quantified tradeoffs between response quality, latency, and cost for different workflow patterns.
                      </p>
                    </div>
                  </div>
                </div>
              </>
            }
          />

          {/* Next Steps CTA */}
          <Card className="bg-gradient-to-br from-teal/5 to-navy/5 border-teal/20 p-12 mt-12">
            <div className="max-w-3xl">
              <h2 className="text-3xl font-bold mb-4">Ready for Phase 5?</h2>
              <p className="text-lg text-gray-700 mb-6">
                The 90-day discovery experiment has generated comprehensive training data showing which collaboration patterns deliver value. Phase 5 transforms these insights into a production-ready orchestrator that routes queries intelligently, manages multi-agent workflows efficiently, and optimizes for the cost-value tradeoffs validated through empirical experimentation.
              </p>
              <a
                href="/solution/phase-5"
                className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal/90 text-white font-medium rounded-lg transition-colors"
              >
                Continue to Phase 5: Orchestrated Intelligence
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </a>
            </div>
          </Card>
        </Container>
      </section>

      <PhaseNav currentPhase={4} />
    </>
  );
}
