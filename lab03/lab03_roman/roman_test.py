from roman import roman

def test_one_digit():
    assert roman('I') == 1
    assert roman('V') == 5
    assert roman('X') == 10
    assert roman('L') == 50

def test_two_digit():
    assert roman('II') == 2
    assert roman('IV') == 4
    assert roman('VI') == 6
    assert roman('XV') == 15

def test_multiple_digit():
    assert roman('XVI') == 16
    assert roman('XXIV') == 24
    assert roman('XVIII') == 18
    assert roman('XLVIII') == 48
    assert roman('LXXVIII') == 78
    assert roman('LXXXVIII') == 88
