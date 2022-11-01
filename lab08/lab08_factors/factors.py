import math 

# You may find this helpful
def is_prime(n):
	return n != 1 and factors(n) == [n]

def factors(n):
	'''
	A function that generates the prime factors of n. For example
	>>> factors(12)
	[2,2,3]

	Params:
		n (int): The operand

	Returns:
		List (int): All the prime factors of n in ascending order.

	Raises:
		ValueError: When n is <= 1.
	'''
	if n <= 1:
		raise ValueError()

	primes = []
    #if is_prime(n):
		#break
    #else:
	while n % 2 == 0:
		primes.append(2)
		n = n / 2

	for i in range(3, int(math.sqrt(n)) + 1 , 2):
		while n % i == 0:
			primes.append(i)
			n = n / i

	if n > 2:
		primes.append(n)
	return sorted(primes)
