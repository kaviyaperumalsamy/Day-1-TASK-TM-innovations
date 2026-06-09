from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    category: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int = 1
    available: int = 1

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: Optional[int] = None
    available: Optional[int] = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    category: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int
    available: int

    class Config:
        from_attributes = True