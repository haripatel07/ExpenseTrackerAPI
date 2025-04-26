from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

# Create a model for the User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    category = relationship("Category", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    incomes = relationship("Income", back_populates="user")
    summary = relationship("Summary", back_populates="user")


# Create model for Category of expense
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="category")
    expenses = relationship("Expense", back_populates="category")
    incomes = relationship("Income", back_populates="category")


# Income Model (For tracking income)
class Income(Base):
    __tablename__ = "incomes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    category = relationship("Category", back_populates="incomes")
    user = relationship("User", back_populates="incomes")


# Expense Model (For tracking expenses)
class Expense(Base):
    __tablename__ = "expenses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")


# Summary Model (For tracking summary of expenses and income)
class Summary(Base):
    __tablename__ = "summary"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    total_expenses: Mapped[float] = mapped_column(Float)
    total_income: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="summary")
