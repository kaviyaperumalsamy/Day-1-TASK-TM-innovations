from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

def get_all_books(db: Session):
    return db.query(models.Book).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def search_books(db: Session, query: str):
    search_term = f"%{query}%"
    return db.query(models.Book).filter(
        or_(
            models.Book.title.ilike(search_term),
            models.Book.author.ilike(search_term),
            models.Book.category.ilike(search_term),
            models.Book.isbn.ilike(search_term)
        )
    ).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        category=book.category,
        year=book.year,
        isbn=book.isbn,
        quantity=book.quantity,
        available=book.available
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_data: schemas.BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    if book_data.title is not None:
        db_book.title = book_data.title
    if book_data.author is not None:
        db_book.author = book_data.author
    if book_data.category is not None:
        db_book.category = book_data.category
    if book_data.year is not None:
        db_book.year = book_data.year
    if book_data.isbn is not None:
        db_book.isbn = book_data.isbn
    if book_data.quantity is not None:
        db_book.quantity = book_data.quantity
    if book_data.available is not None:
        db_book.available = book_data.available
    db.commit()
    db.refresh(db_book)
    return db_book

def patch_book(db: Session, book_id: int, book_data: schemas.BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db.commit()
    db.refresh(db_book)
    return update_book(db, book_id, book_data)

def save_image_path(db: Session, book_id: int, image_path: str):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db_book.image_path = image_path
    db.commit()
    db.refresh(db_book)
    return db_book

def save_pdf_path(db: Session, book_id: int, pdf_path: str):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db_book.pdf_path = pdf_path
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

def filter_books(db: Session, category: str = None, author: str = None, year: int = None, available: int = None):
    query = db.query(models.Book)
    if category:
        query = query.filter(models.Book.category.ilike(f"%{category}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year:
        query = query.filter(models.Book.year == year)
    if available is not None:
        query = query.filter(models.Book.available >= available)
    return query.all()