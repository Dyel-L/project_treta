from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    is_available: Optional[bool] = True

class BookCreate(BaseModel):
    title: str
    author: str
    is_available: bool

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool

class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True
