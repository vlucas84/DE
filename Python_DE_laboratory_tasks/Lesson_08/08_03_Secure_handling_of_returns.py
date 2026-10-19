from typing import Any

MAX_RENTAL_BATCH_LIMIT = 150.0
PERFORMANCE_LOG_PREFIX = "[PERF_LOG]"
TIME_DECIMALS = 8
DEFAULT_RETURN_INDEX_BASE = 10.0

def calculate_overdue_fine(movie: Any, days_overdue: Any, fine_rate: Any) -> tuple[float, float] | None:
    """Calculates overdue fine and return index based on raw input data.

    Args:
        movie: The title of the movie.
        days_overdue: Raw input for overdue days (numeric or convertible).
        fine_rate: Raw input for daily fine rate (numeric or convertible).

    Returns:
        A tuple of (total_fine, return_index) if successful, or None on error.
    """

    try:
        numeric_days = float(days_overdue)
        numeric_rate = float(fine_rate)
        total_fine = numeric_days * numeric_rate
        return_index = round(DEFAULT_RETURN_INDEX_BASE / numeric_days, 2)
        print(f"Movie: '{movie}' | Total fine: {total_fine}$ | Index: {return_index}")
        return total_fine, return_index
    except ValueError as e:
        print(f"[{type(e).__name__}] Unable to convert days/rate to number for '{movie}': {e}")
        return None
    except ZeroDivisionError as e:
        print(f"[{type(e).__name__}] Return on time for '{movie}': {e}")
        return None
    except TypeError as e:
        print(f"[{type(e).__name__}] Incorrect data type for '{movie}': {e}")
        return None
    finally:
        print("--- The refund transaction check is complete. ---")


# Result output directly
calculate_overdue_fine("Matrix", 5, 1.5)
calculate_overdue_fine("Inception", "five", 2.0)
calculate_overdue_fine("Avatar", 0, 2.5)
calculate_overdue_fine("Interstellar", [3, ], 3.0)


