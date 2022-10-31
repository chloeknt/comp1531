from prefix import prefix_search
import pytest

def test_documentation():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a") == { "ac": 1, "ab": 3}

def test_exact_match():
    assert prefix_search({"category": "math", "cat": "animal"}, "cat") == {"category": "math", "cat": "animal"}
    
def test_partial_match():
    assert prefix_search({"namesake": "joe", "nameplate": "josh", "nametag": "jake"}, "name") == {"namesake": "joe", "nameplate": "josh", "nametag": "jake"}
    
def test_no_matches():
    assert prefix_search({"hello": "world", "goodbye": "world"}, "no") == {}
    
def test_empty_fields():
    assert prefix_search({}, "a") == {}
    assert prefix_search({"ac":"yes", "ab": "no"}, "") == {}
