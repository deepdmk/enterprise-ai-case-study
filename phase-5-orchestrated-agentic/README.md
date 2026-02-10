# Phase 5: Orchestrated Agentic

Transform 90-day A2A discovery logs from Phase 4 into an intelligent SLM-based orchestrator through fine-tuning. The orchestrator learns routing decisions from production data rather than using hardcoded rules.

## Overview

**Base Model**: Qwen2.5 7B or Phi-4 (14B)
**Training**: LoRA fine-tuning (r=16, lora_alpha=32)
**Target**: 150ms inference, 94% accuracy on known workflows

Phase 5 takes the discovery data from Phase 4's 90-day agent-to-agent collaboration experiment and uses it to train a small language model (SLM) that can intelligently route queries to the appropriate agents with optimal cascade depth.

## Architecture

### Programs

1. **Program 1: Data Conversion** - Convert Phase 4 discovery logs to training format
2. **Program 2: SLM Fine-tuning** - LoRA fine-tune orchestrator model
3. **Program 3: Inference Server** - Deploy model via vLLM or TGI
4. **Program 4: Orchestrator Service** - FastAPI service wrapping the orchestrator

### Key Components

- **Routing Engine**: SLM-based routing logic with fallback to rule-based routing
- **Agent Client**: A2A protocol client for Phase 4 agents
- **Response Synthesizer**: Combines multi-agent responses
- **Phase 4 Importer**: Imports training data from Phase 4 exports

## Quick Start

### Test Mode (No GPU Required)

```bash
# Install package
pip install -e .

# 1. Generate mock training data
phase5-convert --full-pipeline --test-mode

# 2. Create mock fine-tuned model
phase5-finetune --full-pipeline --test-mode

# 3. Start mock inference server (Terminal 1)
phase5-inference --start --test-mode

# 4. Start orchestrator service (Terminal 2)
phase5-orchestrator --start --test-mode

# 5. Test orchestration
python examples/example_orchestration.py
```

### Production Mode (Requires GPU + Phase 4 Data)

```bash
# 1. Convert Phase 4 data to training format
phase5-convert --full-pipeline

# 2. Fine-tune orchestrator model
phase5-finetune --train --epochs 3

# 3. Evaluate model
phase5-finetune --evaluate

# 4. Export for serving
phase5-finetune --export

# 5. Start vLLM inference server
phase5-inference --start --server vllm

# 6. Start orchestrator service
phase5-orchestrator --start

# 7. Test with Phase 4 agents running
python examples/example_orchestration.py
```

## Installation

```bash
# Clone repository
git clone <repo-url>
cd phase-5-orchestrated-agentic

# Install dependencies
pip install -e .

# For development
pip install -e ".[dev]"
```

## CLI Commands

### Program 1: Data Conversion

```bash
# Import Phase 4 discovery data
phase5-convert --import-phase4

# Generate synthetic intents
phase5-convert --generate-intents

# Augment data
phase5-convert --augment

# Create train/val/test splits
phase5-convert --create-splits

# Run full pipeline
phase5-convert --full-pipeline

# Test mode (100 samples)
phase5-convert --full-pipeline --test-mode
```

### Program 2: SLM Fine-tuning

```bash
# Train model
phase5-finetune --train --epochs 3

# Evaluate model
phase5-finetune --evaluate

# Export for serving
phase5-finetune --export

# Full pipeline
phase5-finetune --full-pipeline

# Test mode (mock training)
phase5-finetune --full-pipeline --test-mode
```

### Program 3: Inference Server

```bash
# Start vLLM server
phase5-inference --start --server vllm

# Start TGI server
phase5-inference --start --server tgi

# Test mode (mock server)
phase5-inference --start --test-mode

# Health check
phase5-inference --health-check

# Test inference
phase5-inference --test-inference --query "Evaluate Kenya project"
```

### Program 4: Orchestrator Service

