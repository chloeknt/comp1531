import pytest
from weather import weather

def test_invalid_location():
    with pytest.raises(Exception):
        assert weather("08-08-2010", "Wonderland")

def test_invalid_date():
    with pytest.raises(Exception):
        assert weather("01-12-2008", "Cobar")

def test_cobar():
    assert weather("10-02-2009", "Cobar") == (-6.2, 2.3)
    
def test_albury():
    assert weather("08-08-2010", "Albury") == (10.8, -10.0)

def test_na_min():
    assert weather("27-02-2010", "Albury") == (None, 3.7)

def test_na_max():
    assert weather("04-03-2010", "Albury") == (-5.6, None)

def test_na_both():
    assert weather("13-06-2014", "BadgerysCreek") == (None, None)