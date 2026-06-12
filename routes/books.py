import os
from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas import BookOut, BookCreate, BookUpdate
from crud import search_books, filter_books, get_all_books, get_book_by_id, create_book, update_book, patch_book, delete_book, save_image_path, save_pdf_path
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

IMAGES_DIR = "images"
PDFS_DIR = "pdfs"

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

@router.post("/{book_id}/upload-image", response_model=BookOut)
def upload_image_route(book_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    allowed_extensions = {".jpg", ".png", ".jpeg"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, and JPEG files are allowed")
    
    file_content = file.file.read()
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 10MB")
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    image_filename = f"book_{book_id}_image{file_ext}"
    image_path = os.path.join(IMAGES_DIR, image_filename)
    
    with open(image_path, "wb") as buffer:
        buffer.write(file_content)
    
    return save_image_path(db, book_id, image_path)

@router.post("/{book_id}/upload-pdf", response_model=BookOut)
def upload_pdf_route(book_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    allowed_extensions = {".pdf"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_content = file.file.read()
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 10MB")
    
    os.makedirs(PDFS_DIR, exist_ok=True)
    pdf_filename = f"book_{book_id}_pdf{file_ext}"
    pdf_path = os.path.join(PDFS_DIR, pdf_filename)
    
    with open(pdf_path, "wb") as buffer:
        buffer.write(file_content)
    
    return save_pdf_path(db, book_id, pdf_path)

@router.delete("/{book_id}")
def delete_book_route(book_id: int, db: Session = Depends(get_db)):
    deleted = delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book '{deleted.title}' deleted successfully", "deleted_id": deleted.id}