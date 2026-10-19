import time
from collections.abc import Callable
from typing import Any

MAX_RENTAL_BATCH_LIMIT = 150.0
PERFORMANCE_LOG_PREFIX = "[PERF_LOG]"
TIME_DECIMALS = 8
DEFAULT_RETURN_INDEX_BASE = 10.0

def performance_logger(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Logs the execution time of a function and formats its output list.

        A decorator that measures the performance of the wrapped function using 
        time.perf_counter() and prints a formatted list of the top revenue 
        categories returned by the function.

        Args:
            func: The target function to be decorated and monitored.

        Returns:
            The wrapper function that executes the target function, prints 
            performance logs, formats the result, and returns the original output.
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)         
        end_time = time.perf_counter()
        execution_time = end_time - start_time       
        print(f"{PERFORMANCE_LOG_PREFIX} The function {func.__name__} executed in {execution_time:.{TIME_DECIMALS}f} sec.")
        print("Top categories by revenue:")
        for i, item in enumerate(result, start=1):
            print(f"{i}. {item[0]}: {item[1]}")
        return result
    return wrapper

@performance_logger
def get_sorted_report(revenue_data: list[dict[str, str | float]]) -> list[tuple[str | float, ...]]:
    """Generates a revenue report sorted by sales in descending order.

    Converts a list of dictionary records containing category revenue data into 
    a list of tuples and ranks them from highest to lowest sales volume.

    Args:
        revenue_data: A list of dictionaries, where each dictionary contains 
            category metrics (e.g., category name and total sales amount).

    Returns:
        A list of tuples containing the extracted record values, sorted in 
        descending order by the second element (sales amount).

    Examples:
        >>> data = [{"category": "Action", "total_sales": 100.0}, {"category": "Drama", "total_sales": 250.0}]
        >>> get_sorted_report(data)
        [('Drama', 250.0), ('Action', 100.0)]
    """
    sorted_list = sorted([tuple(item.values()) for item in revenue_data], key=lambda x: x[1], reverse=True)
    return sorted_list

test1 = [
    {"category": "Action", "total_sales": 4311.85},
    {"category": "Animation", "total_sales": 4656.30},
    {"category": "Children", "total_sales": 3655.55}
    ]

test2 = [
    {"category": "Classics", "total_sales": 1200.10},
    {"category": "Comedy", "total_sales": 4000.00},
    {"category": "Documentary", "total_sales": 4000.00}
    ]

test3 = [
    {"category": "Drama", "total_sales": 500.00}
    ]

get_sorted_report(test1)
get_sorted_report(test2)
get_sorted_report(test3)
