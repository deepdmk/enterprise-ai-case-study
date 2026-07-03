"""
Ingestion Pipeline.

Orchestrates the full ingestion workflow:
1. Extract records from PostgreSQL databases
2. Chunk text
3. Extract metadata
4. Generate embeddings
5. Store in ChromaDB (embeddings + metadata only, NOT text)
"""

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tqdm import tqdm

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import DatabaseConfig, IngestionConfig
from phase0_infra.habitat_logging import get_logger

from src.shared.chromadb_client import ChromaDBClient
from src.shared.chunking import TextChunker
from src.shared.database import DatabaseConnectionManager, ExtractedRecord
from src.shared.embedding_model import EmbeddingModelManager

from .metadata_extractor import MetadataExtractor

logger = get_logger(__name__)


@dataclass
class IngestionStats:
    """Statistics for an ingestion run."""

    total_records: int = 0
    total_chunks: int = 0
    total_embeddings: int = 0
    records_by_db: dict[str, int] = field(default_factory=dict)
    chunks_by_db: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0


@dataclass
class SyncState:
    """State for incremental sync."""

    last_sync: dict[str, dict[str, str]] = field(default_factory=dict)  # db -> table -> timestamp

    def get_last_sync(self, db_name: str, table_name: str) -> str | None:
        """Get last sync timestamp for a table."""
        return self.last_sync.get(db_name, {}).get(table_name)

    def set_last_sync(self, db_name: str, table_name: str, timestamp: str) -> None:
        """Set last sync timestamp for a table."""
        if db_name not in self.last_sync:
            self.last_sync[db_name] = {}
        self.last_sync[db_name][table_name] = timestamp

    def save(self, path: str | Path) -> None:
        """Save state to file."""
        with open(path, "w") as f:
            json.dump({"last_sync": self.last_sync}, f, indent=2)

    @classmethod
    def load(cls, path: str | Path) -> "SyncState":
        """Load state from file."""
        path = Path(path)
        if not path.exists():
            return cls()
        with open(path) as f:
            data = json.load(f)
        return cls(last_sync=data.get("last_sync", {}))


