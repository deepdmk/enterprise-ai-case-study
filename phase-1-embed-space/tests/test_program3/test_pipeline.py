"""Tests for ingestion sync correctness (watermarks, error handling)."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import numpy as np

from config.settings import DatabaseConfig, IngestionConfig, TableConfig
from src.program3_ingestion.pipeline import IngestionPipeline, IngestionStats, SyncState
from src.shared.database import ExtractedRecord

TABLE = TableConfig(
    name="projects",
    text_columns=["body"],
    id_column="id",
    timestamp_column="updated_at",
)
DB_CONFIG = DatabaseConfig(name="db_a", tables=[TABLE])

LONG_TEXT = (
    "This record body is comfortably longer than the minimum chunk length "
    "so the chunker produces at least one chunk for the pipeline to embed."
)


def make_record(doc_id: str, timestamp) -> ExtractedRecord:
    return ExtractedRecord(
        doc_id=doc_id,
        combined_text=LONG_TEXT,
        source_db="db_a",
        source_table="projects",
        metadata={"timestamp": timestamp},
    )


def make_pipeline(records: list[ExtractedRecord]) -> IngestionPipeline:
    db_manager = MagicMock()
    db_manager.extract_records = AsyncMock(return_value=records)
    db_manager.get_records_since = AsyncMock(return_value=records)

    chromadb_client = MagicMock()

    embedding_manager = MagicMock()
    embedding_manager.model_version = "test-model-v1"
    embedding_manager.encode.side_effect = lambda texts, **kw: np.zeros((len(texts), 4))

    return IngestionPipeline(
        db_manager=db_manager,
        chromadb_client=chromadb_client,
        embedding_manager=embedding_manager,
        config=IngestionConfig(),
    )


class TestMaxRecordTimestamp:
    """Tests for the watermark timestamp helper."""

    def test_string_timestamps(self):
        records = [
            make_record("1", "2024-01-01T00:00:00"),
            make_record("2", "2024-03-01T00:00:00"),
            make_record("3", "2024-02-01T00:00:00"),
        ]
        assert IngestionPipeline._max_record_timestamp(records) == "2024-03-01T00:00:00"

    def test_datetime_timestamps_converted_to_iso(self):
        records = [
            make_record("1", datetime(2024, 1, 1, tzinfo=UTC)),
            make_record("2", datetime(2024, 6, 1, tzinfo=UTC)),
        ]
        result = IngestionPipeline._max_record_timestamp(records)
        assert result == datetime(2024, 6, 1, tzinfo=UTC).isoformat()

    def test_no_timestamps_returns_none(self):
        records = [make_record("1", None)]
        assert IngestionPipeline._max_record_timestamp(records) is None


class TestWatermarkAdvancement:
    """The watermark must come from the data and only advance on success."""

    async def test_watermark_set_to_max_data_timestamp(self):
        records = [
            make_record("1", "2024-02-01T00:00:00"),
            make_record("2", "2024-05-01T00:00:00"),
        ]
        pipeline = make_pipeline(records)
        sync_state = SyncState()
        stats = IngestionStats()

        await pipeline.ingest_database("db_a", DB_CONFIG, stats, sync_state)

        # Not the wall clock: exactly the newest record timestamp
        assert sync_state.get_last_sync("db_a", "projects") == "2024-05-01T00:00:00"

    async def test_watermark_held_on_upsert_failure(self):
        records = [make_record("1", "2024-05-01T00:00:00")]
        pipeline = make_pipeline(records)
        pipeline.chromadb_client.upsert_embeddings.side_effect = RuntimeError("chroma down")
        sync_state = SyncState()
        sync_state.set_last_sync("db_a", "projects", "2024-01-01T00:00:00")
        stats = IngestionStats()

        await pipeline.ingest_database("db_a", DB_CONFIG, stats, sync_state)

        # Errors recorded, watermark unchanged so the records retry next sync
        assert stats.errors
        assert sync_state.get_last_sync("db_a", "projects") == "2024-01-01T00:00:00"

    async def test_incremental_pull_deletes_existing_chunks_first(self):
        """Re-ingested documents purge their old chunks (shrink-safe)."""
        records = [make_record("1", "2024-05-01T00:00:00")]
        pipeline = make_pipeline(records)
        sync_state = SyncState()
        sync_state.set_last_sync("db_a", "projects", "2024-01-01T00:00:00")

        await pipeline.ingest_database("db_a", DB_CONFIG, IngestionStats(), sync_state)

        pipeline.db_manager.get_records_since.assert_awaited_once()
        (where,), _ = pipeline.chromadb_client.delete_by_metadata.call_args
        assert {"parent_doc_id": "1"} in where["$and"]
        assert {"source_db": "db_a"} in where["$and"]

    async def test_full_ingest_does_not_delete(self):
        records = [make_record("1", "2024-05-01T00:00:00")]
        pipeline = make_pipeline(records)

        await pipeline.ingest_database("db_a", DB_CONFIG, IngestionStats(), sync_state=None)

        pipeline.chromadb_client.delete_by_metadata.assert_not_called()


class TestModelVersionTagging:
    """Every chunk records which model embedded it."""

    async def test_chunks_tagged_with_model_version(self):
        pipeline = make_pipeline([])
        record = make_record("1", "2024-01-01T00:00:00")

        ids, embeddings, metadatas = await pipeline.process_record(record)

        assert ids
        assert all(m["embedding_model_version"] == "test-model-v1" for m in metadatas)


class TestReconcile:
    """Reconcile deletes chunks whose source record disappeared."""

    async def test_orphan_chunks_deleted(self):
        pipeline = make_pipeline([])
        pipeline.db_manager.get_all_ids = AsyncMock(return_value={"1", "2"})
        pipeline.chromadb_client.iter_metadata.return_value = iter(
            [
                ("chunk_a", {"parent_doc_id": "1"}),
                ("chunk_b", {"parent_doc_id": "gone"}),
                ("chunk_c", {"parent_doc_id": "2"}),
            ]
        )

        deleted = await pipeline.reconcile({"db_a": DB_CONFIG})

        assert deleted == {"db_a.projects": 1}
        (ids,), _ = pipeline.chromadb_client.delete_by_ids.call_args
        assert ids == ["chunk_b"]
