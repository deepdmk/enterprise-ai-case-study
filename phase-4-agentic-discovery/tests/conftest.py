"""
Pytest configuration and fixtures
"""

import pytest
from pathlib import Path
import tempfile


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_config():
    """Test configuration"""
    return {
        "test_mode": True,
        "a2a_protocol": {
            "default_max_depth": 3,
            "default_timeout_ms": 5000
        }
    }
