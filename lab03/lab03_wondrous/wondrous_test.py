from wondrous import wondrous
import pytest

def test_basic():
    assert wondrous(3) == [3, 10, 5, 16, 8, 4, 2, 1]
    
def test_large():
    assert wondrous(22) == [22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]

def test_one():
    assert wondrous(1) == [1]
    
def test_neg():
    with pytest.raises(Exception):
        assert wondrous(-1)
    
def test_zero():
    with pytest.raises(Exception):
        assert wondrous(0)
        
def test_float():
    with pytest.raises(Exception):
        assert wondrous(2.4)
    
