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
            models.Book.author.ilike(search_term)
        )
    ).all()

def create_book(db: Session, book: schemas.BookCreate):
    try:
        data = book.model_dump()
    except AttributeError:
        data = book.dict()
    db_book = models.Book(**data)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_data: schemas.BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    try:
        update_data = book_data.model_dump(exclude_unset=True)
    except AttributeError:
        update_data = book_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book   # return the deleted book so the route can confirm it
