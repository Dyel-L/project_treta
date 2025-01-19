from pydantic import BaseModel
from datetime import date
from typing import Optional

class LoanCreate(BaseModel):
    user_id: int
    book_id: int
    due_date: date

class LoanRead(BaseModel):
    id: int
    user_id: int
    book_id: int
    due_date: date

    class Config:
        orm_mode = True

class LoanResponse(BaseModel):
    id: int
    user_name: str
    book_title: str
    due_date: date

class LoanUpdate(BaseModel):
    due_date: Optional[date]