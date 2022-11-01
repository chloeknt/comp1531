from inverse import inverse
from hypothesis import given, strategies, seed

def test_nums():
    assert inverse({1: 'A', 2: 'B', 3: 'A'}) == {'A': [1, 3], 'B': [2]}

def test_letters():
    assert inverse({'A': 1, 'B': 2, 'C': 1}) == {1: ['A', 'C'], 2: ['B']}

def test_mix():
    assert inverse({1: 'A', 'B': 2, 3: 'A'}) == {'A': [1, 3], 2: ['B']}

@seed(0)
@given(strategies.lists(strategies.integers(), min_size=0, max_size=25))
def test_prime(nums):
    test_dict = {}
    key = 65
    for num in nums:
        test_dict[str(key)] = num
        key += 1
    assert len(inverse(test_dict)) == len(set(nums))
