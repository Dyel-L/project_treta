from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Depends
from app.db.models import Loan, User, Book
from app.schemas.loan import LoanCreate, LoanUpdate, LoanResponse
from app.services.auth_service import get_current_user

def create_loan(loan: LoanCreate, db: Session, current_user: User = Depends(get_current_user)) -> LoanResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Livro não está disponível")

    user = db.query(User).filter(User.id == loan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")

    new_loan = Loan(user_id=loan.user_id, book_id=loan.book_id, due_date=loan.due_date)
    db.add(new_loan)
    book.is_available = False
    db.commit()
    db.refresh(new_loan)

    return LoanResponse(
        id=new_loan.id,
        user_name=user.name,
        book_title=book.title,
        due_date=new_loan.due_date,
    )

def list_loans(db: Session, current_user: User = Depends(get_current_user)) -> list[LoanResponse]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    loans = db.query(Loan).options(joinedload(Loan.user), joinedload(Loan.book)).all()
    return [
        LoanResponse(
            id=loan.id,
            user_name=loan.user.name,
            book_title=loan.book.title,
            due_date=loan.due_date.date(),
        )
        for loan in loans
    ]

def get_loan(loan_id: int, db: Session, current_user: User = Depends(get_current_user)) -> LoanResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    loan = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.book))
        .filter(Loan.id == loan_id)
        .first()
    )
    if not loan:
        raise HTTPException(status_code=404, detail="Emprestimo não encontrado")

    return LoanResponse(
        id=loan.id,
        user_name=loan.user.name,
        book_title=loan.book.title,
        due_date=loan.due_date.date(),
    )

def update_loan(loan_id: int, loan_data: LoanUpdate, db: Session, current_user: User = Depends(get_current_user)) -> LoanResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Emprestimo não encontrado")

    if loan_data.due_date:
        loan.due_date = loan_data.due_date

    db.commit()
    db.refresh(loan)

    return LoanResponse(
        id=loan.id,
        user_name=loan.user.name,
        book_title=loan.book.title,
        due_date=loan.due_date,
    )

def delete_loan(loan_id: int, db: Session, current_user: User = Depends(get_current_user)) -> dict:
    if not current_user:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Emprestimo não encontrado")

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book:
        book.is_available = True

    db.delete(loan)
    db.commit()
    return {"log": f"Emprestimo com o ID {loan_id} deletado"}