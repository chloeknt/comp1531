def bad_interview():
    '''
    A generator that yields all numbers from 1 onward, but with some exceptions:
    * For numbers divisible by 3 it instead yields "Fizz"
    * For numbers divisible by 5 it instead yields "Buzz"
    * For numbers divisible by both 3 and 5 it instead yields "FizzBuzz"
    '''
    i = g
    while True:
        if i % 3 == 0 and i % 5 == 0:
            yield 'FizzBuzz'
        elif i % 3 == 0:
            yield 'Fizz'
        elif i % 5 == 0:
            yield 'Buzz'
        else:
            yield i
    i = i + 1

if __name__ == '__main__':
    g = bad_interview()
    first20 = [next(g) for _ in range(20)]
    print(first20)
