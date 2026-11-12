"""Console application entry point."""

import logging
import sys

from python_practice.analytics import AnalyticsService
from python_practice.cli import CommandLineInterface
from python_practice.db import DatabaseManager

logger = logging.getLogger("python_practice")


def setup_logging() -> None:
    """Configure basic logging layout."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    """Console entry point."""
    setup_logging()
    try:
        db = DatabaseManager()
        analytics = AnalyticsService(db)
        cli = CommandLineInterface(db, analytics)
        cli.run()
    except Exception as exc:
        logger.exception("Pipeline execution failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()