from count import count_char

def test_empty():
    assert count_char("") == {}

def test_simple():
    assert count_char("abc") == {"a": 1, "b": 1, "c": 1}

def test_double():
    assert count_char("aa") == {"a": 2}
    
def test_multiple_double():
    assert count_char("aabbcc") == {"a": 2, "b":2, "c":2}
    
def test_case_sensitive():
    assert count_char("aAa") == {"a":2, "A":1}
    
def test_many():
    assert count_char("aaaaaaaaaaaaaaaa") == {"a":16}
    
def test_nums_symbols():
    assert count_char("@23./}") == {"@": 1, "2":1, "3":1, ".":1, "/":1, "}":1}
    
def test_sentence():
    assert count_char("Hello to the world") == {" ":3, "H":1, "e":2, "l":3, "o":3, "t":2, "h":1, "w":1, "r":1, "d":1}
