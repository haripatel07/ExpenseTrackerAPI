from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schema, crud
from app.database import SessionLocal, get_db
from app.models import User


#Create a router
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schema.UserOut)
def register_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return crud.create_user(db=db, user=user)



