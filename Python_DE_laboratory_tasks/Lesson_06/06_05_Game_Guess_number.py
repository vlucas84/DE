import random

correct_answer = random.randint(1, 20)
attempts = 5

print(f"I have picked a number between 1 and 20. You have {attempts} attempts.")

while attempts > 0:
    print(f"Attempt {6 - attempts}. Enter a number:")
    guess = int(input())
    attempts -= 1
    if guess < correct_answer:
        print(f"Too little! Attempts remaining: {attempts}\n")
    elif guess > correct_answer:
        print(f"Too many! Attempts remaining: {attempts}\n")
    else:
        print(f"You guessed it. The correct answer is {correct_answer}! Great job.")
        break
else:
    print(f"You didn't guess correctly. The right answer is: {correct_answer}.")