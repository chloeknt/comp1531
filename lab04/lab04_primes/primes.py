import math

def factors(num):
    '''
    Returns a list containing the prime factors of 'num'. The primes should be
    listed in ascending order.

    For example:
    >>> factors(16)
    [2, 2, 2, 2]
    >>> factors(21)
    [3, 7]
    '''
    factor_list = []
    i = 2
    while i * i <= num:
        if num % i:
            i += 1
        else:
            num //= i
            factor_list.append(i)
    if num > 1:
        factor_list.append(num)
        
    return factor_list
            
