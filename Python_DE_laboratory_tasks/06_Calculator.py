set_correct_operators = {"+", "-", "*", "/"}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

number1 = input("Enter the first number:\n")
number2 = input("Enter the second number:\n")
operator = input("Select an operator (+, -, *, /):\n")

if not is_number(number1):
    print(f"You entered '{number1}' as the 1st value. This is not a number.")
elif not is_number(number2):
    print(f"You entered '{number2}' as the 2nd value. This is not a number.")
elif operator not in set_correct_operators:
    print(f"You entered '{operator}' as the operator. This is an invalid value. YOu should enter one of the following values: (+, -, *, /).")
else:
    if operator == "+":
        print(f"Result: {float(number1)} + {float(number2)} = {float(number1) + float(number2)}")
    elif operator == "-":
        print(f"Result: {float(number1)} - {float(number2)} = {float(number1) - float(number2)}")
    elif operator == "*":
        print(f"Result: {float(number1)} * {float(number2)} = {float(number1) * float(number2)}")
    elif float(number2) == 0:
        print(f"You entered '{number2}' as the 2nd value. Division cannot be performed.")
    else:
        print(f"Result: {float(number1)} / {float(number2)} = {float(number1) / float(number2)}")
