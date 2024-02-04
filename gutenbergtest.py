import requests
import ipdb


base_url = 'https://gutendex.com/books?languages=en'


book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
books = book_request.json()['results']
book_cache = {}
for book in books:
    print(f"{book['id']}: {book['title']} by {book['authors'][0]['name']}")

