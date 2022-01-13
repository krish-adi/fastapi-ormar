from typing import List

from fastapi import APIRouter, Body, FastAPI, status
from fastapi.exceptions import HTTPException

from .models import Book
from .schemas import BookIn

router = APIRouter()


def setup_router(app: FastAPI):
    app.include_router(router)


@router.get("/", response_model=List[Book])
async def fetch_books():
    try:
        books = await Book.objects.all()
        return books
    except BaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="failed to fetch books")


@router.post("/add", response_model=Book)
async def add_book(book_in: BookIn = Body(...)):
    try:
        book = Book(**book_in.dict())
        await book.save()
        return book
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="failed to add book: " + str(err))
