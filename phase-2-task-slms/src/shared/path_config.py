"""Centralized path configuration for Phase 2 imports.

This module provides a single place to configure paths for importing from
other phases (particularly Phase 0 infrastructure). This avoids fragile
sys.path manipulations scattered across multiple files.

Usage:
    from src.shared.path_config import configure_paths, PHASE2_ROOT, PHASE0_ROOT

    # Call once at the start of a program
    configure_paths()

    # Then import from phase-0-infrastructure
    from habitat_logging import get_logger
"""

import sys
from pathlib import Path

# Phase 2 root directory (parent of src/)
PHASE2_ROOT = Path(__file__).parent.parent.parent.resolve()

# Phase 0 infrastructure root (sibling directory)
PHASE0_ROOT = PHASE2_ROOT.parent / "phase-0-infrastructure"

# Track if paths have been configured
_paths_configured = False


def configure_paths(force: bool = False) -> bool:
    """
    Configure sys.path for Phase 2 imports.

    This function adds the necessary paths to sys.path in the correct order:
    1. Phase 2 root (for config and src imports)
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

    # Add Phase 2 root first (for local config imports)
    phase2_str = str(PHASE2_ROOT)
    if phase2_str not in sys.path:
        sys.path.insert(0, phase2_str)

    # Add Phase 0 infrastructure
    if not PHASE0_ROOT.exists():
        raise FileNotFoundError(
            f"Phase 0 infrastructure not found at: {PHASE0_ROOT}\n"
            f"Expected directory structure:\n"
            f"  enterprise-ai-case-study/\n"
            f"    phase-0-infrastructure/\n"
            f"    phase-2-task-slms/  (current)\n"
        )

    phase0_str = str(PHASE0_ROOT)
    if phase0_str not in sys.path:
        sys.path.insert(0, phase0_str)

    _paths_configured = True
    return True


def is_configured() -> bool:
    """Check if paths have been configured."""
    return _paths_configured


def get_config_path(config_file: str = "config/config.yaml") -> Path:
    """
    Get the path to a configuration file.

    Args:
        config_file: Relative path to config file from Phase 2 root.

    Returns:
        Absolute path to the configuration file.
    """
    return PHASE2_ROOT / config_file


def get_data_path(subpath: str = "") -> Path:
    """
    Get the path to a data directory or file.

    Args:
        subpath: Relative path within the data directory.

    Returns:
        Absolute path to the data location.
    """
    data_path = PHASE2_ROOT / "data"
    if subpath:
        data_path = data_path / subpath
    return data_path
