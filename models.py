from sqlalchemy import Column, Integer, String
from database import Base

class Book(Base):
    __tablename__ = "books"
    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title       = Column(String(255), nullable=False)
    author      = Column(String(255), nullable=False)
    category    = Column(String(100), nullable=True)
    year        = Column(Integer, nullable=True)
    isbn        = Column(String(20), nullable=True)
    quantity    = Column(Integer, default=1)
    available   = Column(Integer, default=1)
    image_path  = Column(String(255), nullable=True)
    pdf_path    = Column(String(255), nullable=True)