import pytest
from datetime import date, time, datetime
from timetable import timetable

def test_dryrun():
	assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) \
	  == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), \
	      datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]

def test_large():
	assert timetable([date(2019,9,27), date(2019,9,30), date(2019, 9, 15), date(2019, 9, 11)], [time(14,10), time(10,30), time(9,8), time(15, 6)]) \
	  == [datetime(2019,9,11,9,8), datetime(2019,9,11,10,30), datetime(2019,9,11,14,10), datetime(2019,9,11,15,6), \
	  	  datetime(2019,9,15,9,8), datetime(2019,9,15,10,30), datetime(2019,9,15,14,10), datetime(2019,9,15,15,6), \
		  datetime(2019,9,27,9,8), datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,27,15,6), \
	      datetime(2019,9,30,9,8), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10), datetime(2019,9,30,15,6)]

def test_invalid():
	with pytest.raises(Exception):
		assert timetable([1, 2], [2, 3])

def test_uneven():
	assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30), time(9,8)]) \
	  == [datetime(2019,9,27,9,8), datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), \
	      datetime(2019,9,30,9,8), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]
