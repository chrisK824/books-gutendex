from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import db_models
import schemas
import calendar


def get_reviews(db: Session, book_id: int):
    # initialize a payload to return
    book_reviews = {}
    book_reviews_texts = []
    book_rating = None

    book_reviews_query_res = db.query(db_models.Review).filter(db_models.Review.book_id == book_id).all()
    # get reviews text from the results of query
    book_reviews_texts = [book_review.review for book_review in book_reviews_query_res]
    if len(book_reviews_query_res) > 0:
        book_rating = round(float(sum(
            [book_review.rating for book_review in book_reviews_query_res])/len(book_reviews_texts)), 2)
    book_reviews['reviews'] = book_reviews_texts
    book_reviews['rating'] = book_rating
    return book_reviews


def get_sorted_top_rated_books(db: Session, books_number: int):
    sorted_n_top_rated_books = {}
    get_top_avg_rated_books_query = f"SELECT book_id, avg(rating) as rating FROM reviews WHERE book_id in (SELECT DISTINCT  book_id FROM reviews) GROUP BY book_id ORDER BY rating DESC LIMIT {books_number}"
    rated_n_book_ids = db.execute(text(get_top_avg_rated_books_query)).all()
    for book in list(rated_n_book_ids):
        sorted_n_top_rated_books[book[0]] = {
            "rating" : round(book[1],2),
            "reviews" : []
        }
    book_ids = tuple([book_id for book_id, _ in sorted_n_top_rated_books.items()])
    if len(book_ids) > 0:
        if len(book_ids) == 1:
            get_reviews_for_top_n_rated_books = f"SELECT book_id, review FROM reviews WHERE book_id == {book_ids[0]}"
        else:
            get_reviews_for_top_n_rated_books = f"SELECT book_id, review FROM reviews WHERE book_id IN {book_ids}"
        reviews_for_top_n_rated_books = db.execute(text(get_reviews_for_top_n_rated_books)).all()
        for review in list(reviews_for_top_n_rated_books):
            sorted_n_top_rated_books[review[0]]['reviews'].append(review[1]) 
    return sorted_n_top_rated_books


def get_monthly_average_rating(db: Session, book_id: int):
    book_reviews = db.query(db_models.Review).filter(db_models.Review.book_id == book_id).all()
    months = list(calendar.month_name)[1:]
    monthly_ratings = {}
    for month in months:
        monthly_ratings[month] = []
    # iterate through reviews per book and append
    # the rating of a review on the corresponding month
    # list that was previously initiated
    for book_review in book_reviews:
        review_month = book_review.timestamp.strftime("%B")
        monthly_ratings[review_month].append(book_review.rating)

    monthly_avg_ratings = {}
    # iterate through months of dictionary
    # calculate the average for each month
    # given that this month contains ratings
    # otherwise set as None
    for month, ratings in monthly_ratings.items():
        if len(ratings) > 0:
            monthly_avg_ratings[month] = round(float(sum(ratings)/len(ratings)), 2)
        else:
            monthly_avg_ratings[month] = None
    return monthly_avg_ratings


def create_review(db: Session, review: schemas.BookReview):
    db_review = db_models.Review(book_id=review.book_id, rating=review.rating, review=review.review)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
