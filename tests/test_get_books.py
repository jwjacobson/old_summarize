import pytest
import requests
from data_processing.get_books import fetch_books, process_books

def test_fetch_books():
    base_url = 'https://gutendex.com/books?languages=en'
    book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
    assert book_request.status_code == 200
    assert 'results' in book_request.json()
    assert len(book_request.json()['results']) == 32


dummy_data = [
    # Normal data
    (
        {
            'id': 123,
            'title': 'Sample Book',
            'authors': [{'name': 'John Doe'}],
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            123: {
                'title': 'Sample Book',
                'author': 'John Doe',
                'url': 'http://example.com'
            }
        }
    ),
    # No title
    (
        {
            'id': 123,
            'authors': [{'name': 'John Doe'}],
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            123: {
                'title': 'No title found.',
                'author': 'John Doe',
                'url': 'http://example.com'
            }
        }
    ),
    # No author
    (
        {
            'id': 123,
            'title': 'Sample Book',
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            123: {
                'title': 'Sample Book',
                'author': 'No author found.',
                'url': 'http://example.com'
            }
        }
    ),
    # No formats
    (
        {
            'id': 123,
            'title': 'Sample Book',
            'authors': [{'name': 'John Doe'}]
        },
        {
            123: {
                'title': 'Sample Book',
                'author': 'John Doe',
                'url': 'No URL found.'
            }
        }
    ),
    # No title or author
    (
        {
            'id': 123,
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            123: {
                'title': 'No title found.',
                'author': 'No author found.',
                'url': 'http://example.com'
            }
        }
    ),
    # no title or formats
    (
        {
            'id': 123,
            'authors': [{'name': 'John Doe'}],
        },
        {
            123: {
                'title': 'No title found.',
                'author': 'John Doe',
                'url': 'No URL found.'
            }
        }
    ),
    # no author or formats
    (
        {
            'id': 123,
            'title': 'Sample Book',
        },
        {
            123: {
                'title': 'Sample Book',
                'author': 'No author found.',
                'url': 'No URL found.'
            }
        }
    ),
    # no title author or formats
    (
        {
            'id': 123,
        },
        {
            123: {
                'title': 'No title found.',
                'author': 'No author found.',
                'url': 'No URL found.'
            }
        }
    ),
    # no plaintext format
    (
        {
            'id': 123,
            'title': 'Sample Book',
            'authors': [{'name': 'John Doe'}],
            'formats': {'xxx': 'http://example.com'}
        },
        {
            123: {
                'title': 'Sample Book',
                'author': 'John Doe',
                'url': 'No plaintext URL found.'
            }
        }
    ),
]


@pytest.mark.parametrize('input, expected', dummy_data)
def test_process_books(input, expected):
    result = process_books([input])
    assert result == expected, f'Expected {expected}, but got {result}'