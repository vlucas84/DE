# Import json module to parse and deserialize JSON formatted data
import json

# Import Path for cross-platform filesystem path manipulation
from pathlib import Path

# Import Any for generic dictionary value type annotations
from typing import Any


def load_json(file_path: str | Path) -> list[dict[str, Any]]:
    """Load and parse records from a JSON file into a list of dictionaries.

    Args:
        file_path: Filesystem path to the target JSON file.

    Returns:
        list[dict[str, Any]]: Parsed records represented as a list of dictionaries.
    """
    # Open the file as UTF-8 text and deserialize JSON data directly into memory
    with Path(file_path).open("r", encoding="utf-8") as f:
        return json.load(f)