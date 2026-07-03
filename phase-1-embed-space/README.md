# Phase 1: Unified Embedding Space

Part of the **Emergent Enterprise AI** framework - building the foundational infrastructure for semantic search across enterprise databases.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start (Test Mode)](#quick-start-test-mode)
- [Production Usage](#production-usage)
- [Data Freshness & Sync](#data-freshness--sync)
- [Programs](#programs)
  - [Program 1: Training Dataset Generator](#program-1-training-dataset-generator)
  - [Program 2: Embedding Fine-Tuning](#program-2-embedding-fine-tuning)
  - [Program 3: Ingestion Pipeline](#program-3-ingestion-pipeline)
  - [Program 4: Search & Retrieval](#program-4-search--retrieval)
- [Shared Modules](#shared-modules)
- [Configuration Reference](#configuration-reference)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Design Decisions](#design-decisions)

---

## Overview

This phase creates a **unified embedding space** that enables semantic search across 3 PostgreSQL databases. It follows the Habitat philosophy: **infrastructure that enables, not constrains**.

The system consists of 4 programs that work together:

| Program | Purpose | Input | Output |
|---------|---------|-------|--------|
| **Program 1** | Generate training data | PostgreSQL DBs | Parquet datasets |
| **Program 2** | Fine-tune embeddings | Training data | Custom model |
| **Program 3** | Ingest to vector DB | PostgreSQL DBs | ChromaDB embeddings |
| **Program 4** | Search interface | User queries | Relevant documents |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 1: UNIFIED EMBEDDING SPACE                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐                                                        │
│  │   PostgreSQL     │                                                        │
│  │   Databases      │                                                        │
│  │                  │                                                        │
│  │  ┌────────────┐  │    Program 1         Program 2                        │
│  │  │ Database 1 │──┼──────────────┐   ┌──────────────┐                     │
│  │  ├────────────┤  │              │   │              │                     │
│  │  │ Database 2 │──┼──────────────┼──▶│  Fine-Tune   │                     │
│  │  ├────────────┤  │   Extract    │   │  Embeddings  │                     │
│  │  │ Database 3 │──┼──────────────┘   │              │                     │
│  │  └────────────┘  │              ▼   └──────┬───────┘                     │
│  └────────┬─────────┘    train.parquet       │                              │
│           │              val.parquet         │ enterprise-embed-v1          │
│           │                                  ▼                              │
│           │              Program 3    ┌──────────────┐                      │
│           │           ┌──────────────▶│   ChromaDB   │                      │
│           └───────────┤   Ingest     │              │                      │
│                       │              │  Embeddings  │◀──────┐               │
│                       └──────────────│  + Metadata  │       │               │
│                                      │  (no text)   │       │               │
│                                      └──────┬───────┘       │               │
│                                             │               │               │
│                                             │ Program 4     │               │
│                                             ▼               │               │
│                                      ┌──────────────┐       │               │
│                                      │   Gradio     │       │               │
│  ┌──────────────┐                   │   Search     │───────┘               │
│  │    User      │◀─────────────────▶│   Interface  │   Parent Doc          │
│  │   Browser    │    http://        └──────────────┘   Retrieval           │
│  └──────────────┘    localhost:7860                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Design Decision**: ChromaDB stores only embeddings and metadata. Actual text is retrieved from source databases at query time (parent document retrieval pattern). This keeps the vector database lean and ensures data consistency with source systems.

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Embedding Model** | all-MiniLM-L6-v2 | 384 dimensions |
| **Fine-tuning** | Sentence-Transformers | >=3.0.0 |
| **Loss Function** | MultipleNegativesRankingLoss | In-batch negatives |
| **Vector Database** | ChromaDB | >=0.5.0 |
| **Source Databases** | PostgreSQL | With asyncpg |
| **UI Framework** | Gradio | >=4.15.0 |
| **Text Processing** | LangChain Text Splitters | RecursiveCharacterTextSplitter |
| **Configuration** | Pydantic Settings | YAML + env vars |
| **Logging** | structlog | JSON formatted |

---

## Project Structure

```
phase-1-embed-space/
├── README.md                         # This file
├── pyproject.toml                    # Dependencies & build config
├── .env.example                      # Environment variable template
├── .gitignore                        # Git ignore rules
│
├── config/
│   ├── __init__.py
│   ├── config.yaml                   # Main configuration (placeholder pattern)
│   ├── config.example.yaml           # Configuration template
│   └── settings.py                   # Pydantic settings models
│
├── docker/
│   └── docker-compose.yml            # ChromaDB server setup
│
├── src/
│   ├── __init__.py
│   │
│   ├── shared/                       # Shared utilities across all programs
│   │   ├── __init__.py
│   │   ├── database.py               # PostgreSQL connection manager
│   │   ├── embedding_model.py        # SentenceTransformer wrapper
│   │   ├── chromadb_client.py        # ChromaDB operations wrapper
│   │   └── chunking.py               # Text chunking strategies
│   │
│   ├── program1_dataset_generator/   # Training data generation
│   │   ├── __init__.py
│   │   ├── main.py                   # Entry point
│   │   ├── extractors/
│   │   │   ├── __init__.py
│   │   │   └── text_extractor.py     # DB extraction + mock data
│   │   └── pair_generators/
│   │       ├── __init__.py
│   │       └── contrastive_pairs.py  # Anchor-positive pair generation
│   │
│   ├── program2_fine_tuning/         # Model fine-tuning
│   │   ├── __init__.py
│   │   ├── main.py                   # Entry point
│   │   ├── trainer.py                # SentenceTransformerTrainer wrapper
│   │   └── evaluator.py              # Evaluation metrics
│   │
│   ├── program3_ingestion/           # Data ingestion to ChromaDB
│   │   ├── __init__.py
│   │   ├── main.py                   # Entry point
│   │   ├── pipeline.py               # Ingestion orchestration
│   │   └── metadata_extractor.py     # Metadata extraction
│   │
│   └── program4_search/              # Search interface
│       ├── __init__.py
│       ├── main.py                   # Entry point
│       ├── retriever.py              # Semantic search with deduplication
│       ├── parent_document_fetcher.py # Fetch full docs from source DBs
│       └── gradio_app.py             # Gradio UI
│
├── data/                             # Generated data (gitignored)
│   ├── training_datasets/            # Parquet files from Program 1
│   │   ├── train.parquet
│   │   ├── validation.parquet
│   │   └── dataset_info.json
│   ├── models/                       # Fine-tuned models from Program 2
│   │   └── enterprise-embed-v1/
│   ├── chromadb/                     # Local ChromaDB storage (fallback)
│   └── logs/                         # Application logs
│
└── tests/
    └── __init__.py
```

---

## Prerequisites

- **Python**: 3.10 or higher
- **Docker**: For ChromaDB server (optional - falls back to local storage)
- **PostgreSQL**: 3 source databases (or use test mode with mock data)
- **GPU** (optional): CUDA or MPS for faster training/inference

---

## Installation

### 1. Clone and Navigate

```bash
cd phase-1-embed-space
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -e .

# For development
pip install -e ".[dev]"
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Start ChromaDB (Optional)

```bash
docker-compose -f docker/docker-compose.yml up -d
```

> **Note**: If Docker is not available, the system automatically falls back to local persistent ChromaDB storage in `data/chromadb/`.

---

## Quick Start (Test Mode)

Test mode uses mock data, allowing you to run the full pipeline without real databases.

```bash
# 1. Generate training dataset (mock data)
python -m src.program1_dataset_generator.main --test-mode

# 2. Fine-tune embedding model (1 epoch for quick test)
python -m src.program2_fine_tuning.main --epochs 1 --test-mode

# 3. Ingest data to ChromaDB (mock data)
python -m src.program3_ingestion.main --test-mode

# 4. Launch search interface
python -m src.program4_search.main --test-mode
```

Open http://localhost:7860 to use the search interface.

### Expected Test Mode Output

| Program | Output |
|---------|--------|
| Program 1 | ~2,700 training pairs + ~300 validation pairs |
| Program 2 | Final loss ~0.15, model saved to `data/models/enterprise-embed-v1/` |
| Program 3 | ~2,700 embeddings in ChromaDB |
| Program 4 | Search UI at http://localhost:7860 |

---

## Production Usage

### 1. Configure Database Connections

Edit `config/config.yaml` to match your actual PostgreSQL schemas:

```yaml
databases:
  database_1:
    host: "${DB1_HOST:-localhost}"
    port: "${DB1_PORT:-5432}"
    name: "${DB1_NAME:-your_database}"
    user: "${DB1_USER:-postgres}"
    password: "${DB1_PASSWORD:-}"
    tables:
      - name: "your_table_name"
        text_columns: ["content_column", "title_column"]
        id_column: "id"
        timestamp_column: "updated_at"
        additional_metadata: ["category", "author"]
```

### 2. Set Environment Variables

```bash
# In .env file
DB1_HOST=your-db-host.example.com
DB1_PORT=5432
DB1_NAME=production_db
DB1_USER=app_user
DB1_PASSWORD=secure_password
```

### 3. Run Full Pipeline

```bash
# Generate training data from real databases
python -m src.program1_dataset_generator.main

# Fine-tune with more epochs
python -m src.program2_fine_tuning.main --epochs 3

# Ingest all data
python -m src.program3_ingestion.main

# Launch search (production mode)
python -m src.program4_search.main
```

### 4. Incremental Updates

For ongoing data updates:

```bash
python -m src.program3_ingestion.main --incremental
```

See [Data Freshness & Sync](#data-freshness--sync) for the full sync model,
including how deletes propagate.

---

## Data Freshness & Sync

The index stays fresh through two complementary mechanisms — watermark-based
incremental sync plus a nightly reconcile pass. There is no CDC
infrastructure; this is a deliberate trade-off (see the accepted staleness
window below).

### Incremental sync (inserts & updates)

`--incremental` ingests only records whose `timestamp_column` is newer than
the per-table watermark stored in `data/sync_state.json`:

- The watermark is the **newest data timestamp observed** in the extracted
  records — not the wall clock — so records committed while a sync runs are
  never skipped.
- The watermark **only advances when every record in the table ingested
  cleanly**. On any processing or upsert error it holds, and the failed
  records are retried on the next run.
- Re-ingested documents have their existing chunks deleted before upsert, so
  documents that shrank don't leave orphan chunks behind.

### Nightly reconcile (deletes)

Incremental sync never observes deletes — a deleted source row simply stops
appearing in queries. The reconcile pass removes its chunks from ChromaDB:

```bash
python -m src.program3_ingestion.main --reconcile
```

For each configured table it pulls all source IDs, pages through the
collection's chunks for that table, and deletes any chunk whose
`parent_doc_id` no longer exists at the source.

**Accepted staleness window**: deletes propagate on the nightly pass, so
deleted source records may keep appearing in search results for up to ~24
hours. This is an accepted design decision — the alternative (CDC / triggers
on the source databases) was rejected as disproportionate infrastructure for
this phase.

Example crontab (hourly incremental, nightly reconcile at 03:15):

```cron
0 * * * *  cd /path/to/phase-1-embed-space && .venv/bin/python -m src.program3_ingestion.main --incremental
15 3 * * * cd /path/to/phase-1-embed-space && .venv/bin/python -m src.program3_ingestion.main --reconcile
```

### Embedding model versions

Every chunk is tagged with `embedding_model_version` (the model path/name
that produced its vector) at ingestion. The search app compares this tag
against its loaded model at startup and logs
`embedding_model_version_mismatch` if they differ.

**After retraining the embedding model (Program 2), re-run a full ingestion**
(`python -m src.program3_ingestion.main`, no `--incremental`) so every chunk
is re-embedded with the new model — query vectors from one model are not
comparable against index vectors from another.

---

## Programs

### Program 1: Training Dataset Generator

**Purpose**: Extract text from PostgreSQL databases and create contrastive training pairs for embedding fine-tuning.

**Location**: `src/program1_dataset_generator/`

```bash
# Usage
python -m src.program1_dataset_generator.main [OPTIONS]

# Options
--config PATH      Configuration file (default: config/config.yaml)
--test-mode        Use mock data instead of real databases
```

**How It Works**:

1. **Extract**: Reads text from configured `text_columns` in each table
2. **Chunk**: Splits documents using RecursiveCharacterTextSplitter (512 chars, 50 overlap)
3. **Pair**: Creates contrastive pairs using adjacent chunks (semantic similarity assumed)
4. **Split**: 90% training / 10% validation
5. **Save**: Outputs Parquet files to `data/training_datasets/`

**Output Files**:
- `data/training_datasets/train.parquet` - Training pairs
- `data/training_datasets/validation.parquet` - Validation pairs
- `data/training_datasets/dataset_info.json` - Dataset statistics

**Pair Generation Strategy**:
```
Document: [chunk_1] [chunk_2] [chunk_3] [chunk_4]
                 ↓       ↓
Pairs:    (chunk_1, chunk_2), (chunk_2, chunk_3), (chunk_3, chunk_4)
```

Adjacent chunks from the same document serve as positive pairs - they share semantic context.

---

### Program 2: Embedding Fine-Tuning

**Purpose**: Fine-tune `all-MiniLM-L6-v2` on enterprise data using Sentence-Transformers.

**Location**: `src/program2_fine_tuning/`

```bash
# Usage
python -m src.program2_fine_tuning.main [OPTIONS]

# Options
--config PATH      Configuration file
--epochs N         Override number of training epochs
--test-mode        Use quick settings for testing
```

**Training Configuration**:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `epochs` | 3 | Training epochs |
| `batch_size` | 64 | Batch size (affects in-batch negatives) |
| `learning_rate` | 2e-5 | Learning rate |
| `warmup_ratio` | 0.1 | Warmup proportion |
| `fp16` | true | Mixed precision (GPU only) |

**Loss Function**: `MultipleNegativesRankingLoss`

This loss uses in-batch negatives - for each anchor-positive pair, all other positives in the batch serve as negatives. Larger batch sizes = more negatives = better training signal.

**Output**: Model saved to `data/models/enterprise-embed-v1/` in SentenceTransformer format.

**Device Selection**:
- CUDA (NVIDIA GPU) - preferred
- MPS (Apple Silicon) - automatic fallback
- CPU - last resort

---

### Program 3: Ingestion Pipeline

**Purpose**: Read records from PostgreSQL, chunk, embed, and store in ChromaDB.

**Location**: `src/program3_ingestion/`

```bash
# Usage
python -m src.program3_ingestion.main [OPTIONS]

# Options
--config PATH      Configuration file
--test-mode        Use mock data
--incremental      Only process new/updated records
--stats-only       Show collection statistics without ingesting
```

**Pipeline Steps**:

1. **Read**: Fetch records from all configured databases/tables
2. **Chunk**: Split text using RecursiveCharacterTextSplitter
3. **Extract Metadata**: Pull metadata fields for each chunk
4. **Embed**: Generate embeddings using fine-tuned model
5. **Store**: Upsert embeddings + metadata to ChromaDB

**What Gets Stored**:

| Stored in ChromaDB | NOT Stored |
|--------------------|------------|
| Embedding vector | Document text |
| chunk_id | Raw content |
| parent_doc_id | |
| source_db | |
| source_table | |
| chunk_index | |
| Additional metadata | |

**Metadata Schema**:
```python
{
    "chunk_id": "db1_table1_doc123_chunk_0",
    "parent_doc_id": "doc123",
    "source_db": "database_1",
    "source_table": "documents",
    "chunk_index": 0,
    "total_chunks": 5,
    # Additional fields from config
}
```

---

### Program 4: Search & Retrieval

**Purpose**: Gradio-based semantic search interface with parent document retrieval.

**Location**: `src/program4_search/`

```bash
# Usage
python -m src.program4_search.main [OPTIONS]

# Options
--config PATH      Configuration file
--test-mode        Use mock parent document fetcher
--port N           Override server port (default: 7860)
--share            Create public Gradio link
```

**Features**:
- Semantic search using fine-tuned embeddings
- Configurable number of results (1-20)
- Database filtering
- Similarity scores
- Parent document retrieval
- Source attribution

**Search Flow**:
```
User Query → Embed → ChromaDB Search → Get Metadata → Fetch Parent Docs → Display
```

**Interface Elements**:
- Query input box
- Results slider (1-20)
- Database filter dropdown
- Search button
- Markdown results display

**URL**: http://localhost:7860

---

## Shared Modules

### `src/shared/database.py`

PostgreSQL connection manager supporting:
- Async connections with `asyncpg`
- Connection pooling
- Schema-agnostic queries via placeholder pattern
- Mock database manager for testing

```python
from src.shared.database import DatabaseConnectionManager

manager = DatabaseConnectionManager(settings.databases)
await manager.initialize()
# Use manager for queries
await manager.close()
```

### `src/shared/embedding_model.py`

SentenceTransformer wrapper with:
- Base model or fine-tuned model loading
- Batch embedding generation
- Device auto-selection (CUDA/MPS/CPU)

```python
from src.shared.embedding_model import EmbeddingModelManager

manager = EmbeddingModelManager(settings.embedding)
manager.load_model()
embeddings = manager.embed(["text1", "text2"])
```

### `src/shared/chromadb_client.py`

ChromaDB wrapper with:
- HTTP server mode (preferred)
- Local persistent mode (fallback)
- Collection management
- CRUD operations

```python
from src.shared.chromadb_client import ChromaDBClient

client = ChromaDBClient(settings.chromadb)
client.connect()  # Auto-fallback to local if server unavailable
client.get_or_create_collection()
```

### `src/shared/chunking.py`

Text chunking strategies:
- RecursiveCharacterTextSplitter
- Configurable chunk size and overlap
- Minimum chunk length filtering

```python
from src.shared.chunking import TextChunker

chunker = TextChunker(chunk_size=512, chunk_overlap=50)
chunks = chunker.split_text("Long document text...")
```

---

## Configuration Reference

### Main Configuration (`config/config.yaml`)

```yaml
# Application settings
app:
  name: "enterprise-embedding-space"
  version: "1.0.0"
  log_level: "INFO"

# Source databases (placeholder pattern)
databases:
  database_1:
    host: "${DB1_HOST:-localhost}"
    tables:
      - name: "documents"
        text_columns: ["content", "title"]  # Which columns contain text
        id_column: "id"                     # Primary key
        timestamp_column: "updated_at"      # For incremental sync
        additional_metadata: ["category"]   # Extra fields to index

# ChromaDB vector database
chromadb:
  host: "${CHROMADB_HOST:-localhost}"
  port: "${CHROMADB_PORT:-8000}"
  collection_name: "enterprise_embeddings"
  hnsw:
    space: "cosine"      # Distance metric

# Embedding model
embedding:
  base_model: "sentence-transformers/all-MiniLM-L6-v2"
  fine_tuned_model_path: "data/models/enterprise-embed-v1"
  embedding_dimension: 384
  batch_size: 32
  device: "auto"         # auto, cuda, cpu, mps

# Program 1: Dataset generator
dataset_generator:
  output_dir: "data/training_datasets"
  samples_per_table: 10000
  chunking:
    chunk_size: 512
    chunk_overlap: 50
  train_val_split: 0.9

# Program 2: Fine-tuning
fine_tuning:
  output_dir: "data/models"
  model_name: "enterprise-embed-v1"
  training:
    epochs: 3
    batch_size: 64
    learning_rate: 2.0e-5
    fp16: true

# Program 3: Ingestion
ingestion:
  chunking:
    chunk_size: 512
    chunk_overlap: 50
  batch_size: 100
  incremental:
    enabled: true

# Program 4: Search
search:
  default_k: 5
  max_k: 20
  gradio:
    host: "0.0.0.0"
    port: 7860
```

### Environment Variables (`.env`)

```bash
# Database 1
DB1_HOST=localhost
DB1_PORT=5432
DB1_NAME=enterprise_db1
DB1_USER=postgres
DB1_PASSWORD=your_password

# Database 2
DB2_HOST=localhost
DB2_PORT=5432
DB2_NAME=enterprise_db2
DB2_USER=postgres
DB2_PASSWORD=your_password

# Database 3
DB3_HOST=localhost
DB3_PORT=5432
DB3_NAME=enterprise_db3
DB3_USER=postgres
DB3_PASSWORD=your_password

# ChromaDB
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
```

---

## Testing

### Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### End-to-End Test (Test Mode)

```bash
# Full pipeline with mock data
python -m src.program1_dataset_generator.main --test-mode && \
python -m src.program2_fine_tuning.main --epochs 1 --test-mode && \
python -m src.program3_ingestion.main --test-mode && \
python -m src.program4_search.main --test-mode
```

### Check ChromaDB Stats

```bash
python -m src.program3_ingestion.main --stats-only
```

---

## Troubleshooting

### Port 7860 Already in Use

```bash
# Find and kill process
lsof -ti:7860 | xargs kill -9

# Then relaunch
python -m src.program4_search.main --test-mode
```

### ChromaDB Connection Failed

The system automatically falls back to local persistent storage:

```
chromadb_http_failed_using_local: Could not connect to a Chroma server
chromadb_connected: mode="local_persistent"
```

To use server mode, ensure Docker is running:

```bash
docker-compose -f docker/docker-compose.yml up -d
docker-compose -f docker/docker-compose.yml logs -f chromadb
```

### Pydantic Protected Namespace Warning

This is a harmless warning about field names starting with `model_`:

```
UserWarning: Field "model_name" has conflict with protected namespace "model_"
```

Can be suppressed by adding to config classes:

```python
model_config = ConfigDict(protected_namespaces=())
```

### CUDA Out of Memory

Reduce batch size in `config/config.yaml`:

```yaml
fine_tuning:
  training:
    batch_size: 32  # Reduce from 64

embedding:
  batch_size: 16    # Reduce from 32
```

### Chunks Too Short

If you see few training pairs, documents may be too short. The mock data generator creates 3-5 paragraphs per document to ensure proper chunking. For real data, ensure your source documents have sufficient text.

---

## Design Decisions

### 1. Parent Document Retrieval Pattern

**Decision**: Store only embeddings + metadata in ChromaDB, not the document text.

**Rationale**:
- Keeps vector database lean
- Ensures consistency with source databases
- Enables real-time data updates without re-embedding
- Metadata-based filtering remains fast

### 2. Placeholder Configuration Pattern

**Decision**: Configure database tables by column roles (`text_columns`, `id_column`) rather than fixed schemas.

**Rationale**:
- Adapts to unknown schemas
- Works with any PostgreSQL database structure
- Single configuration file for multiple databases

### 3. Adjacent Chunks as Positive Pairs

**Decision**: Use adjacent chunks from the same document as contrastive training pairs.

**Rationale**:
- Adjacent chunks share semantic context
- No manual labeling required
- Scales automatically with data volume
- Works across any document type

### 4. ChromaDB with HTTP Fallback

**Decision**: Try HTTP server first, fall back to local persistent storage.

**Rationale**:
- Production use benefits from dedicated server
- Development works without Docker
- Seamless experience either way

### 5. Sentence-Transformers over Unsloth

**Decision**: Use Sentence-Transformers for embedding fine-tuning.

**Rationale**:
- Native support for embedding models
- Built-in contrastive losses
- Mature ecosystem
- (Unsloth focuses on LLM fine-tuning, not embeddings)

### 6. Rerank After Fetch

**Decision**: The CrossEncoder reranker runs *after* the parent-document
fetch, not against the vector index.

Because of decision 1, ChromaDB stores no chunk text — so there is nothing
in the index for a CrossEncoder to score. The search flow is:

```
vector search (k × candidate_multiplier candidates, metadata only)
  → parallel parent-document fetch from source PostgreSQL
  → recover each matched chunk by slicing at its stored char_start/char_end
  → CrossEncoder rerank on the recovered chunk texts
  → dedup by parent document → top-k
```

**Rationale**:
- Preserves the metadata-only index (decision 1)
- Reranking sees the *current* source text, not a stale indexed copy
- Chunk recovery is exact because the fetcher reconstructs the combined
  text with the same expression ingestion used (`COALESCE(col::text, '')`
  joined by single spaces)
- If stored offsets no longer fit the document (record changed since
  ingestion), the app falls back to a window around `char_start` and logs
  `stale_chunk_offsets`

---

## Alignment with Emergent AI Philosophy

This implementation follows the Emergent Enterprise AI principles:

| Principle | How We Implement It |
|-----------|---------------------|
| **Infrastructure, Not System** | Shared embedding infrastructure enables unit-level experimentation |
| **Shared Capabilities** | Unified embedding space serves all future phases |
| **Incremental Value** | Each program delivers standalone value |
| **Placeholder Pattern** | Configuration adapts to actual database schemas |
| **Foundation for Future** | Supports Task SLMs, MoE Agents, and A2A discovery |

---

## Next Steps

After completing Phase 1, proceed to:

- **Phase 2**: Fine-tune Task-specific SLMs using Unsloth
- **Phase 3**: Merge SLMs into Mixture-of-Experts models
- **Phase 4**: Implement A2A protocol for agent collaboration
- **Phase 5**: Train orchestrator SLM from discovery data

See the parent `CLAUDE.md` for the full Emergent Enterprise AI framework.
