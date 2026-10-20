set_correct_operators = {"+", "-", "*", "/"}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

n1_str = input("Enter the first number:\n")
n2_str = input("Enter the second number:\n")
operator = input("Select an operator (+, -, *, /):\n")

if not is_number(n1_str):
    print(f"You entered '{n1_str}' as the 1st value. This is not a number.")
elif not is_number(n2_str):
    print(f"You entered '{n2_str}' as the 2nd value. This is not a number.")
elif operator not in set_correct_operators:
    ops_str = ", ".join(sorted(set_correct_operators))
    print(f"You entered '{operator}' as the operator. This is an invalid value. You should enter one of the following values: ({ops_str}).")
else:
    n1, n2 = float(n1_str), float(n2_str) 
    if operator == '/' and n2 == 0:
        print(f"You entered '{n2_str}' as the 2nd value. Division cannot be performed.")
    else:
        if operator == "+":
            result = n1 + n2
        elif operator == "-":
            result = n1 - n2
        elif operator == "*":
            result = n1 * n2
        else:
            result = n1 / n2         
        print(f"Result: {n1} {operator} {n2} = {result}")
