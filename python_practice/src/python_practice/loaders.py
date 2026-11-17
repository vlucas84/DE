"""Data ingestion and file loader implementations using ABC contracts."""

from abc import ABC, abstractmethod
from collections.abc import Generator
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """Abstract base class defining the contract for data loaders."""

    @abstractmethod
    def load(self, file_path: Path) -> list[dict[str, Any]]:
        """Load and parse entire file into a list of record dictionaries.

        Args:
            file_path: Filesystem path to the input dataset file.

        Returns:
            List of parsed dictionary rows.
        """
        pass

    @abstractmethod
    def load_batches(
        self, file_path: Path, batch_size: int = 1000
    ) -> Generator[list[dict[str, Any]], None, None]:
        """Stream chunks of parsed records using a Python generator.

        Args:
            file_path: Filesystem path to the input dataset file.
            batch_size: Number of records per chunk.

        Yields:
            Batches of parsed dictionary rows.
        """
        pass


class JsonLoader(BaseLoader):
    """Concrete data loader for reading and batching JSON datasets."""

    def load(self, file_path: Path) -> list[dict[str, Any]]:
        """Read and deserialize the entire JSON file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file does not contain a valid JSON array.
        """
        path = Path(file_path)
        if not path.is_file():
            logger.error("Data file does not exist at path: %s", path)
            raise FileNotFoundError(f"File not found: {path}")

        logger.info("Loading JSON dataset from %s", path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            logger.error("Expected JSON array in %s, got %s", path, type(data).__name__)
            raise ValueError(f"JSON root must be a list of records: {path}")

        return data

    def load_batches(
        self, file_path: Path, batch_size: int = 1000
    ) -> Generator[list[dict[str, Any]], None, None]:
        """Stream JSON records in chunks of specified batch_size."""
        records = self.load(file_path)
        total_records = len(records)
        logger.info(
            "Yielding %d records in batches of %d from %s",
            total_records,
            batch_size,
            file_path,
        )

        for i in range(0, total_records, batch_size):
            yield records[i : i + batch_size]