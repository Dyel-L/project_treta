from sqlalchemy import Column, Integer, ForeignKey, DateTime , String, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)

    loans = relationship("Loan", back_populates="book")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

    __table_args__ = {"extend_existing": True}

    loans = relationship("Loan", back_populates="user")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    due_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")