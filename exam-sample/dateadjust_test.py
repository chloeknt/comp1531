from dateadjust import adjust

import pytest

def test_1():
    assert adjust(4, 4, '16:40 on 28 January 2021') == '05:00 on 28 February 2021'
