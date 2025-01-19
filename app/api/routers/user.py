from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.user_service import create_new_user, fetch_user_by_id
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/", response_model=UserRead, tags=["Users"])
def criar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(user, db)


@router.get("/{user_id}", response_model=UserRead, tags=["Users"])
def obter_usuario(user_id: int, db: Session = Depends(get_db)):
    return fetch_user_by_id(user_id, db)
