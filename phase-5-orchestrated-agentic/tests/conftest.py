"""
Shared pytest fixtures for Phase 5 tests.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from config.settings import Settings
from src.shared.routing_schema import TrainingExample, AgentType


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def test_settings(temp_dir):
    """Create test settings"""
    settings = Settings(
        test_mode=True,
        device="cpu",
        paths={
            "data_dir": temp_dir / "data",
            "models_dir": temp_dir / "data/models",
            "training_dir": temp_dir / "data/training",
            "checkpoints_dir": temp_dir / "data/checkpoints",
            "exports_dir": temp_dir / "data/exports",
            "phase4_imports_dir": temp_dir / "data/phase4_imports",
        }
    )

    # Create directories
    for path_name in ["data_dir", "models_dir", "training_dir", "checkpoints_dir", "exports_dir", "phase4_imports_dir"]:
        path = getattr(settings.paths, path_name)
        Path(path).mkdir(parents=True, exist_ok=True)

    return settings


@pytest.fixture
def sample_training_examples():
    """Create sample training examples"""
    examples = [
        TrainingExample(
            query="What is the investment capacity of INV-123?",
            entry_agent=AgentType.FUNDRAISING,
            optimal_depth=1,
            call_sequence=[{"depth": 0, "target": "fundraising-agent", "goal": "Check capacity"}],
            final_response="Investor INV-123 has capacity for $500K",
            metadata={"workflow_id": "test_1", "success": True}
        ),
        TrainingExample(
            query="Evaluate funding opportunity in Kenya",
            entry_agent=AgentType.FIELD_OPERATIONS,
            optimal_depth=3,
            call_sequence=[{"depth": 0, "target": "field-operations-agent", "goal": "Evaluate opportunity"}],
            final_response="Kenya opportunity evaluated",
            metadata={"workflow_id": "test_2", "success": True}
        ),
        TrainingExample(
            query="What RFPs are open in education?",
            entry_agent=AgentType.BUSINESS_DEVELOPMENT,
            optimal_depth=2,
            call_sequence=[{"depth": 0, "target": "business-development-agent", "goal": "List RFPs"}],
            final_response="Found 3 open RFPs in education",
            metadata={"workflow_id": "test_3", "success": True}
        ),
    ]

    return examples


@pytest.fixture
def mock_agent_registry():
    """Mock agent registry for tests"""
    return {
        "fundraising-agent": "http://localhost:8001",
        "business-development-agent": "http://localhost:8002",
        "field-operations-agent": "http://localhost:8003"
    }
