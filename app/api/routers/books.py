from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.book import BookCreate, BookResponse
from app.db.database import get_db
from app.services.auth_service import get_current_user
from app.services.book_service import (
    list_books,
    create_book,
    get_book,
    update_book,
    delete_book,
    toggle_book_availability,
)

router = APIRouter()

@router.get("/", dependencies=[Depends(get_current_user)], tags=["Books"])
def obter_livros(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_books(db, current_user)


@router.post("/", response_model=BookResponse, tags=["Books"])
async def adicionar_livro(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_book(book, db, current_user)


@router.get("/{book_id}", response_model=BookResponse, tags=["Books"])
async def obter_livro_por_id(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_book(book_id, db, current_user)


@router.put("/{book_id}", response_model=BookResponse, tags=["Books"])
async def atualizar_livro(book_id: int, book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_book(book_id, book, db, current_user)


@router.delete("/{book_id}", tags=["Books"])
async def excluir_livro(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_book(book_id, db, current_user)

@router.patch("/{book_id}/availability", response_model=BookResponse, tags=["Books"])
def alterar_disponibilidade(book_id: int, is_available: bool, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return toggle_book_availability(book_id, is_available, db, current_user)