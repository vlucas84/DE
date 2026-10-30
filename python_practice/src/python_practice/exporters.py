"""Data export module for serializing analytics results to JSON and XML formats."""

import json
from decimal import Decimal
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


def _json_serial(obj: Any) -> Any:
    """Fallback JSON serializer for unsupported objects like Decimal."""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return str(obj)


def export_to_json(data: list[dict[str, Any]], output_path: Path | str) -> None:
    """Export a list of dictionaries to a JSON file.

    Args:
        data: List of dictionary records to serialize.
        output_path: Destination path for the output JSON file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=_json_serial)


def export_to_xml(
    data: list[dict[str, Any]],
    output_path: Path | str,
    root_tag: str = "results",
    item_tag: str = "item",
) -> None:
    """Export a list of dictionaries to an XML file.

    Args:
        data: List of dictionary records to serialize.
        output_path: Destination path for the output XML file.
        root_tag: XML root element tag name. Defaults to "results".
        item_tag: XML child element tag name for each record. Defaults to "item".
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    root = ET.Element(root_tag)

    for record in data:
        item = ET.SubElement(root, item_tag)
        for key, value in record.items():
            child = ET.SubElement(item, key)
            child.text = str(value) if value is not None else ""

    ET.indent(root, space="    ")
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)