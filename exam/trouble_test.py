'''
Tests
'''
from trouble import clear, flip_card, is_double_trouble, is_trouble_double, is_empty

def test_simple():
    clear()
    flip_card({
        'suit': 'Hearts',
        'number': '9',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '9',
    })
    assert not is_trouble_double()
    assert not is_empty()
    assert is_double_trouble()

# Write your tests here
def test_suit():
    clear()
    flip_card({
        'suit': 'Clubs',
        'number': '3',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '9',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '6',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '4',
    })
    assert is_trouble_double()
    assert is_empty()
    assert not is_double_trouble()

def test_one_card():
    clear()
    flip_card({
        'suit': 'Hearts',
        'number': '9',
    })
    assert not is_trouble_double()
    assert not is_double_trouble()
    assert not is_empty()

def test_empty():
    clear()
    flip_card({
        'suit': 'Clubs',
        'number': '3',
    })
    clear()
    assert is_empty()

def test_set_empty_double_trouble():
    clear()
    flip_card({
        'suit': 'Hearts',
        'number': '9',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '9',
    })
    assert not is_trouble_double()
    assert not is_empty()
    assert is_double_trouble()
    assert is_empty()

def test_set_empty_trouble_double():
    clear()
    flip_card({
        'suit': 'Clubs',
        'number': '3',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '9',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '6',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '4',
    })
    assert not is_double_trouble()
    assert not is_empty()
    assert is_trouble_double()
    assert is_empty()

def test_same():
    clear()
    flip_card({
        'suit': 'Clubs',
        'number': '3',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '3',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '6',
    })
    flip_card({
        'suit': 'Clubs',
        'number': '4',
    })
    assert not is_double_trouble()
    assert not is_empty()
    assert not is_trouble_double()
    assert not is_empty()