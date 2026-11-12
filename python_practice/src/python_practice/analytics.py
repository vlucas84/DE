"""Analytics service providing dynamic SQL-based aggregated reports."""

import json
import logging
from pathlib import Path
from typing import Any

from python_practice.db import DatabaseManager

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Executes business intelligence queries defined in SQL files."""

    def __init__(self, db_manager: DatabaseManager, sql_dir: Path | str | None = None) -> None:
        """Initialize analytics service with DB manager and SQL directory path."""
        self.db = db_manager
        self.sql_dir = Path(sql_dir) if sql_dir else Path(__file__).resolve().parent / "sql"
        self.registry_path = self.sql_dir / "queries.json"

    def _read_sql(self, filename: str) -> str:
        """Read SQL query text from the sql directory."""
        file_path = self.sql_dir / filename
        if not file_path.is_file():
            raise FileNotFoundError(f"SQL file not found: {file_path}")
        return file_path.read_text(encoding="utf-8").strip()

    def _load_registry(self) -> list[dict[str, str]]:
        """Load and return queries registry from queries.json."""
        if not self.registry_path.is_file():
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")

        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_available_commands(self) -> list[str]:
        """Return a list of all valid query commands from the registry."""
        registry = self._load_registry()
        return ["all"] + [item["command"] for item in registry if "command" in item]

    def run_query_by_command(self, command: str) -> tuple[str, list[dict[str, Any]]]:
        """Execute a single query matching the specified command (e.g. 'q1')."""
        registry = self._load_registry()

        for item in registry:
            if item.get("command") == command:
                key = f"{item['command']}_{item['id']}"
                desc = item.get("description", "")
                logger.info("Executing analytical query: %s (%s)...", key, desc)
                sql = self._read_sql(item["file"])
                return key, self.db.execute_query(sql)

        available = [item.get("command") for item in registry if "command" in item]
        raise ValueError(f"Unknown query command: '{command}'. Available commands: {available}")

    def run_all_queries(self) -> dict[str, list[dict[str, Any]]]:
        """Execute all analytical queries registered in queries.json."""
        registry = self._load_registry()
        results: dict[str, list[dict[str, Any]]] = {}

        for item in registry:
            key = f"{item['command']}_{item['id']}"
            desc = item.get("description", "")
            logger.info("Executing analytical query: %s (%s)...", key, desc)

            sql = self._read_sql(item["file"])
            results[key] = self.db.execute_query(sql)

        return results