```bash
# Start orchestrator service
phase5-orchestrator --start

# Test mode (rule-based routing)
phase5-orchestrator --start --test-mode

# Custom port
phase5-orchestrator --start --port 8080

# Launch Gradio UI (test mode - no services required)
python -m src.program4_orchestrator_service.main --ui --test-mode

# Launch Gradio UI (production mode - requires orchestrator service)
python -m src.program4_orchestrator_service.main --ui

# Gradio UI with custom port
python -m src.program4_orchestrator_service.main --ui --ui-port 7863 --test-mode

# Gradio UI with public link
python -m src.program4_orchestrator_service.main --ui --share --test-mode
```

## API Endpoints

### Orchestrator Service (Port 8000)

**Health Check**
```bash
curl http://localhost:8000/health
```

**Get Routing Decision**
```bash
curl -X POST http://localhost:8000/route \
  -H "Content-Type: application/json" \
  -d '{"query": "Evaluate funding opportunity in Kenya"}'
```

**Full Orchestration**
```bash
curl -X POST http://localhost:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"query": "Should we pursue Kenya climate project?", "execute": true}'
```

**Get Statistics**
```bash
curl http://localhost:8000/stats
```

### Interactive Documentation

- **Orchestrator API**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8000/redoc

### Gradio Interface (Port 7862)

The orchestrator includes a Gradio web interface for interactive testing:

```bash
# Test mode (no services required - uses mock responses)
python -m src.program4_orchestrator_service.main --ui --test-mode

# Production mode (requires orchestrator service running on port 8000)
python -m src.program4_orchestrator_service.main --ui
```

**Features:**
- **Query Input**: Enter queries to test routing and orchestration
- **Route Only**: View routing decision without executing agent calls
- **Full Orchestration**: Execute complete flow with agent responses
- **Agent Response Tabs**: View individual responses from Fundraising, Business Development, and Field Operations agents
- **Performance Metrics**: Monitor latency and success rates

**Test Mode Keywords:**
- `investor`, `portfolio`, `Gates` → Routes to Fundraising agent
- `rfp`, `proposal`, `competitive` → Routes to Business Development agent
- `kenya`, `region`, `project` → Routes to Field Operations agent

Open in browser: http://localhost:7862

## Configuration

Edit `config/config.yaml` to customize:

- Model selection (Qwen2.5 7B vs Phi-4)
- LoRA parameters
- Training hyperparameters
- Inference server settings
- Agent registry URLs
- Path configurations

## Data Formats

### Phase 4 Training Example

```json
{
  "query": "What is the investment capacity of INV-123?",
  "entry_agent": "angel-investors-agent",
  "optimal_depth": 2,
  "call_sequence": [...],
  "final_response": "Successfully processed...",
  "metadata": {"workflow_id": "...", "success": true}
}
```

### ChatML Training Format

```json
{
  "messages": [
    {"role": "system", "content": "You are an intelligent orchestrator..."},
    {"role": "user", "content": "Query: Should we pursue Kenya climate project?"},
    {"role": "assistant", "content": "Entry agent: country-office-agent\nOptimal depth: 3\n..."}
  ]
}
```

### Routing Decision Output

```json
{
  "workflow": "evaluate_funding_opportunity",
  "entry_agent": "country-office-agent",
  "optimal_depth": 3,
  "agent_calls": [...],
  "reasoning": "User wants to evaluate funding opportunity...",
  "estimated_latency_ms": 420,
  "success_probability": 0.98
}
```

## Integration with Phase 0 Infrastructure

Phase 5 integrates with [Phase 0 Infrastructure](../phase-0-infrastructure) for:
- **DataRegistry**: Automatically registers converted training datasets
- **ModelRegistry**: Automatically registers fine-tuned orchestrator models
- **ExperimentTracker**: Logs fine-tuning experiments with full metrics

See [PHASE0_INTEGRATION.md](PHASE0_INTEGRATION.md) for complete details.

### Automatic Tracking

