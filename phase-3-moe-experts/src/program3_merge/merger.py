"""Execute mergekit-moe merge operations."""

import json
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from src.shared.path_config import configure_paths
configure_paths()

from habitat_logging import get_logger

from config.settings import Settings
from src.shared.config_generator import load_mergekit_config, validate_mergekit_config

logger = get_logger(__name__)


@dataclass
class MergeResult:
    """Result of a merge operation."""

    success: bool
    output_dir: Path
    config_path: Path
    start_time: datetime
    end_time: datetime | None = None
    error: str | None = None
    stdout: str = ""
    stderr: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> float | None:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "output_dir": str(self.output_dir),
            "config_path": str(self.config_path),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "error": self.error,
            "metadata": self.metadata,
        }


class MoEMerger:
    """Execute mergekit-moe merge operations."""

    def __init__(self, settings: Settings):
        """
        Initialize the merger.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.configs_dir = self.base_path / settings.paths.configs_dir
        self.merged_dir = self.base_path / settings.paths.merged_dir

    def merge(
        self,
        config_path: str | Path,
        output_dir: str | Path | None = None,
        use_cuda: bool | None = None,
        dry_run: bool = False,
    ) -> MergeResult:
        """
        Execute mergekit-moe merge.

        Args:
            config_path: Path to mergekit-moe config YAML
            output_dir: Output directory for merged model
            use_cuda: Override CUDA setting
            dry_run: Validate config without merging

        Returns:
            MergeResult with operation details
        """
        config_path = Path(config_path)
        start_time = datetime.utcnow()

        # Determine output directory
        if output_dir is None:
            output_dir = self.merged_dir / "enterprise_moe"
        output_dir = Path(output_dir)

        result = MergeResult(
            success=False,
            output_dir=output_dir,
            config_path=config_path,
            start_time=start_time,
        )

        # Validate config
        if not config_path.exists():
            result.error = f"Config file not found: {config_path}"
            result.end_time = datetime.utcnow()
            logger.error("config_not_found", path=str(config_path))
            return result

        config = load_mergekit_config(config_path)
        validation_errors = validate_mergekit_config(config)

        if validation_errors:
            result.error = f"Config validation failed: {validation_errors}"
            result.end_time = datetime.utcnow()
            logger.error("config_validation_failed", errors=validation_errors)
            return result

        # Store config info
        result.metadata["num_experts"] = len(config.get("experts", []))
        result.metadata["architecture"] = config.get("architecture")
        result.metadata["gate_mode"] = config.get("gate_mode")
        result.metadata["base_model"] = config.get("base_model")

        if dry_run:
            result.success = True
            result.end_time = datetime.utcnow()
            logger.info("dry_run_complete", config_valid=True)
            return result

        # Determine CUDA setting
        cuda = use_cuda if use_cuda is not None else self.settings.merge.use_cuda

        # Execute merge
        try:
            result = self._execute_merge(
                config_path=config_path,
                output_dir=output_dir,
                cuda=cuda,
                result=result,
            )
        except (subprocess.SubprocessError, subprocess.TimeoutExpired, OSError, yaml.YAMLError, ValueError) as e:
            result.error = str(e)
            result.end_time = datetime.utcnow()
            logger.error("merge_exception", error=str(e), exc_type=type(e).__name__)
            self._cleanup_failed_merge(output_dir)
        except KeyboardInterrupt:
            result.error = "Merge cancelled by user"
            result.end_time = datetime.utcnow()
            logger.warning("merge_cancelled_by_user")
            self._cleanup_failed_merge(output_dir)
            raise  # Re-raise to allow proper cleanup

        return result

    def _execute_merge(
        self,
        config_path: Path,
        output_dir: Path,
        cuda: bool,
        result: MergeResult,
    ) -> MergeResult:
        """Execute the actual merge command."""
        # Build mergekit-moe command
        cmd = [
            "mergekit-moe",
            str(config_path),
            str(output_dir),
        ]

        if cuda:
            cmd.append("--cuda")

        if self.settings.merge.lazy_unpickle:
            cmd.append("--lazy-unpickle")

        if self.settings.merge.allow_crimes:
            cmd.append("--allow-crimes")

        if self.settings.merge.trust_remote_code:
            cmd.append("--trust-remote-code")

        if self.settings.merge.copy_tokenizer:
            cmd.append("--copy-tokenizer")

        cmd.extend(["--out-shard-size", str(self.settings.merge.out_shard_size)])

        logger.info("executing_merge", command=" ".join(cmd))

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Execute command
        timeout = self.settings.merge.timeout_minutes * 60
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        result.stdout = process.stdout
        result.stderr = process.stderr
        result.end_time = datetime.utcnow()

        if process.returncode != 0:
            result.error = f"mergekit-moe failed with code {process.returncode}: {process.stderr}"
            logger.error(
                "merge_failed",
                return_code=process.returncode,
                stderr=process.stderr[:500],
            )
        else:
            result.success = True
            logger.info(
                "merge_complete",
                output_dir=str(output_dir),
                duration_seconds=result.duration_seconds,
            )

            # Save merge metadata
            self._save_merge_metadata(result)

        return result

    def _save_merge_metadata(self, result: MergeResult) -> None:
        """Save merge metadata to output directory."""
        metadata_path = result.output_dir / "merge_metadata.json"

        with open(metadata_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

        logger.info("metadata_saved", path=str(metadata_path))

    def _cleanup_failed_merge(self, output_dir: Path) -> None:
        """Clean up partial outputs from a failed merge."""
        if output_dir.exists():
            try:
                # Only remove if directory is empty or only contains partial files
                files = list(output_dir.iterdir())
                if not files or all(f.suffix in [".tmp", ".partial"] for f in files):
                    shutil.rmtree(output_dir)
                    logger.info("cleanup_partial_merge", path=str(output_dir))
            except OSError as e:
                logger.warning("cleanup_failed", path=str(output_dir), error=str(e))


class MockMerger:
    """Mock merger for testing without actual mergekit execution."""

    def __init__(self, settings: Settings):
        """
        Initialize mock merger.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.base_path = Path(__file__).parent.parent.parent
        self.merged_dir = self.base_path / settings.paths.merged_dir

    def create_mock_merge(
        self,
        config_path: Path,
        output_dir: Path | None = None,
    ) -> MergeResult:
        """
        Create a mock merged model structure.

        Args:
            config_path: Path to config (for metadata)
            output_dir: Output directory

        Returns:
            MergeResult
        """
        start_time = datetime.utcnow()

        if output_dir is None:
            output_dir = self.merged_dir / "mock_moe"
        output_dir = Path(output_dir)

        result = MergeResult(
            success=False,
            output_dir=output_dir,
            config_path=config_path,
            start_time=start_time,
        )

        try:
            # Load config
            config = load_mergekit_config(config_path)
            num_experts = len(config.get("experts", []))

            # Create mock model directory
            output_dir.mkdir(parents=True, exist_ok=True)

            # Create mock config.json
            mock_config = {
                "model_type": "mixtral",
                "num_local_experts": num_experts,
                "num_experts_per_tok": config.get("experts_per_token", 2),
                "hidden_size": 4096,
                "intermediate_size": 14336,
                "num_hidden_layers": 32,
                "num_attention_heads": 32,
                "vocab_size": 32000,
            }

            with open(output_dir / "config.json", "w") as f:
                json.dump(mock_config, f, indent=2)

            # Create mock tokenizer files
            tokenizer_config = {
                "model_max_length": 32768,
                "tokenizer_class": "LlamaTokenizer",
            }

            with open(output_dir / "tokenizer_config.json", "w") as f:
                json.dump(tokenizer_config, f, indent=2)

            # Create placeholder for model weights
            with open(output_dir / "model.safetensors.index.json", "w") as f:
                json.dump({"weight_map": {}, "metadata": {"mock": True}}, f, indent=2)

            result.success = True
            result.metadata["num_experts"] = num_experts
            result.metadata["mock"] = True

            logger.info(
                "mock_merge_complete",
                output_dir=str(output_dir),
                num_experts=num_experts,
            )

        except (OSError, json.JSONDecodeError, yaml.YAMLError, KeyError) as e:
            result.error = str(e)
            logger.error("mock_merge_failed", error=str(e), exc_type=type(e).__name__)
            # Clean up partial mock output
            if output_dir.exists():
                try:
                    shutil.rmtree(output_dir)
                except OSError:
                    pass

        result.end_time = datetime.utcnow()
        return result


def check_mergekit_available() -> bool:
    """Check if mergekit-moe is available."""
    try:
        result = subprocess.run(
            ["mergekit-moe", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
