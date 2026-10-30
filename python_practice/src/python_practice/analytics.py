"""Analytical queries module for rooms and students statistics."""

from typing import Any
from psycopg import Error as PsycopgError, connect
from psycopg.rows import dict_row

from python_practice.config import db_url

# List of rooms and the number of students in each of them
ROOMS_STUDENT_COUNT_QUERY = """
SELECT r.id, r.room_name, COUNT(s.id) AS total_students
FROM rooms r LEFT JOIN students s ON r.id = s.room_id
GROUP BY r.id, r.room_name
ORDER BY r.id;
"""

# Top 5 rooms with the smallest average age of students
TOP5_YOUNGEST_ROOMS_QUERY = """
SELECT r.id, r.room_name, ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday)))::numeric, 2) AS avg_age
FROM rooms r JOIN students s ON r.id = s.room_id
GROUP BY r.id, r.room_name
ORDER BY avg_age
LIMIT 5;
"""

# Top 5 rooms with the largest difference in student ages
TOP5_ROOMS_BIGGEST_DIFFERENCE_QUERY = """
SELECT r.id, r.room_name, MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) - MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS diff_age
FROM rooms r JOIN students s ON r.id = s.room_id
GROUP BY r.id, r.room_name
ORDER BY diff_age DESC
LIMIT 5;
"""

# List of rooms housing students of different sexes
ROOMS_DIFFERENT_SEX_QUERY = """
SELECT r.id, r.room_name
FROM rooms r JOIN students s ON r.id = s.room_id
GROUP BY r.id, r.room_name
HAVING COUNT(DISTINCT s.sex) > 1
ORDER BY r.id;
"""


def fetch_query(query: str) -> list[dict[str, Any]]:
    """Execute a read-only SQL query and return rows as dictionaries.

    Args:
        query: Raw SQL query string to be executed.

    Returns:
        list[dict[str, Any]]: List of dictionary rows matching column names,
            or an empty list if an error occurs.
    """
    try:
        with connect(db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except PsycopgError as e:
        print(f"Database query error: {e}")
        return []


def get_rooms_with_student_count() -> list[dict[str, Any]]:
    """Retrieve list of all rooms and the total student count in each.

    Returns:
        list[dict[str, Any]]: Dictionaries containing 'id', 'room_name',
            and 'total_students'.
    """
    return fetch_query(ROOMS_STUDENT_COUNT_QUERY)


def get_top_5_youngest_rooms() -> list[dict[str, Any]]:
    """Retrieve top 5 rooms with the lowest average student age.

    Returns:
        list[dict[str, Any]]: Dictionaries containing 'id', 'room_name',
            and 'avg_age'.
    """
    return fetch_query(TOP5_YOUNGEST_ROOMS_QUERY)


def get_top_5_rooms_biggest_age_diff() -> list[dict[str, Any]]:
    """Retrieve top 5 rooms with the highest age variance between students.

    Returns:
        list[dict[str, Any]]: Dictionaries containing 'id', 'room_name',
            and 'diff_age'.
    """
    return fetch_query(TOP5_ROOMS_BIGGEST_DIFFERENCE_QUERY)


def get_rooms_with_mixed_sex() -> list[dict[str, Any]]:
    """Retrieve list of rooms accommodating students of different sexes.

    Returns:
        list[dict[str, Any]]: Dictionaries containing 'id' and 'room_name'.
    """
    return fetch_query(ROOMS_DIFFERENT_SEX_QUERY)