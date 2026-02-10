# Phase 3: MoE Division Agents

Merge Task SLMs (LoRA adapters) from Phase 2 into **3 separate Mixture-of-Experts models** using mergekit-moe - one MoE per organizational unit.

## Overview

This phase takes the fine-tuned Task SLMs from Phase 2 and merges them into per-unit Mixtral-style MoE models. Each MoE powers one A2A agent in Phase 4's agentic network.

**Key Architecture:**
- **3 separate MoE models**, one per organizational unit:
  - Fundraising MoE (5 experts from 5 task SLMs)
  - Business Development MoE (4 experts from 4 task SLMs)
  - Field Operations MoE (5 experts from 5 task SLMs)
- Mixtral-style architecture with 2-of-N expert selection per token
- Hidden gate mode for semantic routing within each unit
- Pre-computed routing embeddings for fast inference
- Each export package feeds one Phase 4 A2A agent

## Architecture

```
Phase 2 Exports (14 LoRA adapters across 3 units)
         ↓
    [Program 1: Import]
    (Organize by unit)
         ↓
    [Program 2: Config Gen]
    (3 MoE configs)
         ↓
    [Program 3: mergekit-moe]
    (3 separate merges)
         ↓
┌────────────────────┬──────────────────────┬────────────────────┐
│ Fundraising        │ Business Development │ Field Operations   │
│ MoE (5 experts)    │ MoE (4 experts)      │ MoE (5 experts)    │
└────────────────────┴──────────────────────┴────────────────────┘
         ↓                    ↓                     ↓
    [Program 5: Export]
    (3 packages)
         ↓                    ↓                     ↓
┌────────────────────┬──────────────────────┬────────────────────┐
│ Fundraising        │ Business Development │ Field Operations   │
│ A2A Agent          │ A2A Agent            │ A2A Agent          │
└────────────────────┴──────────────────────┴────────────────────┘
                     Phase 4 Agentic Network
```

## Quick Start

### Test Mode (No GPU Required)

```bash
# 1. Generate mock Phase 2 exports for 3 units
python -m src.program1_import.main --test-mode

# 2. Generate 3 MoE configurations
python -m src.program2_config_gen.main --test-mode

# 3. Create 3 mock merged models
python -m src.program3_merge.main --test-mode

# 4. Export 3 packages for Phase 4
python -m src.program5_export.main --test-mode

# 5. Launch staff interface (test mode with mock responses)
python -m src.program6_interface.main --test-mode
```

### Production Mode (GPU Required)

```bash
# 1. Import Phase 2 exports (organized by unit)
python -m src.program1_import.main \
    --phase2-export ../phase-2-task-slms/exports

# 2. Generate MoE configuration for all units
python -m src.program2_config_gen.main

# 3. Execute merge for all units (requires GPU)
python -m src.program3_merge.main --cuda

# 4. Export all units for Phase 4
python -m src.program5_export.main \
    --generate-agent-configs \
    --generate-embeddings
```

### Single Unit Operations

```bash
# Merge specific unit only
python -m src.program3_merge.main --unit fundraising --cuda

# Export specific unit only
python -m src.program5_export.main --unit fundraising
```

## Project Structure

```
phase-3-moe-experts/
├── config/
│   ├── config.yaml                    # Main configuration (units defined)
│   ├── settings.py                    # Pydantic settings
│   └── merge_profiles/
│       ├── per_unit_experts.yaml      # Default per-unit profile
│       └── test_mode.yaml             # Test profile
├── src/
│   ├── shared/
│   │   ├── phase2_importer.py         # Import Phase 2 exports
│   │   ├── config_generator.py        # Generate mergekit configs
│   │   └── model_validator.py         # Validate models
│   ├── program1_import/               # Import & validate by unit
│   ├── program2_config_gen/           # Config generation (3 configs)
│   ├── program3_merge/                # Merge execution (3 merges)
│   ├── program4_finetune/             # Optional fine-tuning
│   ├── program5_export/               # Phase 4 export (3 packages)
│   └── program6_interface/            # Staff Gradio interface
├── data/
│   ├── imports/                       # Imported adapters
│   │   ├── import_manifest.json
│   │   ├── fundraising/
│   │   ├── business_development/
│   │   └── field_operations/
│   ├── configs/                       # Generated configs
│   │   ├── fundraising_moe.yaml
│   │   ├── business_development_moe.yaml
│   │   └── field_operations_moe.yaml
│   ├── merged/                        # Merged models
│   │   ├── fundraising_moe/
│   │   ├── business_development_moe/
│   │   └── field_operations_moe/
│   └── exports/                       # Phase 4 exports
│       └── phase4/
│           ├── fundraising/
│           ├── business_development/
│           └── field_operations/
├── notebooks/
│   └── MoE_Merge_Pipeline.ipynb       # Colab notebook
└── tests/
```

## Programs

### Program 1: Import Phase 2 Exports

Import and validate Task SLM adapters, organizing by unit.

```bash
python -m src.program1_import.main \
    --phase2-export ../phase-2-task-slms/exports

# Validate existing imports
python -m src.program1_import.main --validate-only
```

**Output:**
- `data/imports/import_manifest.json` - Lists all adapters by unit
- `data/imports/{unit_id}/{task_id}/v1/model/` - Adapter files

### Program 2: Generate MoE Configuration

Generate mergekit-moe YAML configuration for each unit.

```bash
python -m src.program2_config_gen.main

# Display existing config
python -m src.program2_config_gen.main --show-config data/configs/fundraising_moe.yaml
```

