import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { CodeBlock } from "@/components/ui/CodeBlock";
import { PhaseNav } from "@/components/phases/PhaseNav";
import { PhaseNavTop } from "@/components/phases/PhaseNavTop";
import { PhaseTabs } from "@/components/phases/PhaseTabs";
import { Phase1ArchitectureDiagram } from "@/components/phases/Phase1ArchitectureDiagram";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Phase 1: Unified Embedding Space",
  description:
    "Shared semantic infrastructure enabling cross-divisional search and retrieval through fine-tuned embedding and reranker models",
};

export default function Phase1() {
  return (
    <>
      <PageHeader
        title="Phase 1: Unified Embedding Space"
        subtitle="Shared semantic infrastructure enabling cross-divisional search and retrieval through fine-tuned embedding and reranker models"
      >
        <div className="flex gap-4 mt-4">
          <div className="text-base">
            <span className="text-white/60">Direct Investment:</span>
            <span className="ml-2 font-semibold">$62,400</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Time:</span>
            <span className="ml-2 font-semibold">~15 min training</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Models:</span>
            <span className="ml-2 font-semibold">Embedder | Reranker</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Enables:</span>
            <span className="ml-2 font-semibold">Unified data platform for Phases 2-5</span>
          </div>
        </div>
      </PageHeader>

      <PhaseNavTop currentPhase={1} />

      <section className="py-12">
        <Container>
          <PhaseTabs
            vision={
              <>
                {/* The Problem */}
                <h3 className="text-xl font-bold text-navy mb-3">The Problem</h3>
                <p className="text-lg text-gray-700 leading-relaxed mb-6">
                  Organizational knowledge is siloed across divisions. When Fundraising searches for a specific ongoing investment or need in the field that a funder is interested in scaling, they can&apos;t discover relevant Field Operations data without manual coordination. Generic off-the-shelf embeddings don&apos;t understand organizational domain language or cross-divisional relationships, limiting search to exact keyword matches rather than semantic understanding.
                </p>

                {/* The Solution */}
                <h3 className="text-xl font-bold text-navy mb-3">The Solution</h3>
                <p className="text-lg text-gray-700 leading-relaxed mb-6">
                  Fine-tune custom embedding and reranker models on cross-unit data, creating shared semantic infrastructure that understands organizational relationships. Unlike generic embeddings, these models learn the organization&apos;s domain language and cross-divisional patterns. When Fundraising searches for scaling opportunities matching a funder&apos;s interests, they automatically surface relevant Field Operations project data through improved backend search, not through new processes or coordination.
                </p>

                {/* The Value */}
                <h3 className="text-xl font-bold text-navy mb-3">The Value</h3>
                <p className="text-lg text-gray-700 leading-relaxed">
                  Cross-divisional discovery through existing workflows. No process changes required, immediate improvement in how people find and use knowledge. Divisions maintain complete autonomy over their data while gaining cross-organizational visibility. Training costs under $1 using consumer GPUs with immediate ROI through enhanced data access. Hosting the vector database incurs a small ongoing cost, but this can reduce overall expenses by handling semantic queries through lightweight vectors rather than repeated calls to the source databases. Fine-tuned embedding model trained on cross-unit data, fine-tuned reranker model for precision ranking, ChromaDB vector database with ingested embeddings, and search interface demonstrating enhanced cross-division semantic search within existing workflows.
                </p>
              </>
            }
            approach={
              <Card className="bg-teal/5 border-teal/20 border-t-4 border-t-teal">
                <p className="text-xl text-gray-700 mb-6">
                  A unified embedding layer over existing siloed databases, enabling cross-divisional semantic search through vector representations rather than data consolidation.
                </p>

                <h3 className="text-2xl font-bold text-navy mb-4">Embedding Layer Architecture</h3>
                <p className="text-gray-700 leading-relaxed mb-6">
                  Phase 1 uses an embedding layer approach because it delivers cross-divisional search without disrupting existing systems. Consolidating three divisions&apos; databases would require migrating schemas, reconciling data formats, and coordinating process changes across teams. The embedding layer sidesteps this complexity by creating a semantic index above existing systems. Documents stay where they are; only their vector representations move to the shared layer.
                </p>
                <p className="text-gray-700 leading-relaxed mb-6">
                  This architectural choice minimizes change management while maximizing immediate value. Divisions retain autonomy over their data pipelines and can evolve them independently. The embedding database adapts to changes in underlying systems without requiring coordination.
                </p>

                <h3 className="text-2xl font-bold text-navy mb-4">Fine-Tuning the Embedding Model</h3>
                <p className="text-gray-700 leading-relaxed mb-6">
                  Phase 1 fine-tunes the embedding model rather than using off-the-shelf embeddings because organizational data has domain-specific vocabulary and relationships. Generic models don&apos;t understand that &quot;capacity expansion&quot; in Fundraising relates to &quot;project scaling&quot; in Field Operations. Fine-tuning on cross-unit data teaches the model these organizational semantic relationships, creating vectors that naturally cluster related concepts across divisions. This is what enables automatic cross-divisional discovery without manual mapping.
                </p>

                <h3 className="text-2xl font-bold text-navy mb-4">Adding a Reranker Model</h3>
                <p className="text-gray-700 leading-relaxed mb-6">
                  Phase 1 adds a reranker as a second stage after embedding retrieval to improve precision. Embedding models excel at fast approximate search across millions of documents but have limited context for ranking. The reranker takes top candidates from the embedding model and rescores them using cross-attention mechanisms that can deeply analyze query-document relationships.
                </p>
                <p className="text-gray-700 leading-relaxed mb-6">
                  Fine-tuning the reranker on organizational data teaches it which documents are truly relevant in organizational context. It learns the nuances of how different divisions use similar terms and can distinguish between superficial keyword matches and genuine semantic relevance.
                </p>

                <h3 className="text-2xl font-bold text-navy mb-4">Cross-Unit Training Approach</h3>
                <p className="text-gray-700 leading-relaxed mb-6">
                  Both models train on query-document pairs generated from all three divisions&apos; data. This cross-unit training is what creates the unified semantic space. Training on siloed data would create three separate embedding spaces. Cross-unit training teaches models the relationships between divisions, enabling automatic discovery without manual mapping.
                </p>
                <p className="text-gray-700 leading-relaxed mb-6">
                  The training pipeline incorporates RLHF (Reinforcement Learning from Human Feedback) to adapt as the business evolves. As the organization gains new customers, launches new products, or changes processes, user interactions with search results generate training data that captures these shifts. This creates a feedback loop where models continuously adapt to organizational changes without requiring manual retraining decisions or new labeled datasets.
                </p>

                <h3 className="text-2xl font-bold text-navy mb-4">Phase 0 Registry Integration</h3>
                <p className="text-gray-700 leading-relaxed mb-6">
                  Phase 1 integrates with Phase 0&apos;s registries to enable reproducibility and systematic improvement. DataRegistry tracks which division data went into each training run. ModelRegistry versions both models so changes are traceable. ExperimentTracker logs hyperparameters and metrics, enabling comparison across training runs. This infrastructure turns experimentation into systematic learning.
                </p>

                <div className="mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200">
                  <h3 className="text-lg font-bold text-navy mb-2">
                    Ready to see task-specific intelligence?
                  </h3>
                  <p className="text-gray-700 mb-4">
                    The technical implementation details below are optional. If you want to see how Phase 1&apos;s semantic infrastructure enables specialized task models for each division&apos;s workflows, continue to Phase 2.
                  </p>
                  <a
                    href="/solution/phase-2"
                    className="inline-block px-6 py-3 bg-navy text-white font-medium rounded-md hover:bg-navy/90 transition-colors"
                  >
                    Skip to Phase 2 →
                  </a>
                </div>
              </Card>
            }
            technical={
              <div>
                <p className="text-xl text-gray-700 mb-8">
                  Four-program pipeline using Sentence-Transformers fine-tuning, ChromaDB vector storage, and CrossEncoder reranking with full Phase 0 registry integration.
                </p>

                {/* Architecture Diagram */}
                <div className="mb-12 bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                  <Phase1ArchitectureDiagram />
                </div>

                {/* Part 1: Architecture Overview */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 1: Architecture Overview</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Four-Program Pipeline</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 1 implements a modular four-program architecture where each program handles a distinct stage of the embedding pipeline:
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 1: Dataset Generator</strong> creates training pairs from cross-unit PostgreSQL data. Extracts documents from all three divisions&apos; staged databases, chunks them using LangChain&apos;s RecursiveCharacterTextSplitter (512 characters, 50 overlap), and generates contrastive pairs using adjacent chunk strategy. Outputs train.parquet (2,718 pairs) and validation.parquet (303 pairs).
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 2: Fine-Tuning</strong> trains both embedding and reranker models. Uses Sentence-Transformers library with MultipleNegativesRankingLoss for embedding model fine-tuning. Integrates with Phase 0 ModelRegistry and ExperimentTracker to version models and log training runs with hyperparameters and metrics.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>Program 3: Ingestion</strong> processes documents through the fine-tuned embedding model and stores vectors in ChromaDB. Chunks documents, extracts comprehensive metadata (chunk_id, parent_doc_id, source_db, source_table, chunk_index, plus additional fields like category and author from source databases), generates embeddings in batches, and builds HNSW index for fast approximate nearest neighbor search. ChromaDB stores only embeddings and metadata, not document text.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-6">
                    <strong>Program 4: Search</strong> provides Gradio interface for semantic search with two-stage retrieval: bi-encoder (embedding model) for fast candidate retrieval from ChromaDB, then CrossEncoder (reranker) for precision ranking. Includes RLHF feedback collection and parent document fetching from source databases.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Technology Stack</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Fine-tuning:</strong> sentence-transformers ≥3.0.0, torch ≥2.0.0, transformers ≥4.40.0</li>
                    <li><strong>Vector database:</strong> chromadb ≥0.5.0 (Docker containerized)</li>
                    <li><strong>Data processing:</strong> langchain-text-splitters, pandas, datasets</li>
                    <li><strong>UI:</strong> gradio ≥4.15.0</li>
                    <li><strong>Integration:</strong> Phase 0 registries, PostgreSQL (asyncpg, psycopg2), structlog logging</li>
                  </ul>
                </div>

                {/* Part 2: Embedding Model Fine-Tuning */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 2: Embedding Model Fine-Tuning</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Base Model Selection</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Fine-tunes <code className="bg-gray-100 px-2 py-1 rounded text-sm">sentence-transformers/all-MiniLM-L6-v2</code>, a 384-dimension BERT-based sentence transformer with 512-token max sequence length. At 86MB, the model is small enough for full fine-tuning rather than requiring parameter-efficient approaches like LoRA. This model balances embedding quality with computational efficiency, making it suitable for real-time search across large document collections.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Training Dataset Generation</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Program 1 generates training pairs using adjacent chunk strategy. Documents from all three divisions are chunked using RecursiveCharacterTextSplitter with semantic boundary preservation (prioritizes <code className="bg-gray-100 px-2 py-1 rounded text-sm">\n\n</code>, <code className="bg-gray-100 px-2 py-1 rounded text-sm">\n</code>, <code className="bg-gray-100 px-2 py-1 rounded text-sm">. </code> separators). Adjacent chunks become positive pairs under the assumption that nearby text discusses related concepts.
                  </p>

                  <p className="text-gray-700 leading-relaxed mb-4">Example pairing from a document:</p>
                  <pre className="bg-gray-50 p-4 rounded-lg text-sm overflow-x-auto mb-4">
{`Document: [chunk_0] [chunk_1] [chunk_2] [chunk_3]
              ↓         ↓         ↓
Pairs:   (0,1)     (1,2)     (2,3)`}
                  </pre>

                  <p className="text-gray-700 leading-relaxed mb-4">
                    This creates 2,718 training pairs and 303 validation pairs from cross-unit data.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Fine-Tuning Implementation</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 1 uses the Sentence-Transformers library for full model fine-tuning. The EmbeddingTrainer class wraps SentenceTransformerTrainer with configuration management and Phase 0 registry integration:
                  </p>

                  <CodeBlock
                    language="python"
                    code={`from sentence_transformers import SentenceTransformer, SentenceTransformerTrainer
from sentence_transformers.losses import MultipleNegativesRankingLoss
from sentence_transformers.training_args import SentenceTransformerTrainingArguments

class EmbeddingTrainer:
    """Manages embedding model fine-tuning with Phase 0 integration."""

    def __init__(self, base_model: str, config: FineTuningConfig, device: str = "auto"):
        self.config = config
        self.device = self._select_device(device)
        self.model = SentenceTransformer(base_model, device=self.device)

    def train(self, train_dataset: Dataset, eval_dataset: Dataset | None = None):
        """Full fine-tuning of embedding model."""
        training_config = self.config.training
        output_dir = Path(self.config.output_dir) / self.config.model_name

        # Training arguments
        args = SentenceTransformerTrainingArguments(
            output_dir=str(output_dir),
            num_train_epochs=training_config.epochs,
            per_device_train_batch_size=training_config.batch_size,
            learning_rate=training_config.learning_rate,
            warmup_ratio=training_config.warmup_ratio,
            fp16=training_config.fp16 and self.device == "cuda",
            batch_sampler=BatchSamplers.NO_DUPLICATES,
            save_strategy="epoch",
            logging_steps=training_config.logging_steps,
            eval_strategy="epoch" if eval_dataset else "no",
            save_total_limit=3,
            load_best_model_at_end=bool(eval_dataset),
        )

        # Loss function: MultipleNegativesRankingLoss
        # Uses in-batch negatives - larger batch = more negatives
        loss = MultipleNegativesRankingLoss(self.model)

        # Initialize trainer
        trainer = SentenceTransformerTrainer(
            model=self.model,
            args=args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            loss=loss,
        )

        # Full fine-tuning (all parameters updated)
        trainer.train()

        return TrainingResult(
            final_loss=trainer.state.log_history[-1]["loss"],
            model_path=output_dir
        )`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Training Hyperparameters</h4>
                  <CodeBlock
                    language="yaml"
                    code={`# config.yaml
training:
  epochs: 3
  batch_size: 64                # Large batch = more in-batch negatives
  learning_rate: 2e-5
  warmup_ratio: 0.1             # 10% warmup steps
  fp16: true                    # Mixed precision (CUDA only)
  save_strategy: "epoch"
  logging_steps: 100

loss:
  type: "MultipleNegativesRankingLoss"
  scale: 20.0                   # Temperature for contrastive learning`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">MultipleNegativesRankingLoss</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    This loss function uses in-batch negatives for efficient contrastive learning. For each (anchor, positive) pair in a batch, all other positives in the batch serve as negatives. Larger batch sizes provide more negative examples, improving training. The scale parameter (20.0) controls temperature for sharper similarity distinctions.
                  </p>

                  <div className="mt-4 bg-gray-50 p-4 rounded-lg mb-6">
                    <h5 className="font-bold text-navy mb-2">Key Properties:</h5>
                    <ul className="space-y-1 text-base text-gray-700 list-disc list-inside">
                      <li>In-batch negatives: Automatically creates negatives from other batch samples</li>
                      <li>Efficiency: No need to explicitly mine hard negatives</li>
                      <li>Batch size impact: Larger batches provide more negative examples (batch_size=64 provides 63 negatives per anchor)</li>
                      <li>Scale: Temperature parameter to control sharpness of similarity distinctions</li>
                    </ul>
                  </div>

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Training Commands</h4>
                  <CodeBlock
                    language="bash"
                    code={`# Generate training data from cross-unit databases
python -m src.program1_dataset_generator.main --config config/config.yaml

# Full fine-tuning (3 epochs, batch_size=64, all parameters updated)
python -m src.program2_fine_tuning.main --config config/config.yaml

# Test mode for quick validation (1 epoch, batch_size=16, mock data)
python -m src.program2_fine_tuning.main --test-mode`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Training Results</h4>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><strong>Dataset:</strong> 2,718 training pairs, 303 validation pairs</li>
                    <li><strong>Final loss:</strong> 0.147</li>
                    <li><strong>Training time:</strong> ~15 minutes (V100 GPU)</li>
                    <li><strong>Compute cost:</strong> ~$0.50 (AWS p3.2xlarge) | <strong>Phase 1 Direct Investment:</strong> $62,400</li>
                    <li><strong>Output model:</strong> 86.7 MB (full model, all parameters fine-tuned)</li>
                    <li><strong>Device support:</strong> CUDA (NVIDIA), MPS (Apple Silicon), CPU fallback</li>
                  </ul>

                  <h4 className="text-lg font-bold text-navy mb-3">Full Fine-Tuning vs Parameter-Efficient</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 1 uses full fine-tuning where all model parameters are updated during training. This is practical because:
                  </p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li>Model is small (86MB) - fits easily in GPU memory</li>
                    <li>Training is fast (~15 minutes) - no need for efficiency tricks</li>
                    <li>Full fine-tuning typically achieves better accuracy than LoRA for small models</li>
                    <li>No additional inference complexity (LoRA requires adapter loading)</li>
                  </ul>
                  <p className="text-gray-700 leading-relaxed mb-6">
                    For larger models (&gt;1GB), parameter-efficient methods like LoRA would be necessary, but all-MiniLM-L6-v2&apos;s compact size makes full fine-tuning the simpler, more effective choice.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Output Model Structure</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    The fine-tuned model saves in SentenceTransformer format compatible with Hugging Face:
                  </p>
                  <pre className="bg-gray-50 p-4 rounded-lg text-sm overflow-x-auto mb-4">
{`enterprise-embed-v1/
├── model.safetensors         # Fine-tuned weights (86.7 MB)
├── config.json               # Model configuration
├── tokenizer.json            # Tokenizer
├── vocab.txt                 # Vocabulary
├── 1_Pooling/               # Pooling layer config
├── 2_Normalize/             # Normalization layer
└── training_metrics.json    # Training results`}
                  </pre>

                  <h4 className="text-lg font-bold text-navy mb-3">Loading the Fine-Tuned Model</h4>
                  <CodeBlock
                    language="python"
                    code={`from sentence_transformers import SentenceTransformer

# Direct loading
model = SentenceTransformer("data/models/enterprise-embed-v1")

# Or through EmbeddingModelManager wrapper
from src.shared.embedding_model import EmbeddingModelManager

manager = EmbeddingModelManager(config)
manager.load_model(use_fine_tuned=True)

# Encode queries and documents
query_embedding = model.encode("capacity expansion plans")
doc_embedding = model.encode("Field Operations project scaling initiative")

# Compute similarity
from sentence_transformers.util import cos_sim
similarity = cos_sim(query_embedding, doc_embedding)`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Phase 0 Integration</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Program 2 registers the fine-tuned model with ModelRegistry and logs training with ExperimentTracker:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`from registries.model_registry import ModelRegistry
from registries.experiment_tracker import ExperimentTracker
from registries.schemas import Phase, ModelType, ModelStatus

# Start experiment tracking
experiment = experiment_tracker.start_experiment(
    phase=Phase.PHASE_1,
    unit="shared",
    task="embeddings",
    notes="Full fine-tuning of all-MiniLM-L6-v2 on cross-unit data"
)

# Log hyperparameters
experiment_tracker.log_hyperparameters(
    experiment.experiment_id,
    HyperparameterConfig(
        epochs=3,
        batch_size=64,
        learning_rate=2e-5,
        extra={
            "warmup_ratio": 0.1,
            "fp16": True,
            "loss_function": "MultipleNegativesRankingLoss",
            "full_finetuning": True
        }
    )
)

# After training completes
experiment_tracker.log_training_metrics(
    experiment.experiment_id,
    TrainingMetrics(
        train_loss=0.147,
        training_time_seconds=900
    )
)

# Register fine-tuned model
model_registry.register(
    RegisteredModel(
        model_id="1/shared/embeddings/v1",
        phase=Phase.PHASE_1,
        unit="shared",
        task="embeddings",
        model_type=ModelType.FINE_TUNED,
        base_model="sentence-transformers/all-MiniLM-L6-v2",
        model_path="data/models/enterprise-embed-v1",
        source_dataset_id="1/training/embeddings/v1",
        status=ModelStatus.TRAINED,
        tags=["phase1", "embedding", "full-finetuning"]
    )
)

# Mark experiment complete
experiment_tracker.complete_experiment(
    experiment.experiment_id,
    model_id="1/shared/embeddings/v1"
)`}
                  />
                  <p className="text-gray-700 leading-relaxed mt-4">
                    This creates full lineage: dataset → training run → model, enabling traceability and reproducibility.
                  </p>
                </div>

                {/* Part 3: Reranker Model Integration */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 3: Reranker Model Integration</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Why Add Reranking</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Embedding models encode queries and documents separately (bi-encoder architecture), enabling fast retrieval through pre-computed embeddings but limited cross-attention between query and document. Rerankers use CrossEncoder architecture that jointly encodes query-document pairs, seeing full interaction patterns for more accurate relevance scoring.
                  </p>
                  <p className="text-gray-700 leading-relaxed mb-6">
                    Phase 1 uses two-stage retrieval: bi-encoder retrieves candidates efficiently, CrossEncoder reranks them accurately.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Reranker Model</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Uses <code className="bg-gray-100 px-2 py-1 rounded text-sm">cross-encoder/ms-marco-MiniLM-L-6-v2</code>, a MiniLM-based cross-encoder trained on MS MARCO passage ranking dataset. This model takes [query, document] pairs and outputs relevance scores.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Configuration</h4>
                  <CodeBlock
                    language="yaml"
                    code={`search:
  reranking:
    enabled: true
    model: "cross-encoder/ms-marco-MiniLM-L-6-v2"
    candidate_multiplier: 3`}
                  />
                  <p className="text-gray-700 leading-relaxed mb-6 mt-4">
                    <strong>Candidate multiplier</strong> determines retrieval depth: if user wants top 5 results, system retrieves 15 candidates (5 × 3), then reranks to select best 5.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Implementation</h4>
                  <CodeBlock
                    language="python"
                    code={`from sentence_transformers import CrossEncoder

class SearchReranker:
    def __init__(self, model_name: str):
        self._model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: list[str], top_k: int):
        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]

        # Score all pairs with CrossEncoder
        scores = self._model.predict(pairs)

        # Sort by score and return top_k
        results_with_scores = list(zip(documents, scores))
        reranked = sorted(results_with_scores,
                         key=lambda x: x[1],
                         reverse=True)

        return reranked[:top_k]`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Retrieval Pipeline Integration</h4>
                  <CodeBlock
                    language="python"
                    code={`def search(query: str, k: int = 5):
    # 1. Encode query with embedding model
    query_embedding = embedding_model.encode(query)

    # 2. Retrieve k×3 candidates from ChromaDB
    n_candidates = k * 3  # 15 if k=5
    candidates = chromadb.query(
        query_embeddings=[query_embedding],
        n_results=n_candidates
    )

    # 3. Rerank with CrossEncoder
    reranked = reranker.rerank(
        query=query,
        documents=candidates.documents,
        top_k=k
    )

    return reranked  # Top 5 after reranking`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Architecture Comparison</h4>
                  <div className="mt-6 overflow-x-auto mb-6">
                    <table className="w-full border-collapse">
                      <thead>
                        <tr className="bg-gray-50">
                          <th className="border border-gray-200 px-4 py-2 text-left text-navy">Aspect</th>
                          <th className="border border-gray-200 px-4 py-2 text-left text-navy">Bi-Encoder (Embedding)</th>
                          <th className="border border-gray-200 px-4 py-2 text-left text-navy">CrossEncoder (Reranker)</th>
                        </tr>
                      </thead>
                      <tbody className="text-sm text-gray-700">
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Encoding</td>
                          <td className="border border-gray-200 px-4 py-2">Separate query/doc encoding</td>
                          <td className="border border-gray-200 px-4 py-2">Joint encoding</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Speed</td>
                          <td className="border border-gray-200 px-4 py-2">Fast (pre-computed embeddings)</td>
                          <td className="border border-gray-200 px-4 py-2">Slower (on-demand)</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Accuracy</td>
                          <td className="border border-gray-200 px-4 py-2">Good</td>
                          <td className="border border-gray-200 px-4 py-2">Better</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Use Case</td>
                          <td className="border border-gray-200 px-4 py-2">Initial retrieval</td>
                          <td className="border border-gray-200 px-4 py-2">Final ranking</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Scalability</td>
                          <td className="border border-gray-200 px-4 py-2">Millions of documents</td>
                          <td className="border border-gray-200 px-4 py-2">Hundreds of candidates</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <h4 className="text-lg font-bold text-navy mb-3">Why This Works</h4>
                  <p className="text-gray-700 leading-relaxed mb-6">
                    Bi-encoder handles scale (searching millions of embedded documents takes milliseconds). CrossEncoder handles precision (deeply analyzing 15 candidates takes acceptable time for better ranking). Combined approach gets both speed and accuracy.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Future Enhancement</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Currently uses pre-trained MS MARCO reranker. Can be fine-tuned on enterprise data using RLHF feedback to learn organizational relevance patterns:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`# Future fine-tuning from RLHF feedback
from sentence_transformers import CrossEncoder, InputExample

train_samples = [
    InputExample(texts=['query', 'relevant_doc'], label=1.0),
    InputExample(texts=['query', 'irrelevant_doc'], label=0.0),
]

model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
model.fit(train_dataloader=train_samples, epochs=3)`}
                  />
                </div>

                {/* Part 4: ChromaDB Vector Database */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 4: ChromaDB Vector Database</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Vector Storage Architecture</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    ChromaDB provides persistent vector storage with HNSW (Hierarchical Navigable Small World) indexing for fast approximate nearest neighbor search. Deployed via Docker container with persistent volumes, accessible at localhost:8000.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Docker Configuration</h4>
                  <CodeBlock
                    language="yaml"
                    code={`# docker/docker-compose.yml
services:
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    environment:
      IS_PERSISTENT: "TRUE"
      PERSIST_DIRECTORY: "/chroma/chroma"
    volumes:
      - chromadb_data:/chroma/chroma
    restart: unless-stopped`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Collection Configuration</h4>
                  <CodeBlock
                    language="yaml"
                    code={`chromadb:
  host: "localhost"
  port: 8000
  collection_name: "enterprise_embeddings"
  hnsw:
    space: "cosine"           # Cosine similarity metric
    ef_construction: 200      # Build-time search depth
    ef_search: 40             # Query-time search depth`}
                  />

                  <p className="text-gray-700 mb-2 mt-4"><strong>HNSW Parameters:</strong></p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li><code className="bg-gray-100 px-2 py-1 rounded text-sm">ef_construction: 200</code> controls index build quality (higher = better recall, slower build)</li>
                    <li><code className="bg-gray-100 px-2 py-1 rounded text-sm">ef_search: 40</code> controls query-time accuracy (higher = better recall, slower queries)</li>
                    <li><code className="bg-gray-100 px-2 py-1 rounded text-sm">space: cosine</code> uses cosine similarity for normalized embeddings</li>
                  </ul>

                  <h4 className="text-lg font-bold text-navy mb-3">Metadata Schema</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Each embedded chunk stores metadata enabling parent document retrieval and division-specific filtering. ChromaDB stores only embeddings and metadata, not document text, keeping the vector database lightweight.
                  </p>

                  <p className="text-gray-700 mb-2"><strong>Core metadata (always included):</strong></p>
                  <CodeBlock
                    language="python"
                    code={`metadata = {
    "chunk_id": "db1_table1_doc123_chunk_0",  # Unique chunk identifier
    "parent_doc_id": "doc_12345",             # Original document ID
    "source_db": "field_operations",          # Division database
    "source_table": "project_documents",      # Source table
    "chunk_index": 2,                         # Chunk position (0-indexed)
    "total_chunks": 5,                        # Total chunks in document
}`}
                  />

                  <p className="text-gray-700 mb-2 mt-4"><strong>Additional metadata (from source documents):</strong></p>
                  <CodeBlock
                    language="python"
                    code={`additional_metadata = {
    "category": "project_reports",            # Document type/category
    "author": "john_doe",                     # Document creator
    "created_at": "2024-01-15T00:00:00",     # Creation timestamp
    "ingestion_timestamp": "2026-01-20T10:30:00Z"  # When ingested
    # Any other custom fields from source database
}`}
                  />

                  <p className="text-gray-700 leading-relaxed mb-6 mt-4">
                    This metadata enables division-specific filtering, parent document retrieval, and traceability back to source systems.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Ingestion Pipeline with Metadata Extraction</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Program 3 processes documents through chunking, metadata extraction, embedding generation, and ChromaDB storage:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`from src.shared.chromadb_client import ChromaDBClient
from src.shared.embedding_model import EmbeddingModelManager
from src.program3_ingestion.metadata_extractor import MetadataExtractor

# Initialize components
chromadb = ChromaDBClient(config)
embedding_manager = EmbeddingModelManager(config)
embedding_manager.load_model(use_fine_tuned=True)
metadata_extractor = MetadataExtractor()

# Process documents in batches
for batch in document_batches:
    # 1. Chunk documents
    chunks = chunker.chunk_documents(batch)

    # 2. Extract metadata for each chunk
    chunk_metadatas = metadata_extractor.extract_from_document_chunks(
        chunks=chunks,
        doc_id=record.doc_id,
        source_db=record.source_db,
        source_table=record.source_table,
        additional_metadata=record.metadata  # Category, author, timestamps, etc.
    )

    # 3. Generate embeddings (batch processing)
    texts = [chunk.text for chunk in chunks]
    embeddings = embedding_manager.encode_batch(texts)

    # 4. Prepare metadata dictionaries
    metadata_dicts = [metadata.to_dict() for metadata in chunk_metadatas]

    # Metadata includes:
    # - chunk_id, parent_doc_id
    # - source_db, source_table
    # - chunk_index, total_chunks
    # - category, author, created_at (from source DB)
    # - ingestion_timestamp

    # 5. Upsert to ChromaDB (embeddings + metadata only, no text stored)
    chromadb.upsert(
        embeddings=embeddings,
        metadatas=metadata_dicts,
        ids=[metadata.chunk_id for metadata in chunk_metadatas]
    )`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Query Mechanics</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Semantic search queries ChromaDB with embedded query vector:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`# Encode query
query_embedding = embedding_manager.encode_single("capacity expansion plans")

# Query ChromaDB
results = chromadb.query(
    query_embeddings=[query_embedding],
    n_results=15,  # Retrieve candidates for reranking
    where={"source_db": "fundraising"},  # Optional filter
    include=["metadatas", "distances", "documents"]
)

# Results structure
{
    "ids": [["doc_123_chunk_0", "doc_456_chunk_2", ...]],
    "distances": [[0.23, 0.31, ...]],  # Cosine distances
    "metadatas": [[{...}, {...}, ...]],
    "documents": [["chunk text 1", "chunk text 2", ...]]
}`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Parent Document Retrieval</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    After semantic search returns relevant chunks, system fetches complete parent documents from source databases:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`# Get metadata from search results
chunk_metadata = results.metadatas[0][0]

# Fetch parent document from source database
parent_doc = await database_client.fetch_document(
    database=chunk_metadata["source_db"],
    table=chunk_metadata["source_table"],
    doc_id=chunk_metadata["doc_id"]
)`}
                  />

                  <p className="text-gray-700 leading-relaxed mb-6 mt-4">
                    This architecture keeps ChromaDB lightweight (only embeddings + metadata) while providing access to full documents from authoritative sources.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Client Fallback Strategy</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    ChromaDB client implements automatic fallback from server to local persistent storage:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`try:
    # Try connecting to Docker container
    client = chromadb.HttpClient(host="localhost", port=8000)
    client.heartbeat()
except Exception:
    # Fallback to local persistent storage
    client = chromadb.PersistentClient(path="data/chromadb")`}
                  />
                  <p className="text-gray-700 leading-relaxed mt-4">
                    This enables development without Docker and provides resilience if ChromaDB server is unavailable.
                  </p>
                </div>

                {/* Part 5: RLHF Feedback Pipeline */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 5: RLHF Feedback Pipeline</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Feedback Collection System</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 1 implements production-ready RLHF (Reinforcement Learning from Human Feedback) collection integrated into the search interface. As users interact with search results, their feedback generates training data for future model improvements.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Feedback Types Captured</h4>
                  <CodeBlock
                    language="python"
                    code={`class FeedbackType(str, Enum):
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    RATING = "rating"           # 1-5 scale
    COMMENT = "comment"
    RESULT_CLICK = "result_click"`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Storage Format</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Feedback saves to JSONL (JSON Lines) files with monthly rotation:
                  </p>
                  <pre className="bg-gray-50 p-4 rounded-lg text-sm overflow-x-auto mb-4">
{`data/feedback/
├── feedback_2026-01.jsonl
├── feedback_2026-02.jsonl
└── feedback_stats.json`}
                  </pre>

                  <h4 className="text-lg font-bold text-navy mb-3">Feedback Entry Schema</h4>
                  <CodeBlock
                    language="json"
                    code={`{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-01-20T14:32:15.123456Z",
  "query": "capacity expansion plans",
  "search_results": [
    {
      "chunk_id": "doc_123_chunk_0",
      "source_db": "field_operations",
      "distance": 0.23,
      "rerank_score": 0.89
    }
  ],
  "feedback_type": "thumbs_up",
  "feedback_value": null,
  "result_index": 0,
  "comment": "Found exactly what I needed"
}`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Implementation</h4>
                  <CodeBlock
                    language="python"
                    code={`from src.program4_search.feedback import FeedbackCollector

collector = FeedbackCollector(storage_dir="data/feedback")

# Record search
session_id = collector.start_session()
collector.record_search(
    session_id=session_id,
    query="capacity expansion plans",
    results=search_results
)

# Collect feedback
collector.record_feedback(
    session_id=session_id,
    feedback_type=FeedbackType.THUMBS_UP,
    result_index=0,
    comment="Found exactly what I needed"
)`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Gradio UI Integration</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    The search interface includes feedback buttons for each result:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`def create_search_interface():
    with gr.Blocks() as interface:
        query_input = gr.Textbox(label="Search Query")
        search_btn = gr.Button("Search")
        results_display = gr.HTML()

        # Feedback buttons for each result
        feedback_btns = [
            gr.Button("👍", size="sm"),
            gr.Button("👎", size="sm"),
            gr.Slider(1, 5, label="Rating")
        ]

        # Wire feedback collection
        feedback_btns[0].click(
            fn=lambda: collector.record_feedback(
                session_id=current_session,
                feedback_type=FeedbackType.THUMBS_UP,
                result_index=selected_result
            )
        )`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Adapting to Business Changes</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    The RLHF pipeline enables continuous adaptation as the organization evolves:
                  </p>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>New customers:</strong> When Business Development starts working with new investor types, their search patterns and feedback teach models these new contexts without manual dataset updates.
                  </p>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    <strong>New products:</strong> When Field Operations launches new project categories, user interactions automatically generate training data reflecting new terminology and relationships.
                  </p>
                  <p className="text-gray-700 leading-relaxed mb-6">
                    <strong>Process changes:</strong> When Fundraising modifies their portfolio analysis workflow, search feedback captures new query patterns and relevant document types.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Future Training Pipeline</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Current implementation collects feedback; future work will build retraining pipeline:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`# Planned: Convert feedback to training data
def generate_training_pairs_from_feedback():
    feedback_data = load_feedback_jsonl("data/feedback/")

    training_pairs = []
    for entry in feedback_data:
        if entry.feedback_type == "thumbs_up":
            # Positive pair
            training_pairs.append({
                "anchor": entry.query,
                "positive": entry.search_results[entry.result_index].text,
                "label": 1.0
            })
        elif entry.feedback_type == "thumbs_down":
            # Negative pair
            training_pairs.append({
                "anchor": entry.query,
                "positive": entry.search_results[entry.result_index].text,
                "label": 0.0
            })

    # Register with Phase 0 DataRegistry
    data_registry.register(RegisteredDataset(
        dataset_id="1/training/embeddings-rlhf/v2",
        phase=Phase.PHASE_1,
        data_type=DataType.PREFERENCE_PAIRS,
        train_path="data/rlhf_training_pairs.parquet",
        source_description="Generated from user search feedback"
    ))

    # Retrain models with combined original + RLHF data
    retrain_embedding_model()`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Feedback Statistics</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    System tracks aggregate statistics for monitoring:
                  </p>
                  <CodeBlock
                    language="json"
                    code={`{
  "total_searches": 1247,
  "total_feedback": 892,
  "feedback_rate": 0.715,
  "thumbs_up": 654,
  "thumbs_down": 128,
  "avg_rating": 4.2,
  "top_queries": ["capacity expansion", "investor portfolio", ...]
}`}
                  />
                </div>

                {/* Part 6: Phase 0 Integration Patterns */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 6: Phase 0 Integration Patterns</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Registry Integration Architecture</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    All four Phase 1 programs integrate with Phase 0 registries for full traceability from raw data through trained models to production deployment.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Path Setup</h4>
                  <CodeBlock
                    language="python"
                    code={`# Add phase-0-infrastructure to Python path
import sys
from pathlib import Path

phase0_path = Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"
sys.path.insert(0, str(phase0_path))

# Import Phase 0 registries
from habitat_logging import configure_logging, get_logger
from registries.data_registry import DataRegistry
from registries.model_registry import ModelRegistry
from registries.experiment_tracker import ExperimentTracker
from registries.schemas import (
    Phase, DataType, ModelType, DatasetStatus, ModelStatus,
    RegisteredDataset, RegisteredModel
)`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Program 1: Dataset Registration</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Dataset generator registers training datasets with DataRegistry:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`# Initialize DataRegistry
data_registry = DataRegistry(data_dir="data", test_mode=False)

# Register training dataset
dataset = RegisteredDataset(
    dataset_id="1/training/embeddings/v1",
    phase=Phase.PHASE_1,
    unit="training",
    task="embeddings",
    data_type=DataType.EMBEDDING_DATA,
    train_path="data/training_datasets/train.parquet",
    val_path="data/training_datasets/validation.parquet",
    train_samples=2718,
    val_samples=303,
    source_description="Cross-unit embedding training pairs from adjacent chunks",
    status=DatasetStatus.VALIDATED,
    tags=["phase1", "cross-unit", "adjacent-chunks"]
)

data_registry.register(dataset)`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Program 2: Model and Experiment Registration</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Fine-tuning program registers both models and training runs:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`# Initialize registries
model_registry = ModelRegistry(data_dir="data")
experiment_tracker = ExperimentTracker(data_dir="data")

# Start experiment tracking
experiment = experiment_tracker.start_experiment(
    phase=Phase.PHASE_1,
    unit="shared",
    task="embeddings",
    notes="Fine-tuning all-MiniLM-L6-v2 on cross-unit data"
)

# Log hyperparameters
experiment_tracker.log_hyperparameters(
    experiment.experiment_id,
    HyperparameterConfig(
        epochs=3,
        batch_size=64,
        learning_rate=2e-5,
        extra={
            "warmup_ratio": 0.1,
            "fp16": True,
            "loss_function": "MultipleNegativesRankingLoss"
        }
    )
)

# After training completes
experiment_tracker.log_training_metrics(
    experiment.experiment_id,
    TrainingMetrics(
        train_loss=0.147,
        training_time_seconds=900
    )
)

# Register fine-tuned model
model = RegisteredModel(
    model_id="1/shared/embeddings/v1",
    phase=Phase.PHASE_1,
    unit="shared",
    task="embeddings",
    model_type=ModelType.FINE_TUNED,
    base_model="sentence-transformers/all-MiniLM-L6-v2",
    model_path="data/models/enterprise-embed-v1",
    source_dataset_id="1/training/embeddings/v1",  # Links to DataRegistry
    status=ModelStatus.TRAINED,
    tags=["phase1", "embedding", "sentence-transformer"]
)

model_registry.register(model)

# Complete experiment
experiment_tracker.complete_experiment(
    experiment.experiment_id,
    model_id="1/shared/embeddings/v1"
)`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Lineage Tracing</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Registry integration creates full lineage chain:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`# Start with model
model = model_registry.get("1/shared/embeddings/v1")

# Trace to source dataset
dataset = data_registry.get(model.source_dataset_id)

# Find all experiments using this dataset
experiments = experiment_tracker.list_experiments(
    phase=Phase.PHASE_1,
    unit="shared",
    task="embeddings"
)

# Lineage chain
print(f"Dataset: {dataset.dataset_id}")
print(f"  → Experiment: {experiment.experiment_id}")
print(f"    → Model: {model.model_id}")
print(f"      Status: {model.status}")`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Shared ID Convention</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    All registries use standardized ID format: <code className="bg-gray-100 px-2 py-1 rounded text-sm">{`{phase}/{unit}/{task}/{version}`}</code>
                  </p>
                  <CodeBlock
                    language="python"
                    code={`from config.conventions import make_id, parse_id

# Create ID
dataset_id = make_id(
    phase=1,
    unit="training",
    task="embeddings",
    version="v1"
)
# Returns: "1/training/embeddings/v1"

# Parse ID
components = parse_id(dataset_id)
# Returns: {"phase": "1", "unit": "training", "task": "embeddings", "version": "v1"}`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Configuration Inheritance</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Phase 1 inherits base configuration from Phase 0:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`from config.base_settings import HabitatBaseSettings

class Settings(HabitatBaseSettings):
    """Phase 1 settings extending Phase 0 base."""

    # Inherits from Phase 0:
    # - data_dir: Path
    # - log_level: str
    # - log_format: str

    # Phase 1 specific
    embedding: EmbeddingConfig
    chromadb: ChromaDBConfig
    search: SearchConfig`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Structured Logging Integration</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    All programs use Phase 0&apos;s structured logging:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`from habitat_logging import configure_logging, get_logger

# Configure once at startup
configure_logging(level="INFO", format="console")

# Get logger
logger = get_logger(__name__)

# Structured logging
logger.info(
    "model_registered",
    model_id="1/shared/embeddings/v1",
    model_type="FINE_TUNED",
    base_model="all-MiniLM-L6-v2"
)`}
                  />
                </div>

                {/* Part 7: Gradio Search Interface and Deployment */}
                <div className="mb-12">
                  <h3 className="text-2xl font-bold text-navy mb-4">Part 7: Gradio Search Interface and Deployment</h3>

                  <h4 className="text-lg font-bold text-navy mb-3">Search Interface Implementation</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Program 4 provides Gradio-based web interface demonstrating cross-division semantic search with two-stage retrieval and feedback collection.
                  </p>

                  <h4 className="text-lg font-bold text-navy mb-3">Interface Components</h4>
                  <CodeBlock
                    language="python"
                    code={`import gradio as gr
from src.program4_search.retriever import SemanticRetriever
from src.program4_search.feedback import FeedbackCollector

def create_interface():
    with gr.Blocks(title="Enterprise Semantic Search") as app:
        gr.Markdown("# Cross-Division Semantic Search")

        with gr.Row():
            query_input = gr.Textbox(
                label="Search Query",
                placeholder="e.g., capacity expansion plans"
            )
            db_filter = gr.Dropdown(
                choices=["all", "fundraising", "field_operations", "business_development"],
                value="all",
                label="Filter by Division"
            )

        search_btn = gr.Button("Search", variant="primary")

        results_display = gr.HTML(label="Search Results")

        # Feedback section
        with gr.Row():
            feedback_thumbs = gr.Radio(
                choices=["👍", "👎"],
                label="Was this helpful?"
            )
            feedback_comment = gr.Textbox(
                label="Additional Comments",
                placeholder="Optional feedback..."
            )

        search_btn.click(
            fn=search_and_display,
            inputs=[query_input, db_filter],
            outputs=results_display
        )

    return app`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Search Workflow</h4>
                  <CodeBlock
                    language="python"
                    code={`async def search_and_display(query: str, db_filter: str, k: int = 5):
    # 1. Semantic search with two-stage retrieval
    retriever = SemanticRetriever(config)
    results = retriever.search(
        query=query,
        k=k,
        source_db_filter=None if db_filter == "all" else db_filter
    )

    # 2. Fetch parent documents from source databases
    parent_docs = []
    for result in results:
        doc = await parent_fetcher.fetch_document(
            database=result.metadata["source_db"],
            table=result.metadata["source_table"],
            doc_id=result.metadata["doc_id"]
        )
        parent_docs.append(doc)

    # 3. Format results for display
    html_output = format_results_html(results, parent_docs)

    # 4. Record search for feedback collection
    session_id = feedback_collector.record_search(query, results)

    return html_output`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Two-Stage Retrieval Flow</h4>
                  <CodeBlock
                    language="python"
                    code={`def search(self, query: str, k: int = 5):
    # Stage 1: Bi-encoder retrieval
    query_embedding = self.embedding_manager.encode_single(query)

    n_candidates = k * 3 if self.reranker else k

    chromadb_results = self.chromadb_client.query(
        query_embeddings=[query_embedding],
        n_results=n_candidates,
        include=["metadatas", "distances", "documents"]
    )

    # Stage 2: CrossEncoder reranking
    if self.reranker:
        reranked = self.reranker.rerank(
            query=query,
            results=chromadb_results,
            documents=chromadb_results.documents[0],
            top_k=k
        )
        return reranked

    return chromadb_results[:k]`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Parent Document Fetching</h4>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Search returns relevant chunks, but users need full documents:
                  </p>
                  <CodeBlock
                    language="python"
                    code={`class ParentDocumentFetcher:
    def __init__(self, db_connections: dict):
        self.connections = db_connections

    async def fetch_document(self, database: str, table: str, doc_id: str):
        """Fetch complete document from source database."""
        conn = self.connections[database]

        query = f"SELECT * FROM {table} WHERE id = $1"
        result = await conn.fetchrow(query, doc_id)

        return {
            "id": result["id"],
            "title": result["title"],
            "content": result["content"],
            "metadata": result["metadata"],
            "source_db": database,
            "source_table": table
        }`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Launch Command</h4>
                  <CodeBlock
                    language="bash"
                    code={`# Start ChromaDB (if using Docker)
docker-compose -f docker/docker-compose.yml up -d

# Launch search interface
python -m src.program4_search.main --config config/config.yaml

# Opens Gradio interface at http://localhost:7860`}
                  />

                  <h4 className="text-lg font-bold text-navy mb-3 mt-6">Performance Characteristics</h4>
                  <div className="mt-6 overflow-x-auto mb-6">
                    <table className="w-full border-collapse">
                      <thead>
                        <tr className="bg-gray-50">
                          <th className="border border-gray-200 px-4 py-2 text-left text-navy">Operation</th>
                          <th className="border border-gray-200 px-4 py-2 text-left text-navy">Latency</th>
                          <th className="border border-gray-200 px-4 py-2 text-left text-navy">Notes</th>
                        </tr>
                      </thead>
                      <tbody className="text-sm text-gray-700">
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Embedding generation</td>
                          <td className="border border-gray-200 px-4 py-2">~10ms</td>
                          <td className="border border-gray-200 px-4 py-2">Single query, GPU</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">ChromaDB retrieval</td>
                          <td className="border border-gray-200 px-4 py-2">~20-50ms</td>
                          <td className="border border-gray-200 px-4 py-2">15 candidates from index</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Reranking</td>
                          <td className="border border-gray-200 px-4 py-2">~100-200ms</td>
                          <td className="border border-gray-200 px-4 py-2">CrossEncoder on 15 candidates</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2">Parent doc fetch</td>
                          <td className="border border-gray-200 px-4 py-2">~10-30ms</td>
                          <td className="border border-gray-200 px-4 py-2">PostgreSQL query</td>
                        </tr>
                        <tr>
                          <td className="border border-gray-200 px-4 py-2 font-bold">Total query time</td>
                          <td className="border border-gray-200 px-4 py-2 font-bold">~150-300ms</td>
                          <td className="border border-gray-200 px-4 py-2">End-to-end search</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <h4 className="text-lg font-bold text-navy mb-3">Production Deployment Considerations</h4>

                  <p className="text-gray-700 mb-2 mt-4"><strong>Scaling Vector Database:</strong></p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li>Current: Single ChromaDB container sufficient for proof-of-concept</li>
                    <li>Scale: Add read replicas when query volume exceeds single instance capacity</li>
                    <li>Monitor: Query latency, index build time, storage growth</li>
                  </ul>

                  <p className="text-gray-700 mb-2"><strong>Model Deployment:</strong></p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li>Embedding model: Deploy on GPU for batch processing, CPU acceptable for real-time single queries</li>
                    <li>Reranker: GPU recommended for sub-200ms latency on 15 candidates</li>
                    <li>Memory requirements: ~1GB GPU for both models in production</li>
                  </ul>

                  <p className="text-gray-700 mb-2"><strong>When to Retrain:</strong></p>
                  <p className="text-gray-700 leading-relaxed mb-2">
                    Retrain embedding model when:
                  </p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li>Accumulated significant RLHF feedback (&gt;1000 entries)</li>
                    <li>Business introduces new product lines or customer segments</li>
                    <li>Retrieval quality degrades (monitor through feedback rates)</li>
                    <li>New divisions added requiring cross-unit understanding</li>
                  </ul>

                  <p className="text-gray-700 mb-2"><strong>Migration to Production:</strong></p>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    Current Gradio interface demonstrates capability. Production deployment would:
                  </p>
                  <ul className="space-y-2 text-gray-700 list-disc list-inside mb-6">
                    <li>Replace Gradio with API endpoints (FastAPI, Flask)</li>
                    <li>Integrate with existing portals via REST/GraphQL</li>
                    <li>Add authentication and access control per division</li>
                    <li>Implement caching for frequently accessed documents</li>
                    <li>Add monitoring and alerting (query latency, error rates)</li>
                  </ul>

                  <p className="text-gray-700 mb-2"><strong>Test Mode Support:</strong></p>
                  <p className="text-gray-700 leading-relaxed mb-4">
                    All programs support <code className="bg-gray-100 px-2 py-1 rounded text-sm">--test-mode</code> for rapid validation:
                  </p>
                  <CodeBlock
                    language="bash"
                    code={`# Generate mock data (50 samples)
python -m src.program1_dataset_generator.main --test-mode

# Quick training (1 epoch, batch_size=16)
python -m src.program2_fine_tuning.main --test-mode

# Test ingestion (mock embeddings)
python -m src.program3_ingestion.main --test-mode

# Launch search interface with test data
python -m src.program4_search.main --test-mode`}
                  />
                  <p className="text-gray-700 leading-relaxed mt-4">
                    This enables full pipeline validation in minutes without requiring production databases or GPU training.
                  </p>
                </div>
              </div>
            }
          />

          {/* Next Steps CTA */}
          <div className="bg-navy text-white p-8 rounded-lg mt-12 mb-12">
            <h3 className="text-2xl font-bold mb-4">Next: Phase 2 - Task-Specific SLMs</h3>
            <p className="text-white/90 mb-6">
              With unified semantic infrastructure in place, Phase 2 fine-tunes task-specific small language models for each division&apos;s unique workflows. While Phase 1 enables cross-division discovery through shared embeddings, Phase 2 creates specialized intelligence for individual tasks like portfolio analysis, project assessment, and competitive research. These task models become the expert components in Phase 3&apos;s mixture-of-experts routing system.
            </p>
            <a
              href="/solution/phase-2"
              className="inline-block px-6 py-3 bg-teal text-white font-medium rounded-md hover:bg-teal/90 transition-colors"
            >
              Continue to Phase 2 →
            </a>
          </div>
        </Container>
      </section>

      <PhaseNav currentPhase={1} />
    </>
  );
}
