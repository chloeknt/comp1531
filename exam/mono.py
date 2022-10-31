def monotonic(lists):
    res = []
    for tup in lists:
        if not isinstance(tup, tuple):
            raise ValueError("There is an error in the input")
        if isError(list(tup)):
            raise ValueError("There is an error in the input")
        if increasing(list(tup)):
            res.append('monotonically increasing')
        elif decreasing(list(tup)):
            res.append('monotonically decreasing')
        else:
            res.append('neither')

    return res

def increasing(data):
    return all(x < y for x, y in zip(data, data[1:]))

def decreasing(data):
    return all(x > y for x, y in zip(data, data[1:]))

def isError(data):
    for x in data:
        if abs(x) >= 100000:
            return True
    return False
