# Guess a number between 1 and 100 
print("Pick a number between 1 and 100 (inclusive)")

low = 0
high = 100
answer = (low + high) // 2

while True:
    print("My guess is: " + str(answer))
    check = input("Is my guess too low (L), too high (H), or correct (C)?\n")
    
    if check == 'L':
        low = answer
        answer = (low + high) // 2
    elif check == 'H':
        high = answer
        answer = (low + high) // 2
    elif check == 'C':
        print("Got it!")
        break 
    else:
        print("Invalid input")
    

