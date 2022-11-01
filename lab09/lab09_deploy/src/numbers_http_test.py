import pytest
import json
import requests

URL = 'http://localhost:5000'

OK = 200

def test_multiply_two():
    response = requests.get(f"{URL}/multiply/by/two", params={
        'number' : 2
    })
    assert response.status_code == OK
    data = response.json()
    assert data.get('number') == 4

def test_print_message():
    response = requests.get(f"{URL}/print/message", params={
        'message' : 'hello!'
    })
    assert response.status_code == OK

def test_list_sum():
    response = requests.get(f"{URL}/sum/list/of/numbers", params={
        'list' : json.dumps([1, 2, 3])
    })
    assert response.status_code == OK
    data = response.json()
    assert data.get('sum') == 6

def test_iterable_sum():
    response = requests.get(f"{URL}/sum/iterable/of/numbers", params={
        'list' : json.dumps((1, 2, 3))
    })
    assert response.status_code == OK
    data = response.json()
    assert data.get('sum') == 6

def test_is_in():
    response = requests.get(f"{URL}/is/in", params={
        'needle' : 1,
        'haystack' : json.dumps([1, 2, 3])
    })
    assert response.status_code == OK
    data = response.json()
    assert data.get('bool') == True

def test_get_index():
    response = requests.get(f"{URL}/index/of/number", params={
        'item' : 2,
        'numbers' : json.dumps([1, 2, 3])
    })
    assert response.status_code == OK
    data = response.json()
    assert data.get('index') == 1