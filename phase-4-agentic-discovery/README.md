# Phase 4: Agentic Discovery

**A2A Protocol Implementation & Adaptive Depth Optimization**

This phase implements the critical missing component from Phase 3: **A2A (Agent-to-Agent) fine-tuning** that enables MoE models to make protocol-aware agent calls. It also runs a 90-day discovery experiment to determine optimal cascade depths per workflow.

## Overview

### The Key Gap

Phase 3 MoE models are trained for domain-specific tasks but **NOT** for:
1. Recognizing when to call other agents
2. Generating A2A protocol calls
3. Handling/parsing A2A responses
4. Understanding depth limits

Phase 4 solves this through:
- **Program 1**: A2A fine-tuning (adds protocol capabilities via LoRA)
- **Program 2**: Agent services (FastAPI services with A2A protocol)
- **Program 3**: Discovery pipeline (90-day adaptive depth experiment)
- **Program 4**: Adaptive analyzer (determines optimal depths, exports Phase 5 data)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 4 Components                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Program 1  │  │   Program 2  │  │   Program 3  │      │
│  │ A2A Fine-    │→ │    Agent     │→ │  Discovery   │      │
│  │   Tuning     │  │   Services   │  │   Pipeline   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                  ↓                  ↓              │
│         └──────────────────┴──────────────────┘              │
│                            ↓                                 │
│                   ┌──────────────┐                           │
│                   │   Program 4  │                           │
│                   │   Adaptive   │                           │
│                   │   Analyzer   │                           │
│                   └──────────────┘                           │
│                            ↓                                 │
│                   Phase 5 Training Data                      │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
phase-4-agentic-discovery/
├── config/
│   ├── settings.py              # Pydantic settings
│   └── config.yaml              # Main configuration
├── src/
│   ├── shared/                  # Shared utilities
│   │   ├── a2a_protocol.py      # A2A protocol dataclasses
│   │   ├── discovery_backend.py # Agent discovery (ChromaDB)
│   │   ├── call_logger.py       # Call logging for discovery
│   │   └── moe_loader.py        # Load Phase 3 models
│   ├── program1_a2a_finetuning/ # A2A protocol fine-tuning
│   ├── program2_agent_services/ # FastAPI agent services
│   ├── program3_discovery_pipeline/ # 90-day experiment
│   └── program4_adaptive_analyzer/  # Analysis & Phase 5 export
├── data/
│   ├── training/                # A2A training datasets
│   ├── logs/                    # Discovery call logs
│   ├── models/                  # A2A adapters
│   └── exports/                 # Phase 5 training data
├── tests/
├── pyproject.toml
└── README.md
```

## Installation

### Prerequisites

- Python 3.9+
- Phase 3 MoE models (optional, can use test mode)
- CUDA-capable GPU (optional, CPU/MPS supported)

### Setup

```bash
# Navigate to project directory
cd phase-4-agentic-discovery

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package and dependencies
pip install -e .

# Or with development tools
pip install -e ".[dev]"
```

### Configuration

Edit `config/config.yaml` to customize:
- A2A protocol settings (max depth, timeouts)
- Fine-tuning hyperparameters
- Agent service ports
- Discovery pipeline parameters

## Usage

### Program 1: A2A Fine-Tuning

Fine-tune Phase 3 MoE models to add A2A protocol capabilities.

```bash
# Full pipeline (generate data, train, validate)
phase4-a2a-finetune --full-pipeline --unit fundraising --test-mode

# Or individual steps:

# 1. Generate training data
phase4-a2a-finetune --generate-data --unit fundraising --num-examples 1000

# 2. Train A2A adapter
phase4-a2a-finetune --train --unit fundraising

# 3. Validate adapter
phase4-a2a-finetune --validate --unit fundraising
```

**Available units:**
- `fundraising`
- `business_development`
- `field_operations`

**Output:**
- Training data: `data/training/{unit}/a2a_training.jsonl`
- A2A adapter: `data/models/a2a_adapters/{unit}/`

### Program 2: Agent Services

Start FastAPI services for A2A agents.

```bash
# Start all agents
phase4-agent-services --start-all --test-mode

# Start specific agent
phase4-agent-services --start fundraising-agent --port 8001 --test-mode

# List available agents
phase4-agent-services --list
```

**Endpoints (per agent):**
- `GET /health` - Health check
- `GET /capability` - Agent capability info
- `POST /a2a` - A2A protocol endpoint
- `POST /query` - Simple query endpoint

**Test an agent:**
```bash
# Health check
curl http://localhost:8001/health

# A2A call
curl -X POST http://localhost:8001/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Profile investor INV-123",
    "target": "fundraising-agent",
    "parameters": {}
  }'
```

### Program 3: Discovery Pipeline

Run the 90-day adaptive depth discovery experiment.

```bash
# Show schedule
phase4-discovery --show-schedule

# Show workflows
phase4-discovery --show-workflows

# Run test (7 days instead of 90)
phase4-discovery --run --test-mode

# Run full experiment (requires agent services running)
phase4-discovery --run

