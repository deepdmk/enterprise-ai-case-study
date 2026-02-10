import Image from "next/image";
import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { CodeBlock } from "@/components/ui/CodeBlock";
import { PhaseNav } from "@/components/phases/PhaseNav";
import { PhaseNavTop } from "@/components/phases/PhaseNavTop";
import { PhaseTabs } from "@/components/phases/PhaseTabs";
import { Phase2ArchitectureDiagram } from "@/components/phases/Phase2ArchitectureDiagram";
import { getAssetPath } from "@/lib/assets";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Phase 2: Task-Specific SLMs",
  description: "Fine-tuning small language models for unit-specific tasks",
};

export default function Phase2() {
  return (
    <>
      <PageHeader
        title="Phase 2: Task-Specific SLMs"
        subtitle="Fine-tuned small language models for unit tasks"
      >
        <div className="flex gap-4 mt-4">
          <div className="text-base">
            <span className="text-white/60">Direct Investment:</span>
            <span className="ml-2 font-semibold">$43,600</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Time:</span>
            <span className="ml-2 font-semibold">~12 hours</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Models:</span>
            <span className="ml-2 font-semibold">14 Task SLMs</span>
          </div>
        </div>
      </PageHeader>

      <PhaseNavTop currentPhase={2} />

      <section className="py-12">
        <Container>
          <PhaseTabs
            vision={
              <>
                <div className="mb-12">
                  {/* The Problem */}
                  <h3 className="text-xl font-bold text-navy mb-3">The Problem</h3>
                  <p className="text-lg text-gray-700 leading-relaxed mb-6">
                    Enterprise AI typically starts backwards: vendors push generic solutions onto teams, forcing adoption of tools not tuned to actual needs. It&apos;s a solution in search of a problem. Commercial AI tools can&apos;t learn organization-specific patterns. They don&apos;t understand your investment decisions, RFP win patterns, or field operation standards. The AI you pay for never becomes a competitive advantage because it wasn&apos;t built around where your teams actually need help.
                  </p>

                  {/* The Solution */}
                  <h3 className="text-xl font-bold text-navy mb-3">The Solution</h3>
                  <p className="text-lg text-gray-700 leading-relaxed mb-6">
                    Invert the approach: let teams identify where AI would actually help, then fine-tune task-specific models for those exact needs. At ~$214 compute per model and ~1 hour to train, experimentation is cheap. Teams can try an AI application, test it for a week, and decide based on results. Models that save time get refined and deployed. Models that don&apos;t fit cost an afternoon to learn from. Value emerges from real workflows, not vendor assumptions.
                  </p>

                  {/* The Value */}
                  <h3 className="text-xl font-bold text-navy mb-3">The Value</h3>
                  <p className="text-lg text-gray-700 leading-relaxed">
                    Teams discover where AI creates genuine value for their specific work, not where vendors claim it should. $214 per model creating competitive moat that deepens with use. The organization isn&apos;t just getting working models. It&apos;s learning which problems are actually worth solving with AI, creating institutional knowledge about where automation delivers return. Each proven task model becomes an expert component ready for Phase 3&apos;s division-level agents, but delivers immediate return regardless of whether you continue building.
                  </p>
                </div>
              </>
            }
            approach={
              <>
                <Card className="mb-12 bg-amber/5 border-amber/20 border-t-4 border-t-amber">
                  <p className="text-xl text-gray-700 mb-6">
                    Phase 2 used a team-level fine-tuning approach with lightweight technical infrastructure to build task-specific models that created immediate value while preparing for division-level agents in Phase 3.
                  </p>

                  {/* Subsection 2.1: Decentralized AI Capability Building */}
                  <h3 className="text-2xl font-bold text-navy mb-4">Decentralized AI Capability Building</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 2 decentralized AI development to the team level rather than centralizing it with IT because that&apos;s where task expertise lives. Traditional enterprise AI deployments fail when central IT tries to capture requirements from distant teams, build generic tools, and mandate adoption. Teams struggle to articulate what they need, IT struggles to build for workflows they don&apos;t understand, and the resulting tools don&apos;t fit how work actually happens.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 2 inverted this by giving teams the capability to build their own models. Within Fundraising, teams fine-tuned models for investor profiling, fit assessment, capacity analysis, engagement strategy, and portfolio synthesis. Within Business Development, teams built models for RFP analysis, competitive positioning, proposal drafting, win probability, and funder priorities. Within Field Operations, teams created models for market assessment, project performance, capacity mapping, and demand forecasting.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    This approach worked because teams had both the task expertise and the data. They knew which examples represented good work. They understood the nuances of their decision criteria. They could test models against real workflows and iterate based on results. The bounded investment of $214 per model and ~1 hour training time made this experimentation practical. Models that delivered efficiency got refined and deployed. Models that didn&apos;t fit the workflow cost an afternoon and $214 to learn from.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    The organization provided decentralized AI expertise and support to enable teams rather than centralizing model development. This builds organizational capability while keeping decision-making where expertise lives.
                  </p>

                  {/* Subsection 2.2: Task-Specific Fine-Tuning Strategy */}
                  <h3 className="text-2xl font-bold text-navy mb-4 mt-8">Task-Specific Fine-Tuning Strategy</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 2 fine-tuned narrow task-specific models rather than deploying general-purpose LLMs because specificity creates both performance and competitive advantage. General-purpose models try to do everything adequately. Task-specific models do one thing extremely well, tuned to the organization&apos;s standards, data formats, and decision criteria.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    This specificity created competitive differentiation. When teams fine-tuned a portfolio analysis model on 10 years of investment decisions, it learned patterns no commercial LLM could replicate. It understood the organization&apos;s risk tolerance, sector preferences, and due diligence priorities. The model became an artifact of institutional intelligence, not a commodity tool.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    The technical approach used Unsloth and LoRA (Low-Rank Adaptation) to make fine-tuning economically viable. Unsloth accelerated training by 2-5x through optimized memory management. LoRA fine-tuned only a small subset of model parameters (typically less than 1% of total), drastically reducing compute requirements. 4-bit quantization enabled training on free Google Colab T4 instances. 2-epoch training on 500-2000 task-specific examples achieved strong performance without overfitting.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    A typical workflow: team collected examples of the task done well, formatted them as training data, ran the Unsloth fine-tuning script in a Colab notebook, and deployed the resulting model. Total time: ~1 hour. Compute cost: ~$214 per model. This made experimentation practical at scale across 14 different tasks. Phase 2 Direct Investment of $43,600 includes $3,600 infrastructure and $40,000 in training programs.
                  </p>

                  {/* Subsection 2.3: Foundation for Phase 3 Division-Level Agents */}
                  <h3 className="text-2xl font-bold text-navy mb-4 mt-8">Foundation for Phase 3 Division-Level Agents</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 2 task models are designed as building blocks for Phase 3&apos;s Mixture-of-Experts (MoE) architecture rather than standalone endpoints. Each task SLM became a specialized expert that a division-level router could orchestrate.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    This staging approach de-risked the progression to intelligent agents. Phase 3 didn&apos;t start from zero. It inherited 14 proven, fine-tuned experts already working in production. Fundraising&apos;s MoE agent orchestrated 5 task experts (investor profiling, fit assessment, capacity analysis, engagement strategy, portfolio synthesis). Business Development&apos;s agent combined 5 experts (RFP analysis, competitive positioning, proposal drafting, win probability, funder priorities). Field Operations&apos; agent leveraged 4 experts (market assessment, project performance, capacity mapping, demand forecasting).
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    The Phase 3 router learned which expert to invoke for each query, combining specialized capabilities into multi-task agents. This only worked because each expert was already trained, tested, and refined by the teams who used them daily. The task models had proven value and known performance characteristics, not theoretical capabilities.
                  </p>

                  <p className="text-gray-700 leading-relaxed">
                    This staged approach avoided betting on hypothetical capabilities. The organization invested $43,600 (Phase 2 Direct Investment) in 14 task models that delivered immediate value. Phase 3&apos;s division-level agents were an option enabled by proven components, not a requirement for Phase 2 to deliver ROI.
                  </p>

                  {/* Subsection 2.4: Phase 0 Registry Integration */}
                  <h3 className="text-2xl font-bold text-navy mb-4 mt-8">Phase 0 Registry Integration</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 2 integrated with Phase 0&apos;s ModelRegistry and ExperimentTracker to enable systematic learning across 14 models and multiple teams. ModelRegistry tracked each task model&apos;s metadata, performance metrics, training cost, and deployment endpoint. This creates visibility into which models deliver the most value and which training approaches worked best.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    ExperimentTracker logged every training run with hyperparameters, duration, and results. When a Fundraising team found hyperparameters that worked well for portfolio analysis, Business Development teams could try similar settings for RFP generation. This turned experimentation into organizational learning rather than isolated trials.
                  </p>

                  <p className="text-gray-700 leading-relaxed">
                    The registry infrastructure also prepared for Phase 3. When building division-level MoE agents, the router queried ModelRegistry to discover available experts, their capabilities, and performance characteristics. This made the transition from task models to orchestrated agents systematic rather than manual.
                  </p>
                </Card>

                <Card className="mb-12 bg-white/50 border border-gray-200">
                  <h3 className="text-lg font-bold text-navy mb-2">
                    Ready to see the technical implementation?
                  </h3>
                  <p className="text-gray-700 mb-4">
                    The Technical section below provides complete code examples, architecture diagrams, and deployment instructions. If you&apos;d prefer to explore the next phase first, you can skip ahead:
                  </p>
                  <a
                    href="/solution/phase-3"
                    className="inline-block px-6 py-3 bg-navy text-white font-medium rounded-md hover:bg-navy/90 transition-colors"
                  >
                    Continue to Phase 3 →
                  </a>
                </Card>
              </>
            }
            technical={
              <>
                {/* Architecture Diagram */}
                <div className="mb-12 bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                  <Phase2ArchitectureDiagram />
                </div>

                {/* Architecture Overview */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Architecture Overview</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Four-Program Pipeline</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 2 implements a modular four-program architecture where each program handles a distinct stage of the task SLM training pipeline:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 1: Data Preparation</strong> transforms raw task examples into training-ready datasets. Converts unit-specific data into standardized ChatML format with system prompts, user queries, and expected responses.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 2: Fine-Tuning</strong> trains LoRA adapters on quantized Llama 3.1 8B using Unsloth acceleration. Each task model trains on 500-2000 examples in approximately 1 hour on T4 GPU.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 3: Evaluation</strong> benchmarks trained models against held-out test sets, measuring task-specific accuracy and response quality before deployment.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    <strong>Program 4: Export</strong> packages trained adapters for Phase 3 MoE merging, registering each model in Phase 0&apos;s ModelRegistry with full lineage tracking.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Technology Stack</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Training:</strong> Unsloth + HuggingFace TRL (SFTTrainer) with 4-bit quantization</li>
                    <li><strong>Base model:</strong> Llama 3.1 8B (unsloth/llama-3.1-8b-bnb-4bit)</li>
                    <li><strong>Adaptation:</strong> LoRA (rank=16, alpha=16) targeting all projection layers</li>
                    <li><strong>Compute:</strong> Google Colab T4 (free tier) or local RTX 4090</li>
                    <li><strong>Integration:</strong> Phase 0 ModelRegistry and ExperimentTracker</li>
                  </ul>
                </div>

                {/* Part 1: Task Model Details */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">1. Task Model Details</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 2 creates <strong>14 task-specific SLMs</strong> as teams within three divisions fine-tune models for their specific tasks:
                  </p>

                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-navy mb-2">Fundraising (5 models):</h4>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      <li>Investor Profiling SLM</li>
                      <li>Investor-Opportunity Fit Assessment SLM</li>
                      <li>Investment Capacity Analysis SLM</li>
                      <li>Engagement Strategy Generation SLM</li>
                      <li>Portfolio Pattern Synthesis SLM</li>
                    </ul>
                  </div>

                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-navy mb-2">Business Development (5 models):</h4>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      <li>RFP Requirements Analysis SLM</li>
                      <li>Competitive Landscape Analysis SLM</li>
                      <li>Proposal Section Drafting SLM</li>
                      <li>Win Probability Assessment SLM</li>
                      <li>Funder Priorities Analysis SLM</li>
                    </ul>
                  </div>

                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-navy mb-2">Field Operations (4 models):</h4>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      <li>Local Market Assessment SLM</li>
                      <li>Project Performance Analysis SLM</li>
                      <li>Local Capacity Mapping SLM</li>
                      <li>Regional Demand Forecasting SLM</li>
                    </ul>
                  </div>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Each model:
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li>Starts from <strong>Llama 3.1 8B</strong> base (quantized to 4-bit)</li>
                    <li>Fine-tuned with <strong>LoRA adapters</strong> (rank=16, alpha=16)</li>
                    <li>Trained on <strong>500-2000 task-specific examples</strong></li>
                    <li>Optimized for <strong>2048-token context windows</strong></li>
                    <li>Registered in <strong>Phase 0 ModelRegistry</strong> for versioning</li>
                  </ul>

                  <div className="relative w-full aspect-[16/10] rounded-lg overflow-hidden border border-gray-200">
                    <Image
                      src={getAssetPath("/visuals/SLM_visual.png")}
                      alt="Phase 2 Task-Specific SLM Architecture showing 14 specialized models across Fundraising, Business Development, and Field Operations"
                      fill
                      className="object-contain"
                    />
                  </div>
                </div>

                {/* Part 2: Base Model Selection & Quantization */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">2. Base Model Selection & Quantization</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    We use <strong>Llama 3.1 8B</strong> as the base model for all Phase 2 SLMs:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Why Llama 3.1 8B?</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li><strong>Strong instruction-following:</strong> Pre-trained on high-quality instruction datasets</li>
                    <li><strong>Efficient inference:</strong> 8B parameters run on consumer GPUs (T4, L4, local RTX 4090)</li>
                    <li><strong>Good transfer learning:</strong> Strong performance with minimal fine-tuning data</li>
                    <li><strong>Open weights:</strong> No API costs, full model ownership</li>
                  </ul>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Quantization to 4-bit:</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li>Reduces memory footprint from ~32GB to ~5GB</li>
                    <li>Enables training on free Google Colab T4 instances (16GB VRAM)</li>
                    <li>Minimal accuracy loss (&lt;2% on benchmarks)</li>
                    <li>Uses <strong>bitsandbytes</strong> NF4 quantization</li>
                  </ul>

                  <CodeBlock
                    code={`from unsloth import FastLanguageModel

# Load quantized base model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.1-8b-bnb-4bit",  # Pre-quantized by Unsloth
    max_seq_length=2048,
    dtype=None,  # Auto-detect based on GPU
    load_in_4bit=True,
)

# Verify model loaded correctly
print(f"Model parameters: {model.num_parameters():,}")
print(f"Trainable parameters: {model.num_parameters(only_trainable=True):,}")`}
                    language="python"
                  />
                </div>

                {/* Part 3: LoRA Fine-Tuning Configuration */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">3. LoRA Fine-Tuning Configuration</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>LoRA (Low-Rank Adaptation)</strong> fine-tunes only a small subset of model weights, making training 10-100x faster and cheaper than full fine-tuning.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>How LoRA Works:</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li>Freezes the base model weights (7.25B parameters)</li>
                    <li>Adds small &quot;adapter&quot; matrices to attention layers (~20M parameters)</li>
                    <li>Trains only the adapter weights</li>
                    <li>Merges adapters back into base model after training</li>
                  </ul>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Configuration:</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li><strong>Rank (r):</strong> 16 (controls adapter size—higher = more capacity, slower training)</li>
                    <li><strong>Alpha:</strong> 16 (scaling factor—typically set equal to rank)</li>
                    <li><strong>Target modules:</strong> <code>q_proj</code>, <code>k_proj</code>, <code>v_proj</code>, <code>o_proj</code>, <code>up_proj</code>, <code>down_proj</code>, <code>gate_proj</code> (attention and MLP projection layers)</li>
                    <li><strong>Dropout:</strong> 0 (disabled for small datasets to prevent underfitting)</li>
                    <li><strong>RSLoRA:</strong> Enabled (rank-stabilized LoRA for improved training stability)</li>
                  </ul>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    This configuration trains ~0.3% of total model parameters, reducing compute cost from ~$2,000 to ~$214 per model.
                  </p>

                  <CodeBlock
                    code={`from unsloth import FastLanguageModel

# Add LoRA adapters to base model
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # Rank of LoRA adapters
    target_modules=[
        "q_proj",  # Query projection (attention)
        "k_proj",  # Key projection (attention)
        "v_proj",  # Value projection (attention)
        "o_proj",  # Output projection (attention)
        "up_proj",  # Up projection (MLP)
        "down_proj",  # Down projection (MLP)
        "gate_proj",  # Gate projection (MLP)
    ],
    lora_alpha=16,  # Scaling factor
    lora_dropout=0,  # No dropout for small datasets
    bias="none",  # Don't train bias terms
    use_rslora=True,  # Rank-stabilized LoRA
    use_gradient_checkpointing="unsloth",  # Memory optimization
    random_state=42,
)

# Check trainable parameters
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(f"Trainable: {trainable_params:,} ({100 * trainable_params / total_params:.2f}%)")
# Output: Trainable: 20,971,520 (0.29%)`}
                    language="python"
                  />
                </div>

                {/* Part 4: Training Data Preparation */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">4. Training Data Preparation</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Each task SLM requires <strong>500-2000 high-quality examples</strong> in instruction-tuning format:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Example: Investor Profiling SLM Training Data</strong>
                  </p>

                  <CodeBlock
                    code={`{
  "instruction": "Profile investor Sarah Chen who focuses on AI/ML startups",
  "input": "Sarah Chen\\nFocus: AI/ML, seed stage\\nLocation: Austin\\nCheck size: $250K-500K\\nInvestments/year: 10-15",
  "output": "## Investment Thesis\\nSarah Chen focuses on AI/ML investments, typically at the seed stage.\\n\\n## Historical Patterns\\n- Average check size: $250,000-500,000\\n- Investments per year: 10-15\\n- Preferred sectors: AI/ML, developer tools\\n\\n## Preferences\\n- Stage: seed\\n- Geography: Austin\\n- Team requirements: Technical founders preferred\\n\\n## Key Insights\\nSarah Chen shows strong preference for AI/ML with proven traction. Co-invests frequently with YC alumni network."
}`}
                    language="json"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    <strong>Data Collection Strategies:</strong>
                  </p>
                  <ol className="list-decimal list-inside text-gray-700 space-y-2 mb-6">
                    <li><strong>Historical Examples:</strong> Export past decisions (successful grants, rejected proposals, approved projects) from existing systems</li>
                    <li><strong>Expert Annotation:</strong> Have senior staff annotate 100-200 examples, showing their reasoning process</li>
                    <li><strong>Synthetic Augmentation:</strong> Use GPT-4 to generate variations of real examples (different sectors, amounts, risk profiles)</li>
                    <li><strong>Continuous Learning:</strong> Add new examples monthly as teams make decisions, improving model over time</li>
                  </ol>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Data Formatting:</strong>
                  </p>

                  <CodeBlock
                    code={`from datasets import Dataset

# Convert examples to Llama 3.1 instruction format
def format_example(example):
    return {
        "text": f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert investment analyst specializing in investor profiling.<|eot_id|><|start_header_id|>user<|end_header_id|>

{example['instruction']}

{example['input']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{example['output']}<|eot_id|>"""
    }

# Load and format training data
train_examples = load_from_json("fundraising_investor_profiling_examples.json")
train_dataset = Dataset.from_list([format_example(ex) for ex in train_examples])`}
                    language="python"
                  />
                </div>

                {/* Part 5: Training Loop & Hyperparameters */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">5. Training Loop & Hyperparameters</h3>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Training Configuration:</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li><strong>Epochs:</strong> 2 (more causes overfitting on small datasets)</li>
                    <li><strong>Batch size:</strong> 4 (with gradient accumulation to simulate larger batches)</li>
                    <li><strong>Learning rate:</strong> 2e-4 (standard for LoRA fine-tuning)</li>
                    <li><strong>Optimizer:</strong> AdamW 8-bit (memory-efficient variant)</li>
                    <li><strong>Scheduler:</strong> Linear warmup (10% of steps) + cosine decay</li>
                    <li><strong>Max sequence length:</strong> 2048 tokens</li>
                    <li><strong>Gradient checkpointing:</strong> Enabled (reduces VRAM by ~40%)</li>
                  </ul>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Training Time & Cost:</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li><strong>Duration:</strong> ~45-75 minutes on Google Colab T4 (free tier)</li>
                    <li><strong>Cost:</strong> ~$0 (free Colab) or ~$0.80/hour (Colab Pro with A100)</li>
                    <li><strong>VRAM usage:</strong> ~12GB (fits on T4&apos;s 16GB)</li>
                  </ul>

                  <CodeBlock
                    code={`from trl import SFTTrainer
from transformers import TrainingArguments

# Training configuration
training_args = TrainingArguments(
    output_dir="./fundraising_investor_profiling_slm",
    num_train_epochs=2,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # Effective batch size: 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_steps=10,
    logging_steps=10,
    save_strategy="epoch",
    optim="adamw_8bit",  # Memory-efficient optimizer
    fp16=True,  # Mixed precision training
    seed=42,
)

# Initialize trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    max_seq_length=2048,
    args=training_args,
    dataset_text_field="text",  # Field containing formatted examples
)

# Train model
trainer.train()

# Save LoRA adapters (only ~40MB vs 16GB for full model)
model.save_pretrained("./fundraising_investor_profiling_slm_adapters")
tokenizer.save_pretrained("./fundraising_investor_profiling_slm_adapters")

print("Training complete! Model saved to ./fundraising_investor_profiling_slm_adapters")`}
                    language="python"
                  />
                </div>

                {/* Part 6: Phase 0 Integration & Model Registry */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">6. Phase 0 Integration & Model Registry</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Every Phase 2 SLM registers with <strong>Phase 0&apos;s ModelRegistry</strong> for versioning, metadata tracking, and deployment management.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Model Registry Entry Structure:</strong>
                  </p>

                  <CodeBlock
                    code={`{
    "model_id": "fundraising/investor_profiling_v1",
    "base_model": "unsloth/llama-3.1-8b-bnb-4bit",
    "model_type": "task_slm",
    "task": "investor_profiling",
    "division": "fundraising",
    "lora_rank": 16,
    "training_examples": 1247,
    "training_date": "2024-01-15",
    "training_cost": 214.30,
    "training_duration_minutes": 68,
    "evaluation_metrics": {
        "accuracy": 0.89,
        "precision": 0.91,
        "recall": 0.87,
        "f1": 0.89
    },
    "adapters_path": "s3://models/fundraising_investor_profiling_v1_adapters",
    "deployment_endpoint": "http://slm-api:8000/fundraising/investor_profiling",
    "version": "1.0.0",
    "created_by": "jdoe@org.com",
    "status": "production"
}`}
                    language="json"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    <strong>Registration Code:</strong>
                  </p>

                  <CodeBlock
                    code={`import json
from datetime import datetime

# Register model in Phase 0 ModelRegistry
def register_model(model_info):
    registry_path = "/path/to/phase0/registries/model_registry.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "model_registered",
        **model_info
    }

    with open(registry_path, "a") as f:
        f.write(json.dumps(entry) + "\\n")

    print(f"✓ Registered {model_info['model_id']} in ModelRegistry")

# Example: Register investor profiling model
register_model({
    "model_id": "fundraising/investor_profiling_v1",
    "base_model": "unsloth/llama-3.1-8b-bnb-4bit",
    "model_type": "task_slm",
    "task": "investor_profiling",
    "division": "fundraising",
    "lora_rank": 16,
    "training_examples": 1247,
    "training_cost": 214.30,
    "adapters_path": "s3://models/fundraising_investor_profiling_v1_adapters",
    "deployment_endpoint": "http://slm-api:8000/fundraising/investor_profiling",
    "version": "1.0.0",
    "created_by": "jdoe@org.com",
    "status": "production"
})`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    <strong>Benefits of Registry Integration:</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li><strong>Version control:</strong> Track model iterations as teams refine training data</li>
                    <li><strong>Metadata tracking:</strong> Cost, performance, training duration for all 14 models</li>
                    <li><strong>Deployment management:</strong> Map model IDs to API endpoints</li>
                    <li><strong>Audit trail:</strong> Who trained what model, when, and at what cost</li>
                    <li><strong>Phase 3 preparation:</strong> MoE router queries registry to find available experts</li>
                  </ul>
                </div>

                {/* Part 7: Deployment & Inference */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">7. Deployment & Inference</h3>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 2 models deploy as lightweight <strong>FastAPI endpoints</strong> running on CPU or low-end GPU instances.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Deployment Architecture:</strong>
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1 mb-6">
                    <li><strong>Container:</strong> Docker image with Unsloth + model adapters (~2GB)</li>
                    <li><strong>Runtime:</strong> FastAPI server handling inference requests</li>
                    <li><strong>Hardware:</strong> AWS t3.medium (2 vCPU, 4GB RAM) for CPU inference, or g4dn.xlarge (1 GPU) for faster throughput</li>
                    <li><strong>Cost:</strong> ~$30/month per model (CPU) or ~$150/month (GPU)</li>
                    <li><strong>Latency:</strong> ~2-5 seconds per query (CPU), ~500ms (GPU)</li>
                  </ul>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Inference Code:</strong>
                  </p>

                  <CodeBlock
                    code={`from fastapi import FastAPI
from pydantic import BaseModel
from unsloth import FastLanguageModel

app = FastAPI()

# Load model at startup
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="./fundraising_investor_profiling_slm_adapters",
    max_seq_length=2048,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)  # Optimize for inference

class AnalysisRequest(BaseModel):
    instruction: str
    input_data: str

@app.post("/analyze")
async def analyze_investor(request: AnalysisRequest):
    # Format prompt
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert investment analyst.<|eot_id|><|start_header_id|>user<|end_header_id|>

{request.instruction}

{request.input_data}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.3,  # Low temperature for consistent outputs
        top_p=0.9,
        do_sample=True,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract assistant's response
    response = response.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()

    return {"analysis": response}

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "model": "fundraising/investor_profiling_v1"}`}
                    language="python"
                  />

                  <p className="text-gray-700 leading-relaxed mb-4 mt-6">
                    <strong>Client Usage:</strong>
                  </p>

                  <CodeBlock
                    code={`import requests

# Query the deployed model
response = requests.post(
    "http://slm-api:8000/analyze",
    json={
        "instruction": "Profile this investor",
        "input_data": "Sarah Chen\\nAI/ML focus\\nSeed stage\\nAustin"
    }
)

print(response.json()["analysis"])`}
                    language="python"
                  />
                </div>
              </>
            }
          />

          {/* Next Steps CTA */}
          <div className="bg-navy text-white p-8 rounded-lg mt-12 mb-12">
            <h3 className="text-2xl font-bold mb-4">Next: Phase 3 - Mixture-of-Experts Agents</h3>
            <p className="text-white/90 mb-4">
              Phase 3 merges your 14 task SLMs into <strong>3 intelligent MoE agents</strong>—one per division. Each agent routes queries to the appropriate expert, combining specialized capabilities into multi-task assistants.
            </p>
            <p className="text-white/90 mb-6">
              The Fundraising MoE can analyze investors, assess fit, analyze capacity, generate engagement strategies, and synthesize portfolio patterns—all by orchestrating the 5 experts you built in Phase 2.
            </p>
            <a
              href="/solution/phase-3"
              className="inline-block px-6 py-3 bg-teal text-white font-medium rounded-md hover:bg-teal/90 transition-colors"
            >
              Continue to Phase 3 →
            </a>
          </div>
        </Container>
      </section>

      <PhaseNav currentPhase={2} />
    </>
  );
}
