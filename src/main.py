import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Query
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database_crud, db_models
from database import SessionLocal, engine
from schemas import BookReview, BookSearch, BookDetails, TopRatedBooks
import gutendexAPI

db_models.Base.metadata.create_all(bind=engine)

def get_reviews_db():
    reviews_db = SessionLocal()
    try:
        yield reviews_db
    finally:
        reviews_db.close()

description = """
Gutendex books API helps people
to easily search for books to read, review a book they read
and see reviews for recommended books.

#### Users

You will be able to:

* Search for books given a title.
* Post a review and a rating for a specific book.
* Get the details and the average rating of a specific book.
* Get the top N books based on their average rating.
* Get a book's average rating per month.
"""

booksAPI = FastAPI(
    title='Gutendex books API integration',
    description=description,
    contact={
        "name": "Christos Karvouniaris",
        "email": "christos.karvouniaris247@gmail.com",
        "url" : "https://www.linkedin.com/in/chriskarvouniaris/"
    },
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs"
)

booksAPI.add_middleware(CORSMiddleware, allow_origins=['*'])

@booksAPI.get("/v1/books/search", response_model=BookSearch, summary ="Search for books from Gutendex based on title keywords", tags=["Books search"])
def search_books(keyword : str, request: Request,  page : int = 1):
    """
    Returns all books from Gutendex search endpoint
    based on the given keyword
    (books objects are trimmed for the desired fields)
    """
    try:
        result = gutendexAPI.search_books(keyword, page)
        base_url = str(request.base_url)
        base_url = base_url[:-1]
        path = request.scope['path']
        if result['next']:
            next_page = page + 1
            result['next'] = f"{base_url}{path}?keyword={keyword}&page={next_page}"
        if result['previous']:
            previous_page = page -1
            result['previous']
            result['previous'] = f"{base_url}{path}?keyword={keyword}&page={previous_page}"
        return result
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@booksAPI.get("/v1/books/{book_id}/details", response_model=BookDetails, summary ="Get a book's details by ID", tags=["Books details"])
def get_book_details(book_id : int, db: Session = Depends(get_reviews_db)):
    """
    Given a book ID, returns a book
    from Gutendex, combined with 
    rating average and reviews array
    """
    try:
        result = gutendexAPI.get_book(book_id)
        book_reviews = database_crud.get_reviews(db, book_id)
        result['reviews'] = book_reviews['reviews'] or []
        result['rating'] = book_reviews['rating'] or None
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@booksAPI.post("/v1/reviews", summary="Review a book from Gutendex by it's ID", tags=["Books reviews"])
def post_review(review : BookReview, db: Session = Depends(get_reviews_db)):
    """
    Posts a review for a book, 
    with a rating number and 
    a text comment.
    """
    try:
        book = gutendexAPI.get_book(review.book_id)
        database_crud.create_review(db, review)
        return {"result" : f"Review posted successfully for book {book['id']}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@booksAPI.get("/v1/reviews/top", response_model=TopRatedBooks, summary="Get top N rated books from Gutendex", tags=["Books reviews"])
def get_top_n_rated_books(books_number : int = Query(ge=1), db: Session = Depends(get_reviews_db)):
    """
    Given an N number, returns N top rated books, 
    based on their average rating.
    By default returns the top 1 (best rated) book
    """
    try:
        books = []
        top_rated_books = database_crud.get_sorted_top_rated_books(db, books_number)
        for book_id, reviews in top_rated_books.items():
            book = gutendexAPI.get_book(book_id)
            book['reviews'] = reviews['reviews']
            book['rating'] = reviews['rating']
            books.append(book)
        return {"books" : books}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@booksAPI.get("/v1/reviews/monthly", summary="Get monthly average rating for a given book ID from Gutendex", tags=["Books reviews"])
def get_monthly_average_rating(book_id : int, db: Session = Depends(get_reviews_db)):
    """
    Given a book ID, returns the
    average rating of the book per month
    """
    try:
        book_avg_rating_per_month = database_crud.get_monthly_average_rating(db, book_id)
        return {
            "result": {
                "book_id" : book_id,
                "average_ratings" : book_avg_rating_per_month
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

if __name__ == '__main__':
    uvicorn.run(booksAPI, host="0.0.0.0", port=9999)
