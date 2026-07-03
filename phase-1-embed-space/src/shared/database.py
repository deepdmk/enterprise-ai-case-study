"""
PostgreSQL Database Connection Manager.

Provides async connection pooling and query execution for multiple PostgreSQL databases.
Supports the placeholder pattern for unknown schemas with schema discovery capabilities.
"""

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator

import asyncpg

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import DatabaseConfig, TableConfig
from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


def quote_identifier(name: str) -> str:
    """Quote a config-sourced SQL identifier (double internal quotes)."""
    return '"' + name.replace('"', '""') + '"'


@dataclass
class ColumnInfo:
    """Information about a database column."""

    name: str
    data_type: str
    is_nullable: bool = True


@dataclass
class TableSchema:
    """Schema information for a database table."""

    name: str
    columns: list[ColumnInfo]

    def get_text_columns(self) -> list[str]:
        """Get columns that likely contain text data."""
        text_types = {"text", "varchar", "character varying", "char", "character"}
        return [col.name for col in self.columns if col.data_type.lower() in text_types]


@dataclass
class ExtractedRecord:
    """A record extracted from the database."""

    doc_id: str
    combined_text: str
    source_db: str
    source_table: str
    metadata: dict[str, Any]


class DatabaseConnectionManager:
    """
    Manages connections to multiple PostgreSQL databases with connection pooling.

    Supports:
    - Async connection pooling per database
    - Query execution with automatic retry
    - Schema discovery for unknown tables
    - Streaming records for large datasets
    """

    def __init__(self, databases: dict[str, DatabaseConfig]):
        """
        Initialize the connection manager.

        Args:
            databases: Dictionary mapping database names to their configurations.
        """
        self.configs = databases
        self._pools: dict[str, asyncpg.Pool] = {}
        self._initialized = False

    async def initialize(self, max_retries: int = 3, base_delay: float = 2.0) -> None:
        """Initialize connection pools for all configured databases.

        Args:
            max_retries: Maximum retry attempts per database connection
            base_delay: Base delay in seconds between retries (exponential backoff)
        """
        if self._initialized:
            return

        for db_name, config in self.configs.items():
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    pool = await asyncpg.create_pool(
                        host=config.host,
                        port=int(config.port),
                        database=config.name,
                        user=config.user,
                        password=config.password,
                        min_size=1,
                        max_size=config.pool_size,
                    )
                    self._pools[db_name] = pool
                    logger.info("database_pool_created", db_name=db_name, pool_size=config.pool_size)
                    break
                except (OSError, ConnectionError, asyncpg.PostgresError) as e:
                    last_error = e
                    if attempt < max_retries:
                        import asyncio
                        delay = base_delay * (2 ** (attempt - 1))
                        logger.warning(
                            "database_connection_retry",
                            db_name=db_name,
                            attempt=attempt,
                            max_retries=max_retries,
                            delay=delay,
                            error=str(e),
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            "database_pool_creation_failed",
                            db_name=db_name,
                            attempts=max_retries,
                            error=str(e),
                        )
                        raise

        self._initialized = True

    async def close(self) -> None:
        """Close all connection pools."""
        for db_name, pool in self._pools.items():
            await pool.close()
            logger.info("database_pool_closed", db_name=db_name)
        self._pools.clear()
        self._initialized = False

    @asynccontextmanager
    async def get_connection(self, db_name: str) -> AsyncIterator[asyncpg.Connection]:
        """
        Get a connection from the pool for the specified database.

        Args:
            db_name: Name of the database (key in configs dict).

        Yields:
            An asyncpg connection.
        """
        if db_name not in self._pools:
            raise ValueError(f"Unknown database: {db_name}")

        async with self._pools[db_name].acquire() as conn:
            yield conn

    async def execute_query(
        self, db_name: str, query: str, params: list[Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Execute a query and return results as list of dicts.

        Args:
            db_name: Name of the database.
            query: SQL query to execute.
            params: Query parameters.

        Returns:
            List of records as dictionaries.
        """
        async with self.get_connection(db_name) as conn:
            if params:
                rows = await conn.fetch(query, *params)
            else:
                rows = await conn.fetch(query)
            return [dict(row) for row in rows]

    async def stream_records(
        self, db_name: str, query: str, params: list[Any] | None = None, batch_size: int = 100
    ) -> AsyncIterator[list[dict[str, Any]]]:
        """
        Stream records from a query in batches.

        Args:
            db_name: Name of the database.
            query: SQL query to execute.
            params: Query parameters.
            batch_size: Number of records per batch.

        Yields:
            Batches of records as dictionaries.
        """
        async with self.get_connection(db_name) as conn:
            # Use a cursor for streaming
            async with conn.transaction():
                if params:
                    cursor = await conn.cursor(query, *params)
                else:
                    cursor = await conn.cursor(query)

                while True:
                    rows = await cursor.fetch(batch_size)
                    if not rows:
                        break
                    yield [dict(row) for row in rows]

    async def discover_schema(self, db_name: str) -> dict[str, TableSchema]:
        """
        Discover table schemas for a database.

        Useful for initial setup when actual schemas are unknown.

        Args:
            db_name: Name of the database.

        Returns:
            Dictionary mapping table names to their schemas.
        """
        query = """
        SELECT
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
        """
        rows = await self.execute_query(db_name, query)

        schemas: dict[str, TableSchema] = {}
        for row in rows:
            table_name = row["table_name"]
            if table_name not in schemas:
                schemas[table_name] = TableSchema(name=table_name, columns=[])
            schemas[table_name].columns.append(
                ColumnInfo(
                    name=row["column_name"],
                    data_type=row["data_type"],
                    is_nullable=row["is_nullable"] == "YES",
                )
            )

        return schemas

    def _build_select_query(
        self,
        table_config: TableConfig,
        since: bool = False,
        limit: int | None = None,
    ) -> tuple[str, list[Any]]:
        """
        Build the shared extraction SELECT for a table.

        Args:
            table_config: Configuration for the table.
            since: If True, filter on timestamp > $1 (incremental sync) and
                order ascending; otherwise order descending (newest first).
            limit: Optional limit, passed as a query parameter.

        Returns:
            (query, params) — params ordered to match the placeholders.
        """
        text_cols = [quote_identifier(col) for col in table_config.text_columns]
        id_col = quote_identifier(table_config.id_column)
        ts_col = quote_identifier(table_config.timestamp_column)
        meta_cols = [quote_identifier(col) for col in table_config.additional_metadata]

        # Combine text columns with COALESCE for NULL handling
        text_expression = " || ' ' || ".join(f"COALESCE({col}::text, '')" for col in text_cols)

        select_parts = [
            f"{id_col} AS doc_id",
            f"({text_expression}) AS combined_text",
            f"{ts_col} AS timestamp",
        ]
        select_parts.extend(meta_cols)

        params: list[Any] = []
        where_clauses = []
        if since:
            # Cast the ISO-string parameter: asyncpg does not coerce str to timestamp
            params.append(None)  # placeholder value filled in by caller
            where_clauses.append(f"{ts_col} > ${len(params)}::timestamptz")
        where_clauses.append(f"LENGTH({text_expression}) > 50")

        query = f"""
        SELECT {', '.join(select_parts)}
        FROM {quote_identifier(table_config.name)}
        WHERE {' AND '.join(where_clauses)}
        ORDER BY {ts_col} {'ASC' if since else 'DESC'}
        """

        if limit:
            params.append(limit)
            query += f" LIMIT ${len(params)}"

        return query, params

    def build_extraction_query(
        self, table_config: TableConfig, limit: int | None = None
    ) -> tuple[str, list[Any]]:
        """
        Build a SQL query to extract text data from a table.

        Uses the placeholder pattern - columns defined in config.

        Args:
            table_config: Configuration for the table.
            limit: Optional limit on number of records.

        Returns:
            (query, params) tuple for execute_query.
        """
        return self._build_select_query(table_config, since=False, limit=limit)

    def _rows_to_records(
        self, rows: list[dict[str, Any]], db_name: str, table_config: TableConfig
    ) -> list[ExtractedRecord]:
        """Convert query rows into ExtractedRecords."""
        records = []
        for row in rows:
            metadata = {
                col: row.get(col) for col in table_config.additional_metadata if col in row
            }
            metadata["timestamp"] = row.get("timestamp")

            records.append(
                ExtractedRecord(
                    doc_id=str(row["doc_id"]),
                    combined_text=row["combined_text"],
                    source_db=db_name,
                    source_table=table_config.name,
                    metadata=metadata,
                )
            )
        return records

    async def extract_records(
        self,
        db_name: str,
        table_config: TableConfig,
        limit: int | None = None,
    ) -> list[ExtractedRecord]:
        """
        Extract records from a table using the placeholder pattern.

        Args:
            db_name: Name of the database.
            table_config: Configuration for the table.
            limit: Optional limit on number of records.

        Returns:
            List of extracted records.
        """
        query, params = self.build_extraction_query(table_config, limit)
        rows = await self.execute_query(db_name, query, params or None)
        return self._rows_to_records(rows, db_name, table_config)

    async def get_record_by_id(
        self, db_name: str, table_config: TableConfig, doc_id: str
    ) -> dict[str, Any] | None:
        """
        Fetch a single record by its ID (for parent document retrieval).

        Args:
            db_name: Name of the database.
            table_config: Configuration for the table.
            doc_id: Document ID to fetch.

        Returns:
            Record as dictionary, or None if not found.
        """
        # Cast the id column to text: the config column may be int-typed and
        # asyncpg will not coerce a str parameter to match
        query = f"""
        SELECT *
        FROM {quote_identifier(table_config.name)}
        WHERE {quote_identifier(table_config.id_column)}::text = $1
        """
        rows = await self.execute_query(db_name, query, [doc_id])
        return rows[0] if rows else None

    async def get_all_ids(self, db_name: str, table_config: TableConfig) -> set[str]:
        """
        Fetch every record ID in a table (for the nightly reconcile pass).

        Args:
            db_name: Name of the database.
            table_config: Configuration for the table.

        Returns:
            Set of all IDs, as strings.
        """
        query = f"""
        SELECT {quote_identifier(table_config.id_column)}::text AS doc_id
        FROM {quote_identifier(table_config.name)}
        """
        rows = await self.execute_query(db_name, query)
        return {row["doc_id"] for row in rows}

    async def get_records_since(
        self,
        db_name: str,
        table_config: TableConfig,
        since_timestamp: str,
        limit: int | None = None,
    ) -> list[ExtractedRecord]:
        """
        Get records modified since a given timestamp (for incremental sync).

        Args:
            db_name: Name of the database.
            table_config: Configuration for the table.
            since_timestamp: ISO format timestamp.
            limit: Optional limit on number of records.

        Returns:
            List of extracted records modified since the timestamp.
        """
        query, params = self._build_select_query(table_config, since=True, limit=limit)
        params[0] = since_timestamp
        rows = await self.execute_query(db_name, query, params)
        return self._rows_to_records(rows, db_name, table_config)


class MockDatabaseManager(DatabaseConnectionManager):
    """
    Mock database manager for testing without real PostgreSQL connections.

    Generates synthetic data that mimics the expected structure.
    """

    def __init__(self, databases: dict[str, DatabaseConfig]):
        super().__init__(databases)
        self._mock_data: dict[str, dict[str, list[dict]]] = {}

    async def initialize(self, *args: Any, **kwargs: Any) -> None:
        """Initialize with mock data (no actual connections)."""
        self._initialized = True
        logger.info("mock_database_initialized")

    async def close(self) -> None:
        """Close mock manager."""
        self._initialized = False

    def add_mock_data(self, db_name: str, table_name: str, records: list[dict]) -> None:
        """Add mock data for testing."""
        if db_name not in self._mock_data:
            self._mock_data[db_name] = {}
        self._mock_data[db_name][table_name] = records

    async def extract_records(
        self,
        db_name: str,
        table_config: TableConfig,
        limit: int | None = None,
    ) -> list[ExtractedRecord]:
        """Extract mock records."""
        table_data = self._mock_data.get(db_name, {}).get(table_config.name, [])

        if limit:
            table_data = table_data[:limit]

        records = []
        for row in table_data:
            # Combine text columns exactly like the SQL builder: every column
            # contributes (empty string for NULL), joined with single spaces
            combined = " ".join(
                "" if row.get(col) is None else str(row.get(col))
                for col in table_config.text_columns
            )

            metadata = {col: row.get(col) for col in table_config.additional_metadata}
            metadata["timestamp"] = row.get(table_config.timestamp_column)

            records.append(
                ExtractedRecord(
                    doc_id=str(row.get(table_config.id_column, "")),
                    combined_text=combined,
                    source_db=db_name,
                    source_table=table_config.name,
                    metadata=metadata,
                )
            )

        return records

    async def get_records_since(
        self,
        db_name: str,
        table_config: TableConfig,
        since_timestamp: str,
        limit: int | None = None,
    ) -> list[ExtractedRecord]:
        """Extract mock records newer than the watermark."""
        records = await self.extract_records(db_name, table_config, limit=None)
        newer = [
            r
            for r in records
            if r.metadata.get("timestamp") is not None
            and str(r.metadata["timestamp"]) > since_timestamp
        ]
        if limit:
            newer = newer[:limit]
        return newer

    async def get_record_by_id(
        self, db_name: str, table_config: TableConfig, doc_id: str
    ) -> dict[str, Any] | None:
        """Fetch mock record by ID."""
        table_data = self._mock_data.get(db_name, {}).get(table_config.name, [])
        for row in table_data:
            if str(row.get(table_config.id_column)) == doc_id:
                return row
        return None

    async def get_all_ids(self, db_name: str, table_config: TableConfig) -> set[str]:
        """Fetch all mock record IDs."""
        table_data = self._mock_data.get(db_name, {}).get(table_config.name, [])
        return {str(row.get(table_config.id_column)) for row in table_data}
