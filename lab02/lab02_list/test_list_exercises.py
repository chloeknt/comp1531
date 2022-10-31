from list_exercises import reverse_list, minimum, sum_list

def test_reverse():
    l = ["how", "are", "you"]
    reverse_list(l)
    assert l == ["you", "are", "how"]
    l = ["you", "you", "you"]
    reverse_list(l)
    assert l == ["you", "you", "you"]
    l.append("today")
    reverse_list(l)
    assert l == ["today","you", "you", "you"]

def test_min_positive():
    assert minimum([1, 2, 3, 10]) == 1
    assert minimum([10, 5, 2, 1]) == 1
    assert minimum([1, 1, 1, 1]) == 1

def test_min_negative():
    assert minimum([-1, -2, -3, -10]) == -10
    assert minimum([-10, -5, -2, -1]) == -10
    assert minimum([-1, -1, -1, -1]) == -1

def test_sum_positive():
    assert sum_list([7, 7, 7]) == 21
    assert sum_list([5, 3, 1]) == 9
    assert sum_list([1]) == 1
    
def test_sum_negative():
    assert sum_list([-7, -7, -7]) == -21
    assert sum_list([-5, -3, -1]) == -9
    assert sum_list([-1]) == -1
