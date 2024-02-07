import requests

base_url = 'https://gutendex.com/books?languages=en'
book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
if book_request.status_code != 200:
    raise Exception("Failed to fetch books from Gutendex API")
books = book_request.json()['results']
book_data = {}

def remove_parens(author):
    """
    Remove parentheticals from an author's name, for passing back to author_parse function
    """
    
    parens = {'(', ')'}  
    split_author = author.split()

    while split_author[-1][-1] in parens or split_author[-1][0] in parens: # Remove parentheticals
        split_author.pop()

    return ' '.join(split_author)

def author_parse(author):
    """
    Take the author information which is stored in Last, First Middle format and convert it to First Middle Last.
    For now it only handles the first author, so second authors of multiauthor books are out of luck.
    Examples:
    'Shelley, Mary Wollstonecraft' -> 'Mary Wollstonecraft Shelley'
    'Von Arnim, Elizbeth' -> 'Elizbeth Von Arnim'
    """

    if author[-1] == ')':
        author = remove_parens(author)

    split_author = author.split(',')

    if len(split_author) == 1: # One-name authors require no processing
        return author
    elif len(split_author) == 2: # Presence of only one comma implies 'conventional' name structure (last + first [+ middle])
        return split_author[1].lstrip() + ' ' + split_author[0]
    else:                       # Presence of more than one comma implies a suffix like "Jr."
        return split_author[1].lstrip() + ' ' + split_author[0] + ' ' + split_author[2].lstrip()


def get_books():
    base_url = 'https://gutendex.com/books?languages=en'
    book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
    if book_request.status_code != 200:
        raise Exception("Failed to fetch books from Gutendex API")
    books = book_request.json()['results']
    book_data = {}
    
    for book in books:
        title = book.get('title', 'No title found...')
        author = book.get('authors', 'No author found...')[0]['name']
        author = author_parse(author)
        urls = book.get('formats', 'No URLs found...')
        url = urls.get('text/plain; charset=us-ascii', 'No plaintext URL found...')
        
        book_data[book['id']] = {
            'title': title,
            'author': author,
            'url': url
            }

    return book_data

if __name__ == "__main__":
    book_data = get_books()