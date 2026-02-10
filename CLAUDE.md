# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL: Working Directory

**ALWAYS create files in the current working directory specified in the environment info, NEVER in the location of reference documents.** Reference documents (implementation plans, specs, etc.) provide instructions only - their file path is irrelevant to where code should be written. If a reference document is at `/some/other/path/PLAN.md`, you still create files in THIS repository.

## Project Overview

This is a research and development repository for **Emergent Enterprise AI** - a bottom-up approach to enterprise AI deployment. The core philosophy is that AI capabilities should emerge organically from unit-level experimentation rather than top-down system design.

The project implements a 5-phase framework for enterprise AI transformation using a funder intelligence system as the case study (international development organizations optimizing funding strategy).

## Architecture

### Phase Structure

The codebase is organized into sequential phases:

1. **Phase 1: Unified Embedding Space** (`phase-1-embed-space/`) - Shared embedding infrastructure with:
   - Training dataset generator from PostgreSQL databases
   - Sentence-Transformers fine-tuning (all-MiniLM-L6-v2)
   - ChromaDB ingestion pipeline (embeddings + metadata, parent document retrieval)
   - Gradio search interface

2. **Phase 2: Task SLMs** (`phase-2-task-slms/`) - Fine-tuning small language models for specific unit tasks using Unsloth and LoRA

3. **Phase 3: MoE Experts** (`phase-3-moe-experts/`) - Merging fine-tuned SLMs into Mixture-of-Experts models using mergekit

4. **Phase 4: Agentic Discovery** (`phase-4-agentic-discovery/`) - A2A (Agent-to-Agent) protocol implementation for autonomous agent collaboration with adaptive depth limiting. Contains:
   - A2A protocol implementation (FastAPI services)
   - Adaptive depth testing framework (7-phase discovery over 90 days)
   - Training data preparation pipeline

5. **Phase 5: Orchestrated Agentic** (`phase-5-orchestrated-agentic/`) - SLM orchestrator fine-tuning from discovery data

### Key Components

**A2A Protocol Agents** (used throughout Phase 4-5):
- `fundraising-agent`: Investor intelligence (portfolio, interests, capacity)
- `business-development-agent`: RFP tracking and competitive landscape
- `field-operations-agent`: Local market intelligence and project performance

**MoE Architecture** (Phase 3):
- Creates **3 separate MoE models**, one per organizational unit:
  - Fundraising MoE (5 experts from 5 task SLMs)
  - Business Development MoE (4 experts from 4 task SLMs)
  - Field Operations MoE (5 experts from 5 task SLMs)
