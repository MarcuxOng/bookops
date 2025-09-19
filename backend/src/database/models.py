import enum

from typing import Optional, List
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.database.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class RequestTier(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    borrowed_books: Mapped[List["BorrowedBook"]] = relationship(back_populates="user")
    customer_requests: Mapped[List["CustomerRequest"]] = relationship(back_populates="user")

class Book(Base):
    __tablename__ = "books"

    isbn: Mapped[str] = mapped_column(String(20), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))
    publisher: Mapped[str] = mapped_column(String(100))
    language: Mapped[str] = mapped_column(String(50))
    copies: Mapped[int] = mapped_column(Integer)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    publication_year: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    borrowing_records: Mapped[List["BorrowedBook"]] = relationship(back_populates="book")

class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    borrow_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    isbn: Mapped[str] = mapped_column(ForeignKey("books.isbn"))
    borrowed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    returned_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="borrowed_books")
    book: Mapped["Book"] = relationship(back_populates="borrowing_records")

class CustomerRequest(Base):
    __tablename__ = "customer_requests"

    request_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    request_detail: Mapped[str] = mapped_column(Text)
    tier: Mapped[RequestTier] = mapped_column(Enum(RequestTier))
    points: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="customer_requests")