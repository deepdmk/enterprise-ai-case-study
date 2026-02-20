"""Tests for JSONStorage."""

import json
import threading

import pytest

from registries.storage import JSONStorage


class TestJSONStorage:
    """Test JSONStorage class."""

    def test_initialization_creates_file(self, temp_storage_dir):
        """Test that initialization creates file and directories."""
        storage_file = temp_storage_dir / "test.json"
        JSONStorage(storage_file)  # Side effect: creates file

        assert storage_file.exists()
        assert storage_file.parent.exists()

    def test_initialization_without_auto_create(self, temp_storage_dir):
        """Test initialization without auto_create."""
        storage_file = temp_storage_dir / "test.json"
        JSONStorage(storage_file, auto_create=False)  # Side effect: no file created

        # File should not exist
        assert not storage_file.exists()

    def test_save_and_load_roundtrip(self, temp_storage_dir):
        """Test save and load roundtrip."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        test_data = {
            "key1": "value1",
            "key2": {"nested": "value2"},
            "key3": [1, 2, 3],
        }

        storage.save(test_data)
        loaded_data = storage.load()

        assert loaded_data == test_data

    def test_update_single_key(self, temp_storage_dir):
        """Test updating a single key."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        # Initial data
        storage.save({"key1": "value1", "key2": "value2"})

        # Update one key
        storage.update("key1", "new_value1")

        # Load and verify
        data = storage.load()
        assert data["key1"] == "new_value1"
        assert data["key2"] == "value2"

    def test_update_adds_new_key(self, temp_storage_dir):
        """Test that update can add new keys."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})
        storage.update("key2", "value2")

        data = storage.load()
        assert "key1" in data
        assert "key2" in data

    def test_delete_existing_key(self, temp_storage_dir):
        """Test deleting an existing key."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1", "key2": "value2"})
        result = storage.delete("key1")

        assert result is True
        data = storage.load()
        assert "key1" not in data
        assert "key2" in data

    def test_delete_nonexistent_key(self, temp_storage_dir):
        """Test deleting a nonexistent key."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})
        result = storage.delete("nonexistent")

        assert result is False

    def test_get_existing_key(self, temp_storage_dir):
        """Test getting an existing key."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})
        value = storage.get("key1")

        assert value == "value1"

    def test_get_nonexistent_key_returns_default(self, temp_storage_dir):
        """Test getting nonexistent key returns default."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})
        value = storage.get("nonexistent", "default_value")

        assert value == "default_value"

    def test_get_nonexistent_key_returns_none(self, temp_storage_dir):
        """Test getting nonexistent key returns None by default."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})
        value = storage.get("nonexistent")

        assert value is None

    def test_exists_for_existing_key(self, temp_storage_dir):
        """Test exists returns True for existing key."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})
        assert storage.exists("key1") is True

    def test_exists_for_nonexistent_key(self, temp_storage_dir):
        """Test exists returns False for nonexistent key."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})
        assert storage.exists("nonexistent") is False

    def test_clear_removes_all_data(self, temp_storage_dir):
        """Test clear removes all data."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1", "key2": "value2", "key3": "value3"})
        storage.clear()

        data = storage.load()
        assert data == {}

    def test_keys_returns_all_keys(self, temp_storage_dir):
        """Test keys returns all keys."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1", "key2": "value2", "key3": "value3"})
        keys = storage.keys()

        assert set(keys) == {"key1", "key2", "key3"}

    def test_keys_returns_empty_list_for_empty_storage(self, temp_storage_dir):
        """Test keys returns empty list for empty storage."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        keys = storage.keys()
        assert keys == []

    def test_storage_format_includes_metadata(self, temp_storage_dir):
        """Test that storage format includes metadata wrapper."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        storage.save({"key1": "value1"})

        # Read raw file
        with open(storage_file) as f:
            raw_data = json.load(f)

        assert "version" in raw_data
        assert "updated_at" in raw_data
        assert "data" in raw_data
        assert raw_data["data"] == {"key1": "value1"}

    def test_legacy_format_compatibility(self, temp_storage_dir):
        """Test that legacy format (without wrapper) is supported."""
        storage_file = temp_storage_dir / "test.json"

        # Write legacy format directly
        legacy_data = {"key1": "value1", "key2": "value2"}
        with open(storage_file, "w") as f:
            json.dump(legacy_data, f)

        # Load with JSONStorage
        storage = JSONStorage(storage_file, auto_create=False)
        data = storage.load()

        assert data == legacy_data

    def test_concurrent_writes_with_file_locking(self, temp_storage_dir):
        """Test that concurrent writes are handled safely with file locking."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        # Number of concurrent threads
        num_threads = 10
        results = []
        errors = []

        def write_data(thread_id):
            try:
                storage.update(f"key_{thread_id}", f"value_{thread_id}")
                results.append(thread_id)
            except Exception as e:
                errors.append((thread_id, str(e)))

        # Start concurrent writes
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=write_data, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Verify no errors
        assert len(errors) == 0, f"Concurrent write errors: {errors}"

        # Verify all data was written
        data = storage.load()
        for i in range(num_threads):
            assert f"key_{i}" in data
            assert data[f"key_{i}"] == f"value_{i}"

    def test_concurrent_reads_with_file_locking(self, temp_storage_dir):
        """Test that concurrent reads work correctly."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        # Initial data
        initial_data = {f"key_{i}": f"value_{i}" for i in range(10)}
        storage.save(initial_data)

        # Number of concurrent threads
        num_threads = 10
        results = []
        errors = []

        def read_data(thread_id):
            try:
                data = storage.load()
                results.append((thread_id, data))
            except Exception as e:
                errors.append((thread_id, str(e)))

        # Start concurrent reads
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=read_data, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Verify no errors
        assert len(errors) == 0, f"Concurrent read errors: {errors}"

        # Verify all reads got the same data
        assert len(results) == num_threads
        for thread_id, data in results:
            assert data == initial_data

    def test_invalid_json_raises_error(self, temp_storage_dir):
        """Test that invalid JSON raises appropriate error."""
        storage_file = temp_storage_dir / "test.json"

        # Write invalid JSON
        with open(storage_file, "w") as f:
            f.write("not valid json {[}")

        storage = JSONStorage(storage_file, auto_create=False)

        with pytest.raises(ValueError, match="Failed to decode JSON"):
            storage.load()

    def test_non_serializable_data_raises_error(self, temp_storage_dir):
        """Test that non-serializable data raises error."""
        storage_file = temp_storage_dir / "test.json"
        storage = JSONStorage(storage_file)

        # Try to save non-serializable data
        class NonSerializable:
            pass

        with pytest.raises(ValueError, match="Failed to encode data as JSON"):
            storage.save({"key": NonSerializable()})

    def test_load_nonexistent_file_returns_empty_dict(self, temp_storage_dir):
        """Test that loading nonexistent file returns empty dict."""
        storage_file = temp_storage_dir / "nonexistent.json"
        storage = JSONStorage(storage_file, auto_create=False)

        data = storage.load()
        assert data == {}
