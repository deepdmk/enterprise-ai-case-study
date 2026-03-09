"""Phase 2 import utilities for loading exported Task SLM adapters."""

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class AdapterInfo:
    """Information about an imported adapter."""

    model_id: str
    unit_id: str
    task_id: str
    version: str
    source_path: Path
    import_path: Path
    base_model: str
    positive_prompts: list[str] = field(default_factory=list)
    negative_prompts: list[str] = field(default_factory=list)
    metrics: dict[str, Any] | None = None
    is_merged: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "model_id": self.model_id,
            "unit_id": self.unit_id,
            "task_id": self.task_id,
            "version": self.version,
            "source_path": str(self.source_path),
            "import_path": str(self.import_path),
            "base_model": self.base_model,
            "positive_prompts": self.positive_prompts,
            "negative_prompts": self.negative_prompts,
            "metrics": self.metrics,
            "is_merged": self.is_merged,
        }


@dataclass
class ImportResult:
    """Result of Phase 2 import operation."""

    adapters: list[AdapterInfo]
    base_model: str
    source_manifest: dict[str, Any]
    import_dir: Path

    @property
    def total_adapters(self) -> int:
        return len(self.adapters)

    @property
    def units(self) -> list[str]:
        return list(set(a.unit_id for a in self.adapters))

    def get_adapters_by_unit(self, unit_id: str) -> list[AdapterInfo]:
        return [a for a in self.adapters if a.unit_id == unit_id]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_adapters": self.total_adapters,
            "base_model": self.base_model,
            "units": self.units,
            "adapters": [a.to_dict() for a in self.adapters],
            "import_dir": str(self.import_dir),
        }


