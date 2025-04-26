from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import asc, desc
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Expense, Income
from app.models import User
from app.schema import SummaryOut
from app.routes.auth_router import get_current_user

router = APIRouter(prefix="/summary", tags=["summary"])

# Get total income and expense for the user
@router.get("/", response_model=SummaryOut)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("amount", description="Field to sort by (amount/date)"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
):
    query_expenses = db.query(Expense).filter(Expense.user_id == current_user.id)
    query_incomes = db.query(Income).filter(Income.user_id == current_user.id)

    if not query_expenses.count() and not query_incomes.count():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expenses or incomes found for the user.",
        )

    if start_date:
        query_expenses= query_expenses.filter(Expense.date >= start_date)
        query_incomes = query_incomes.filter(Income.date >= start_date)
    if end_date:
        query_expenses = query_expenses.filter(Expense.date <= end_date)
        query_incomes = query_incomes.filter(Income.date <= end_date)
    if category_id:
        query_expenses = query_expenses.filter(Expense.category_id == category_id)
        query_incomes = query_incomes.filter(Income.category_id == category_id)

    if sort_by in ["amount", "date"]:
        order_func = asc if sort_order == "asc" else desc
        query_expenses = query_expenses.order_by(order_func(getattr(Expense, sort_by)))
        query_incomes = query_incomes.order_by(order_func(getattr(Income, sort_by)))

    expenses = query_expenses.all()
    incomes = query_incomes.all()
    # Calculate the total amount
    total_expenses = sum(expense.amount for expense in expenses)
    total_income = sum(income.amount for income in incomes)

    # Return the summary
    return {
        "total_expenses": total_expenses,
        "total_income": total_income,
    }
