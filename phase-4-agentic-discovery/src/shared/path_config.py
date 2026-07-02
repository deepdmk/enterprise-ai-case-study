"""Centralized path configuration for Phase 4 imports.

This module provides a single place to configure paths for importing from
other phases (particularly Phase 0 infrastructure). This avoids fragile
sys.path manipulations scattered across multiple files.

Usage:
    from src.shared.path_config import configure_paths, PHASE4_ROOT, PHASE0_ROOT

    # Call once at the start of a program
    configure_paths()

    # Then import from phase-0-infrastructure
    from phase0_infra.habitat_logging import get_logger
"""

import sys
from pathlib import Path

# Phase 4 root directory (parent of src/)
PHASE4_ROOT = Path(__file__).parent.parent.parent.resolve()

# Phase 0 infrastructure root (sibling directory)
PHASE0_ROOT = PHASE4_ROOT.parent / "phase-0-infrastructure"

# Phase 1 root (for embedding/search integration)
PHASE1_ROOT = PHASE4_ROOT.parent / "phase-1-embed-space"

# Phase 3 root (for MoE model loading)
PHASE3_ROOT = PHASE4_ROOT.parent / "phase-3-moe-experts"

# Track if paths have been configured
_paths_configured = False


def configure_paths(force: bool = False) -> bool:
    """
    Configure sys.path for Phase 4 imports.

    Adds the necessary paths to sys.path in the correct order:
    1. Phase 4 root (for config and src imports)
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

    # Add Phase 4 root first (for local config imports)
    phase4_str = str(PHASE4_ROOT)
    if phase4_str not in sys.path:
        sys.path.insert(0, phase4_str)

    # Add Phase 0 infrastructure
    if not PHASE0_ROOT.exists():
        raise FileNotFoundError(
            f"Phase 0 infrastructure not found at: {PHASE0_ROOT}\n"
            f"Expected directory structure:\n"
            f"  enterprise-ai-case-study/\n"
            f"    phase-0-infrastructure/\n"
            f"    phase-4-agentic-discovery/  (current)\n"
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
    return PHASE4_ROOT / config_file


def get_data_path(subpath: str = "") -> Path:
    """Get the path to a data directory or file."""
    data_path = PHASE4_ROOT / "data"
    if subpath:
        data_path = data_path / subpath
    return data_path
