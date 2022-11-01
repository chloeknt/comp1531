from circle import Circle

def test_small():
    c = Circle(3)
    assert(round(c.circumference(), 1) == 18.8)
    assert(round(c.area(), 1) == 28.3)

def test_medium():
    c = Circle(12)
    assert(round(c.circumference(), 1) == 75.4)
    assert(round(c.area(), 1) == 452.2)

def test_large():
    c = Circle(100)
    assert(round(c.circumference(), 1) == 628)
    assert(round(c.area(), 1) == 31400)

def test_float():
    c = Circle(6.52)
    assert(round(c.circumference(), 1) == 40.9)
    assert(round(c.area(), 1) == 133.5)
