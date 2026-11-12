"""Command Line Interface and ETL pipeline orchestrator."""

import argparse
import logging
from pathlib import Path
from typing import Any

from python_practice.analytics import AnalyticsService
from python_practice.db import DatabaseManager
from python_practice.exporters import get_exporter
from python_practice.loaders import JsonLoader

logger = logging.getLogger("python_practice")


class CommandLineInterface:
    """Encapsulates CLI argument parsing and pipeline orchestration."""

    def __init__(
        self,
        db_manager: DatabaseManager,
        analytics_service: AnalyticsService,
        argv: list[str] | None = None,
    ) -> None:
        """Initialize CLI with injected services and parsed arguments."""
        self.db = db_manager
        self.analytics = analytics_service
        self.parser = self._build_parser()
        self.args = self.parser.parse_args(argv)

    def _build_parser(self) -> argparse.ArgumentParser:
        """Construct the CLI argument schema."""
        parser = argparse.ArgumentParser(
            description="ETL Pipeline: Load students and rooms datasets into PostgreSQL and export analytics."
        )
        parser.add_argument(
            "--students",
            "-s",
            type=Path,
            required=True,
            help="Path to students dataset (JSON file).",
        )
        parser.add_argument(
            "--rooms",
            "-r",
            type=Path,
            required=True,
            help="Path to rooms dataset (JSON file).",
        )
        parser.add_argument(
            "--format",
            "-f",
            choices=["json", "xml"],
            required=True,
            help="Output export format for reports (json or xml).",
        )
        
        available_queries = self.analytics.get_available_commands()
        parser.add_argument(
            "--query",
            "-q",
            default="all",
            choices=available_queries,
            help=f"Specific query to run. Available: {', '.join(available_queries)}. Defaults to 'all'.",
        )

        parser.add_argument(
            "--output-dir",
            "-o",
            type=Path,
            default=Path("output"),
            help="Directory to save exported report files (defaults to 'output/').",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Batch size for inserting records into PostgreSQL (default: 1000).",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Enable debug-level logging.",
        )
        return parser

    def run(self) -> None:
        """Execute complete data pipeline: ingestion, DB persistence, and analytics export."""
        if self.args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        loader = JsonLoader()
        exporter = get_exporter(self.args.format)

        # 1. DDL
        logger.info("Initializing schema...")
        self.db.init_schema()

        # 2. Rooms
        logger.info("Loading rooms data from %s...", self.args.rooms)
        for rooms_batch in loader.load_batches(self.args.rooms, batch_size=self.args.batch_size):
            self.db.insert_rooms_batch(rooms_batch)

        # 3. Students
        logger.info("Loading students data from %s...", self.args.students)
        for students_batch in loader.load_batches(self.args.students, batch_size=self.args.batch_size):
            self.db.insert_students_batch(students_batch)

        # 4. Analytics
        logger.info("Running analytical queries (target: %s)...", self.args.query)
        reports: dict[str, list[dict[str, Any]]] = {}

        if self.args.query == "all":
            reports = self.analytics.run_all_queries()
        else:
            report_name, data = self.analytics.run_query_by_command(self.args.query)
            reports[report_name] = data

        # 5. Export
        self.args.output_dir.mkdir(parents=True, exist_ok=True)
        ext = self.args.format.lower()

        for report_name, data in reports.items():
            dest = self.args.output_dir / f"{report_name}.{ext}"
            exported_path = exporter.export(data, dest)
            logger.info("Saved report '%s' to %s (%d rows)", report_name, exported_path, len(data))

        logger.info("Pipeline completed successfully!")