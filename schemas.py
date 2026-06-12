import os
from pydantic import BaseModel, field_validator, computed_field
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    category: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int = 1
    available: int = 1

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v):
        if v is not None and len(v) > 20:
            raise ValueError('ISBN must be 20 characters or less')
        return v

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
    image_path: Optional[str] = None
    pdf_path: Optional[str] = None

    class Config:
        from_attributes = True

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.image_path:
            return f"/images/{os.path.basename(self.image_path)}"
        return None

    @computed_field
    @property
    def pdf_url(self) -> Optional[str]:
        if self.pdf_path:
            return f"/pdfs/{os.path.basename(self.pdf_path)}"
        return None