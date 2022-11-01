from datetime import date, time, datetime
from timetable import timetable 
import pytest

def test_one():
    assert timetable([date(2019,9,27)], [time(14,10)]) == [datetime(2019,9,27,14,10)]

def test_two():
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]

def test_multiple():
    assert timetable([date(2019,9,27), date(2019,9,30), date(2019,10,2)], [time(14,10), time(10,30), time(8,20)]) == [datetime(2019,9,27,8,20), datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,8,20), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10), datetime(2019,10,2,8,20), datetime(2019,10,2,10,30), datetime(2019,10,2,14,10)]
    
def test_uneven_less_time():
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10)]) == [datetime(2019,9,27,14,10), datetime(2019,9,30,14,10)]
    
def test_uneven_less_date():
    assert timetable([date(2019,9,27)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10)]