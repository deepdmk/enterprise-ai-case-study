"""Export merged MoE models for Phase 4 A2A agents - one per unit."""

import json
import shutil
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger

from config.settings import Settings
from src.shared.phase2_importer import AdapterInfo

logger = get_logger(__name__)


@dataclass
class ExportResult:
    """Result of Phase 4 export operation."""

    success: bool
    export_dir: Path
    unit_id: str = ""
    model_exported: bool = False
    routing_exported: bool = False
    agent_config_exported: bool = False
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "export_dir": str(self.export_dir),
            "unit_id": self.unit_id,
            "model_exported": self.model_exported,
            "routing_exported": self.routing_exported,
            "agent_config_exported": self.agent_config_exported,
            "errors": self.errors,
            "metadata": self.metadata,
        }


class Phase4Exporter:
    """Export merged MoE models for Phase 4 A2A agents - one per unit."""

    def __init__(self, settings: Settings):
        """
        Initialize the exporter.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.merged_dir = self.base_path / settings.paths.merged_dir
        self.exports_dir = self.base_path / settings.paths.exports_dir

    def export_all(
        self,
        adapters: list[AdapterInfo],
        generate_agent_configs: bool = True,
        generate_routing_embeddings: bool = True,
        dry_run: bool = False,
    ) -> dict[str, ExportResult]:
        """
        Export all units' MoE models for Phase 4.

        Args:
            adapters: All adapter info records
            generate_agent_configs: Whether to generate A2A agent configs
            generate_routing_embeddings: Whether to compute routing embeddings
            dry_run: Validate configuration without writing files

        Returns:
            Dictionary mapping unit_id to ExportResult
        """
        # Group adapters by unit
        units: dict[str, list[AdapterInfo]] = {}
        for adapter in adapters:
            if adapter.unit_id not in units:
                units[adapter.unit_id] = []
            units[adapter.unit_id].append(adapter)

        results = {}

        for unit_id, unit_adapters in units.items():
            model_path = self.merged_dir / f"{unit_id}_moe"
            output_dir = self.exports_dir / "phase4" / unit_id

            result = self.export_unit(
                unit_id=unit_id,
                model_path=model_path,
                output_dir=output_dir,
                adapters=unit_adapters,
                generate_agent_config=generate_agent_configs,
                generate_routing_embeddings=generate_routing_embeddings,
                dry_run=dry_run,
            )
            results[unit_id] = result

        return results

    def export_unit(
        self,
        unit_id: str,
        model_path: str | Path,
        output_dir: str | Path | None = None,
        adapters: list[AdapterInfo] | None = None,
        generate_agent_config: bool = True,
        generate_routing_embeddings: bool = True,
        dry_run: bool = False,
    ) -> ExportResult:
        """
        Export a single unit's MoE model for Phase 4.

        Args:
            unit_id: Unit ID being exported
            model_path: Path to merged model for this unit
            output_dir: Output directory (uses default if not specified)
            adapters: Adapter info for this unit's experts
            generate_agent_config: Whether to generate A2A agent config
            generate_routing_embeddings: Whether to compute routing embeddings
            dry_run: Validate configuration without writing files

        Returns:
            ExportResult
        """
        model_path = Path(model_path)

        if output_dir is None:
            output_dir = self.exports_dir / "phase4" / unit_id
        output_dir = Path(output_dir)

        result = ExportResult(
            success=False,
            export_dir=output_dir,
            unit_id=unit_id,
        )

        # Dry run: validate configuration only
        if dry_run:
            if not model_path.exists():
                result.errors.append(f"Model path not found: {model_path}")
            if not adapters:
                result.errors.append("No adapters provided")
            result.success = len(result.errors) == 0
            result.metadata["dry_run"] = True
            logger.info("dry_run_complete", unit=unit_id, valid=result.success)
            return result

        # Use atomic writes via temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix=f"export_{unit_id}_"))
        try:
            # Export model
            if model_path.exists():
                model_result = self._export_model(model_path, temp_dir)
                result.model_exported = model_result
            else:
                result.errors.append(f"Model path not found: {model_path}")

            # Export routing metadata
            if adapters:
                routing_result = self._export_routing(adapters, temp_dir, unit_id)
                result.routing_exported = routing_result

                if generate_routing_embeddings:
                    self._export_routing_embeddings(adapters, temp_dir)

            # Generate agent config
            if generate_agent_config and adapters:
                agent_result = self._generate_agent_config(unit_id, adapters, temp_dir)
                result.agent_config_exported = agent_result

            # Create export manifest
            self._create_manifest(result, model_path, adapters, temp_dir)

            # Only move to final location if no errors
            if len(result.errors) == 0:
                # Remove existing output directory if present
                if output_dir.exists():
                    shutil.rmtree(output_dir)
                # Move temp directory to final location
                output_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(temp_dir), str(output_dir))
                result.success = True
                logger.info(
                    "unit_export_complete",
                    unit=unit_id,
                    success=result.success,
                    export_dir=str(output_dir),
                )
            else:
                # Clean up temp directory on error
                shutil.rmtree(temp_dir, ignore_errors=True)
                logger.warning(
                    "unit_export_partial_failure",
                    unit=unit_id,
                    errors=result.errors,
                )

        except (OSError, IOError, shutil.Error) as e:
            result.errors.append(str(e))
            # Clean up temp directory on exception
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.error("unit_export_failed", unit=unit_id, error=str(e), exc_type=type(e).__name__)
        except KeyboardInterrupt:
            # Clean up temp directory on interrupt
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.warning("unit_export_cancelled", unit=unit_id)
            raise

        return result

    def _export_model(self, model_path: Path, output_dir: Path) -> bool:
        """Export the merged model."""
        model_export_dir = output_dir / "model"

        try:
            # Copy or link model directory
            if model_export_dir.exists():
                shutil.rmtree(model_export_dir)

            shutil.copytree(model_path, model_export_dir)

            logger.info(
                "model_exported",
                source=str(model_path),
                destination=str(model_export_dir),
            )
            return True

        except Exception as e:
            logger.error("model_export_failed", error=str(e))
            return False

    def _export_routing(
        self,
        adapters: list[AdapterInfo],
        output_dir: Path,
        unit_id: str,
    ) -> bool:
        """Export routing metadata for a unit's MoE."""
        routing_dir = output_dir / "routing"
        routing_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Expert registry for this unit
            registry = {
                "unit_id": unit_id,
                "total_experts": len(adapters),
                "experts": {},
            }
            for idx, adapter in enumerate(adapters):
                registry["experts"][str(idx)] = {
                    "expert_id": idx,
                    "model_id": adapter.model_id,
                    "unit_id": adapter.unit_id,
                    "task_id": adapter.task_id,
                }

            with open(routing_dir / "expert_registry.json", "w") as f:
                json.dump(registry, f, indent=2)

            # Intent mapping for this unit
            intent_map = self._build_intent_mapping(adapters)
            with open(routing_dir / "intent_mapping.json", "w") as f:
                json.dump(intent_map, f, indent=2)

            logger.info("routing_metadata_exported", unit=unit_id, path=str(routing_dir))
            return True

        except Exception as e:
            logger.error("routing_export_failed", unit=unit_id, error=str(e))
            return False

    def _build_intent_mapping(
        self,
        adapters: list[AdapterInfo],
    ) -> dict[str, list[int]]:
        """Build intent to expert ID mapping for a unit's experts."""
        intent_map: dict[str, list[int]] = {}

        for idx, adapter in enumerate(adapters):
            # Map by task
            task_key = f"task:{adapter.task_id}"
            if task_key not in intent_map:
                intent_map[task_key] = []
            intent_map[task_key].append(idx)

            # Map positive prompts
            for prompt in adapter.positive_prompts:
                prompt_key = prompt.lower().strip()
                if prompt_key not in intent_map:
                    intent_map[prompt_key] = []
                intent_map[prompt_key].append(idx)

        return intent_map

    def _export_routing_embeddings(
        self,
        adapters: list[AdapterInfo],
        output_dir: Path,
    ) -> bool:
        """Export pre-computed routing embeddings for a unit's experts."""
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np

            routing_dir = output_dir / "routing"
            routing_dir.mkdir(parents=True, exist_ok=True)

            model = SentenceTransformer(self.settings.export_config.embedding_model)

            # Collect all prompts
            all_positive = []
            all_negative = []
            prompt_to_expert: dict[str, list[int]] = {}

            for idx, adapter in enumerate(adapters):
                for prompt in adapter.positive_prompts:
                    all_positive.append(prompt)
                    if prompt not in prompt_to_expert:
                        prompt_to_expert[prompt] = []
                    prompt_to_expert[prompt].append(idx)

                for prompt in adapter.negative_prompts:
                    all_negative.append(prompt)

            # Compute embeddings
            if all_positive:
                positive_embeddings = model.encode(all_positive)
                np.save(routing_dir / "positive_embeddings.npy", positive_embeddings)

            if all_negative:
                negative_embeddings = model.encode(all_negative)
                np.save(routing_dir / "negative_embeddings.npy", negative_embeddings)

            # Save prompt mapping
            with open(routing_dir / "prompt_mapping.json", "w") as f:
                json.dump({
                    "positive_prompts": all_positive,
                    "negative_prompts": all_negative,
                    "prompt_to_expert": prompt_to_expert,
                }, f, indent=2)

            logger.info("routing_embeddings_exported", path=str(routing_dir))
            return True

        except ImportError:
            logger.warning("sentence_transformers_not_available")
            return False
        except Exception as e:
            logger.error("embedding_export_failed", error=str(e))
            return False

    def _generate_agent_config(
        self,
        unit_id: str,
        adapters: list[AdapterInfo],
        output_dir: Path,
    ) -> bool:
        """Generate A2A agent configuration for a unit."""
        agent_dir = output_dir / "agent_config"
        agent_dir.mkdir(parents=True, exist_ok=True)

        try:
            agent_config = self._create_agent_config(unit_id, adapters)
            config_path = agent_dir / f"{unit_id}_agent.yaml"

            with open(config_path, "w") as f:
                yaml.dump(agent_config, f, default_flow_style=False)

            logger.info("agent_config_generated", unit=unit_id, path=str(config_path))
            return True

        except Exception as e:
            logger.error("agent_config_generation_failed", unit=unit_id, error=str(e))
            return False

    def _create_agent_config(
        self,
        unit_id: str,
        adapters: list[AdapterInfo],
    ) -> dict[str, Any]:
        """Create A2A agent configuration for a unit's MoE."""
        # Get unit display name from settings if available
        unit_name = unit_id.replace("_", " ").title()
        if hasattr(self.settings, "units") and unit_id in self.settings.units:
            unit_def = self.settings.units[unit_id]
            if hasattr(unit_def, "name"):
                unit_name = unit_def.name

        return {
            "agent": {
                "id": f"{unit_id}_agent",
                "name": f"{unit_name} Agent",
                "description": f"A2A agent powered by {unit_id} MoE with {len(adapters)} experts",
            },
            "model": {
                "type": "moe",
                "path": "./model",
                "architecture": self.settings.moe.architecture,
                "num_experts": len(adapters),
                "experts_per_token": min(
                    self.settings.moe.experts_per_token,
                    len(adapters),
                ),
                "experts": [
                    {
                        "expert_id": idx,
                        "task_id": adapter.task_id,
                        "positive_prompts": adapter.positive_prompts,
                    }
                    for idx, adapter in enumerate(adapters)
                ],
            },
            "routing": {
                "method": "semantic",
                "gate_mode": self.settings.moe.gate_mode,
                "embedding_model": self.settings.export_config.embedding_model,
            },
            "tasks": [adapter.task_id for adapter in adapters],
        }

    def _create_manifest(
        self,
        result: ExportResult,
        model_path: Path,
        adapters: list[AdapterInfo] | None,
        target_dir: Path | None = None,
    ) -> None:
        """Create export manifest for a unit.

        Args:
            result: ExportResult being populated
            model_path: Source model path
            adapters: Adapter info for this unit
            target_dir: Directory to write manifest to (uses result.export_dir if None)
        """
        manifest = {
            "exported_at": datetime.utcnow().isoformat(),
            "unit_id": result.unit_id,
            "model_source": str(model_path),
            "export_dir": str(result.export_dir),
            "components": {
                "model": result.model_exported,
                "routing": result.routing_exported,
                "agent_config": result.agent_config_exported,
            },
            "num_experts": len(adapters) if adapters else 0,
            "tasks": [a.task_id for a in adapters] if adapters else [],
            "errors": result.errors,
        }

        output_path = target_dir if target_dir else result.export_dir
        manifest_path = output_path / "export_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        result.metadata = manifest
        logger.info("manifest_created", unit=result.unit_id, path=str(manifest_path))