class IngestionPipeline:
    """
    Main ingestion pipeline for populating ChromaDB.

    IMPORTANT: This pipeline stores ONLY embeddings and metadata in ChromaDB.
    The actual chunk text is NOT stored. Parent documents are retrieved
    from source databases at query time.
    """

    def __init__(
        self,
        db_manager: DatabaseConnectionManager,
        chromadb_client: ChromaDBClient,
        embedding_manager: EmbeddingModelManager,
        config: IngestionConfig,
    ):
        """
        Initialize the ingestion pipeline.

        Args:
            db_manager: Database connection manager.
            chromadb_client: ChromaDB client.
            embedding_manager: Embedding model manager.
            config: Ingestion configuration.
        """
        self.db_manager = db_manager
        self.chromadb_client = chromadb_client
        self.embedding_manager = embedding_manager
        self.config = config

        # Initialize components
        self.chunker = TextChunker(
            chunk_size=config.chunking.chunk_size,
            chunk_overlap=config.chunking.chunk_overlap,
            strategy=config.chunking.strategy,
        )
        self.metadata_extractor = MetadataExtractor()

    async def process_record(
        self,
        record: ExtractedRecord,
    ) -> tuple[list[str], list[list[float]], list[dict[str, Any]]]:
        """
        Process a single record: chunk, extract metadata, generate embeddings.

        Args:
            record: Extracted record from database.

        Returns:
            Tuple of (chunk_ids, embeddings, metadatas).
        """
        # Chunk the text
        chunks = self.chunker.chunk_text(record.combined_text)

        if not chunks:
            return [], [], []

        # Extract metadata for each chunk
        chunk_metadatas = self.metadata_extractor.extract_from_document_chunks(
            chunks=chunks,
            doc_id=record.doc_id,
            source_db=record.source_db,
            source_table=record.source_table,
            additional_metadata=record.metadata,
        )

        # Generate embeddings for chunk texts
        chunk_texts = [c.text for c in chunks]
        embeddings = self.embedding_manager.encode(chunk_texts, show_progress=False)

        # Prepare for ChromaDB
        ids = [m.chunk_id for m in chunk_metadatas]
        embedding_lists = [emb.tolist() for emb in embeddings]
        metadata_dicts = [m.to_dict() for m in chunk_metadatas]

        # Tag which model produced these embeddings so the search app can
        # detect stale vectors after a model retrain
        model_version = self.embedding_manager.model_version
        for metadata in metadata_dicts:
            metadata["embedding_model_version"] = model_version

        return ids, embedding_lists, metadata_dicts

    async def process_batch(
        self,
        records: list[ExtractedRecord],
        stats: IngestionStats,
        replace_existing: bool = False,
    ) -> None:
        """
        Process a batch of records and upsert to ChromaDB.

        Args:
            records: List of records to process.
            stats: Statistics tracker.
            replace_existing: If True (incremental re-ingest), delete each
                document's existing chunks first so documents that shrank
                don't leave orphan chunks behind.
        """
        all_ids = []
        all_embeddings = []
        all_metadatas = []

        for record in records:
            try:
                ids, embeddings, metadatas = await self.process_record(record)

                if replace_existing:
                    self.chromadb_client.delete_by_metadata(
                        {
                            "$and": [
                                {"parent_doc_id": str(record.doc_id)},
                                {"source_db": record.source_db},
                                {"source_table": record.source_table},
                            ]
                        }
                    )

                all_ids.extend(ids)
                all_embeddings.extend(embeddings)
                all_metadatas.extend(metadatas)

                # Update stats
                if record.source_db not in stats.chunks_by_db:
                    stats.chunks_by_db[record.source_db] = 0
                stats.chunks_by_db[record.source_db] += len(ids)

            except Exception as e:
                error_msg = f"Error processing record {record.doc_id}: {str(e)}"
                logger.error("record_processing_error", doc_id=record.doc_id, error=str(e))
                stats.errors.append(error_msg)

        # Upsert to ChromaDB
        if all_ids:
            try:
                self.chromadb_client.upsert_embeddings(
                    ids=all_ids,
                    embeddings=all_embeddings,
                    metadatas=all_metadatas,
                )
            except Exception as e:
                error_msg = f"Error upserting batch of {len(all_ids)} chunks: {str(e)}"
                logger.error("batch_upsert_error", chunks=len(all_ids), error=str(e))
                stats.errors.append(error_msg)
                return
            stats.total_chunks += len(all_ids)
            stats.total_embeddings += len(all_ids)

    async def ingest_database(
        self,
        db_name: str,
        db_config: DatabaseConfig,
        stats: IngestionStats,
        sync_state: SyncState | None = None,
    ) -> None:
        """
        Ingest all tables from a database.

        Args:
            db_name: Database name.
            db_config: Database configuration.
            stats: Statistics tracker.
            sync_state: Optional sync state for incremental ingestion.
        """
        for table_config in db_config.tables:
            logger.info(
                "ingesting_table",
                db=db_name,
                table=table_config.name,
            )

            try:
                # Extract records
                incremental_pull = False
                if sync_state and self.config.incremental.enabled:
                    last_sync = sync_state.get_last_sync(db_name, table_config.name)
                    if last_sync:
                        records = await self.db_manager.get_records_since(
                            db_name=db_name,
                            table_config=table_config,
                            since_timestamp=last_sync,
                        )
                        incremental_pull = True
                    else:
                        records = await self.db_manager.extract_records(
                            db_name=db_name,
                            table_config=table_config,
                        )
                else:
                    records = await self.db_manager.extract_records(
                        db_name=db_name,
                        table_config=table_config,
                    )

                if not records:
                    logger.info("no_records_found", db=db_name, table=table_config.name)
                    continue

                # Update stats
                stats.total_records += len(records)
                if db_name not in stats.records_by_db:
                    stats.records_by_db[db_name] = 0
                stats.records_by_db[db_name] += len(records)

                # Process in batches
                errors_before = len(stats.errors)
                batch_size = self.config.batch_size
                for i in tqdm(
                    range(0, len(records), batch_size),
                    desc=f"Processing {db_name}.{table_config.name}",
                ):
                    batch = records[i : i + batch_size]
                    await self.process_batch(batch, stats, replace_existing=incremental_pull)

                # Advance the watermark to the newest *data* timestamp seen, and
                # only when every record in the table landed — otherwise the
                # failed records would be silently skipped on the next sync
                if sync_state:
                    if len(stats.errors) > errors_before:
                        logger.warning(
                            "sync_watermark_held",
                            db=db_name,
                            table=table_config.name,
                            errors=len(stats.errors) - errors_before,
                        )
                    else:
                        max_timestamp = self._max_record_timestamp(records)
                        if max_timestamp:
                            sync_state.set_last_sync(db_name, table_config.name, max_timestamp)

                logger.info(
                    "table_ingestion_complete",
                    db=db_name,
                    table=table_config.name,
                    records=len(records),
                )

            except Exception as e:
                error_msg = f"Error ingesting {db_name}.{table_config.name}: {str(e)}"
                logger.error("table_ingestion_error", db=db_name, table=table_config.name, error=str(e))
                stats.errors.append(error_msg)

    @staticmethod
    def _max_record_timestamp(records: list[ExtractedRecord]) -> str | None:
        """Newest source timestamp among the records, as an ISO string."""
        timestamps = []
        for record in records:
            ts = record.metadata.get("timestamp")
            if ts is None:
                continue
            timestamps.append(ts.isoformat() if isinstance(ts, datetime) else str(ts))
        return max(timestamps) if timestamps else None

    async def reconcile(self, databases: dict[str, DatabaseConfig]) -> dict[str, int]:
        """
        Remove ChromaDB chunks whose parent record no longer exists in the
        source database. Intended to run nightly — incremental sync never
        observes deletes, so this pass is what propagates them.

        Args:
            databases: Database configurations.

        Returns:
            Mapping of "db.table" to number of chunks deleted.
        """
        self.chromadb_client.get_or_create_collection()
        deleted_by_table: dict[str, int] = {}

        for db_name, db_config in databases.items():
            for table_config in db_config.tables:
                source_ids = await self.db_manager.get_all_ids(db_name, table_config)

                orphan_chunk_ids = [
                    chunk_id
                    for chunk_id, metadata in self.chromadb_client.iter_metadata(
                        where={
                            "$and": [
                                {"source_db": db_name},
                                {"source_table": table_config.name},
                            ]
                        }
                    )
                    if metadata.get("parent_doc_id") not in source_ids
                ]

                if orphan_chunk_ids:
                    self.chromadb_client.delete_by_ids(orphan_chunk_ids)

                deleted_by_table[f"{db_name}.{table_config.name}"] = len(orphan_chunk_ids)
                logger.info(
                    "reconcile_table_complete",
                    db=db_name,
                    table=table_config.name,
                    source_records=len(source_ids),
                    orphan_chunks_deleted=len(orphan_chunk_ids),
                )

        return deleted_by_table

    async def run(
        self,
        databases: dict[str, DatabaseConfig],
        incremental: bool = False,
    ) -> IngestionStats:
        """
        Run the full ingestion pipeline.

        Args:
            databases: Database configurations.
            incremental: Whether to run incremental sync.

        Returns:
            IngestionStats with results.
        """
        start_time = datetime.now(UTC)
        stats = IngestionStats()

        # Load sync state if incremental
        sync_state = None
        if incremental and self.config.incremental.enabled:
            sync_state = SyncState.load(self.config.incremental.state_file)

        # Ensure collection exists
        self.chromadb_client.get_or_create_collection()

        # Load embedding model
        self.embedding_manager.load_model()

        # Process each database
        for db_name, db_config in databases.items():
            logger.info("ingesting_database", db=db_name)
            await self.ingest_database(db_name, db_config, stats, sync_state)

        # Save sync state
        if sync_state:
            state_path = Path(self.config.incremental.state_file)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            sync_state.save(state_path)

        # Calculate duration
        stats.duration_seconds = (datetime.now(UTC) - start_time).total_seconds()

        logger.info(
            "ingestion_complete",
            total_records=stats.total_records,
            total_chunks=stats.total_chunks,
            duration_seconds=stats.duration_seconds,
            errors=len(stats.errors),
        )

        return stats
