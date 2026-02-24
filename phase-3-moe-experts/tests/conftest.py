"""Shared test fixtures for Phase 3 MoE tests."""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import Settings
from src.shared.phase2_importer import AdapterInfo


@pytest.fixture
def test_settings():
    """Create test settings with test mode enabled."""
    settings = Settings()
    settings.test_mode = True
    return settings


@pytest.fixture
def mock_export_dir():
    """Get path to mock Phase 2 export directory."""
    return Path(__file__).parent / "fixtures" / "mock_phase2_export"


@pytest.fixture
def temp_import_dir(tmp_path):
    """Create temporary import directory."""
    return tmp_path / "imports"


@pytest.fixture
def temp_configs_dir(tmp_path):
    """Create temporary configs directory."""
    return tmp_path / "configs"


@pytest.fixture
def temp_merged_dir(tmp_path):
    """Create temporary merged models directory."""
    return tmp_path / "merged"


@pytest.fixture
def temp_exports_dir(tmp_path):
    """Create temporary exports directory."""
    return tmp_path / "exports"


@pytest.fixture
def mock_adapters():
    """Create mock adapter info objects for all 3 units."""
    base_path = Path("/mock/imports")

    adapters = [
        # Fundraising unit
        AdapterInfo(
            model_id="fundraising_investor_profiling_v1",
            unit_id="fundraising",
            task_id="investor_profiling",
            version="v1",
            source_path=base_path / "fundraising" / "investor_profiling" / "v1" / "model",
            import_path=base_path / "fundraising" / "investor_profiling" / "v1" / "model",
            base_model="HuggingFaceTB/SmolLM-135M",
            positive_prompts=["Profile this investor", "Create investor profile"],
            negative_prompts=["Analyze RFP"],
        ),
        AdapterInfo(
            model_id="fundraising_funding_opportunity_v1",
            unit_id="fundraising",
            task_id="funding_opportunity",
            version="v1",
            source_path=base_path / "fundraising" / "funding_opportunity" / "v1" / "model",
            import_path=base_path / "fundraising" / "funding_opportunity" / "v1" / "model",
            base_model="HuggingFaceTB/SmolLM-135M",
            positive_prompts=["Evaluate funding opportunity"],
            negative_prompts=["Profile investor"],
        ),
        # Business development unit
        AdapterInfo(
            model_id="business_development_rfp_analysis_v1",
            unit_id="business_development",
            task_id="rfp_analysis",
            version="v1",
            source_path=base_path / "business_development" / "rfp_analysis" / "v1" / "model",
            import_path=base_path / "business_development" / "rfp_analysis" / "v1" / "model",
            base_model="HuggingFaceTB/SmolLM-135M",
            positive_prompts=["Analyze this RFP"],
            negative_prompts=["Profile investor"],
        ),
        AdapterInfo(
            model_id="business_development_competitive_landscape_v1",
            unit_id="business_development",
            task_id="competitive_landscape",
            version="v1",
            source_path=base_path / "business_development" / "competitive_landscape" / "v1" / "model",
            import_path=base_path / "business_development" / "competitive_landscape" / "v1" / "model",
            base_model="HuggingFaceTB/SmolLM-135M",
            positive_prompts=["Analyze competitive landscape"],
            negative_prompts=["Profile investor"],
        ),
        # Field operations unit
        AdapterInfo(
            model_id="field_operations_market_intelligence_v1",
            unit_id="field_operations",
            task_id="market_intelligence",
            version="v1",
            source_path=base_path / "field_operations" / "market_intelligence" / "v1" / "model",
            import_path=base_path / "field_operations" / "market_intelligence" / "v1" / "model",
            base_model="HuggingFaceTB/SmolLM-135M",
            positive_prompts=["Analyze market conditions"],
            negative_prompts=["Analyze RFP"],
        ),
        AdapterInfo(
            model_id="field_operations_project_performance_v1",
            unit_id="field_operations",
            task_id="project_performance",
            version="v1",
            source_path=base_path / "field_operations" / "project_performance" / "v1" / "model",
            import_path=base_path / "field_operations" / "project_performance" / "v1" / "model",
            base_model="HuggingFaceTB/SmolLM-135M",
            positive_prompts=["Evaluate project performance"],
            negative_prompts=["Analyze competition"],
        ),
    ]

    return adapters


