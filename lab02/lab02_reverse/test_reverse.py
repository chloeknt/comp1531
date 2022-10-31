'''
Tests for reverse_words()
'''
from reverse import reverse_words

def test_example():
    assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']
    
def test_one():
    assert reverse_words(["Hello World"]) == ['World Hello']
    
def test_three():
    assert reverse_words(["Hello World", "I am here", "Goodbye to you"]) == ["World Hello", "here am I", "you to Goodbye"]
    
def test_duplicate():
    assert reverse_words(["Hello World", "Hello World"]) == ["World Hello", "World Hello"]
    
def test_many_small():
    assert reverse_words(["at", "in", "to", "by", "am", "it"]) == ["at", "in", "to", "by", "am", "it"]
    
def test_many_assorted():
    assert reverse_words(["Hello", "to you", "too"]) == ["Hello", "you to", "too"]
    
def test_empty():
    assert reverse_words([]) == [] 

