"""JSON storage backend with file locking for thread-safe operations."""

from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime, UTC
from typing import Any
from filelock import FileLock
import structlog

logger = structlog.get_logger(__name__)


class JSONStorage:
    """Thread-safe JSON file storage with file locking."""

    LOCK_TIMEOUT = 10  # seconds

    def __init__(self, file_path: str | Path, auto_create: bool = True):
        """
        Initialize JSON storage.

        Args:
            file_path: Path to JSON file
            auto_create: Create file if doesn't exist
        """
        self.file_path = Path(file_path)
        self.lock_path = self.file_path.with_suffix(self.file_path.suffix + ".lock")
        self.auto_create = auto_create

        # Create parent directories if needed
        if auto_create:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Initialize file with empty data if it doesn't exist
            if not self.file_path.exists():
                self._write_data({})

        logger.info(
            "initialized_json_storage",
            file_path=str(self.file_path),
            auto_create=auto_create,
        )

    def _write_data(self, data: dict[str, Any]) -> None:
        """Write data to file with metadata."""
        storage_data = {
            "version": "1.0",
            "updated_at": datetime.now(UTC).isoformat(),
            "data": data,
        }

        try:
            with open(self.file_path, "w") as f:
                json.dump(storage_data, f, indent=2, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            logger.error(
                "json_encoding_error",
                error=str(e),
                file_path=str(self.file_path),
            )
            raise ValueError(f"Failed to encode data as JSON: {e}") from e

    def _read_data(self) -> dict[str, Any]:
        """Read data from file, extracting the data section."""
        if not self.file_path.exists():
            logger.debug("file_not_found", file_path=str(self.file_path))
            return {}

        try:
            with open(self.file_path, "r") as f:
                storage_data = json.load(f)

            # Handle legacy format (direct data without metadata wrapper)
            if "data" not in storage_data:
                logger.warning(
                    "legacy_format_detected",
                    file_path=str(self.file_path),
                )
                return storage_data

            return storage_data["data"]
        except json.JSONDecodeError as e:
            logger.error(
                "json_decode_error",
                error=str(e),
                file_path=str(self.file_path),
            )
            raise ValueError(f"Failed to decode JSON from file: {e}") from e
        except Exception as e:
            logger.error(
                "read_error",
                error=str(e),
                file_path=str(self.file_path),
            )
            raise

    def load(self) -> dict[str, Any]:
        """
        Load and return all data from file.

        Returns:
            Dictionary containing all stored data. Returns empty dict if file doesn't exist.
        """
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                data = self._read_data()
                logger.debug(
                    "loaded_data",
                    file_path=str(self.file_path),
                    num_keys=len(data),
                )
                return data
        except Exception as e:
            logger.error(
                "load_failed",
                error=str(e),
                file_path=str(self.file_path),
            )
            raise

    def save(self, data: dict[str, Any]) -> None:
        """
        Save data to file with file locking.

        Args:
            data: Dictionary to save
        """
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                self._write_data(data)
                logger.info(
                    "saved_data",
                    file_path=str(self.file_path),
                    num_keys=len(data),
                )
        except Exception as e:
            logger.error(
                "save_failed",
                error=str(e),
                file_path=str(self.file_path),
            )
            raise

    def update(self, key: str, value: Any) -> None:
        """
        Update a single key in the storage.

        Args:
            key: Key to update
            value: Value to set
        """
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                data = self._read_data()
                data[key] = value
                self._write_data(data)
                logger.debug(
                    "updated_key",
                    file_path=str(self.file_path),
                    key=key,
                )
        except Exception as e:
            logger.error(
                "update_failed",
                error=str(e),
                file_path=str(self.file_path),
                key=key,
            )
            raise

    def delete(self, key: str) -> bool:
        """
        Delete a key from storage.

        Args:
            key: Key to delete

        Returns:
            True if key was deleted, False if key not found
        """
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                data = self._read_data()
                if key in data:
                    del data[key]
                    self._write_data(data)
                    logger.debug(
                        "deleted_key",
                        file_path=str(self.file_path),
                        key=key,
                    )
                    return True
                else:
                    logger.debug(
                        "key_not_found",
                        file_path=str(self.file_path),
                        key=key,
                    )
                    return False
        except Exception as e:
            logger.error(
                "delete_failed",
                error=str(e),
                file_path=str(self.file_path),
                key=key,
            )
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a single key from storage.

        Args:
            key: Key to retrieve
            default: Default value if key not found

        Returns:
            Value associated with key, or default if not found
        """
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                data = self._read_data()
                value = data.get(key, default)
                logger.debug(
                    "retrieved_key",
                    file_path=str(self.file_path),
                    key=key,
                    found=key in data,
                )
                return value
        except Exception as e:
            logger.error(
                "get_failed",
                error=str(e),
                file_path=str(self.file_path),
                key=key,
            )
            raise

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in storage.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                data = self._read_data()
                exists = key in data
                logger.debug(
                    "checked_key_existence",
                    file_path=str(self.file_path),
                    key=key,
                    exists=exists,
                )
                return exists
        except Exception as e:
            logger.error(
                "exists_check_failed",
                error=str(e),
                file_path=str(self.file_path),
                key=key,
            )
            raise

    def clear(self) -> None:
        """Clear all data from storage."""
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                self._write_data({})
                logger.info(
                    "cleared_storage",
                    file_path=str(self.file_path),
                )
        except Exception as e:
            logger.error(
                "clear_failed",
                error=str(e),
                file_path=str(self.file_path),
            )
            raise

    def keys(self) -> list[str]:
        """
        Get all keys from storage.

        Returns:
            List of all keys in storage
        """
        lock = FileLock(self.lock_path, timeout=self.LOCK_TIMEOUT)

        try:
            with lock:
                data = self._read_data()
                key_list = list(data.keys())
                logger.debug(
                    "retrieved_keys",
                    file_path=str(self.file_path),
                    num_keys=len(key_list),
                )
                return key_list
        except Exception as e:
            logger.error(
                "keys_retrieval_failed",
                error=str(e),
                file_path=str(self.file_path),
            )
            raise
