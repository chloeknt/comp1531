from filter import filter_string
import pytest

def test_1():
    assert(filter_string("Hello, my name is Mr O'Toole.") == "Hello my name is mr otoole")

def test_all_punct():
    assert filter_string(""",.""'';?!""") == ""

def test_num():
    with pytest.raises(ValueError):
        assert filter_string("H3ll0.") 

def test_all_capitals():
    assert filter_string("HELLO, MY NAME IS MR O'TOOLE.") == "Hello my name is mr otoole"

def test_some_capitals():
    assert filter_string("HeLlO, My NaMe Is Mr o'ToOlE.") == "Hello my name is mr otoole"

def test_noncap():
    assert filter_string("hello, my name is Mr O'Toole.") == "Hello my name is mr otoole"