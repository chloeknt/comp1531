from random import randint

num_one = randint(2, 12)
num_two = randint(2, 12)
ans = num_one * num_two

while True:
    number = int(input(f"What is {num_one} x {num_two}? "))
    if number == ans:
        print("Correct!")
        break
    else:
        print("Incorrect - try again.")