@pytest.fixture
def mock_moe_model(tmp_path):
    """Create a mock MoE model directory."""
    model_dir = tmp_path / "mock_moe"
    model_dir.mkdir(parents=True)

    # Create mock config.json
    config = {
        "model_type": "mixtral",
        "num_local_experts": 2,
        "num_experts_per_tok": 2,
        "hidden_size": 4096,
        "intermediate_size": 14336,
        "num_hidden_layers": 32,
        "num_attention_heads": 32,
        "vocab_size": 32000,
    }
    with open(model_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Create mock tokenizer config
    tokenizer_config = {
        "model_max_length": 32768,
        "tokenizer_class": "LlamaTokenizer",
    }
    with open(model_dir / "tokenizer_config.json", "w") as f:
        json.dump(tokenizer_config, f, indent=2)

    # Create mock weights index
    with open(model_dir / "model.safetensors.index.json", "w") as f:
        json.dump({"weight_map": {}, "metadata": {"mock": True}}, f, indent=2)

    return model_dir


@pytest.fixture
def mock_adapter_dir(tmp_path):
    """Create a mock adapter directory with valid structure."""
    adapter_dir = tmp_path / "mock_adapter"
    adapter_dir.mkdir(parents=True)

    # Create adapter_config.json
    adapter_config = {
        "base_model_name_or_path": "HuggingFaceTB/SmolLM-135M",
        "r": 16,
        "lora_alpha": 16,
        "lora_dropout": 0.0,
        "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
        "bias": "none",
        "task_type": "CAUSAL_LM",
        "peft_type": "LORA",
    }
    with open(adapter_dir / "adapter_config.json", "w") as f:
        json.dump(adapter_config, f, indent=2)

    return adapter_dir


@pytest.fixture
def mock_mergekit_config():
    """Create a valid mergekit-moe configuration."""
    return {
        "base_model": "HuggingFaceTB/SmolLM-135M",
        "architecture": "mixtral",
        "gate_mode": "hidden",
        "dtype": "float16",
        "experts_per_token": 2,
        "experts": [
            {
                "source_model": "/path/to/expert1",
                "positive_prompts": ["Profile investor"],
                "negative_prompts": ["Analyze RFP"],
            },
            {
                "source_model": "/path/to/expert2",
                "positive_prompts": ["Analyze RFP"],
                "negative_prompts": ["Profile investor"],
            },
        ],
    }


def create_mock_adapter_files(adapter_dir: Path, adapter_info: AdapterInfo) -> None:
    """Helper to create mock adapter files for testing."""
    adapter_dir.mkdir(parents=True, exist_ok=True)

    # Create adapter_config.json
    adapter_config = {
        "base_model_name_or_path": adapter_info.base_model,
        "r": 16,
        "lora_alpha": 16,
        "lora_dropout": 0.0,
        "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
        "bias": "none",
        "task_type": "CAUSAL_LM",
        "peft_type": "LORA",
    }
    with open(adapter_dir / "adapter_config.json", "w") as f:
        json.dump(adapter_config, f, indent=2)

    # Create manifest.json
    manifest = {
        "model_id": adapter_info.model_id,
        "unit_id": adapter_info.unit_id,
        "task_id": adapter_info.task_id,
        "version": adapter_info.version,
        "base_model": adapter_info.base_model,
        "positive_prompts": adapter_info.positive_prompts,
        "negative_prompts": adapter_info.negative_prompts,
    }
    manifest_path = adapter_dir.parent / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
