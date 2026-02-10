# Phase 2: Task-Specific SLMs

Fine-tune Llama 3.1 8B using Unsloth + LoRA for specific organizational tasks. Each of 3 units (Fundraising, Field Operations, Business Development) gets specialized Task SLMs that feed into Phase 3 MoE merging.

## Overview

This phase creates 14 specialized Task SLMs:

| Unit | Tasks |
|------|-------|
| **Fundraising** | investor_profiling, fit_assessment, capacity_analysis, engagement_strategy, portfolio_synthesis |
| **Field Operations** | market_assessment, project_performance, capacity_mapping, demand_forecasting |
| **Business Development** | rfp_analysis, competitive_positioning, proposal_drafting, win_probability, funder_priorities |

## Technology Stack

- **Fine-tuning**: Unsloth + LoRA (Linux/CUDA) or HuggingFace PEFT (fallback)
- **Base Model**: `unsloth/Meta-Llama-3.1-8B-bnb-4bit`
- **Training**: SFTTrainer with ChatML format
- **RLHF**: Gradio preference collection for future DPO

**Environment Note**: Unsloth requires Linux + CUDA. Mac MPS falls back to slower HF+PEFT.

## Quick Start

### 1. Install Dependencies

```bash
pip install -e .
```

For Colab/GPU environments:
```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

### 2. Test Mode Pipeline

> **Warning**: Test mode generates **synthetic mock data** for pipeline verification only. Models trained on mock data will not perform well on real tasks. Always use real domain data for production training (see Section 3).

```bash
# Generate mock training data
python -m src.program1_data_preparation.main --test-mode --unit fundraising

# Fine-tune (1 epoch with mock data)
python -m src.program2_fine_tuning.main --test-mode --unit fundraising --task investor_profiling

# Evaluate
python -m src.program3_evaluation.main --test-mode --unit fundraising --task investor_profiling

# Register model
python -m src.program4_model_registry.main scan

# View registry
python -m src.program4_model_registry.main summary
```

### 3. Production Pipeline

Production training requires **real domain data**. The quality of your Task SLMs depends entirely on the quality and quantity of your training examples.

**Data requirements:**
- 200-500 examples per task (minimum 100)
- Format: JSONL with `input` and `output` fields
- Place files in `data/raw/{unit}/{task}/`

```bash
# Prepare real data (place in data/raw/{unit}/{task}/)
python -m src.program1_data_preparation.main --unit fundraising

# Fine-tune with full settings
python -m src.program2_fine_tuning.main --unit fundraising --task investor_profiling

# Evaluate trained model
python -m src.program3_evaluation.main --unit fundraising --task investor_profiling

# Export for Phase 3 MoE
python -m src.program4_model_registry.main export --output-dir exports/ --merge
```

## Project Structure

```
phase-2-task-slms/
├── config/
│   ├── config.yaml                    # Main configuration
│   ├── settings.py                    # Pydantic settings
│   └── tasks/                         # Task definitions per unit
│       ├── fundraising.yaml
│       ├── field_operations.yaml
│       └── business_development.yaml
├── src/
│   ├── shared/
│   │   ├── model_loader.py            # Unsloth/HF abstraction
│   │   ├── data_formatter.py          # ChatML formatting
│   │   ├── mock_data_generator.py     # Synthetic data for test mode
│   │   ├── model_registry.py          # Track models for Phase 3
│   │   ├── embedding_bridge.py        # Phase 1 integration (RAG)
│   │   └── environment_detector.py    # Detect Colab/CUDA/MPS
│   ├── program1_data_preparation/     # Collect & format training data
│   ├── program2_fine_tuning/          # Unsloth LoRA training
│   ├── program3_evaluation/           # Model evaluation
│   ├── program4_model_registry/       # Registry for Phase 3
│   └── program5_rlhf_collection/      # Preference signals (future)
├── notebooks/
│   └── Fine_Tune_Task_SLM.ipynb       # Colab training notebook
├── data/                              # gitignored
│   ├── raw/                           # Raw data per unit
│   ├── processed/                     # Formatted JSONL
│   ├── models/                        # Trained LoRA adapters
│   ├── evaluations/                   # Eval reports
│   └── registry/                      # Model registry
└── tests/
```

## Programs

### Program 1: Data Preparation

Collects and formats training data for each task.

```bash
# All units
python -m src.program1_data_preparation.main

# Specific unit
python -m src.program1_data_preparation.main --unit fundraising

# Specific task
python -m src.program1_data_preparation.main --unit fundraising --task investor_profiling

# Test mode (generates mock data)
python -m src.program1_data_preparation.main --test-mode --unit fundraising
```

**Input**: Raw data in `data/raw/{unit}/{task}/` (CSV, JSON, JSONL)

**Output**: Formatted JSONL in `data/processed/{unit}/{task}/train.jsonl`

### Program 2: Fine-Tuning

Trains LoRA adapters using Unsloth (GPU) or HF+PEFT (fallback).

```bash
# Train specific task
python -m src.program2_fine_tuning.main --unit fundraising --task investor_profiling

# Force specific backend
python -m src.program2_fine_tuning.main --unit fundraising --task investor_profiling --backend transformers

# Test mode (1 epoch, small batch)
python -m src.program2_fine_tuning.main --test-mode --unit fundraising --task investor_profiling

