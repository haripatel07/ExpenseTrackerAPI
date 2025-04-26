from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Income, User
from app.schema import IncomeCreate, IncomeOut
from app.routes.auth_router import get_current_user
from typing import Optional
from datetime import date

router = APIRouter(prefix="/income", tags=["Income"])

# Create a new income
@router.post("/", response_model=IncomeOut)
def add_income(income: IncomeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_income = Income(**income.dict(), user_id=user.id)
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

# Get all incomes
@router.get("/", response_model=list[IncomeOut])
def get_incomes(
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
    query = db.query(Income).filter(Income.user_id == current_user.id)

    if start_date:
        query = query.filter(Income.date >= start_date)
    if end_date:
        query = query.filter(Income.date <= end_date)
    if category_id:
        query = query.filter(Income.category_id == category_id)

    if sort_by in ["amount", "date"]:
        order_func = asc if sort_order == "asc" else desc
        query = query.order_by(order_func(getattr(Income, sort_by)))

    return query.offset(skip).limit(limit).all()

# Delete an income by ID
@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(
    income_id : int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_income = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == current_user.id
    ).first()

    if not db_income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income not found or not authorized"
        )
    db.delete(db_income)
    db.commit()
    return {"detail": "Income deleted successfully"}

    
