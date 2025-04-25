from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Category, User
from app.schema import CategoryCreate, CategoryOut
from app.routes.auth_router import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])

# Create a new category
@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_category = Category(name=category.name, user_id=user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Get all categories
@router.get("/", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Category).filter(Category.user_id == user.id).all()