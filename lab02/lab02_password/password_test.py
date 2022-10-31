'''
Tests for check_password()
'''
from password import check_password

def test_strong():
    assert(check_password("H3ll0w0rld12")) == "Strong password"

def test_strong_missing_one():
    assert(check_password("H3ll0w0rld")) == "Moderate password"

def test_moderate():
    assert(check_password("hello123")) == "Moderate password"

def test_mod_missing_one():
    assert(check_password("greetings")) == "Poor password"

def test_poor():
    assert(check_password("hello")) == "Poor password"

def test_horrible():
    assert(check_password("123456")) == "Horrible password"
    assert(check_password("password")) == "Horrible password"
    assert(check_password("iloveyou")) == "Horrible password"

