from requests_cache import CachedSession
from urllib.parse import quote_plus

GUTENDEX_BASIC_URL = "https://gutendex.com/"
# cache time in seconds, 15 minutes
# it's unlikely that some book gets inserted in
# the cache time or that a user will search for it
# for more than this time
CACHE_TIME = 900

GUTENDEX_SESSION = CachedSession(expire_after=CACHE_TIME, cache_control=True)
GUTENDEX_SESSION.headers.update({'Content-Type': 'application/json'})


def search_books(keyword, page):
    search_res = GUTENDEX_SESSION.get(
        f"{GUTENDEX_BASIC_URL}books?search={quote_plus(keyword)}&page={page}")
    search_res_dict = search_res.json()
    result = {
        "count": search_res_dict['count'] if 'count' in search_res_dict else 0,
        "next": search_res_dict['next'] if 'next' in search_res_dict else None,
        "previous": search_res_dict['previous'] if 'previous' in search_res_dict else None,
        "books": search_res_dict['results'] if 'previous' in search_res_dict else []
    }
    return result


def get_book(book_id):
    book = None
    response = GUTENDEX_SESSION.get(f"{GUTENDEX_BASIC_URL}books/{book_id}")
    http_status = response.status_code
    response_json = response.json()
    if http_status != 200:
        raise ValueError(f"No book found with ID {book_id}")
    else:
        book = response_json
        return book
