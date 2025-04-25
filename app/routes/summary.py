from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import asc, desc
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Expense, Income
from sqlalchemy import func
from app.models import User
from app.schema import SummaryOut
from app.routes.auth_router import get_current_user

router = APIRouter(prefix="/summary", tags=["summary"])

# Get total income and expense for the user
@router.get("/")
@router.get("/summary", response_model=SummaryOut)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("amount", description="Field to sort by (amount/date)"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
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

    expenses = query.all()

    # Calculate the total amount
    total_amount = sum(expense.amount for expense in expenses)
    total_income = sum(expense.income.amount for expense in expenses)  # Assuming income is related to expense

    # Return the summary
    return {
        "total_expenses": total_amount,
        "total_income": total_income,
    }