# Analyze specific phase
phase4-discovery --analyze-phase 3
```

**7-Phase Schedule:**

| Phase | Days | Depth | Purpose |
|-------|------|-------|---------|
| 1 | 1-7 | 1 | Baseline (no cascading) |
| 2 | 8-21 | 2 | Single cascade |
| 3 | 22-35 | 3 | Two-level cascade |
| 4 | 36-49 | 2 | Control #1 |
| 5 | 50-63 | 4 | Outer bounds |
| 6 | 64-75 | 2 | Control #2 |
| 7 | 76-90 | adaptive | Per-workflow optimization |

**Output:**
- Call logs: `data/logs/discovery/phase_{N}.jsonl`
- Results: `data/logs/discovery/all_results.json`

### Program 4: Adaptive Analyzer

Analyze discovery results and export Phase 5 training data.

```bash
# Quick summary
phase4-analyze --summary

# Full analysis
phase4-analyze --analyze

# Export for Phase 5
phase4-analyze --export-phase5

# Full pipeline (analyze + export)
phase4-analyze --full-pipeline
```

**Output:**
- Analysis: `data/exports/analysis_results.json`
- Phase 5 training: `data/exports/orchestrator_chat.jsonl`
- Summary: `data/exports/phase5_summary.json`

## Complete Workflow

Here's the recommended end-to-end workflow:

```bash
# 1. Fine-tune all units for A2A (test mode)
for unit in fundraising business_development field_operations; do
  phase4-a2a-finetune --full-pipeline --unit $unit --test-mode
done

# 2. Start agent services (in separate terminal)
phase4-agent-services --start-all --test-mode

# 3. Run discovery pipeline (test mode: 7 days)
phase4-discovery --run --test-mode

# 4. Analyze and export for Phase 5
phase4-analyze --full-pipeline
```

## Test Mode

All programs support `--test-mode`:
- **Program 1**: Mock training (fast, no GPU needed)
- **Program 2**: Mock models (no Phase 3 models needed)
- **Program 3**: 7 days instead of 90
- **Program 4**: Works with test data

Use test mode for:
- Development and testing
- CI/CD pipelines
- Validating integration

## Integration with Other Phases

### Phase 0 (Infrastructure)
- Uses `DataRegistry` for datasets
- Uses `ModelRegistry` for A2A adapters
- Uses `ExperimentTracker` for fine-tuning

### Phase 1 (Embeddings)
- Imports `ChromaDBClient` for agent discovery
- Uses fine-tuned embedding model

### Phase 3 (MoE)
- Loads models from `phase-3-moe-experts/data/exports/phase4/`
- Applies A2A LoRA adapter on top

### Phase 5 (Orchestrators)
- Exports training data: `orchestrator_chat.jsonl`
- Optimal depths per workflow
- Phase 5 recommendations

## Key Concepts

### A2A Protocol

The A2A (Agent-to-Agent) protocol enables agents to call each other:

```python
# A2A Request
{
  "goal": "What you need from the agent",
  "target": "agent-id",
  "parameters": {},
  "metadata": {
    "call_depth": 1,
    "max_depth": 3,
    ...
  }
}

# A2A Response
{
  "status": "success",
  "content": "Response content",
  "cascaded_calls": ["other-agent"],
  "execution_time_ms": 245.3
}
```

### Cascade Depth

Cascade depth controls how many levels of agent calls are allowed:

- **Depth 1**: No cascading (agent responds directly)
- **Depth 2**: One level (agent can call one other agent)
- **Depth 3**: Two levels (agent → agent → agent)
- **Depth 4**: Three levels (maximum explored)

### Adaptive Depth

Phase 7 of discovery uses **adaptive depth**:
- Different workflows have different optimal depths
- Simple queries: depth 1
- Complex queries: depth 2-3
- Orchestrator decides based on query complexity

## Troubleshooting

### Common Issues

**"Agent services not responding"**
- Ensure agent services are running: `phase4-agent-services --start-all --test-mode`
- Check ports are not in use: `lsof -i :8001-8003`

**"Phase 3 models not found"**
- Use `--test-mode` to run with mock models
- Or set `paths.phase3_path` in `config.yaml`

**"Out of memory during fine-tuning"**
- Reduce `batch_size` in config
- Use gradient checkpointing
- Use smaller model or CPU

**"Discovery pipeline has no logs"**
- Ensure you ran the pipeline first
- Check `data/logs/discovery/` directory exists

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_a2a_protocol.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff src/ tests/

# Type check
mypy src/
```

## Performance

### Benchmarks (Test Mode)

- **A2A Fine-tuning**: ~2 minutes per unit (mock)
- **Agent Services**: <1s startup
- **Discovery Pipeline**: ~5 minutes (7 days, 70 queries)
- **Adaptive Analyzer**: <1 minute

### Production Scale

- **A2A Fine-tuning**: ~30 minutes per unit (GPU)
- **Discovery Pipeline**: 90 days continuous (can be parallelized)
- **Total queries**: 900 (90 days × 10/day)

## Citation

If you use this work, please cite:

```bibtex
@software{phase4_agentic_discovery,
  title = {Phase 4: Agentic Discovery with A2A Protocol},
  author = {Your Organization},
  year = {2024},
  description = {A2A protocol fine-tuning and adaptive depth optimization for multi-agent systems}
}
```

## License

[Your License]

## Support

For issues and questions:
- GitHub Issues: [Your Repo]
- Documentation: [Your Docs]
- Contact: [Your Contact]
