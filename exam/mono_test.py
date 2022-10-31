from mono import monotonic
import pytest

def test_1():
    data = [(1,3,2),(1,2)]
    out = ['neither', 'monotonically increasing']
    assert monotonic(data) == out

def test_long():
    data = [(1,3,2),(1,2),(3, 4, 5),(7, 8, 3), (9, 3, 2)]
    out = ['neither', 'monotonically increasing', 'monotonically increasing', 'neither', 'monotonically decreasing']
    assert monotonic(data) == out

def test_float():
    data = [(1.12,1.14,1.13),(1.23,2.45)]
    out = ['neither', 'monotonically increasing']
    assert monotonic(data) == out

def test_same():
    data = [(1,1,1),(2,2,2)]
    out = ['neither', 'neither']
    assert monotonic(data) == out

def test_too_big_error():
    data = [(100000,3,2),(1,2)]
    with pytest.raises(ValueError):
        assert monotonic(data) 

def test_element_error():
    data = [(1),(1,3,2),(1,2)]
    with pytest.raises(ValueError):
        assert monotonic(data)