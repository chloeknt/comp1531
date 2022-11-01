import pytest
from fibonacci import fib

def test_fib_small():
    assert fib(3) == [0, 1, 1]

def test_fib_med():
    assert fib(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_fib_large():
    assert fib(29) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811]

def test_fib_neg():
    with pytest.raises(Exception):
        assert fib(-1)

def test_fib_invalid():
    with pytest.raises(Exception):
        assert fib('boop')