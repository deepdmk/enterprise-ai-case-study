"""Centralized path configuration for Phase 5 imports.

This module provides a single place to configure paths for importing from
other phases (particularly Phase 0 infrastructure). This avoids fragile
sys.path manipulations scattered across multiple files.

Usage:
    from src.shared.path_config import configure_paths, PHASE5_ROOT, PHASE0_ROOT

    # Call once at the start of a program
    configure_paths()

    # Then import from phase-0-infrastructure
    from habitat_logging import get_logger
"""

import sys
from pathlib import Path

# Phase 5 root directory (parent of src/)
PHASE5_ROOT = Path(__file__).parent.parent.parent.resolve()

# Phase 0 infrastructure root (sibling directory)
PHASE0_ROOT = PHASE5_ROOT.parent / "phase-0-infrastructure"

# Phase 4 root (for importing discovery data)
PHASE4_ROOT = PHASE5_ROOT.parent / "phase-4-agentic-discovery"

# Track if paths have been configured
_paths_configured = False


def configure_paths(force: bool = False) -> bool:
    """
    Configure sys.path for Phase 5 imports.

    Adds the necessary paths to sys.path in the correct order:
    1. Phase 5 root (for config and src imports)
    2. Phase 0 infrastructure (for habitat_logging, registries, etc.)

    Args:
        force: If True, reconfigure paths even if already configured.

    Returns:
        True if paths were configured, False if already configured (and not forced).

    Raises:
        FileNotFoundError: If Phase 0 infrastructure directory doesn't exist.
    """
    global _paths_configured

    if _paths_configured and not force:
        return False

    # Add Phase 5 root first (for local config imports)
    phase5_str = str(PHASE5_ROOT)
    if phase5_str not in sys.path:
        sys.path.insert(0, phase5_str)

    # Add Phase 0 infrastructure
    if not PHASE0_ROOT.exists():
        raise FileNotFoundError(
            f"Phase 0 infrastructure not found at: {PHASE0_ROOT}\n"
            f"Expected directory structure:\n"
            f"  enterprise-ai-case-study/\n"
            f"    phase-0-infrastructure/\n"
            f"    phase-5-orchestrated-agentic/  (current)\n"
        )

    phase0_str = str(PHASE0_ROOT)
    if phase0_str not in sys.path:
        sys.path.insert(0, phase0_str)

    _paths_configured = True
    return True


def is_configured() -> bool:
    """Check if paths have been configured."""
    return _paths_configured


def get_config_path(config_file: str = "config/settings.yaml") -> Path:
    """Get the path to a configuration file."""
    return PHASE5_ROOT / config_file


def get_data_path(subpath: str = "") -> Path:
    """Get the path to a data directory or file."""
    data_path = PHASE5_ROOT / "data"
    if subpath:
        data_path = data_path / subpath
    return data_path
