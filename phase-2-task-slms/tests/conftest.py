"""Pytest configuration and shared fixtures for Phase 2 tests."""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add phase-0-infrastructure to path
phase0_path = project_root.parent / "phase-0-infrastructure"
if phase0_path.exists():
    sys.path.insert(0, str(phase0_path))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file for testing."""
    csv_content = """input,output,category
"What is investor A's portfolio?","Investor A focuses on renewable energy with $50M AUM.",energy
"Analyze market trends","Current trends show growth in AI sector.",technology
"Short input","Output text that meets minimum length requirements for validation.",general"""

    csv_path = temp_dir / "sample.csv"
    csv_path.write_text(csv_content)
    return csv_path


@pytest.fixture
def sample_json_file(temp_dir):
    """Create a sample JSON file for testing."""
    json_data = [
        {
            "input": "Describe the investment strategy",
            "output": "The investment strategy focuses on long-term growth with diversified holdings across sectors.",
            "source": "manual"
        },
        {
            "input": "What are the key metrics?",
            "output": "Key metrics include ROI, IRR, and portfolio diversification scores. These help track performance.",
            "category": "metrics"
        }
    ]

    json_path = temp_dir / "sample.json"
    json_path.write_text(json.dumps(json_data, indent=2))
    return json_path


@pytest.fixture
def sample_jsonl_file(temp_dir):
    """Create a sample JSONL file for testing."""
    examples = [
        {"input": "First example input with enough characters for validation", "output": "First example output that is long enough to pass the minimum length validation check."},
        {"input": "Second example input with sufficient length for testing", "output": "Second example output that provides meaningful content for the test validation."},
        {"input": "Third example input for completeness of test data", "output": "Third example output with adequate length to satisfy validation requirements."},
    ]

    jsonl_path = temp_dir / "sample.jsonl"
    with open(jsonl_path, "w") as f:
        for example in examples:
            f.write(json.dumps(example) + "\n")
    return jsonl_path


@pytest.fixture
def sample_sharegpt_file(temp_dir):
    """Create a sample ShareGPT format file for testing."""
    sharegpt_data = [
        {
            "conversations": [
                {"from": "human", "value": "What is the current market analysis?"},
                {"from": "gpt", "value": "The current market shows positive trends with growth in technology and renewable energy sectors."}
            ]
        },
        {
            "conversations": [
                {"from": "human", "value": "Analyze the portfolio performance over the last quarter."},
                {"from": "gpt", "value": "Portfolio performance has exceeded benchmarks by 5% due to strategic allocation shifts."}
            ]
        }
    ]

    file_path = temp_dir / "sharegpt.json"
    file_path.write_text(json.dumps(sharegpt_data, indent=2))
    return file_path


@pytest.fixture
def valid_examples():
    """Create a list of valid training examples."""
    return [
        {
            "input": "Analyze the investor profile for potential engagement opportunities and strategic alignment.",
            "output": "## Investment Thesis\nThe investor focuses on early-stage technology companies.\n\n## Portfolio Summary\nCurrent AUM: $100M with 20 active investments."
        },
        {
            "input": "Provide market intelligence on emerging trends in sustainable finance.",
            "output": "## Investment Thesis\nSustainable finance is growing rapidly.\n\n## Portfolio Summary\nESG-focused funds have seen 30% growth."
        },
        {
            "input": "Evaluate the competitive landscape for our new product offering.",
            "output": "## Investment Thesis\nThe market is competitive but underserved.\n\n## Portfolio Summary\nTop competitors hold 60% market share."
        }
    ]


@pytest.fixture
def invalid_examples():
    """Create a list of invalid training examples."""
    return [
        {"input": "", "output": "Valid output content that meets requirements"},  # Missing input
        {"input": "Valid input content", "output": ""},  # Missing output
        {"input": "Short", "output": "Short"},  # Both too short
        {"input": "Same content for both fields", "output": "Same content for both fields"},  # Identical
    ]


@pytest.fixture
def mixed_examples(valid_examples, invalid_examples):
    """Create a mixed list of valid and invalid examples."""
    return valid_examples + invalid_examples