```bash
# Data conversion automatically registers dataset
phase5-convert --full-pipeline

# Fine-tuning automatically logs experiment and registers model
phase5-finetune --full-pipeline
```

**Registered Assets:**
- Dataset: `phase-5/orchestrator/converted/v1`
- Model: `phase-5/orchestrator/qwen2.5-7b/v1`
- Experiment: `phase-5/orchestrator/fine-tuning/v1`

### Graceful Degradation

Phase 5 works without Phase 0 (warnings logged, functionality intact).

## Integration with Phase 4

The orchestrator integrates with Phase 4 agents via the A2A protocol:

1. **Agent Registry**: Configure agent URLs in `config/config.yaml`
2. **A2A Protocol**: Uses Phase 4's agent-to-agent communication protocol
3. **Training Data**: Imports discovery logs from Phase 4 exports

### Phase 4 Agents

Ensure these agents are running for full orchestration:

```bash
# Terminal 1: Fundraising Agent
cd ../phase-4-agentic-discovery
uvicorn a2a_protocol_implementation:fundraising_app --port 8001

# Terminal 2: Business Development Agent
uvicorn a2a_protocol_implementation:business_development_app --port 8002

# Terminal 3: Field Operations Agent
uvicorn a2a_protocol_implementation:field_operations_app --port 8003
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_all.py::TestDataConversion -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Examples

See `examples/` directory for detailed examples:

- `example_data_conversion.py` - Data pipeline demo
- `example_inference.py` - Inference server usage
- `example_orchestration.py` - Full orchestration demo

## Development

```bash
# Format code
black src/ tests/ examples/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## Performance Targets

| Metric | Target | Test Mode |
|--------|--------|-----------|
| Inference Latency | <150ms | ~100ms |
| Routing Accuracy | >94% | ~80% (rule-based) |
| Agent Call Latency | <500ms | N/A |
| Total Orchestration | <1000ms | N/A |

## Directory Structure

```
phase-5-orchestrated-agentic/
├── config/                  # Configuration
├── src/
│   ├── shared/              # Shared utilities
│   ├── program1_data_conversion/
│   ├── program2_slm_finetuning/
│   ├── program3_inference_server/
│   └── program4_orchestrator_service/
│       ├── gradio_app.py        # Gradio web interface
│       └── mock_orchestrator.py # Mock client for test mode
├── tests/                   # Test suite
├── examples/                # Example scripts
├── notebooks/               # Jupyter notebooks
├── data/                    # Data storage
│   ├── phase4_imports/
│   ├── training/
│   ├── models/
│   ├── checkpoints/
│   └── exports/
└── scripts/                 # Utility scripts
```

## Troubleshooting

### Model not found
```bash
# Ensure you've run fine-tuning and export
phase5-finetune --full-pipeline --test-mode
```

### Phase 4 data not found
```bash
# Set Phase 4 path in config.yaml or export Phase 4 data
cd ../phase-4-agentic-discovery
python -m src.program4_adaptive_analyzer.main --export
```

### Inference server connection error
```bash
# Ensure inference server is running
phase5-inference --start --test-mode
```

### Agent connection error
```bash
# Check agent URLs in config/config.yaml
# Ensure Phase 4 agents are running
```

## Next Steps

After completing Phase 5:

1. **Deploy to Production**: Use TGI for production deployment
2. **Monitor Performance**: Track routing accuracy and latency
3. **Continuous Improvement**: Retrain with new discovery data
4. **Scale**: Add more agents to the registry
5. **Optimize**: Fine-tune for specific workflows

## Resources

- **Phase 4 Repository**: `../phase-4-agentic-discovery`
- **Strategy Notebook**: `notebooks/slm_orchestrator_finetuning.ipynb`
- **Configuration**: `config/config.yaml`
- **API Docs**: http://localhost:8000/docs
- **Gradio Interface**: http://localhost:7862 (when running with `--ui`)

## License

MIT
