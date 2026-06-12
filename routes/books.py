from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas import BookOut, BookCreate, BookUpdate
from crud import search_books, filter_books, get_all_books, get_book_by_id, create_book, update_book, patch_book, delete_book
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookOut])
def get_all_books_route(db: Session = Depends(get_db)):
    return get_all_books(db)

@router.get("/search", response_model=List[BookOut])
def search_books_route(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    results = search_books(db, q)
    return results

@router.get("/filter", response_model=List[BookOut])
def filter_books_route(
    category: Optional[str] = Query(None), 
    author: Optional[str] = Query(None),
    year: Optional[int] = Query(None), 
    available: Optional[int] = Query(None), 
    db: Session = Depends(get_db)
):
    return filter_books(db, category, author, year, available)

@router.get("/{book_id}", response_model=BookOut)
def get_book_route(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book_route(book_data: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book_data)

@router.post("/bulk", response_model=List[BookOut], status_code=status.HTTP_201_CREATED)
def create_books_bulk(books_data: List[BookCreate], db: Session = Depends(get_db)):
    books = []
    for book_data in books_data:
        db_book = create_book(db, book_data)
        books.append(db_book)
    return books

@router.put("/{book_id}", response_model=BookOut)
def update_book_route(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    updated = update_book(db, book_id, book_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.patch("/{book_id}", response_model=BookOut)
def patch_book_route(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    updated = patch_book(db, book_id, book_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}")
def delete_book_route(book_id: int, db: Session = Depends(get_db)):
    deleted = delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book '{deleted.title}' deleted successfully", "deleted_id": deleted.id}