import pytest
from data_processing.get_books import author_parse

def test_one_name():
    assert author_parse('Anonymous') == 'Anonymous'

def test_last_first():
    assert author_parse('Austen, Jane') == 'Jane Austen'

def test_last_first_middle():
    assert author_parse('Stevenson, Robert Louis') == 'Robert Louis Stevenson'

def test_parentheticals():
    assert author_parse('Chesterton, G. K. (Gilbert Keith)') == 'G. K. Chesterton'

def test_parentheticals_irregular():
    assert author_parse('H. D. (Hilda Doolittle)') == 'H. D.'

def test_von():
    assert author_parse('Von Arnim, Elizabeth') == 'Elizabeth Von Arnim'

def test_van():
    assert author_parse('Sanchez, Nellie Van de Grift') == 'Nellie Van de Grift Sanchez'

def test_compound_last_1():
    assert author_parse('Martinez de la Torre, Rafael') == 'Rafael Martinez de la Torre'

def test_compound_last_2():
    assert author_parse('Cervantes Saavedra, Miguel de') == 'Miguel de Cervantes Saavedra'

def test_jr():
    assert author_parse('Alger, Horatio, Jr.') == 'Horatio Alger Jr.'