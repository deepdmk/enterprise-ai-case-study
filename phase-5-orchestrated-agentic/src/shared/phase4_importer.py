"""
Phase 4 Data Importer

Imports training data exported from Phase 4 discovery experiments.
"""

import json
import os
from pathlib import Path
from typing import Any

from habitat_logging import get_logger

try:
    from config.phase_boundary_schemas import (
        Phase4TrainingExample,
        validate_phase4_training_examples,
    )
    _HAS_SCHEMAS = True
except ImportError:
    _HAS_SCHEMAS = False

logger = get_logger(__name__)


class Phase4Importer:
    """
    Imports Phase 4 orchestrator training data.

    Expected files from Phase 4 exports:
    - orchestrator_training.json: Training examples (dict format)
    - orchestrator_training.jsonl: Training examples (JSONL format)
    - orchestrator_chat.jsonl: ChatML format examples
    - phase5_summary.json: Summary with optimal depths
    """

    def __init__(self, phase4_exports_dir: Path | None = None):
        """
        Initialize importer.

        Args:
            phase4_exports_dir: Path to Phase 4 exports directory.
                               If None, will auto-detect.
        """
        self.logger = logger.bind(component="phase4_importer")
        self.exports_dir = self._resolve_exports_dir(phase4_exports_dir)

    def _resolve_exports_dir(self, exports_dir: Path | None) -> Path:
        """
        Resolve Phase 4 exports directory.

        Auto-detection strategy:
        1. Use provided path if given
        2. Check PHASE4_EXPORTS_DIR environment variable
        3. Check relative paths from this file's location
        """
        if exports_dir:
            return Path(exports_dir)

        # Check environment variable
        env_path = os.environ.get("PHASE4_EXPORTS_DIR")
        if env_path:
            return Path(env_path)

        # Auto-detect relative to this file's location (src/shared/ -> phase root -> repo root)
        repo_root = Path(__file__).parent.parent.parent.parent
        candidates = [
            repo_root / "phase-4-agentic-discovery" / "data" / "exports",
            Path("../phase-4-agentic-discovery/data/exports"),
            Path("../../phase-4-agentic-discovery/data/exports"),
        ]

        for candidate in candidates:
            if candidate.exists():
                self.logger.info("auto_detected_phase4_exports", path=str(candidate))
                return candidate

        # Return default (may not exist yet)
        return repo_root / "phase-4-agentic-discovery" / "data" / "exports"

    def import_training_examples(self) -> list[dict[str, Any]]:
        """
        Import training examples from Phase 4.

        Returns:
            List of training examples (dict format)
        """
        training_file = self.exports_dir / "orchestrator_training.json"

        if not training_file.exists():
            self.logger.warning(
                "training_file_not_found",
                path=str(training_file),
                message="Phase 4 training data not found. Run Phase 4 export first."
            )
            return []

        with open(training_file) as f:
            examples = json.load(f)

        # Validate against schema if available
        if _HAS_SCHEMAS and examples:
            validated, result = validate_phase4_training_examples(examples)
            if result.records_skipped > 0:
                self.logger.warning(
                    "schema_validation_warnings",
                    skipped=result.records_skipped,
                    errors=result.errors[:5],
                )

        self.logger.info("imported_training_examples", count=len(examples))
        return examples

    def import_chat_examples(self) -> list[dict[str, Any]]:
        """
        Import ChatML format examples from Phase 4.

        Returns:
            List of ChatML examples
        """
        chat_file = self.exports_dir / "orchestrator_chat.jsonl"

        if not chat_file.exists():
            self.logger.warning(
                "chat_file_not_found",
                path=str(chat_file),
                message="Phase 4 chat data not found. Run Phase 4 export first."
            )
            return []

        examples = []
        with open(chat_file) as f:
            for line in f:
                if line.strip():
                    examples.append(json.loads(line))

        self.logger.info("imported_chat_examples", count=len(examples))
        return examples

    def import_phase5_summary(self) -> dict[str, Any]:
        """
        Import Phase 5 summary (optimal depths, recommendations).

        Returns:
            Summary dictionary
        """
        summary_file = self.exports_dir / "phase5_summary.json"

        if not summary_file.exists():
            self.logger.warning(
                "summary_file_not_found",
                path=str(summary_file),
                message="Phase 5 summary not found."
            )
            return {"optimal_depths": {}, "workflows": {}}

        with open(summary_file) as f:
            summary = json.load(f)

        self.logger.info("imported_phase5_summary", workflows=len(summary.get("workflows", {})))
        return summary

    def import_all(self) -> dict[str, Any]:
        """
        Import all Phase 4 data.

        Returns:
            Dictionary containing:
            - training_examples: List of training examples
            - chat_examples: List of ChatML examples
            - summary: Phase 5 summary
        """
        return {
            "training_examples": self.import_training_examples(),
            "chat_examples": self.import_chat_examples(),
            "summary": self.import_phase5_summary()
        }

    def export_to_local(self, output_dir: Path) -> None:
        """
        Copy Phase 4 exports to local Phase 5 imports directory.

        Args:
            output_dir: Local directory to copy files to
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        files_to_copy = [
            "orchestrator_training.json",
            "orchestrator_training.jsonl",
            "orchestrator_chat.jsonl",
            "phase5_summary.json"
        ]

        copied = 0
        for filename in files_to_copy:
            source = self.exports_dir / filename
            dest = output_dir / filename

            if source.exists():
                import shutil
                shutil.copy2(source, dest)
                copied += 1
                self.logger.info("copied_file", source=str(source), dest=str(dest))
            else:
                self.logger.warning("file_not_found", path=str(source))

        self.logger.info("export_complete", files_copied=copied, total_files=len(files_to_copy))

    def get_optimal_depths(self) -> dict[str, int]:
        """
        Get optimal depths for known workflows.

        Returns:
            Dictionary mapping workflow_id to optimal depth
        """
        summary = self.import_phase5_summary()
        return summary.get("optimal_depths", {})

    def get_workflow_stats(self) -> dict[str, dict[str, Any]]:
        """
        Get workflow statistics from Phase 4 discovery.

        Returns:
            Dictionary mapping workflow_id to statistics
        """
        summary = self.import_phase5_summary()
        return summary.get("workflows", {})

    def validate_imports(self) -> bool:
        """
        Validate that all required Phase 4 exports exist.

        Returns:
            True if all files exist, False otherwise
        """
        required_files = [
            "orchestrator_training.json",
            "orchestrator_chat.jsonl",
            "phase5_summary.json"
        ]

        all_exist = True
        for filename in required_files:
            file_path = self.exports_dir / filename
            exists = file_path.exists()

            if not exists:
                self.logger.error("required_file_missing", path=str(file_path))
                all_exist = False

        if all_exist:
            self.logger.info("validation_passed", exports_dir=str(self.exports_dir))
        else:
            self.logger.error(
                "validation_failed",
                exports_dir=str(self.exports_dir),
                message="Run Phase 4 export first: python -m src.program4_adaptive_analyzer.main"
            )

        return all_exist
