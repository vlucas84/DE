# Import Path for cross-platform file path management
from pathlib import Path

# Import Any for generic type hinting
from typing import Any

# Import the direct PostgreSQL database adapter and error class
from psycopg import Error as PsycopgError, connect

# Import the formatted database connection URL from config.py module
from python_practice.config import db_url


def check_connection() -> bool:
    """Checks database availability by executing a simple 'SELECT 1' query.

    Returns:
        True if connection succeeded, False otherwise.
    """
    try:
        # Establish a connection with a 3-second timeout limit
        with connect(db_url, connect_timeout=3) as conn:
            # Open a cursor context to execute raw SQL queries
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1;")
        
        return True   
    except Exception:
        # Catch and print connection failures (e.g., timeout, bad credentials)
        return False


def db_init() -> bool:
    """Reads schema.sql and creates initial database tables.

    Returns:
        True if schema execution succeeded, False otherwise.
    """
    # Define absolute path to schema.sql in the project root
    schema_path = Path(__file__).resolve().parent / "sql" / "schema.sql"
    # Ensure the file actually exists before reading
    if not schema_path.is_file():
        print(f"Error: Schema file not found at {schema_path}")
        return False

    # Read SQL queries from file
    sql_script = schema_path.read_text(encoding="utf-8")
    
    try:
        with connect(db_url, connect_timeout=3) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)
        return True
    except PsycopgError as e:
        print(f"Database error while initializing schema: {e}")
        return False


def insert_rooms(rooms: list[dict[str, Any]]) -> bool:
    """Inserts a batch of rooms into the database.

    Args:
        rooms: List of dictionaries containing room records.

    Returns:
        True if insertion succeeded, False otherwise.
    """
    query = """
        INSERT INTO rooms (id, room_name)
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE SET room_name = EXCLUDED.room_name;
    """
    records = [(r["id"], r["name"]) for r in rooms]
    try:
        with connect(db_url, connect_timeout=3) as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, records)
        return True
    except PsycopgError as err:
        print(f"Database error while inserting rooms: {err}")
        return False


def insert_students(students: list[dict[str, Any]]) -> bool:
    """Inserts a batch of students into the database.

    Args:
        students: List of dictionaries containing student records.

    Returns:
        True if insertion succeeded, False otherwise.
    """
    query = """
        INSERT INTO students (id, student_name, sex, birthday, room_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            student_name = EXCLUDED.student_name,
            sex = EXCLUDED.sex,
            birthday = EXCLUDED.birthday,
            room_id = EXCLUDED.room_id;
    """
    records = [(r["id"], r["name"], r["sex"], r["birthday"], r["room"]) for r in students]
    try:
        with connect(db_url, connect_timeout=3) as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, records)
        return True
    except PsycopgError as err:
        print(f"Database error while inserting students: {err}")
        return False
