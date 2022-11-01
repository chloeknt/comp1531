from factors import factors, is_prime
from hypothesis import given, strategies, settings, Verbosity, seed
import pytest
from functools import reduce

def test_normal():
    assert factors(12) == [2, 2, 3]

def test_two():
    assert factors(2) == [2]

@seed(0)
@given(strategies.integers())
@settings(max_examples = 10)
def test_prime(num):
    if num > 1:
        for factor in factors(num):
            assert is_prime(factor) == True
    else:
        with pytest.raises(ValueError):
            assert factors(num)

@seed(0)
@given(strategies.integers())
@settings(max_examples = 10)
def test_factors(num):
    if num > 1:
        factor_list = factors(num)
        assert reduce((lambda x, y: x * y), factor_list) == num
    else:
        with pytest.raises(ValueError):
            assert factors(num)
