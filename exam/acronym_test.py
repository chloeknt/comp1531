from acronym import acronym_make

def test_1():
    assert acronym_make(['I am very tired today']) == ['VTT']

def test_normal_list():
    assert acronym_make(['Very tired today', 'Hello to you too']) == ['VTT', 'HTYT']

def test_all_vowel():
    assert acronym_make(['Annoying orange egg']) == ['']

def test_mix_list():
    assert acronym_make(['The annoying orange tree', "Annoying orange egg"]) == ['TT', '']

def test_too_long():
    assert acronym_make(['Kn Ne Be Ma He Ju Ka Ls Be No Ye']) == ['N/A']
