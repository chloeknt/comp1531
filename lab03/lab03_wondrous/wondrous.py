def wondrous(start):
    '''
    Returns the wondrous sequence for a given number.
    '''
    if start < 1 or not isinstance(start, int):
        raise(Exception("Integer should be equal or greater than one")) 
    
    current = start
    sequence = [start]

    while current != 1:
        if (current % 2 == 0):
            current = int(current / 2)
        else:
            current = int((current * 3) + 1)
        sequence.append(current)

    return sequence