**Output:**
- `data/configs/fundraising_moe.yaml`
- `data/configs/business_development_moe.yaml`
- `data/configs/field_operations_moe.yaml`
- `data/configs/{unit_id}_routing.json` - Routing configurations

### Program 3: Execute Merge

Run mergekit-moe to create merged models for each unit.

```bash
# Dry run (validate all configs)
python -m src.program3_merge.main --dry-run

# Full merge with CUDA for all units
python -m src.program3_merge.main --cuda

# Merge specific unit only
python -m src.program3_merge.main --unit fundraising --cuda
```

**Output:**
- `data/merged/fundraising_moe/`
- `data/merged/business_development_moe/`
- `data/merged/field_operations_moe/`

### Program 4: Fine-tune MoE (Optional)

Optional LoRA fine-tuning to improve routing within each unit's MoE.

```bash
python -m src.program4_finetune.main \
    --model-path data/merged/fundraising_moe \
    --output-dir data/merged/fundraising_moe_finetuned \
    --epochs 2
```

### Program 5: Export for Phase 4

Export each unit's MoE with routing metadata for its A2A agent.

```bash
# Export all units
python -m src.program5_export.main \
    --generate-agent-configs \
    --generate-embeddings

# Export specific unit
python -m src.program5_export.main --unit fundraising
```

**Export Structure (per unit):**
```
data/exports/phase4/{unit_id}/
├── model/                           # MoE model files
├── routing/
│   ├── expert_registry.json         # Expert ID → task mapping
│   ├── routing_embeddings.npy       # Pre-computed embeddings
│   ├── intent_mapping.json          # Intent → expert IDs
│   └── a2a_routing_config.json      # A2A protocol config
├── agent_config/
│   └── {unit_id}_agent.yaml         # A2A agent configuration
└── export_manifest.json
```

### Program 6: Staff Interface

Gradio-based web interface for staff to interact with MoE models and collect RLHF feedback.

```bash
# Launch in test mode (no GPU required, uses mock responses)
python -m src.program6_interface.main --test-mode

# Launch with production models
python -m src.program6_interface.main

# Custom host/port
python -m src.program6_interface.main --host 0.0.0.0 --port 7861

# Create public sharing link
python -m src.program6_interface.main --share
```

**Features:**
- Query MoE models with natural language
- Select target unit (Fundraising, Business Development, Field Operations)
- View expert routing decisions
- Collect preference feedback for RLHF training
- Response quality ratings

**URL:** http://localhost:7861 (default)

## Configuration

### Main Settings (config/config.yaml)

```yaml
moe:
  architecture: mixtral
  gate_mode: hidden
  dtype: float16
  experts_per_token: 2      # Within each unit's MoE

merge:
  use_cuda: true
  lazy_unpickle: true
  timeout_minutes: 120

# Unit definitions - each becomes a separate MoE
units:
  fundraising:
    name: "Fundraising"
    tasks:
      - investor_profiling
      - funding_opportunity_analysis
      - proposal_evaluation
      - portfolio_matching
      - engagement_recommendation
  business_development:
    name: "Business Development"
    tasks:
      - rfp_analysis
      - competitive_landscape
      - proposal_scoring
      - funding_trends
  field_operations:
    name: "Field Operations"
    tasks:
      - market_intelligence
      - project_performance
      - partner_assessment
      - regulatory_compliance
      - risk_assessment

import_config:
  phase2_export_dir: "../phase-2-task-slms/exports"
```

### Environment Variables

```bash
export HF_TOKEN="your-huggingface-token"
export TEST_MODE=false
export LOG_LEVEL=INFO
```

## Requirements

### Dependencies

```bash
pip install torch transformers peft accelerate
pip install mergekit  # For MoE merging
pip install sentence-transformers  # For routing embeddings
pip install pydantic pydantic-settings pyyaml structlog
```

### Hardware Requirements

- **Test Mode**: CPU only, minimal memory
- **Full Merge**: GPU with 24GB+ VRAM (per unit merge)
- **Disk Space**: ~30GB per unit merged (3 units = ~90GB total)

## Integration Points

### Phase 2 Input

Consumes exports from Phase 2 model registry:
```bash
# Phase 2 export command
python -m src.program4_model_registry.main export --output-dir exports/ --merge
```

Expected structure:
```
phase-2-task-slms/exports/
├── export_manifest.json
├── fundraising/{task}/v1/model/
├── business_development/{task}/v1/model/
└── field_operations/{task}/v1/model/
```

### Phase 4 Output

Provides to Phase 4 A2A agents (one package per agent):
- Merged MoE model with unit-specific experts
- Expert registry mapping task IDs to expert indices
- Routing embeddings for fast intent matching
- Agent configuration YAML file

## Testing

```bash
# Run tests
pytest tests/ -v

# Run test mode pipeline (creates 3 mock MoE models)
python -m src.program1_import.main --test-mode
python -m src.program2_config_gen.main --test-mode
python -m src.program3_merge.main --test-mode
python -m src.program5_export.main --test-mode
```

## Colab Notebook

For GPU-based merging, use the Colab notebook:
- Open `notebooks/MoE_Merge_Pipeline.ipynb`
- Set `TEST_MODE = False` for production
- Requires A100 GPU runtime for full merges

## Troubleshooting

### mergekit-moe not found
```bash
pip install mergekit
```

### Out of memory during merge
- Use `lazy_unpickle: true` in config
- Merge one unit at a time with `--unit {unit_id}`
- Use A100 40GB or larger GPU

### Adapter validation failures
- Check that Phase 2 exports have `adapter_config.json`
- Verify base model compatibility across all adapters in the unit

## License

MIT