class Phase2Importer:
    """Import Phase 2 exported adapters for MoE merging."""

    def __init__(
        self,
        phase2_export_dir: str | Path,
        import_dir: str | Path,
        required_units: list[str] | None = None,
        required_files: list[str] | None = None,
    ):
        """
        Initialize the importer.

        Args:
            phase2_export_dir: Path to Phase 2 exports directory
            import_dir: Path to import destination directory
            required_units: List of required unit IDs (validates all present)
            required_files: List of required files per adapter
        """
        self.phase2_export_dir = Path(phase2_export_dir)
        self.import_dir = Path(import_dir)
        self.required_units = required_units or []
        self.required_files = required_files or ["adapter_config.json"]

    def import_all(self, copy_files: bool = True) -> ImportResult:
        """
        Import all adapters from Phase 2 exports.

        Args:
            copy_files: If True, copy files to import_dir; if False, just validate

        Returns:
            ImportResult with all imported adapters
        """
        # Load export manifest
        manifest = self._load_manifest()
        base_model = manifest.get("base_model", "")

        # Discover adapters
        adapters = self._discover_adapters(manifest)

        # Validate required units
        self._validate_required_units(adapters)

        # Copy or link files
        if copy_files:
            self._copy_adapters(adapters)

        # Save import manifest
        self._save_import_manifest(adapters, base_model)

        result = ImportResult(
            adapters=adapters,
            base_model=base_model,
            source_manifest=manifest,
            import_dir=self.import_dir,
        )

        logger.info(
            "import_complete",
            total_adapters=result.total_adapters,
            units=result.units,
        )

        return result

    def _load_manifest(self) -> dict[str, Any]:
        """Load the Phase 2 export manifest."""
        manifest_path = self.phase2_export_dir / "export_manifest.json"

        if not manifest_path.exists():
            logger.warning("manifest_not_found", path=str(manifest_path))
            return {}

        with open(manifest_path) as f:
            return json.load(f)

    def _discover_adapters(self, manifest: dict[str, Any]) -> list[AdapterInfo]:
        """Discover all adapters from the export directory."""
        adapters = []

        # Try manifest-based discovery first
        if "units" in manifest:
            adapters = self._discover_from_manifest(manifest)
        else:
            # Fall back to directory-based discovery
            adapters = self._discover_from_directory()

        return adapters

    def _discover_from_manifest(self, manifest: dict[str, Any]) -> list[AdapterInfo]:
        """Discover adapters based on manifest structure."""
        adapters = []

        for unit_export in manifest.get("units", []):
            unit_id = unit_export.get("unit_id", "")

            for model_info in unit_export.get("models", []):
                model_id = model_info.get("model_id", "")
                task_id = model_info.get("task_id", "")
                version = model_info.get("version", "v1")

                source_path = Path(model_info.get("model_path", ""))
                if not source_path.is_absolute():
                    source_path = self.phase2_export_dir / source_path

                import_path = self.import_dir / unit_id / task_id / version / "model"

                adapter = AdapterInfo(
                    model_id=model_id,
                    unit_id=unit_id,
                    task_id=task_id,
                    version=version,
                    source_path=source_path,
                    import_path=import_path,
                    base_model=model_info.get("base_model", manifest.get("base_model", "")),
                    positive_prompts=model_info.get("positive_prompts", []),
                    negative_prompts=model_info.get("negative_prompts", []),
                    metrics=model_info.get("metrics"),
                    is_merged=model_info.get("merged", False),
                )
                adapters.append(adapter)

        return adapters

    def _discover_from_directory(self) -> list[AdapterInfo]:
        """Discover adapters by scanning directory structure."""
        adapters = []

        if not self.phase2_export_dir.exists():
            logger.warning("export_dir_not_found", path=str(self.phase2_export_dir))
            return adapters

        # Scan unit directories
        for unit_dir in self.phase2_export_dir.iterdir():
            if not unit_dir.is_dir() or unit_dir.name.startswith("."):
                continue

            unit_id = unit_dir.name

            # Scan task directories
            for task_dir in unit_dir.iterdir():
                if not task_dir.is_dir():
                    continue

                task_id = task_dir.name

                # Scan version directories
                for version_dir in task_dir.iterdir():
                    if not version_dir.is_dir():
                        continue

                    version = version_dir.name
                    model_dir = version_dir / "model"

                    if not model_dir.exists():
                        model_dir = version_dir

                    # Load manifest if exists
                    manifest_file = version_dir / "manifest.json"
                    model_manifest = {}
                    if manifest_file.exists():
                        with open(manifest_file) as f:
                            model_manifest = json.load(f)

                    adapter = AdapterInfo(
                        model_id=f"{unit_id}_{task_id}_{version}",
                        unit_id=unit_id,
                        task_id=task_id,
                        version=version,
                        source_path=model_dir,
                        import_path=self.import_dir / unit_id / task_id / version / "model",
                        base_model=model_manifest.get("base_model", ""),
                        positive_prompts=model_manifest.get("positive_prompts", []),
                        negative_prompts=model_manifest.get("negative_prompts", []),
                        metrics=model_manifest.get("metrics"),
                        is_merged=model_manifest.get("merged", False),
                    )
                    adapters.append(adapter)

        return adapters

    def _validate_required_units(self, adapters: list[AdapterInfo]) -> None:
        """Validate that all required units are present."""
        found_units = set(a.unit_id for a in adapters)
        missing_units = set(self.required_units) - found_units

        if missing_units:
            raise ValueError(f"Missing required units: {missing_units}")

        logger.info(
            "units_validated",
            required=self.required_units,
            found=list(found_units),
        )

    def _validate_adapter_files(self, adapter: AdapterInfo) -> list[str]:
        """Validate that required files exist for an adapter."""
        missing = []
        for filename in self.required_files:
            file_path = adapter.source_path / filename
            if not file_path.exists():
                missing.append(filename)
        return missing

    def _copy_adapters(self, adapters: list[AdapterInfo]) -> None:
        """Copy adapter files to import directory."""
        self.import_dir.mkdir(parents=True, exist_ok=True)

        for adapter in adapters:
            if not adapter.source_path.exists():
                logger.warning(
                    "adapter_source_not_found",
                    model_id=adapter.model_id,
                    path=str(adapter.source_path),
                )
                continue

            # Validate files
            missing = self._validate_adapter_files(adapter)
            if missing:
                logger.warning(
                    "adapter_missing_files",
                    model_id=adapter.model_id,
                    missing=missing,
                )

            # Copy directory
            adapter.import_path.parent.mkdir(parents=True, exist_ok=True)
            if adapter.import_path.exists():
                shutil.rmtree(adapter.import_path)

            shutil.copytree(adapter.source_path, adapter.import_path)

            logger.info(
                "adapter_copied",
                model_id=adapter.model_id,
                destination=str(adapter.import_path),
            )

    def _save_import_manifest(
        self,
        adapters: list[AdapterInfo],
        base_model: str,
    ) -> None:
        """Save import manifest for downstream programs."""
        self.import_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "total_adapters": len(adapters),
            "base_model": base_model,
            "units": list(set(a.unit_id for a in adapters)),
            "adapters": [a.to_dict() for a in adapters],
        }

        manifest_path = self.import_dir / "import_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        logger.info("import_manifest_saved", path=str(manifest_path))


def load_import_manifest(import_dir: str | Path) -> ImportResult:
    """Load previously imported adapters from manifest."""
    import_dir = Path(import_dir)
    manifest_path = import_dir / "import_manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Import manifest not found: {manifest_path}")

    with open(manifest_path) as f:
        data = json.load(f)

    adapters = []
    for adapter_data in data.get("adapters", []):
        adapter = AdapterInfo(
            model_id=adapter_data["model_id"],
            unit_id=adapter_data["unit_id"],
            task_id=adapter_data["task_id"],
            version=adapter_data["version"],
            source_path=Path(adapter_data["source_path"]),
            import_path=Path(adapter_data["import_path"]),
            base_model=adapter_data["base_model"],
            positive_prompts=adapter_data.get("positive_prompts", []),
            negative_prompts=adapter_data.get("negative_prompts", []),
            metrics=adapter_data.get("metrics"),
            is_merged=adapter_data.get("is_merged", False),
        )
        adapters.append(adapter)

    return ImportResult(
        adapters=adapters,
        base_model=data.get("base_model", ""),
        source_manifest=data,
        import_dir=import_dir,
    )
