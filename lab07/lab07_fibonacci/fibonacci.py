def fib(n):
    if not isinstance(n, int):
        raise Exception
    elif n < 0:
        raise Exception
        
    fibs = []
    i = 0
    first = 0
    second = 1

    while i < n:
        fibs.append(first)
        temp = first + second
        first = second
        second = temp
        i += 1
    return fibs
