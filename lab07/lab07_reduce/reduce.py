def reduce(f, xs):
    if len(xs) == 0:
        return None
    if len(xs) == 1:
        return xs[0]
    result = xs[0]
    for i in range(1, len(xs)):
        result = f(result, xs[i])
    return result

if __name__ == '__main__':
    print(reduce(lambda x, y: x + y, []))
    print(reduce(lambda x, y: x + y, [1]))
    print(reduce(lambda x, y: x + y, [1,2,3,4,5]))
    print(reduce(lambda x, y: x + y, 'abcdef'))
    print(reduce(lambda x, y: x * y, [1,2,3,4,5]))