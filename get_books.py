import requests

base_url = 'https://gutendex.com/books?languages=en'
book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
if book_request.status_code != 200:
    raise Exception("Failed to fetch books from Gutendex API")
books = book_request.json()['results']
book_data = {}

def author_parse(author):
    parens = {'(', ')'}
    vanvon = {'van', 'von'}
    split_author = author.split()
    while split_author[-1][-1] in parens or split_author[-1][0] in parens:
        split_author.pop()
    last_name = split_author.pop(0)
    if last_name[-1] == ',':
        split_author.append(last_name[:-1])
    else:
        split_author.append(last_name)
    if split_author[-1].lower() in vanvon:
        split_author.append(split_author.pop(0)[:-1])
    new_author = ' '.join(split_author)
    return new_author


def get_books():
    base_url = 'https://gutendex.com/books?languages=en'
    book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
    if book_request.status_code != 200:
        raise Exception("Failed to fetch books from Gutendex API")
    books = book_request.json()['results']
    book_data = {}
    
    for book in books:
        title = book['title']
        author = author_parse(book['authors'][0]['name'])
        url = book['formats'].get('text/plain; charset=us-ascii', 'Plaintext URL not available')
        
        book_data[book['id']] = {
            'title': title,
            'author': author,
            'url': url
            }

    return book_data

if __name__ == "__main__":
    book_data = get_books()