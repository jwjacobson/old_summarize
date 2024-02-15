import pytest
import requests
from data_processing.get_books import fetch_books, process_books

def test_gutendex_api():
    base_url = 'https://gutendex.com/books?languages=en'
    book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
    assert book_request.status_code == 200
    assert 'results' in book_request.json()
    assert len(book_request.json()['results']) == 32

def test_fetch_books_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'results': ['book1', 'book2']}
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    books = fetch_books()
    assert books == ['book1', 'book2']

def test_fetch_books_http_error(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.HTTPError("Http Error"))

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_books()

def test_fetch_books_connection_error(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection Error"))

    with pytest.raises(requests.exceptions.ConnectionError):
        fetch_books()

def test_fetch_books_timeout(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.Timeout("Timeout Error"))

    with pytest.raises(requests.exceptions.Timeout):
        fetch_books()

def test_fetch_books_request_exception(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException("Exotic Error"))

    with pytest.raises(requests.exceptions.RequestException):
        fetch_books()


dummy_data = [
    # Normal data
    (
        {
            'id': 123,
            'title': 'Sample Book',
            'authors': [{'name': 'Doe, John'}],
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
            'authors': [{'name': 'Doe, John'}],
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
            'authors': [{'name': 'Doe, John'}]
        },
        {
            123: {
                'title': 'Sample Book',
                'author': 'John Doe',
                'url': 'No URLs found.'
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
            'authors': [{'name': 'Doe, John'}],
        },
        {
            123: {
                'title': 'No title found.',
                'author': 'John Doe',
                'url': 'No URLs found.'
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
                'url': 'No URLs found.'
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
                'url': 'No URLs found.'
            }
        }
    ),
    # no plaintext format
    (
        {
            'id': 123,
            'title': 'Sample Book',
            'authors': [{'name': 'Doe, John'}],
            'formats': {'xxx': 'http://example.com'}
        },
        {
            123: {
                'title': 'Sample Book',
                'author': 'John Doe',
                'url': 'No URL found.'
            }
        }
    ),
]


@pytest.mark.parametrize('input, expected', dummy_data)
def test_process_books(input, expected):
    result = process_books([input])
    assert result == expected, f'Expected {expected}, but got {result}'
