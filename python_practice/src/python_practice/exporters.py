"""Data export implementations and factory using ABC contracts."""

from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import Decimal
import json
import logging
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def _json_serial_fallback(obj: Any) -> Any:
    """Serialize dates and Decimals that PostgreSQL drivers commonly return."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj).__name__} is not JSON serializable")


class BaseExporter(ABC):
    """Abstract base class defining the contract for data exporters."""

    @abstractmethod
    def export(self, data: list[dict[str, Any]], destination: Path) -> Path:
        """Export dataset to the destination file path.

        Args:
            data: List of dictionary records to serialize.
            destination: Target file path on disk.

        Returns:
            Resolved Path to the created output file.
        """
        pass


class JsonExporter(BaseExporter):
    """Concrete exporter for formatting records into pretty-printed JSON."""

    def export(self, data: list[dict[str, Any]], destination: Path) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Exporting %d records to JSON at %s", len(data), path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
                default=_json_serial_fallback,
            )

        return path


class XmlExporter(BaseExporter):
    """Concrete exporter for formatting records into an XML document."""

    def export(self, data: list[dict[str, Any]], destination: Path) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Exporting %d records to XML at %s", len(data), path)

        root = ET.Element("results")
        for row in data:
            item = ET.SubElement(root, "item")
            for key, value in row.items():
                child = ET.SubElement(item, str(key))
                if value is None:
                    child.text = ""
                elif isinstance(value, (datetime, date)):
                    child.text = value.isoformat()
                else:
                    child.text = str(value)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")

        with path.open("wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

        return path


# Реестр доступных форматов экспорта
_EXPORTER_REGISTRY: dict[str, type[BaseExporter]] = {
    "json": JsonExporter,
    "xml": XmlExporter,
}


def get_exporter(format_name: str) -> BaseExporter:
    """Factory function to instantiate an exporter based on requested format.

    Args:
        format_name: Name of format, case-insensitive (e.g. 'json', 'xml').

    Returns:
        Instance of a concrete BaseExporter class.

    Raises:
        ValueError: If format_name is not supported.
    """
    normalized_format = format_name.strip().lower()
    exporter_cls = _EXPORTER_REGISTRY.get(normalized_format)

    if exporter_cls is None:
        supported = ", ".join(f"'{k}'" for k in _EXPORTER_REGISTRY.keys())
        logger.error("Unsupported export format requested: %s", format_name)
        raise ValueError(
            f"Unsupported format '{format_name}'. Supported formats are: {supported}"
        )

    return exporter_cls()