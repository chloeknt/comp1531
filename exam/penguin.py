EVEN = '02468'

def validate(penguin_number):
    # LNNNNLNNNNNL format
    if not formatted(penguin_number):
        return False
    if penguin_number[0].islower() or penguin_number[5].islower() or penguin_number[11].islower():
        return False
    # first letter must be closer than to start than second, second closer than third
    if penguin_number[0] >= penguin_number[5]:
        return False
    if penguin_number[5] >= penguin_number[11]:
        return False
    # sum of digits must be even
    if not sumEven(penguin_number):
        return False
    # last number must be even
    if penguin_number[10] not in EVEN:
        return False
    return True

def formatted(num):
    if num[0].isalpha() and num[5].isalpha() and num[11].isalpha():
        for i in range(1, 5):
            if not num[i].isnumeric():
                return False
        for i in range(6, 11):
            if not num[i].isnumeric():
                return False
        return True
    return False

def sumEven(num):
    nSum = 0
    for i in range(1, 5):
        nSum += int(num[i])
    for i in range(6, 11):
        nSum += int(num[i])
    s = str(nSum)
    if s[len(s) - 1] not in EVEN:
        return False
    return True

print(validate('A7964B94933C'))