# Show environment info
python -m src.program2_fine_tuning.main --show-env
```

**Output**: LoRA adapter in `data/models/{unit}/{task}_v1/`

### Program 3: Evaluation

Evaluates trained models on format compliance, content coverage, and latency.

```bash
# Evaluate latest model
python -m src.program3_evaluation.main --unit fundraising --task investor_profiling

# Specify adapter path
python -m src.program3_evaluation.main --unit fundraising --task investor_profiling \
    --adapter-path data/models/fundraising/investor_profiling_v1

# Limit samples
python -m src.program3_evaluation.main --unit fundraising --task investor_profiling --num-samples 10
```

**Output**: Reports in `data/evaluations/{unit}/{task}_v1/`

### Program 4: Model Registry

Tracks trained models and exports for Phase 3 MoE merging.

```bash
# Scan and register new models
python -m src.program4_model_registry.main scan

# List registered models
python -m src.program4_model_registry.main list
python -m src.program4_model_registry.main list --unit fundraising

# Show summary
python -m src.program4_model_registry.main summary

# Export for Phase 3
python -m src.program4_model_registry.main export --output-dir exports/
python -m src.program4_model_registry.main export --output-dir exports/ --unit fundraising --merge
```

**Output**: `data/registry/model_registry.json` and exports for MoE

## Configuration

### LoRA Config (matches Phase 3 expectations)

```yaml
lora:
  r: 16
  lora_alpha: 16
  lora_dropout: 0
  target_modules: [q_proj, k_proj, v_proj, o_proj, up_proj, down_proj, gate_proj]
  use_rslora: true
```

### Training Defaults

```yaml
training:
  epochs: 3
  batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 3.0e-4
  warmup_steps: 10
```

### Task Definition Format

```yaml
unit:
  id: "fundraising"
  name: "Fundraising Intelligence Unit"

tasks:
  - id: "investor_profiling"
    name: "Investor Profiling"
    system_prompt: "You are an expert analyst..."
    positive_prompts: ["Profile this investor", "Create investor profile"]
    negative_prompts: ["Analyze RFP", "Assess market"]
    examples_required: 300
    required_sections: ["Investment Thesis", "Preferences"]
```

## Colab Training

For GPU training in Google Colab:

1. Open `notebooks/Fine_Tune_Task_SLM.ipynb` in Colab
2. Set `UNIT_ID` and `TASK_ID` in the configuration cell
3. Run all cells
4. Download the trained adapter

## Integration with Phase 1 (Embedding Bridge)

Optionally augment training inputs with RAG context from Phase 1:

```python
from src.shared.embedding_bridge import EmbeddingBridge

bridge = EmbeddingBridge("../phase-1-embed-space/config/config.yaml")
augmented_prompt = bridge.augment_prompt(input_text, k=3)
```

## Integration with Phase 3 (MoE Export)

Export trained adapters for Phase 3 Mixture-of-Experts merging:

```python
from src.shared.model_registry import ModelRegistry
from src.program4_model_registry.exporter import ModelExporter

registry = ModelRegistry("data/registry")
exporter = ModelExporter(registry, settings)

# Export all models for MoE
exporter.export_for_moe("exports/", merge_models=True)
```

The export includes:
- Merged model weights (optional)
- Positive/negative prompts for MoE routing
- Training metadata and metrics

## Environment Detection

The system automatically detects the compute environment:

| Environment | Backend | Notes |
|-------------|---------|-------|
| Google Colab + GPU | Unsloth | Fastest training |
| Linux + CUDA | Unsloth | Production training |
| Mac MPS | HF + PEFT | Slower, but works |
| CPU only | HF + PEFT | Very slow, testing only |

Check your environment:
```bash
python -m src.program2_fine_tuning.main --show-env
```

## Data Format

Training data should be in JSONL format with `input` and `output` fields:

```jsonl
{"input": "Profile investor John Smith who focuses on fintech", "output": "## Investment Thesis\n..."}
{"input": "Create a comprehensive profile for Sarah Chen", "output": "## Investment Thesis\n..."}
```

Supported source formats:
- JSONL (`.jsonl`)
- JSON (`.json`)
- CSV (`.csv`)
- ShareGPT format

## Expected Outputs

### After Data Preparation
```
data/processed/fundraising/investor_profiling/
├── train.jsonl       # Training data
├── val.jsonl         # Validation data
└── examples.jsonl    # Raw examples
```

### After Fine-Tuning
```
data/models/fundraising/investor_profiling_v1/
├── adapter_model.safetensors
├── adapter_config.json
└── training_metadata.json
```

### After Evaluation
```
data/evaluations/fundraising/investor_profiling_v1/
├── evaluation_report.json
└── evaluation_report.md
```

### Model Registry
```
data/registry/model_registry.json
```

## Phase 0 Integration

Phase 2 integrates with [Phase 0 Infrastructure](../phase-0-infrastructure) for:
- **DataRegistry**: Track training datasets with full lineage
- **ModelRegistry**: Version control for trained LoRA adapters
- **ExperimentTracker**: Log fine-tuning experiments

For migration details, see:
- [PHASE0_MIGRATION.md](PHASE0_MIGRATION.md) - Migration guide from inline registries
- [EVALUATION_SCHEMA_UPDATE.md](EVALUATION_SCHEMA_UPDATE.md) - Updated metrics schema

## License

MIT
