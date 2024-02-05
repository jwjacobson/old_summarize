import requests

def get_books():
    base_url = 'https://gutendex.com/books?languages=en'
    book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
    if book_request.status_code != 200:
        raise Exception("Failed to fetch books from Gutendex API")
    books = book_request.json()['results']
    book_data = {}
    
    for book in books:
        book_data[book['id']] = {
            'title': book['title'],
            'author': book['authors'][0]['name'].split()[0][:-1],
            'url': book['formats'].get('text/plain; charset=us-ascii', 'Plaintext URL not available')
            }

    return book_data

if __name__ == "__main__":
    book_data = get_books()