from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Expense, User, Category
from app.schema import ExpenseCreate, ExpenseOut
from app.routes.auth_router import get_current_user
from typing import Optional
from datetime import date

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Create a new expense
@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == expense.category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or not authorized"
        )

    db_expense = Expense(
        description=expense.description,
        amount=expense.amount,
        date=expense.date,
        category_id=expense.category_id,
        user_id=current_user.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Get all expenses with filters, sorting, and pagination
@router.get("/", response_model=list[ExpenseOut])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("date", description="Field to sort by (amount/date)"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return")
):
    query = db.query(Expense).filter(Expense.user_id == current_user.id)

    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    if category_id:
        query = query.filter(Expense.category_id == category_id)

    if sort_by in ["amount", "date"]:
        order_func = asc if sort_order == "asc" else desc
        query = query.order_by(order_func(getattr(Expense, sort_by)))

    return query.offset(skip).limit(limit).all()
