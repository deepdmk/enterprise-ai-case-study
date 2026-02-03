# Emergent Enterprise AI Development

> **Bottom-up AI emergence framework for enterprise transformation**

A research and development repository demonstrating how enterprise AI capabilities should emerge organically from unit-level experimentation rather than top-down system design.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Core Philosophy](#core-philosophy)
- [Architecture](#architecture)
- [The Five Phases](#the-five-phases)
- [Quick Start](#quick-start)
- [Use Case: Funder Intelligence System](#use-case-funder-intelligence-system)
- [Key Technologies](#key-technologies)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Enterprise AI Habitat** is a framework for building enterprise AI systems that emphasizes:

1. **Infrastructure over systems** - Build enabling capabilities, not rigid solutions
2. **Bottom-up emergence** - Let intelligence emerge from unit-level experimentation
3. **Incremental value** - Deliver value at each phase, regardless of what comes next
4. **Organizational learning** - Build AI capability into teams, not just tools

This repository implements the complete 5-phase framework using a **funder intelligence system** as a case study (international development organizations optimizing funding strategy).

### Why This Matters

Traditional top-down enterprise AI deployments fail because they:
- Design complete systems before understanding actual needs
- Assume uniform requirements across diverse organizational units
- Create data debt by requiring cleanup before value delivery
- Lock organizations into initial architectural decisions
- Separate AI systems from actual work patterns

The Habitat approach succeeds by:
- Enabling experimentation at the edges (teams, units, individuals)
- Creating conditions for AI to work bottom-up
- Capturing data naturally from work, not warehouses
- Letting successful patterns scale organically
- Building sustainable organizational AI capability

---

## Core Philosophy

### The Fundamental Insight

**"You can't scale top-down AI solutions without first building the conditions for AI to work bottom-up."**

### Habitat vs Traditional

| Aspect | Traditional (Top-Down) | Habitat (Bottom-Up) |
|--------|----------------------|-------------------|
| **Design** | System designed first | Patterns emerge from use |
| **Timeline** | Fixed (18-24 months) | Adaptive and incremental |
| **Scope** | Comprehensive from start | Incremental value delivery |
| **Team Role** | Passive consumers | Active experimenters |
| **Data Strategy** | Centralize and clean first | Distribute and capture naturally |
| **Failure Mode** | Entire project fails | Individual experiments fail cheaply |
| **Success Pattern** | Mandate global rollout | Organic adoption of what works |
| **Adaptation** | Requires redesign | Continuous evolution |
| **Training Data** | Prepared upfront | Captured from actual work |

### Key Principles

1. **Enable, Don't Constrain**: Infrastructure should open possibilities, not limit them
2. **Capture at Point of Value**: Data flows from where work happens
3. **Share Capabilities, Not Systems**: Common infrastructure, diverse applications
4. **Learn Before Scaling**: Prove value at unit level before enterprise-wide deployment
5. **Emergent Intelligence**: System behavior emerges from agent autonomy, not central design

For a deep dive into the philosophy, see the [`enterprise_ai_habitat.ipynb`](./enterprise_ai_habitat.ipynb) notebook.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    ENTERPRISE AI HABITAT FRAMEWORK                        │
│                         5-Phase Evolution                                 │
└──────────────────────────────────────────────────────────────────────────┘

Phase 0: Infrastructure Foundation
├─ Shared registries (datasets, models, experiments)
├─ Structured logging and configuration
├─ Evaluation schemas and metrics
└─ Cross-phase data tracking
          │
          ↓
Phase 1: Unified Embedding Space
├─ Fine-tuned embedding model (all-MiniLM-L6-v2)
├─ ChromaDB vector database
├─ Semantic search across enterprise data
└─ Foundation for cross-unit intelligence
          │
          ↓
Phase 2: Task-Specific SLMs (per unit)
├─ 3-5 specialized models per organizational unit
├─ Fine-tuned on unit-specific tasks (Unsloth + LoRA)
├─ Lightweight, focused, high-quality
└─ Unit autonomy in AI capabilities
          │
          ↓
Phase 3: Mixture-of-Experts Models (per unit)
├─ Merge unit's task SLMs into unified MoE agent
├─ 3 separate MoE models (one per unit)
├─ Mixtral-style architecture with hidden gate routing
└─ Each unit owns their AI agent
          │
          ↓
Phase 4: Agentic Discovery (A2A Protocol)
├─ Agent-to-Agent communication protocol
├─ 90-day adaptive depth experiment
├─ Discover optimal collaboration patterns
└─ Generate orchestrator training data
          │
          ↓
Phase 5: Orchestrated Agentic System
├─ SLM orchestrator (Qwen2.5 7B or Phi-4)
├─ Trained on Phase 4 discovery data
├─ Learned routing, not rule-based
└─ Emergent multi-agent intelligence
```

---

## The Five Phases

### Phase 0: Infrastructure Foundation

**Status**: ✅ Complete
**Location**: [`phase-0-infrastructure/`](./phase-0-infrastructure/)

Foundational infrastructure for all downstream phases:
- **DataRegistry**: Track datasets with full lineage
- **ModelRegistry**: Version control for models
- **ExperimentTracker**: Log training experiments
- **Structured Logging**: JSON + console formatters
- **Evaluation Schemas**: Standardized metrics

[📄 Phase 0 Documentation](./phase-0-infrastructure/README.md)

---

### Phase 1: Unified Embedding Space

**Status**: ✅ Complete
**Location**: [`phase-1-embed-space/`](./phase-1-embed-space/)

Semantic search infrastructure enabling cross-database intelligence:

**4 Programs**:
1. **Dataset Generator**: Extract training data from PostgreSQL databases
2. **Embedding Fine-Tuning**: Fine-tune `all-MiniLM-L6-v2` on enterprise data
3. **Ingestion Pipeline**: Chunk, embed, and store in ChromaDB
4. **Search Interface**: Gradio UI with parent document retrieval

**Quick Start**:
```bash
cd phase-1-embed-space

# Test mode (mock data, no databases required)
python -m src.program1_dataset_generator.main --test-mode
python -m src.program2_fine_tuning.main --epochs 1 --test-mode
python -m src.program3_ingestion.main --test-mode
python -m src.program4_search.main --test-mode  # http://localhost:7860
```

**Key Technologies**: Sentence-Transformers, ChromaDB, Gradio, PostgreSQL (asyncpg)

[📄 Phase 1 Documentation](./phase-1-embed-space/README.md)

---

### Phase 2: Task-Specific SLMs

**Status**: ✅ Complete
**Location**: [`phase-2-task-slms/`](./phase-2-task-slms/)

Fine-tune small language models for unit-specific tasks:

**Per-Unit Tasks**:
- **Fundraising Unit**: Portfolio analysis, investor profiling, market sizing, fit scoring, briefing generation
- **Business Development Unit**: RFP analysis, positioning strategy, win probability, proposal writing
- **Field Operations Unit**: Market assessment, program design, risk analysis, impact forecasting, stakeholder mapping

**Technology**: Unsloth for fast LoRA fine-tuning on Llama 3.1 8B

**Example**:
```python
# Fine-tuning notebook (Google Colab)
# See: phase-2-task-slms/Fine_Tune_Llama_3_1_8B_with_Unsloth.ipynb
```

[📄 Phase 2 Documentation](./phase-2-task-slms/README.md)

---

### Phase 3: Mixture-of-Experts Models

**Status**: ✅ Complete
**Location**: [`phase-3-moe-experts/`](./phase-3-moe-experts/)

Merge each unit's task SLMs into a unified MoE agent:

**Architecture**:
- **3 separate MoE models** (one per organizational unit)
- **Mixtral-style MoE** with hidden gate routing
- **2-of-N expert selection** per token
- **Base model**: Llama 3.1 8B
- **Merging tool**: mergekit

**Programs**:
```bash
cd phase-3-moe-experts

# Test mode (no GPU required)
python -m src.program1_import.main --test-mode
python -m src.program2_config_gen.main --test-mode
python -m src.program3_merge.main --test-mode
python -m src.program5_export.main --test-mode

# Production (requires GPU + Phase 2 models)
python -m src.program1_import.main --phase2-export ../phase-2-task-slms/exports
python -m src.program3_merge.main --cuda
python -m src.program5_export.main --generate-agent-configs
```

[📄 Phase 3 Documentation](./phase-3-moe-experts/README.md)

---

### Phase 4: Agentic Discovery (A2A Protocol)

**Status**: ✅ Complete
**Location**: [`phase-4-agentic-discovery/`](./phase-4-agentic-discovery/)

Agent-to-Agent protocol implementation with adaptive depth optimization:

**Components**:
1. **A2A Fine-Tuning**: Add protocol capabilities to MoE models via LoRA
2. **Agent Services**: FastAPI services implementing A2A protocol
3. **Discovery Pipeline**: 90-day experiment varying cascade depths
4. **Adaptive Analyzer**: Determine optimal depths, export Phase 5 training data

**90-Day Discovery Schedule**:
| Phase | Days | Depth | Purpose |
|-------|------|-------|---------|
| 1 | 1-7 | 1 | Baseline (no cascading) |
| 2 | 8-21 | 2 | Single cascade |
| 3 | 22-35 | 3 | Two-level cascade |
| 4 | 36-49 | 2 | Control #1 (detect drift) |
| 5 | 50-63 | 4 | Outer bounds exploration |
| 6 | 64-75 | 2 | Control #2 (stability) |
| 7 | 76-90 | adaptive | Per-workflow optimization |

**Quick Start**:
```bash
cd phase-4-agentic-discovery

# Start all agent services (Terminal 1)
phase4-agent-services --start-all --test-mode

# Run 7-day test discovery (Terminal 2)
phase4-discovery --run --test-mode

# Analyze and export for Phase 5
phase4-analyze --full-pipeline
```

**Key Innovation**: Adaptive depth limiting - the system discovers optimal collaboration patterns rather than having them designed upfront.

[📄 Phase 4 Documentation](./phase-4-agentic-discovery/README.md)

---

### Phase 5: Orchestrated Agentic System

**Status**: ✅ Complete
**Location**: [`phase-5-orchestrated-agentic/`](./phase-5-orchestrated-agentic/)

SLM orchestrator trained on Phase 4 discovery data:

**Approach**:
- **Orchestrator Model**: Fine-tuned SLM (Qwen2.5 7B or Phi-4)
- **Training Data**: Generated from Phase 4 A2A call logs
- **Routing Strategy**: Learned from actual agent interactions, not rule-based
- **Workflow Patterns**: Extracted from 90-day discovery

**Why This Works**:
- Orchestrator learns from **actual usage patterns**, not theoretical designs
- Routing decisions based on **what worked**, not assumptions
- Agent performance profiles captured from **real data**
- Error modes and recovery strategies **discovered**, not designed

**Programs**:
```bash
cd phase-5-orchestrated-agentic

# Import Phase 4 discovery data
python -m src.program1_import_discovery.main

# Prepare orchestrator training data
python -m src.program2_orchestrator_training.main

# Fine-tune orchestrator
python -m src.program3_finetune_orchestrator.main

# Deploy orchestrated system
python -m src.program4_deploy.main
```

[📄 Phase 5 Documentation](./phase-5-orchestrated-agentic/README.md)

---

## Quick Start

### Prerequisites

- **Python 3.10+** (tested on 3.11, 3.12)
- **Git** for cloning
- **Docker** (optional, for ChromaDB in Phase 1)
- **CUDA GPU** (optional, for faster training in Phases 2-5)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/emergent-enterprise-ai.git
cd emergent-enterprise-ai

# Each phase is self-contained
cd phase-1-embed-space
pip install -e .
```

### Test Mode Quick Tour

Run all phases in test mode (mock data, no external dependencies):

```bash
# Phase 1: Unified Embedding Space
cd phase-1-embed-space
python -m src.program1_dataset_generator.main --test-mode
python -m src.program2_fine_tuning.main --epochs 1 --test-mode
python -m src.program3_ingestion.main --test-mode
python -m src.program4_search.main --test-mode
# Open http://localhost:7860

# Phase 3: MoE Models (skip Phase 2 notebook for test mode)
cd ../phase-3-moe-experts
python -m src.program1_import.main --test-mode
python -m src.program2_config_gen.main --test-mode
python -m src.program3_merge.main --test-mode
python -m src.program5_export.main --test-mode

# Phase 4: A2A Discovery
cd ../phase-4-agentic-discovery
phase4-agent-services --start-all --test-mode  # Terminal 1
phase4-discovery --run --test-mode             # Terminal 2
phase4-analyze --full-pipeline

# Phase 5: Orchestrator
cd ../phase-5-orchestrated-agentic
python -m src.program1_import_discovery.main --test-mode
python -m src.program2_orchestrator_training.main --test-mode
```

---

## Use Case: Funder Intelligence System

This framework is demonstrated through a **funder intelligence system** for international development organizations.

### Organizational Units

**1. Fundraising Unit**
- Track individual funder portfolios, interests, and capacity
- Profile investors for funding opportunities
- Assess investor-opportunity fit

**2. Business Development Unit**
- Monitor RFPs (Requests for Proposals)
- Track competitive landscape
- Optimize positioning strategy

**3. Field Operations Unit**
- Local market intelligence
- Project performance tracking
- Risk and impact assessment

### How The Phases Apply

| Phase | What It Enables |
|-------|----------------|
| **Phase 0** | Shared data tracking and model registry across all units |
| **Phase 1** | Cross-database semantic search (investors, RFPs, project data) |
| **Phase 2** | Each unit fine-tunes 3-5 SLMs for their specific workflows |
| **Phase 3** | Each unit gets a unified MoE agent combining their capabilities |
| **Phase 4** | Agents discover collaboration patterns (e.g., Country Office ← Angel Investors ← Competitive Funders) |
| **Phase 5** | Orchestrator learns to route complex queries across units optimally |

### Example Workflow

**Query**: *"Which investors should we approach for a climate adaptation project in Bangladesh?"*

**Phase 5 Orchestrator**:
1. Routes to **Field Operations Agent** (depth 1)
   - Provides: Bangladesh market context, project risks, local partners
2. Field Operations calls **Fundraising Agent** (depth 2)
   - Provides: Climate-focused investors, portfolio fit analysis
3. Fundraising calls **Business Development Agent** (depth 3)
   - Provides: Similar successful proposals, positioning strategy

**Result**: Comprehensive recommendation combining local intelligence, investor profiling, and competitive insights.

---

## Key Technologies

### Fine-Tuning & Training
- **Unsloth**: Fast LoRA fine-tuning for LLMs (Phases 2, 4, 5)
- **Sentence-Transformers**: Embedding model training (Phase 1)
- **mergekit**: MoE model merging (Phase 3)
- **LoRA/QLoRA**: Parameter-efficient fine-tuning

### Infrastructure
- **ChromaDB**: Vector database for embeddings
- **PostgreSQL**: Source databases (with asyncpg)
- **FastAPI**: Agent services (Phase 4)
- **Pydantic**: Configuration and data validation

### Models
- **Llama 3.1 8B**: Base model for task SLMs and MoE
- **all-MiniLM-L6-v2**: Base embedding model
- **Qwen2.5 7B / Phi-4**: Orchestrator models (Phase 5)

### MLOps
- **Pydantic Settings**: Configuration management
- **structlog**: Structured logging
- **File-based registries**: Dataset/model tracking (Phase 0)
- **JSON schemas**: Standardized evaluation metrics

---

## Project Structure

```
emergent-enterprise-ai/
├── README.md                          # This file
├── CLAUDE.md                          # Guidance for Claude Code
├── enterprise_ai_habitat.ipynb       # Philosophy deep dive
│
├── docs/                              # Additional documentation
│   ├── diagrams/                      # Architecture diagrams
│   └── visuals/                       # Visualizations
│
├── phase-0-infrastructure/            # Shared registries & logging
│   ├── registries/                    # DataRegistry, ModelRegistry, ExperimentTracker
│   ├── logging/                       # Structured logging
│   ├── evaluation/                    # Metrics schemas
│   └── README.md
│
├── phase-1-embed-space/               # Unified embeddings
│   ├── src/
│   │   ├── program1_dataset_generator/
│   │   ├── program2_fine_tuning/
│   │   ├── program3_ingestion/
│   │   └── program4_search/
│   └── README.md
│
├── phase-2-task-slms/                 # Task-specific SLMs
│   ├── Fine_Tune_Llama_3_1_8B_with_Unsloth.ipynb
│   └── README.md
│
├── phase-3-moe-experts/               # MoE model merging
│   ├── src/
│   │   ├── program1_import/
│   │   ├── program2_config_gen/
│   │   ├── program3_merge/
│   │   └── program5_export/
│   └── README.md
│
├── phase-4-agentic-discovery/         # A2A protocol & discovery
│   ├── src/
│   │   ├── program1_a2a_finetuning/
│   │   ├── program2_agent_services/
│   │   ├── program3_discovery_pipeline/
│   │   └── program4_adaptive_analyzer/
│   └── README.md
│
└── phase-5-orchestrated-agentic/      # Orchestrator training
    ├── src/
    │   ├── program1_import_discovery/
    │   ├── program2_orchestrator_training/
    │   ├── program3_finetune_orchestrator/
    │   └── program4_deploy/
    └── README.md
```

---

## Documentation

### Core Documentation
- **[CLAUDE.md](./CLAUDE.md)**: Instructions for Claude Code when working with this repository
- **[enterprise_ai_habitat.ipynb](./enterprise_ai_habitat.ipynb)**: Deep dive into the Habitat philosophy

### Phase-Specific Docs
- **[Phase 0 README](./phase-0-infrastructure/README.md)**: Infrastructure foundation
- **[Phase 1 README](./phase-1-embed-space/README.md)**: Unified embedding space
- **[Phase 2 README](./phase-2-task-slms/README.md)**: Task-specific SLMs
- **[Phase 3 README](./phase-3-moe-experts/README.md)**: MoE model merging
- **[Phase 4 README](./phase-4-agentic-discovery/README.md)**: A2A protocol & discovery
- **[Phase 5 README](./phase-5-orchestrated-agentic/README.md)**: Orchestrator training

### Additional Resources
- **Phase 0**: [PHASE0_INTEGRATION.md](./phase-0-infrastructure/README.md) - Integration guide
- **Phase 2**: [EVALUATION_SCHEMA_UPDATE.md](./phase-2-task-slms/EVALUATION_SCHEMA_UPDATE.md) - Metrics update
- **Phase 4**: [IMPLEMENTATION_CHECKLIST.md](./phase-4-agentic-discovery/IMPLEMENTATION_CHECKLIST.md) - Implementation guide

---

## Contributing

We welcome contributions! This is a research framework, and we're interested in:

1. **Extensions**: Applying the framework to new domains
2. **Improvements**: Better implementations of individual phases
3. **Experiments**: Testing alternative architectures or approaches
4. **Documentation**: Clarifying concepts or adding examples

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-improvement`)
3. Make your changes with clear commit messages
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Each phase is self-contained - changes should not break other phases
- Maintain test mode functionality for CI/CD
- Update documentation when adding features
- Follow the existing code style (Black formatting, Ruff linting)
- Use structured logging (`structlog`)
- Register datasets/models in Phase 0 registries

---

## License

[Specify your license here - e.g., MIT, Apache 2.0, etc.]

---

## Citation

If you use this framework in your research or projects, please cite:

```bibtex
@software{enterprise_ai_habitat,
  title = {Enterprise AI Habitat: Bottom-Up Emergence Framework},
  author = {[Your Name/Organization]},
  year = {2024},
  description = {A 5-phase framework for building enterprise AI systems through bottom-up emergence},
  url = {https://github.com/yourusername/emergent-enterprise-ai}
}
```

---

## Acknowledgments

This framework builds on research in:
- **Mixture-of-Experts architectures** (Mixtral, Switch Transformers)
- **Agent-to-Agent protocols** (Multi-agent systems research)
- **Parameter-efficient fine-tuning** (LoRA, QLoRA)
- **Embedding fine-tuning** (Sentence-Transformers)
- **Enterprise AI transformation** (Habitat thinking, bottom-up emergence)

Special thanks to the open-source communities behind:
- Hugging Face Transformers
- Unsloth
- mergekit
- ChromaDB
- Sentence-Transformers

---

## Support

For questions, issues, or discussions:
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/emergent-enterprise-ai/issues)
- **Documentation**: See phase-specific READMEs
- **Philosophy**: Read [`enterprise_ai_habitat.ipynb`](./enterprise_ai_habitat.ipynb)

---

**Enterprise AI Habitat** | Version 1.0.0 | Building Intelligence from the Bottom Up
