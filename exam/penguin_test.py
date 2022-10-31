from penguin import validate

def test_1():
    assert validate('P8464Q94944Z')

def test_2():
    assert validate('A1234B12344C')

def test_3():
    assert not validate('A1234567890B')

def test_sum_not_even():
    assert not validate('A2244B68834C')
    
def test_not_last_even():
    assert not validate('A1234B67833C')

def test_no_letters():
    assert not validate('11234567833')

def test_no_first_numbers():
    assert not validate('A8P64Q94944Z')

def test_no_last_numbers():
    assert not validate('A8464Q94X44Z')

def test_not_upper():
    assert not validate('p8464Q94944Z')

def test_not_ordered_first():
    assert not validate('C8464B94944E')

def test_not_ordered_second():
    assert not validate('B8464C94944A')