import pytest
import requests
from data_processing.get_books import get_books

def test_fetch_books():
    base_url = 'https://gutendex.com/books?languages=en'
    book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
    assert book_request.status_code == 200
    assert 'results' in book_request.json()
    assert len(book_request.json()['results']) == 32
    books = book_request.json()['results']