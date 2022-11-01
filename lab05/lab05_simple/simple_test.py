import pytest
import json
import urllib
import requests

URL = 'http://localhost:5000'

OK = 200

@pytest.fixture
def setup():
    requests.delete(f'{URL}/names/clear')

def test_add_get(setup):
    response = requests.post(f"{URL}/names/add", json={
        'name' : 'Asus'
    })
    assert response.status_code == OK

    response = requests.get(f"{URL}/names")
    assert response.status_code == OK

    assert response.json() == {'names' : ['Asus']}

def test_add_remove(setup):
    response = requests.post(f"{URL}/names/add", json={
        'name' : 'Asus'
    })
    assert response.status_code == OK

    response = requests.get(f"{URL}/names")
    assert response.status_code == OK

    response = requests.delete(f"{URL}/names/remove", json={
        'name' : 'Asus'
    })

    assert response.status_code == OK

    assert response.json() == {}

def test_add_clear(setup):
    response = requests.post(f"{URL}/names/add", json={
        'name' : 'Asus'
    })
    assert response.status_code == OK

    response = requests.post(f"{URL}/names/add", json={
        'name' : 'Bill'
    })
    assert response.status_code == OK

    response = requests.delete(f"{URL}/names/clear")
    assert response.status_code == OK

    assert response.json() == {}
