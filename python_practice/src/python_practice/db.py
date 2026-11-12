"""Database connection and repository management for PostgreSQL (psycopg 3)."""

from contextlib import contextmanager
import logging
from typing import Any, Generator
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from python_practice import config

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages PostgreSQL connections, schema initialization, and data insertion."""

    def __init__(self) -> None:
        """Initialize connection parameters strictly from config."""
        self.dbname = config.db_name
        self.user = config.db_user

        if not config.db_password:
            raise ValueError(
                "Database password is required. Please set DB_PASSWORD in your .env file or environment."
            )
        self.password = config.db_password

        self.host = config.db_host
        self.port = int(config.db_port) # Приводим к int, так как os.getenv возвращает str

    @contextmanager
    def get_connection(self) -> Generator[psycopg.Connection, None, None]:
        """Context manager providing a transactional PostgreSQL connection.

        Automatically commits on success or rolls back on exception.
        """
        conn = psycopg.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            connect_timeout=3,
        )
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            logger.exception("Database transaction failed; rolled back.")
            raise
        finally:
            conn.close()

    def init_schema(self, schema_file: Path | str | None = None) -> None:
        """Create tables and schema from the external SQL file."""
        if schema_file is None:
            schema_path = Path(__file__).resolve().parent / "sql" / "schema.sql"
        else:
            schema_path = Path(schema_file)

        if not schema_path.is_file():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        ddl = schema_path.read_text(encoding="utf-8")

        logger.info("Initializing database schema from %s...", schema_path.name)
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
        logger.info("Database schema initialized successfully.")

    def insert_rooms_batch(self, rooms: list[dict[str, Any]]) -> None:
        """Batch insert room records into the database."""
        if not rooms:
            return

        query = """
        INSERT INTO rooms (id, name)
        VALUES (%(id)s, %(name)s)
        ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, rooms)
        logger.info("Inserted/Updated %d room records.", len(rooms))

    def insert_students_batch(self, students: list[dict[str, Any]]) -> None:
        """Batch insert student records into the database."""
        if not students:
            return

        query = """
        INSERT INTO students (id, name, birthday, sex, room)
        VALUES (%(id)s, %(name)s, %(birthday)s, %(sex)s, %(room)s)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            birthday = EXCLUDED.birthday,
            sex = EXCLUDED.sex,
            room = EXCLUDED.room;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, students)
        logger.info("Inserted/Updated %d student records.", len(students))

    def execute_query(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> list[dict[str, Any]]:
        """Execute a read-only SQL query and return results as a list of dictionaries."""
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                records = cur.fetchall()
                return records