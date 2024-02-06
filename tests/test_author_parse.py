import pytest
from data_processing.get_books import author_parse

def test_last_first():
    assert author_parse('Austen, Jane') == 'Jane Austen'

def test_last_first_middle():
    assert author_parse('Stevenson, Robert Louis') == 'Robert Louis Stevenson'

def test_parentheticals():
    assert author_parse('Chesterton, G. K. (Gilbert Keith)') == 'G. K. Chesterton'

def test_von():
    assert author_parse('Von Arnim, Elizabeth') == 'Elizabeth Von Arnim'

def test_van():
    assert author_parse('Van Pelt, Linus') == 'Linus Van Pelt'

def test_compound_last_1():
    assert author_parse('Martinez de la Torre, Rafael') == 'Rafael Martinez de la Torre'

def test_compound_last_2(:)
    assert author_parse('Cervantes Saavedra, Miguel de') == 'Miguel de Cervantes Saavedra'

def test_jr():
    assert author_parse('Alger, Horatio, Jr.') == 'Horatio Alger Jr.'