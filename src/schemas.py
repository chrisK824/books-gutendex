from pydantic import BaseModel, Field
from typing import Optional, List, Union

class BookReview(BaseModel):
    book_id : int
    # accept only a rating number from range (0-5)
    rating : int = Field(..., ge=0, le=5)
    review : str
    class Config:
        orm_mode = True

class Book(BaseModel):
    id : int
    title : str
    authors : list
    languages : list
    download_count : int

class BookSearch(BaseModel):
    count : Optional[int] = 0
    next: Optional[str] = None
    previous : Optional[str] = None
    books : List[Book]

class BookDetails(Book):
    rating: Optional[float] = None
    reviews : Optional[list] = []

class TopRatedBooks(BaseModel):
    books: List[Union[BookDetails, None]] = []
