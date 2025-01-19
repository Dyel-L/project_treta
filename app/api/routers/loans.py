from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.schemas.loan import LoanCreate, LoanUpdate, LoanResponse
from app.services.auth_service import get_current_user
from app.services.loan_service import (
    create_loan,
    list_loans,
    get_loan,
    update_loan,
    delete_loan,
)

router = APIRouter()

@router.post("/", response_model=LoanResponse, tags=["Loans"])
def adicionar_emprestimo(loan: LoanCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_loan(loan, db, current_user)


@router.get("/", response_model=list[LoanResponse], tags=["Loans"])
def obter_emprestimos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_loans(db, current_user)


@router.get("/{loan_id}", response_model=LoanResponse, tags=["Loans"])
def obter_emprestimo_por_id(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_loan(loan_id, db, current_user)


@router.put("/{loan_id}", response_model=LoanResponse, tags=["Loans"])
def atualizar_emprestimo(loan_id: int, loan_data: LoanUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_loan(loan_id, loan_data, db, current_user)


@router.delete("/{loan_id}", tags=["Loans"])
def excluir_emprestimo(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_loan(loan_id, db, current_user)
