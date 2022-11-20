from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from database import Base

class Review(Base):
    __tablename__ = "reviews"
    # autoincreament id for each review insertion
    id = Column(Integer, primary_key=True, index=True)
    # timestamp is assigned automatically as
    # a column value for a review when this is
    # inserted in the db
    timestamp = Column(DateTime, default=func.now())
    book_id = Column(Integer)
    rating = Column(Integer)
    review = Column(String)

