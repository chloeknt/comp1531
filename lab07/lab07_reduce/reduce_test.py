from reduce import reduce
import pytest

def test_empty():
    assert reduce(lambda x, y: x + y, []) == None

def test_one():
    assert reduce(lambda x, y: x + y, [1]) == 1

def test_add():
    assert reduce(lambda x, y: x + y, [1,2,3,4,5]) == 15

def test_invalid():
    assert reduce(lambda x, y: x * y, [1,2,3,4,5]) == 120

def test_mul():
    assert reduce(lambda x, y: x + y, 'abcdef') == 'abcdef'