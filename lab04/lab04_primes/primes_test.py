from primes import factors
import pytest

def test_zero():
    assert factors(0) == []
    
def test_simple():
    assert factors(3) == [3]
    assert factors(6) == [2, 3]
    assert factors(12) == [2, 2, 3]

def test_medium():
    assert factors(32) == [2,2,2,2,2]
    assert factors(48) == [2,2,2,2,3]
    assert factors(52) == [2,2,13]

def test_complex():
    assert factors(128) == [2,2,2,2,2,2,2]
    assert factors(2187) == [3,3,3,3,3,3,3]
    assert factors(1953125) == [5,5,5,5,5,5,5,5,5]
