"""
Text Data Extractor.

Extracts text samples from PostgreSQL databases for training dataset generation.
Uses the placeholder pattern for unknown schemas.
"""

from dataclasses import dataclass

from src.shared.path_config import configure_paths
configure_paths()

from config.settings import DatabaseConfig, TableConfig
from habitat_logging import get_logger

from src.shared.database import DatabaseConnectionManager, ExtractedRecord

logger = get_logger(__name__)


@dataclass
class ExtractionResult:
    """Result of extracting text samples."""

    records: list[ExtractedRecord]
    total_extracted: int
    source_db: str
    source_tables: list[str]


class TextDataExtractor:
    """
    Extracts text samples from configured database tables.

    Supports:
    - Extracting from multiple tables per database
    - Configurable sample limits per table
    - Filtering short/empty text
    """

    def __init__(
        self,
        db_manager: DatabaseConnectionManager,
        min_text_length: int = 50,
    ):
        """
        Initialize the text extractor.

        Args:
            db_manager: Database connection manager.
            min_text_length: Minimum text length to include.
        """
        self.db_manager = db_manager
        self.min_text_length = min_text_length

    async def extract_from_table(
        self,
        db_name: str,
        table_config: TableConfig,
        limit: int | None = None,
    ) -> list[ExtractedRecord]:
        """
        Extract text samples from a single table.

        Args:
            db_name: Name of the database.
            table_config: Table configuration.
            limit: Maximum records to extract.

        Returns:
            List of extracted records.
        """
        logger.info(
            "extracting_from_table",
            db=db_name,
            table=table_config.name,
            limit=limit,
        )

        records = await self.db_manager.extract_records(
            db_name=db_name,
            table_config=table_config,
            limit=limit,
        )

        # Filter by minimum text length
        filtered = [r for r in records if len(r.combined_text) >= self.min_text_length]

        logger.info(
            "extraction_complete",
            db=db_name,
            table=table_config.name,
            extracted=len(filtered),
            filtered_out=len(records) - len(filtered),
        )

        return filtered

    async def extract_from_database(
        self,
        db_name: str,
        db_config: DatabaseConfig,
        samples_per_table: int | None = None,
    ) -> ExtractionResult:
        """
        Extract text samples from all configured tables in a database.

        Args:
            db_name: Name of the database.
            db_config: Database configuration with table configs.
            samples_per_table: Maximum samples per table.

        Returns:
            ExtractionResult with all extracted records.
        """
        all_records = []
        tables_processed = []

        for table_config in db_config.tables:
            try:
                records = await self.extract_from_table(
                    db_name=db_name,
                    table_config=table_config,
                    limit=samples_per_table,
                )
                all_records.extend(records)
                tables_processed.append(table_config.name)
            except Exception as e:
                logger.error(
                    "table_extraction_failed",
                    db=db_name,
                    table=table_config.name,
                    error=str(e),
                )

        return ExtractionResult(
            records=all_records,
            total_extracted=len(all_records),
            source_db=db_name,
            source_tables=tables_processed,
        )

    async def extract_all(
        self,
        databases: dict[str, DatabaseConfig],
        samples_per_table: int | None = None,
    ) -> list[ExtractedRecord]:
        """
        Extract text samples from all configured databases.

        Args:
            databases: Dictionary of database configurations.
            samples_per_table: Maximum samples per table.

        Returns:
            Combined list of all extracted records.
        """
        all_records = []

        for db_name, db_config in databases.items():
            try:
                result = await self.extract_from_database(
                    db_name=db_name,
                    db_config=db_config,
                    samples_per_table=samples_per_table,
                )
                all_records.extend(result.records)
                logger.info(
                    "database_extraction_complete",
                    db=db_name,
                    tables=result.source_tables,
                    total=result.total_extracted,
                )
            except Exception as e:
                logger.error(
                    "database_extraction_failed",
                    db=db_name,
                    error=str(e),
                )

        logger.info("all_extraction_complete", total_records=len(all_records))
        return all_records


def generate_mock_samples(
    num_samples: int = 1000,
    source_db: str = "mock_db",
    source_table: str = "mock_table",
) -> list[ExtractedRecord]:
    """
    Generate mock text samples for testing without a database.

    Args:
        num_samples: Number of samples to generate.
        source_db: Name for the mock database.
        source_table: Name for the mock table.

    Returns:
        List of mock ExtractedRecord objects.
    """
    import random

    # Sample topics and content templates
    topics = [
        "climate change adaptation",
        "sustainable agriculture",
        "renewable energy",
        "water resource management",
        "biodiversity conservation",
        "urban development",
        "public health initiatives",
        "education programs",
        "economic development",
        "disaster risk reduction",
    ]

    regions = [
        "East Africa",
        "West Africa",
        "South Asia",
        "Southeast Asia",
        "Latin America",
        "Caribbean",
        "Middle East",
        "Central Asia",
        "Pacific Islands",
        "Sub-Saharan Africa",
    ]

    templates = [
        "The {topic} program in {region} has shown significant progress. Initial assessments indicate that community engagement has been strong, with over {num} participants actively involved in the initiative. Key challenges include infrastructure limitations and funding constraints, but the team has developed innovative solutions to address these issues.",
        "Funding opportunities for {topic} in {region} continue to expand. Recent grants from international donors have enabled the scaling of successful pilot projects. The {num}-month implementation timeline allows for comprehensive monitoring and evaluation of outcomes.",
        "Research findings on {topic} demonstrate the importance of local context in {region}. The study involved {num} communities and revealed that integrated approaches yield better results than siloed interventions. Recommendations include increased stakeholder consultation and adaptive management strategies.",
        "The annual report on {topic} activities in {region} highlights key achievements and lessons learned. Despite challenges posed by the global situation, the program reached {num} beneficiaries and established partnerships with local organizations. Future plans include expansion to neighboring regions.",
        "Technical assessment of {topic} interventions in {region} provides evidence of positive impact. Quantitative indicators show a {num}% improvement in target metrics compared to baseline measurements. Qualitative feedback from beneficiaries suggests high satisfaction with program delivery.",
    ]

    records = []
    for i in range(num_samples):
        topic = random.choice(topics)
        region = random.choice(regions)

        # Combine multiple paragraphs to create longer documents (for chunking)
        num_paragraphs = random.randint(3, 5)
        paragraphs = []
        for _ in range(num_paragraphs):
            template = random.choice(templates)
            num = random.randint(50, 5000)
            paragraphs.append(template.format(topic=topic, region=region, num=num))

        text = "\n\n".join(paragraphs)

        records.append(
            ExtractedRecord(
                doc_id=f"doc_{i:06d}",
                combined_text=text,
                source_db=source_db,
                source_table=source_table,
                metadata={
                    "topic": topic,
                    "region": region,
                    "category": random.choice(["report", "proposal", "assessment", "study"]),
                },
            )
        )

    return records
