"""Base settings classes for all phase configurations.

This module provides base Pydantic settings classes that are used
across all phases of the emergent-enterprise-ai project.
"""

from pathlib import Path
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class HabitatBaseSettings(BaseSettings):
    """Base settings class for all phase configurations.

    Provides common configuration options like test mode, data directories,
    and logging settings. All phase-specific settings should inherit from this.

    Attributes:
        test_mode: Enable test mode (also reads from PHASE0_TEST_MODE env var)
        data_dir: Root directory for data storage
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log output format (console, json)
    """

    test_mode: bool = Field(
        default=False,
        description="Enable test mode",
        validation_alias="PHASE0_TEST_MODE"
    )
    data_dir: Path = Field(
        default=Path("./data"),
        description="Root directory for data storage"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    log_format: str = Field(
        default="console",
        description="Log output format (console or json)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix=""
    )


class PhaseSettings(HabitatBaseSettings):
    """Phase-specific settings that extend the base configuration.

    Adds phase-specific attributes like phase number, unit, and registry
    directory paths.

    Attributes:
        phase: Phase number (1-5)
        unit: Optional unit identifier within the phase
        registry_dir: Directory for phase registry (computed from data_dir)
    """

    phase: int = Field(
        description="Phase number (1-5)",
        ge=1,
        le=5
    )
    unit: str | None = Field(
        default=None,
        description="Optional unit identifier"
    )

    @computed_field
    @property
    def registry_dir(self) -> Path:
        """Compute registry directory from data_dir if not explicitly set.

        Returns:
            Path to the registry directory for this phase
        """
        return self.data_dir / "registry"