- Base model: Llama 3.1 8B
- Architecture: Mixtral-style MoE (per-unit expert pools)
- Router: Hidden gate mode with positive/negative prompt embeddings
- Expert selection: 2-of-N per token (within each unit's MoE)
- Each MoE powers one A2A agent in Phase 4's agentic network
- Fine-tuning: LoRA with target modules `[q_proj, k_proj, v_proj, o_proj, up_proj, down_proj, gate_proj]`

## Commands

### Phase 1: Unified Embedding Space
```bash
cd phase-1-embed-space

# Start ChromaDB server
docker-compose -f docker/docker-compose.yml up -d

# Generate training dataset (use --test-mode for mock data)
python -m src.program1_dataset_generator.main --test-mode

# Fine-tune embedding model
python -m src.program2_fine_tuning.main --epochs 1 --test-mode

# Ingest data to ChromaDB
python -m src.program3_ingestion.main --test-mode

# Launch search interface (http://localhost:7860)
python -m src.program4_search.main --test-mode
```

### Phase 2: Fine-tuning Task SLMs
```bash
# Run Unsloth fine-tuning notebook (requires Colab or GPU environment)
# See: phase-2-task-slms/Fine_Tune_Llama_3_1_8B_with_Unsloth.ipynb
```

### Phase 3: MoE Merging (3 Models)
```bash
cd phase-3-moe-experts

# Test mode pipeline (no GPU required) - creates 3 mock MoE models
python -m src.program1_import.main --test-mode      # Generate mock adapters for 3 units
python -m src.program2_config_gen.main --test-mode  # Generate 3 MoE configs
python -m src.program3_merge.main --test-mode       # Create 3 mock merged models
python -m src.program5_export.main --test-mode      # Export 3 packages for Phase 4

# Production mode (requires GPU) - merges 3 separate MoE models
python -m src.program1_import.main --phase2-export ../phase-2-task-slms/exports
python -m src.program2_config_gen.main              # Generate configs for all units
python -m src.program3_merge.main --cuda            # Merge all 3 MoEs
python -m src.program5_export.main --generate-agent-configs --generate-embeddings

# Single unit operations
python -m src.program3_merge.main --unit fundraising --cuda
python -m src.program5_export.main --unit fundraising

# Utility commands
python -m src.program3_merge.main --dry-run         # Validate configs only
python -m src.program2_config_gen.main --show-config data/configs/fundraising_moe.yaml
```

### Phase 4: A2A Agents (requires 3 terminals)
```bash
# Terminal 1: Fundraising Agent
uvicorn a2a_protocol_implementation:fundraising_app --port 8001

# Terminal 2: Business Development Agent
uvicorn a2a_protocol_implementation:business_development_app --port 8002

# Terminal 3: Field Operations Agent
uvicorn a2a_protocol_implementation:field_operations_app --port 8003

# Health check
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health

# Get call statistics
curl http://localhost:8001/stats
```

## Dependencies

**Phase 1 (Embeddings):**
- `sentence-transformers` - Embedding model training and inference
- `chromadb` - Vector database
- `asyncpg`, `psycopg2-binary` - PostgreSQL connections
- `gradio` - Search UI
- `langchain-text-splitters` - Text chunking

**ML/Fine-tuning:**
- `unsloth` - Fast LLM fine-tuning
- `transformers`, `peft`, `trl` - Hugging Face training stack
- `bitsandbytes` - 8-bit quantization
- `mergekit` - MoE model merging
- `sentence-transformers` - Routing embeddings for MoE

**A2A Protocol:**
- `fastapi`, `uvicorn` - API services
- `httpx` - Async HTTP client
- `pydantic` - Data validation

## Key Concepts

**Adaptive Depth Limiting**: The 90-day discovery phase varies depth limits (1→2→3→2→4→2→adaptive) to understand workflow patterns and optimal cascading depths. Control phases (depth=2 on days 8-21, 36-49, 64-75) detect system drift.

**Discovery → Training Pipeline**: A2A call logs from the discovery phase are converted to fine-tuning data for the orchestrator SLM. The pipeline extracts workflow patterns, agent performance profiles, and error modes.

**Orchestrator Training**: The final orchestrator is a fine-tuned SLM (recommended: Qwen2.5 7B or Phi-4) that learns routing decisions from discovery data rather than using hardcoded rules.

### Phase 5: Orchestrated Agentic
```bash
cd phase-5-orchestrated-agentic

# Install package
pip install -e .

# Test mode pipeline (no GPU required)
phase5-convert --full-pipeline --test-mode      # Convert discovery data
phase5-finetune --full-pipeline --test-mode     # Mock fine-tuning
phase5-inference --start --test-mode            # Start mock inference server
phase5-orchestrator --start --test-mode         # Start orchestrator service

# Production mode (requires GPU + Phase 4 data)
phase5-convert --full-pipeline                  # Convert Phase 4 data
phase5-finetune --train --epochs 3              # Fine-tune orchestrator
phase5-inference --start --server vllm          # Start vLLM inference server
phase5-orchestrator --start                     # Start orchestrator service

# Launch Gradio UI
python -m src.program4_orchestrator_service.main --ui --test-mode
```
