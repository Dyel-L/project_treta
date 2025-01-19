from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.security import pwd_context
from app.db.models import User
from app.schemas.user import UserCreate


def create_new_user(user_data: UserCreate, db: Session):
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def fetch_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return user
