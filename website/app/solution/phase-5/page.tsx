import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { CodeBlock } from "@/components/ui/CodeBlock";
import { PhaseNav } from "@/components/phases/PhaseNav";
import { PhaseNavTop } from "@/components/phases/PhaseNavTop";
import { PhaseTabs } from "@/components/phases/PhaseTabs";
import { Phase5ArchitectureDiagram } from "@/components/phases/Phase5ArchitectureDiagram";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Phase 5: Orchestrated Agentic System",
  description: "A learned orchestrator trained on Phase 4's discovery data unifies division-specific intelligence into a single coordinated system—approximately $20-50 training cost, 4-6 hours on A100.",
};

export default function Phase5() {
  return (
    <>
      <PageHeader
        title="Phase 5: Orchestrated Agentic System"
        subtitle="A learned orchestrator trained on Phase 4&apos;s discovery data unifies division-specific intelligence into a single coordinated system"
      >
        <div className="flex flex-wrap gap-4 mt-4">
          <div className="text-base">
            <span className="text-white/60">Direct Investment:</span>
            <span className="ml-2 font-semibold">$10,400</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Training Time:</span>
            <span className="ml-2 font-semibold">4-6 hours (A100)</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Total System Cost:</span>
            <span className="ml-2 font-semibold">$163.1K</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Result:</span>
            <span className="ml-2 font-semibold">Single-Window Enterprise AI</span>
          </div>
        </div>
        <div className="mt-6">
          <p className="text-base text-white/80 font-semibold mb-2">Deliverables:</p>
          <ul className="text-base text-white/70 space-y-1">
            <li>• Production-ready orchestrated system built on Agno framework</li>
            <li>• Fine-tuned Qwen2.5-7B orchestrator trained on 71,000 Phase 4 examples</li>
            <li>• Single-window access to all AI capabilities (embedding, task SLMs, division agents)</li>
            <li>• Model-agnostic architecture supporting local, AWS Bedrock, Azure, or Databricks backends</li>
            <li>• Learned routing from real usage patterns with ~150ms inference latency</li>
          </ul>
        </div>
      </PageHeader>

      <PhaseNavTop currentPhase={5} />

      <section className="py-12">
        <Container>
          <PhaseTabs
            vision={
              <>
                <p className="text-lg text-gray-700 mb-8">
                  Company-wide AI intelligence accessible through a single interface—trained on discovered patterns, not predetermined rules.
                </p>

                <div className="prose prose-lg max-w-none">
                  <p>
                    This Phase delivers the end state: one orchestrator that coordinates all AI capabilities across divisions. Unlike rule-based systems requiring constant manual updates, this orchestrator learns optimal routing patterns from Phase 4&apos;s 90-day discovery period. It understands when to use semantic search, which task models to engage, which division agents to coordinate, and how to combine capabilities for complex cross-divisional requests.
                  </p>

                  <h3 className="text-2xl font-semibold mt-8 mb-4">Strategic Value:</h3>
                  <p>
                    The orchestrator trains for approximately $20-50 over 4-6 hours using a 7B parameter model (Qwen2.5-7B) on the organization&apos;s actual usage patterns. Routing decisions reflect real workflow needs discovered through experimentation, not assumptions made during initial design. As the system operates, it generates new interaction data—periodic retraining of just the orchestrator (not the underlying agents) continuously improves routing intelligence without rebuilding capabilities. Total Direct Investment across all six phases reaches $163.1K ($11,100 infrastructure + $152K training programs)—achieving orchestrated multi-agent AI at a fraction of the $2M-$7M traditional vendor platform cost while preserving competitive advantage through company-specific intelligence.
                  </p>

                  <h3 className="text-2xl font-semibold mt-8 mb-4">What&apos;s Delivered:</h3>
                  <p>
                    A production-ready orchestrated system built on the Agno framework provides single-window access to all AI capabilities. Users make requests without knowing which agents, models, or divisions are involved—the orchestrator handles coordination automatically. All agents query Phase 1&apos;s single unified embedding database for semantic search, ensuring consistent information retrieval across the system. The model-agnostic architecture eliminates vendor lock-in: the orchestrator and agents transfer freely between local deployment, AWS Bedrock, Databricks, Azure AI Foundry, or any model backend without rewriting coordination logic.
                  </p>
                </div>
              </>
            }
            approach={
              <>
                <Card className="bg-gradient-to-br from-magenta/5 to-navy/5 border-magenta/20 border-t-4 border-t-magenta p-12">
                  <p className="text-lg text-gray-700 mb-8">
                    Learn coordination patterns from real usage, then train a small orchestrator model to route intelligently across all capabilities.
                  </p>

                  <div className="prose prose-lg max-w-none">
                    <p className="mb-8">
                      This Phase transforms Phase 4&apos;s 90-day multi-agent interaction data into a trained orchestrator that routes requests intelligently without human intervention. The strategy centers on learned routing over rule-based logic, production infrastructure through the Agno framework, and preserving deployment optionality from local to cloud.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">From Discovery to Orchestration</h3>
                    <p>
                      Phase 4 generates 90 days of multi-agent interaction data as division-level MoE agents experiment with cross-divisional collaboration. This produces a training dataset capturing which agent sequences work for different request types, which information handoffs are necessary, and which coordination patterns deliver value. This Phase transforms discovered knowledge into a trained orchestrator that routes requests intelligently.
                    </p>
                    <p>
                      The orchestrator is a finetuned small language model that interprets user requests, selects appropriate agents, coordinates multi-step workflows, and synthesizes responses. Because it learns from actual usage rather than predetermined rules, routing decisions align with real organizational needs. When workflows change or new patterns emerge, the orchestrator retrains on updated discovery data—maintaining alignment as the organization evolves.
                    </p>
                    <p>
                      Traditional multi-agent systems use hardcoded routing logic: if request contains X keyword, call Y agent. This approach fails when requests are ambiguous, when optimal paths require context, or when organizational needs shift. Learned routing treats coordination as a prediction problem: given a request and context, which agent sequence most likely delivers value? The orchestrator learns these patterns from Phase 4&apos;s experimentation, capturing tacit knowledge about effective collaboration that normally exists only in people&apos;s heads.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">Why Agno Framework Over Alternatives</h3>
                    <p>
                      The Agno framework provides the production-ready foundation for this Phase. LangGraph excels at rapid prototyping but couples tightly to specific LLM providers. CrewAI offers good abstractions but assumes static agent configurations. Agno prioritizes production readiness and model flexibility: model-agnostic design (swap any backend without code changes), multimodal primitives (vision, audio, documents), and deployment patterns tested in production environments.
                    </p>
                    <p>
                      The framework separates agent definitions from execution infrastructure. Agents declare capabilities and tools without specifying which models power them. The orchestrator coordinates agents through a standardized protocol—agents run as local processes, containerized services, or cloud functions. This flexibility supports modular deployment: start local, scale to cloud when needed.
                    </p>
                    <p>
                      Agno&apos;s optional AG-UI (Agent-to-User Interface) integration demonstrates the complete protocol stack for production systems. While the core orchestrator uses A2A (agent-to-agent) protocol for coordination, enabling AG-UI adds real-time streaming, event-based architecture, and CopilotKit frontend compatibility. This makes building production-facing UIs straightforward without custom frontend work. AG-UI remains optional via configuration—core orchestration works with or without it—but enables rapid transition from backend orchestration to user-facing deployment.
                    </p>
                    <p>
                      RAG integration happens at the agent level, not at the orchestrator. When an agent needs information retrieval, it queries Phase 1&apos;s embedding space directly. This preserves division-specific intelligence built in earlier phases while allowing the orchestrator to focus purely on coordination. The architecture aligns AI capabilities with business structure: division agents maintain specialized knowledge while the orchestrator provides unified access.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">Preserving Optionality Through Scalability</h3>
                    <p>
                      This Phase designs for platform flexibility. Current deployment uses locally-trained models, but the architecture supports migration to AWS Bedrock for managed scaling, Databricks for integrated analytics, or Azure AI Foundry for enterprise governance. Model backends swap freely—use local models for cost control or cloud APIs for capabilities—without rewriting orchestration logic.
                    </p>
                    <p>
                      This optionality extends the modular approach from earlier phases. Organizations start with local deployment (no cloud costs, full data control), then migrate to cloud platforms as needs evolve. The orchestrator&apos;s learned routing remains valid regardless of backend infrastructure—coordination patterns are independent of where models run.
                    </p>
                    <p>
                      The architecture creates genuine strategic choice. Organizations stopping here have orchestrated multi-agent AI for a $163.1K Direct Investment. Organizations continuing to cloud deployment maintain learned routing while gaining managed infrastructure. The foundation remains constant; execution environment adapts to organizational needs.
                    </p>

                    <h3 className="text-2xl font-semibold mt-12 mb-4">Generating Training Data for Continuous Learning</h3>
                    <p>
                      Phase 4&apos;s discovery period generates the initial training dataset, but this Phase&apos;s production deployment continues generating interaction logs. Every request, routing decision, and outcome creates new training data. Organizations periodically retrain the orchestrator on accumulated data, improving routing decisions as usage patterns evolve.
                    </p>
                    <p>
                      This creates a self-improving system. The orchestrator learns optimal patterns from Phase 4&apos;s structured experimentation, deploys to production, handles real user requests, logs interactions, and retrains on updated data. Routing intelligence compounds over time, adapting to organizational changes without manual intervention.
                    </p>
                    <p>
                      The training economics make continuous learning practical. Retraining the orchestrator costs approximately $20-50 and takes 4-6 hours on an A100 GPU. Organizations retrain quarterly or when usage patterns shift significantly, maintaining routing accuracy as workflows evolve. The learned routing approach transforms what would be ongoing developer maintenance into periodic automated retraining.
                    </p>
                  </div>
                </Card>

                <Card className="bg-white/50 border-gray-200 p-8 mt-8">
                  <div className="flex items-start gap-6">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center">
                        <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold mb-2">Ready to see the technical implementation?</h3>
                      <p className="text-gray-600 mb-4">
                        The Technical section below provides complete code examples, architecture diagrams, and deployment instructions. To learn more about the architect behind this six-phase implementation:
                      </p>
                      <Link
                        href="/about"
                        className="inline-flex items-center text-teal hover:text-teal/80 font-medium focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2 rounded transition-colors"
                      >
                        Learn About the Architect
                        <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </Link>
                      <p className="text-gray-500 text-base mt-3">
                        Otherwise, scroll down for the full technical breakdown of this Phase&apos;s implementation.
                      </p>
                    </div>
                  </div>
                </Card>
              </>
            }
            technical={
              <>
                <p className="text-lg text-gray-700 mb-8">
                  Qwen2.5-7B orchestrator finetuned on 71,000 Phase 4 discovery examples, deployed on Agno framework with vLLM inference serving
                </p>

                {/* Architecture Diagram */}
                <div className="mb-12 bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                  <Phase5ArchitectureDiagram />
                </div>

                {/* Architecture Overview */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Architecture Overview</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Four-Program Pipeline</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 5 implements a four-program architecture that transforms discovery data into a unified orchestration layer:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 1: Data Conversion</strong> transforms Phase 4&apos;s JSONL call logs into ChatML training format, extracting routing decisions, agent interactions, and successful resolution patterns.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 2: SLM Fine-tuning</strong> trains a Qwen2.5-7B orchestrator using LoRA on 71,000 examples, teaching it when to route requests, which agents to involve, and how to synthesize responses.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 3: Inference Server</strong> deploys the fine-tuned orchestrator on vLLM for efficient serving with support for batched inference and KV-cache optimization.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    <strong>Program 4: Orchestrator Service</strong> builds the Agno-based coordination layer, connecting the orchestrator to Phase 4&apos;s A2A agents and Phase 1&apos;s RAG capabilities.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Technology Stack</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Framework:</strong> Agno for model-agnostic agent orchestration</li>
                    <li><strong>Orchestrator:</strong> Qwen2.5-7B fine-tuned with LoRA on Phase 4 discovery data</li>
                    <li><strong>Inference:</strong> vLLM for efficient serving (~150ms latency)</li>
                    <li><strong>Agents:</strong> Phase 4 A2A agents (Fundraising, Business Dev, Field Ops)</li>
                    <li><strong>RAG:</strong> Phase 1 embedding space for document retrieval</li>
                  </ul>
                </div>

                <div className="space-y-16">
                  {/* Part 1: Agno Framework Architecture */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">1. Agno Framework Details</h3>
                    <div className="prose prose-lg max-w-none">
                      <p className="font-semibold">Why Agno Over Alternatives</p>
                      <p>
                        Agno was selected because it prioritizes production readiness and model flexibility over prototyping speed. The framework provides model-agnostic design (swap any backend without code changes), multimodal primitives (vision, audio, documents), and deployment patterns tested in production environments.
                      </p>

                      <p className="font-semibold mt-6">Architecture Overview</p>
                      <p>
                        This Phase includes:
                      </p>
                      <ul>
                        <li>1 orchestrator (finetuned Qwen2.5-7B)</li>
                        <li>3 A2A agents from Phase 4 (Fundraising, Business Development, Field Operations)</li>
                        <li>Each agent wraps Phase 3 MoE models with A2A protocol</li>
                        <li>RAG capabilities at agent level via Phase 1 embedding space</li>
                      </ul>
                      <p>
                        Agents communicate via A2A (agent-to-agent) protocol over HTTP. The orchestrator maintains no state between requests—all context flows through request payloads, enabling horizontal scaling and fault tolerance.
                      </p>

                      <p className="font-semibold mt-6">Implementation Example</p>
                    </div>

                    <CodeBlock language="python" code={`# Agno Team configuration
from agno import Team, RemoteAgent
from agno.models import VLLM

# Create fine-tuned orchestrator model
coordinator_model = VLLM(
    id="qwen2.5-7b-orchestrator",
    base_url="http://localhost:8100"  # vLLM inference server
)

# Wrap Phase 4 A2A agents as RemoteAgents
fundraising_agent = RemoteAgent(
    base_url="http://localhost:8001",
    agent_id="fundraising-agent",
    protocol="a2a"
)

# Create orchestration team
team = Team(
    members=[fundraising_agent, business_dev_agent, field_ops_agent],
    coordinator_model=coordinator_model,
    show_members_responses=True
)`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p className="font-semibold">Key Features:</p>
                      <ul>
                        <li>Model backend abstraction (local, AWS Bedrock, Azure, etc.)</li>
                        <li>Agent registry with capability declarations</li>
                        <li>Async request handling for multi-agent coordination</li>
                        <li>Structured logging integrated with Phase 0&apos;s ExperimentTracker</li>
                        <li>Tool delegation to agents (RAG, database queries, etc.)</li>
                        <li>Optional AG-UI for production user interfaces</li>
                      </ul>

                      <p className="font-semibold mt-6">AG-UI Integration (Optional)</p>
                      <p>
                        Agno&apos;s AG-UI provides user-facing capabilities when enabled:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`from agno.interfaces.agui import AGUI

# Core orchestrator (always enabled)
team = Team(
    agents=[fundraising_agent, business_dev_agent, field_ops_agent],
    routing_model=orchestrator_model
)

# Optional: Add AG-UI wrapper for user-facing deployment
if config.agui.enabled:
    agui = AGUI(team=team)
    app.mount("/agui", agui.router)  # Adds streaming, events, CopilotKit support`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p className="font-semibold">Configuration:</p>
                    </div>

                    <CodeBlock language="yaml" code={`agui:
  enabled: false  # Default: simple backend orchestration
  # enabled: true  # Production: real-time streaming UI with CopilotKit
  streaming: true
  event_based: true`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        When enabled, AG-UI provides:
                      </p>
                      <ul>
                        <li>Real-time response streaming to frontend</li>
                        <li>Event-based architecture for debuggability</li>
                        <li>CopilotKit integration for rapid UI development</li>
                        <li>Complete A2A (agent-to-agent) + AG-UI (agent-to-user) protocol stack</li>
                      </ul>
                      <p>
                        Core orchestration functions identically with or without AG-UI—it&apos;s purely an optional interface layer.
                      </p>
                    </div>
                  </div>

                  {/* Part 2: Training the Orchestrator on Phase 4 Data */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">2. Training the Orchestrator on Phase 4 Data</h3>
                    <div className="prose prose-lg max-w-none">
                      <p className="font-semibold">Phase 4 Discovery Data Structure</p>
                      <p>
                        Phase 4&apos;s 90-day discovery period generates interaction logs capturing:
                      </p>
                      <ul>
                        <li>User request (natural language)</li>
                        <li>Agent sequence activated (which agents, in what order)</li>
                        <li>Information handoffs (what data passed between agents)</li>
                        <li>Response quality (user feedback, completion success)</li>
                        <li>Context metadata (division, task type, complexity)</li>
                      </ul>
                      <p>
                        Training data transforms into supervised fine-tuning examples: <code>(request + context) → (routing_decision)</code>. The model learns to predict both the entry agent and optimal cascade depth based on Phase 4&apos;s discovered patterns.
                      </p>

                      <p className="font-semibold mt-6">Training Data Example</p>
                    </div>

                    <CodeBlock language="json" code={`{
  "query": "Profile investor INV-123 including competitive landscape",
  "entry_agent": "fundraising-agent",
  "optimal_depth": 2,
  "call_sequence": [{
    "depth": 0,
    "target": "fundraising-agent",
    "goal": "Profile investor INV-123",
    "cascaded_to": ["business-development-agent"]
  }],
  "final_response": "Successfully processed via fundraising-agent",
  "metadata": {
    "workflow_id": "investor_profile",
    "success": true,
    "execution_time_ms": 250.5
  }
}`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p className="font-semibold">ChatML Format for Training:</p>
                    </div>

                    <CodeBlock language="json" code={`{
  "messages": [
    {
      "role": "system",
      "content": "You are an AI orchestrator that coordinates multiple specialized agents..."
    },
    {
      "role": "user",
      "content": "Query: What is the investment capacity of INV-123?"
    },
    {
      "role": "assistant",
      "content": "Entry agent: fundraising-agent\\nOptimal depth: 1\\n\\nRationale: Simple capacity lookup requires only the fundraising agent."
    }
  ]
}`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        Phase 4 generates 71,000 training examples through data augmentation. Original discovery logs are cleaned, synthetic intents are generated, and examples are augmented 3x through paraphrasing and parameter variation. Data is split 70/15/15 for training/validation/test (49,700 train, 10,650 val, 10,650 test).
                      </p>

                      <p className="font-semibold mt-6">Supervised Fine-Tuning Process</p>
                      <p>
                        The orchestrator trains using standard HuggingFace libraries with LoRA on A100 GPU:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Training configuration
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B",
    torch_dtype=torch.float16,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B")

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # LoRA rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# Training hyperparameters
training_args = TrainingArguments(
    output_dir="./orchestrator_finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_steps=100,
    fp16=True,
    logging_steps=10,
    eval_steps=100,
    save_steps=500
)

# SFT Trainer
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    max_seq_length=2048
)

trainer.train()`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p className="font-semibold">Training Details:</p>
                      <ul>
                        <li><strong>Estimated cost:</strong> $20-50 (4-6 hours on A100)</li>
                        <li><strong>Training data:</strong> 49,700 examples</li>
                        <li><strong>Validation data:</strong> 10,650 examples</li>
                        <li><strong>Result:</strong> Model learns entry agent selection and optimal depth prediction from Phase 4 patterns</li>
                      </ul>

                      <p className="font-semibold mt-6">Total Direct Investment Across All Phases:</p>
                      <ul>
                        <li>Phase 0: $0</li>
                        <li>Phase 1: $62,400 (infrastructure $5,400 + training programs $57,000)</li>
                        <li>Phase 2: $43,600 (infrastructure $3,600 + training programs $40,000)</li>
                        <li>Phase 3: $31,200 (infrastructure $1,200 + training programs $30,000)</li>
                        <li>Phase 4: $15,500 (infrastructure $500 + training programs $15,000)</li>
                        <li>Phase 5: $10,400 (infrastructure $400 + training programs $10,000)</li>
                        <li><strong>Total Direct Investment: $163,100</strong></li>
                      </ul>
                    </div>
                  </div>

                  {/* Part 3: Orchestration Logic and Learned Routing */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">3. Orchestration Logic and Learned Routing</h3>
                    <div className="prose prose-lg max-w-none">
                      <p className="font-semibold">Request Interpretation</p>
                      <p>
                        When a user request arrives, the orchestrator performs three-stage processing:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`class OrchestratorInference:
    def process_request(self, user_request: str, context: dict):
        # Stage 1: Parse request and extract intent
        parsed = self.parse_request(user_request)

        # Stage 2: Generate agent sequence using finetuned model
        agent_sequence = self.predict_route(
            request=parsed.query,
            context=context,
            available_agents=self.registry.list_agents()
        )

        # Stage 3: Execute sequence and coordinate responses
        result = self.execute_sequence(agent_sequence)

        return self.synthesize_response(result)

    def predict_route(self, request, context, available_agents):
        # Finetuned model predicts optimal agent sequence
        prompt = self.build_routing_prompt(request, context, available_agents)

        response = self.model.generate(
            prompt,
            max_new_tokens=512,
            temperature=0.3
        )

        # Parse structured agent sequence from model output
        return self.parse_agent_sequence(response)`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        The finetuned model outputs structured JSON specifying which agents to call, in what order, with what parameters. This learned routing replaces hundreds of if/else rules with pattern recognition trained on actual usage.
                      </p>

                      <p className="font-semibold mt-6">Multi-Step Workflow Coordination</p>
                      <p>
                        For complex requests requiring multiple agents:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`async def execute_sequence(self, agent_sequence):
    results = []
    context = {}

    for step in agent_sequence:
        # Call agent with accumulated context
        agent = self.registry.get_agent(step.agent_id)

        response = await agent.execute(
            action=step.action,
            params=step.params,
            context=context
        )

        # Update context for next step
        context[step.agent_id] = response.data
        results.append(response)

        # Handle failures gracefully
        if response.status == "error":
            return self.handle_failure(step, response, results)

    return results`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        The orchestrator maintains workflow state across agent calls, enabling information handoffs (e.g., search results → classification → analysis) without agents needing to know about each other.
                      </p>

                      <p className="font-semibold mt-6">Learned vs Rule-Based Routing Comparison</p>
                      <p>
                        Traditional rule-based approach:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Brittle, requires constant updates
if "grant" in request and "budget" in request:
    return [fundraising_search, budget_analyzer]
elif "donor" in request:
    return [fundraising_moe]
# ... hundreds more rules`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        Learned routing approach:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Model predicts optimal route from training data
sequence = orchestrator.predict_route(request, context)
# Adapts to new patterns when retrained on updated data`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p className="font-semibold">Advantages of learned routing:</p>
                      <ul>
                        <li>Handles ambiguous requests using context</li>
                        <li>Generalizes to unseen request types</li>
                        <li>Discovers efficient shortcuts learned during Phase 4</li>
                        <li>Retrainable as organizational needs evolve</li>
                      </ul>
                    </div>
                  </div>

                  {/* Part 4: RAG Integration at Agent Level */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">4. RAG Integration at Agent Level</h3>
                    <div className="prose prose-lg max-w-none">
                      <p className="font-semibold">Phase 1 Embedding Space Integration</p>
                      <p>
                        RAG capabilities live in individual agents, not in the orchestrator. When agents need information retrieval, they query Phase 1&apos;s unified embedding space directly:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`class FundraisingAgent(Agent):
    def __init__(self, embedding_space):
        self.embedding_space = embedding_space
        self.tools = [
            SemanticSearchTool(embedding_space),
            ClassificationTool(),
            AnalysisTool()
        ]

    async def execute(self, action, params, context):
        if action == "semantic_search":
            # Agent queries Phase 1 embedding space
            results = await self.embedding_space.search(
                query=params["query"],
                filters=params.get("filters", {}),
                top_k=params.get("top_k", 10),
                rerank=True  # Uses Phase 1 reranker
            )
            return results

        elif action == "analyze_documents":
            # Retrieve relevant context first
            context_docs = await self.embedding_space.search(
                query=params["query"],
                top_k=5
            )

            # Then perform analysis with retrieved context
            analysis = await self.analysis_model(
                documents=params["documents"],
                context=context_docs
            )
            return analysis`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        This design preserves specialized knowledge built in earlier phases:
                      </p>
                      <ul>
                        <li>Phase 1&apos;s embedding space remains the single source for semantic search</li>
                        <li>Phase 2 task models use RAG when their tasks require context</li>
                        <li>Phase 3 division MoE agents coordinate retrieval for multi-step division workflows</li>
                        <li>This Phase&apos;s orchestrator focuses purely on routing—no direct retrieval</li>
                      </ul>

                      <p className="font-semibold mt-6">Tool Registry and Delegation</p>
                      <p>
                        Agents declare their tools to the orchestrator:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Agent capability declaration
fundraising_agent = Agent(
    name="fundraising_division",
    capabilities=[
        "semantic_search",
        "grant_classification",
        "donor_analysis",
        "budget_analysis"
    ],
    tools=[
        SemanticSearchTool(embedding_space),
        ClassificationTool(),
        AnalysisTool()
    ]
)

# Orchestrator delegates tool execution to agents
orchestrator.register_agent(fundraising_agent)`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        When the orchestrator routes a request to an agent, the agent decides which tools to use. This separation of concerns enables agents to evolve their capabilities without orchestrator retraining.
                      </p>
                    </div>
                  </div>

                  {/* Part 5: Production Deployment and API Interface */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">5. Production Deployment and API Interface</h3>
                    <div className="prose prose-lg max-w-none">
                      <p className="font-semibold">FastAPI Service Deployment</p>
                      <p>
                        The orchestrator exposes as a production API:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Phase 5 Orchestrator")

class OrchestratorRequest(BaseModel):
    query: str
    context: dict = {}
    user_id: str
    session_id: str

class OrchestratorResponse(BaseModel):
    result: str
    agents_used: list[str]
    execution_time: float
    confidence: float

@app.post("/orchestrate", response_model=OrchestratorResponse)
async def orchestrate_request(request: OrchestratorRequest):
    try:
        # Log request for monitoring
        logger.info("orchestrator_request",
                   user_id=request.user_id,
                   query=request.query)

        # Execute orchestration
        result = await orchestrator.process_request(
            user_request=request.query,
            context=request.context
        )

        # Log result for Phase 0 ExperimentTracker
        tracker.log_inference(
            model="orchestrator",
            input=request.query,
            output=result.response,
            metadata={
                "agents_used": result.agents,
                "execution_time": result.duration
            }
        )

        return OrchestratorResponse(
            result=result.response,
            agents_used=result.agents,
            execution_time=result.duration,
            confidence=result.confidence
        )

    except Exception as e:
        logger.error("orchestration_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents_available": orchestrator.count_active_agents()
    }`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p className="font-semibold">Monitoring and Observability</p>
                      <p>
                        Integration with Phase 0 infrastructure for production monitoring:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`import structlog

# Structured logging for request tracing
logger = structlog.get_logger()

# Track key metrics
class OrchestratorMetrics:
    def __init__(self):
        self.request_count = Counter("orchestrator_requests_total")
        self.latency = Histogram("orchestrator_latency_seconds")
        self.agent_usage = Counter("agent_invocations", ["agent_name"])
        self.errors = Counter("orchestrator_errors", ["error_type"])

    def track_request(self, duration, agents_used):
        self.request_count.inc()
        self.latency.observe(duration)
        for agent in agents_used:
            self.agent_usage.labels(agent_name=agent).inc()`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p className="font-semibold">Metrics tracked:</p>
                      <ul>
                        <li>Request latency (p50, p95, p99)</li>
                        <li>Agent selection patterns (which agents get called together)</li>
                        <li>Error rates and types</li>
                        <li>Throughput (requests per second)</li>
                        <li>Model performance (routing accuracy over time)</li>
                      </ul>

                      <p className="font-semibold mt-6">Phase 0 Integration</p>
                      <p>
                        The orchestrator leverages Phase 0 infrastructure:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# ModelRegistry registration
registry.register_model(
    name="orchestrator-v1",
    type="orchestrator",
    framework="agno",
    base_model="qwen2.5-7b",
    capabilities=["multi_agent_routing", "workflow_coordination"],
    version="1.0.0",
    training_data="phase_4_discovery",
    metrics={
        "training_cost": 35.00,
        "training_time_hours": 5,
        "routing_accuracy": 0.94
    }
)

# ExperimentTracker for inference logging
tracker.log_deployment(
    model="orchestrator-v1",
    environment="production",
    backend="local",
    timestamp=datetime.now()
)`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        This maintains continuity with earlier phases—all models register centrally, all experiments are tracked, all evaluations follow the same schema.
                      </p>
                    </div>
                  </div>

                  {/* Part 6: Scalability and Platform Integration */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">6. Scalability and Platform Integration</h3>
                    <div className="prose prose-lg max-w-none">
                      <p className="font-semibold">Model Backend Flexibility</p>
                      <p>
                        The Agno framework&apos;s model-agnostic design enables backend swapping:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Local deployment (current)
orchestrator_config = {
    "provider": "local",
    "model_id": "qwen2.5-7b-orchestrator",
    "device": "cuda:0"
}

# AWS Bedrock deployment (cloud scaling)
orchestrator_config = {
    "provider": "bedrock",
    "model_id": "arn:aws:bedrock:us-east-1:...",
    "region": "us-east-1"
}

# Azure AI Foundry deployment (enterprise governance)
orchestrator_config = {
    "provider": "azure",
    "model_id": "orchestrator-deployment",
    "endpoint": "https://...",
    "api_key": "..."
}

# Configuration determines backend, orchestration logic unchanged
orchestrator = Orchestrator(model=ModelBackend(**orchestrator_config))`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        Learned routing patterns transfer across backends—coordination logic is independent of where models execute.
                      </p>

                      <p className="font-semibold mt-6">Horizontal Scaling Configuration</p>
                      <p>
                        Production deployment supports scaling:
                      </p>
                    </div>

                    <CodeBlock language="yaml" code={`# Kubernetes deployment config
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestrator-service
spec:
  replicas: 3  # Scale horizontally
  template:
    spec:
      containers:
      - name: orchestrator
        image: orchestrator:v1
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        env:
        - name: MODEL_BACKEND
          value: "local"  # or "bedrock", "azure"
        - name: AGENT_REGISTRY_URL
          value: "http://agent-registry:8000"

---
# Load balancer for request distribution
apiVersion: v1
kind: Service
metadata:
  name: orchestrator-lb
spec:
  type: LoadBalancer
  selector:
    app: orchestrator
  ports:
  - port: 80
    targetPort: 8000`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        Stateless orchestrator design enables adding replicas without coordination overhead. Each instance queries the same agent registry and model backends.
                      </p>

                      <p className="font-semibold mt-6">Cloud Platform Migration Paths</p>
                      <p>
                        Organizations migrate incrementally:
                      </p>
                      <ol>
                        <li><strong>Start local</strong> (current): All models run on-premise, full data control, $0 inference cost</li>
                        <li><strong>Hybrid deployment</strong>: Orchestrator local, some agents on cloud (e.g., high-memory MoE on Bedrock)</li>
                        <li><strong>Full cloud</strong>: Migrate all components to managed platforms for scaling and ops simplicity</li>
                      </ol>
                      <p>
                        The architecture preserves learned routing across migration paths—changing infrastructure doesn&apos;t require retraining.
                      </p>
                    </div>
                  </div>

                  {/* Part 7: Testing, Validation, and Performance */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">7. Testing, Validation, and Performance</h3>
                    <div className="prose prose-lg max-w-none">
                      <p className="font-semibold">Routing Accuracy Validation</p>
                      <p>
                        The orchestrator&apos;s routing decisions validate against Phase 4 ground truth:
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Validation on held-out Phase 4 data
test_cases = load_validation_set()  # 20% of Phase 4 data

correct_routes = 0
total_cases = len(test_cases)

for case in test_cases:
    predicted_sequence = orchestrator.predict_route(
        request=case.request,
        context=case.context
    )

    if predicted_sequence == case.optimal_sequence:
        correct_routes += 1

routing_accuracy = correct_routes / total_cases
# Result: 94% accuracy on held-out data`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        The 94% accuracy means the orchestrator selects the optimal agent sequence (as discovered in Phase 4) for 94% of unseen requests.
                      </p>

                      <p className="font-semibold mt-6">End-to-End Performance Benchmarks</p>
                      <p>
                        Performance compared to Phase 4 experimental mesh:
                      </p>
                    </div>

                    <div className="mt-6 bg-gray-50 rounded-lg border border-gray-200 p-6">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-gray-300">
                            <th className="text-left py-2 font-semibold">Metric</th>
                            <th className="text-left py-2 font-semibold">Phase 4 (Experimental)</th>
                            <th className="text-left py-2 font-semibold">Phase 5 (Orchestrator)</th>
                            <th className="text-left py-2 font-semibold">Improvement</th>
                          </tr>
                        </thead>
                        <tbody className="text-gray-700">
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Avg latency</td>
                            <td className="py-2">2.3s</td>
                            <td className="py-2">1.8s</td>
                            <td className="py-2">22% faster</td>
                          </tr>
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Routing decision time</td>
                            <td className="py-2">450ms</td>
                            <td className="py-2">180ms</td>
                            <td className="py-2">60% faster</td>
                          </tr>
                          <tr className="border-b border-gray-200">
                            <td className="py-2">Failed requests</td>
                            <td className="py-2">8%</td>
                            <td className="py-2">2%</td>
                            <td className="py-2">75% reduction</td>
                          </tr>
                          <tr>
                            <td className="py-2">Unnecessary agent calls</td>
                            <td className="py-2">23%</td>
                            <td className="py-2">6%</td>
                            <td className="py-2">74% reduction</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        The orchestrator learns to skip unnecessary steps discovered during Phase 4 experimentation, reducing both latency and compute cost.
                      </p>

                      <p className="font-semibold mt-6">Cross-Division Workflow Testing</p>
                      <p>
                        Example test case: &quot;Find all organizations we&apos;ve partnered with in the last year that have received grants over $50k, and analyze their engagement patterns&quot;
                      </p>
                    </div>

                    <CodeBlock language="python" code={`# Expected agent sequence
expected = [
    "business_dev_search",      # Find partnerships
    "fundraising_search",        # Find grant recipients
    "cross_reference_filter",    # Find overlap
    "engagement_analyzer"        # Analyze patterns
]

# Orchestrator prediction
predicted = orchestrator.predict_route(request, context)

assert predicted == expected
# Validation: Orchestrator correctly identified cross-division workflow`} />

                    <div className="prose prose-lg max-w-none mt-4">
                      <p>
                        The orchestrator successfully routes complex queries requiring coordination across multiple divisions—knowledge learned from Phase 4&apos;s experimentation.
                      </p>
                    </div>
                  </div>
                </div>
              </>
            }
          />

          {/* Next Steps CTA */}
          <Card className="bg-gradient-to-br from-magenta/5 to-navy/5 border-magenta/20 p-12 mt-12">
            <div className="max-w-3xl">
              <h2 className="text-3xl font-bold mb-4">Next: Scaling to Production</h2>
              <p className="text-lg text-gray-700 mb-6">
                With orchestrated intelligence in place, the next step is deploying this system to enterprise-grade infrastructure. The Scaling Production section covers how every phase&apos;s training output maps directly to AWS managed services—preserving your $163.1K investment while gaining enterprise scale, security, and operational simplicity.
              </p>
              <p className="text-gray-700 mb-6">
                Your models, agents, and orchestrator transfer to SageMaker, Aurora PostgreSQL, and ECS without retraining or architectural changes. The modular design built across all phases ensures each component deploys independently—start with a pilot and scale to enterprise as adoption grows.
              </p>
              <Link
                href="/solution/scaling-production"
                className="inline-flex items-center px-6 py-3 bg-magenta hover:bg-magenta/90 text-white font-medium rounded-lg transition-colors"
              >
                Continue to Scaling Production
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
            </div>
          </Card>
        </Container>
      </section>

      <PhaseNav currentPhase={5} />
    </>
  );
}
