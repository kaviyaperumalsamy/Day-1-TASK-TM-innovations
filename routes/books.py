# routes/books.py
# ─────────────────────────────────────────────
# This file defines all the API ENDPOINTS (URLs) for books.
# Think of endpoints as doors — the frontend knocks on a door,
# and this file answers with the right data.
#
# Endpoints we're creating:
#   GET    /books/           → get all books
#   GET    /books/search     → search books by title/author
#   GET    /books/{id}       → get one book by ID
#   POST   /books/           → add a new book
#   PUT    /books/{id}       → update a book
#   DELETE /books/{id}       → delete a book
# ─────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

import crud, schemas
from database import get_db

# APIRouter groups related endpoints together
# We tell main.py to include this router with prefix "/books"
router = APIRouter(
    prefix="/books",
    tags=["Books"]      # shows as a group label in /docs
)


# ── GET all books ────────────────────────────
@router.get("/", response_model=List[schemas.BookOut])
def get_all_books(db: Session = Depends(get_db)):
    """Return a list of all books in the library."""
    books = crud.get_all_books(db)
    return books


# ── GET search (must be above /{book_id} to avoid conflict) ──
@router.get("/search", response_model=List[schemas.BookOut])
def search_books(
    q: str = Query(..., min_length=1, description="Search by title or author"),
    db: Session = Depends(get_db)
):
    """Search books by title or author name."""
    results = crud.search_books(db, q)
    if not results:
        raise HTTPException(status_code=404, detail="No books found matching your search.")
    return results


# ── GET one book by ID ───────────────────────
@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Return a single book by its ID."""
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found.")
    return book


# ── POST create a new book ───────────────────
@router.post("/", response_model=schemas.BookOut, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Add a new book to the library."""
    new_book = crud.create_book(db, book)
    return new_book


# ── PUT update a book ────────────────────────
@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update details of an existing book."""
    updated = crud.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found.")
    return updated


# ── DELETE remove a book ─────────────────────
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book from the library."""
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found.")
    return {"message": f"Book '{deleted.title}' deleted successfully."}
