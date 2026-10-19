MAX_RENTAL_BATCH_LIMIT = 150.0
PERFORMANCE_LOG_PREFIX = "[PERF_LOG]"
TIME_DECIMALS = 8
DEFAULT_RETURN_INDEX_BASE = 10.0

def calculate_rental_batch(quantity: int, rental_rate: float, discount: float = 0.0) -> tuple[float, bool]:
    """Calculates total rental cost and checks against maximum batch limit.

    Args:
        quantity (int): The number of items in the batch.
        rental_rate (float): The base cost per single rental item.
        discount (float): Optional discount rate as a fraction (e.g., 0.1 for 10%). Defaults to 0.0.

    Returns:
        A tuple containing two values:
            - final_sum (float): The calculated total cost rounded to 2 decimal places.
            - is_limit_exceeded (bool): True if final_sum exceeds MAX_RENTAL_BATCH_LIMIT, False otherwise.
    """
    final_sum = round(quantity * rental_rate * (1 - discount), 2)
    if final_sum > MAX_RENTAL_BATCH_LIMIT:
        is_limit_exceeded = True
    else:
        is_limit_exceeded = False
    return final_sum, is_limit_exceeded

# Result output in the format specified in the task
test = [(1, "Academy Dinosaur", 30, 2.99, False), 
        (2, "Affair Prejudice", 40, 4.99, 0.1),
        (3, "Agent Truman", 10, 1.99, False),
        (4, "African Egg", 50, 3.5, 0.2)]

for number, name, count, price, discount in test:
    amount, limit = calculate_rental_batch(count, price, discount)
    print(f"Shipment {number} ({name}): Amount {amount}$. Exceeding the limit: {limit}.")

# Result output directly
print(calculate_rental_batch(30, 2.99))
print(calculate_rental_batch(40, 4.99, 0.1))
print(calculate_rental_batch(10, 1.99))
print(calculate_rental_batch(50, 3.5, 0.2))
