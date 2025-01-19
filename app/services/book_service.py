from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from typing import List, Type
from app.db.models import Book
from app.schemas.book import BookCreate, BookResponse
from app.services.auth_service import get_current_user
from app.db.models import User

def list_books(db: Session, current_user: User = Depends(get_current_user)) -> list[Type[Book]]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    return db.query(Book).all()

def create_book(book: BookCreate, db: Session, current_user: User = Depends(get_current_user)) -> BookResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    new_book = Book(title=book.title, author=book.author, is_available=book.is_available)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_book(book_id: int, db: Session, current_user: User = Depends(get_current_user)) -> BookResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book

def update_book(book_id: int, book: BookCreate, db: Session, current_user: User = Depends(get_current_user)) -> BookResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    existing_book.title = book.title
    existing_book.author = book.author
    existing_book.is_available = book.is_available
    db.commit()
    db.refresh(existing_book)
    return existing_book

def delete_book(book_id: int, db: Session, current_user: User = Depends(get_current_user)) -> dict:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(existing_book)
    db.commit()
    return {"detail": "Book deleted successfully"}

def toggle_book_availability(book_id: int, is_available: bool, db: Session, current_user: User = Depends(get_current_user)) -> Book:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    book.is_available = is_available
    db.commit()
    db.refresh(book)
    return book