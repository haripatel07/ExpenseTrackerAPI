from pydantic import BaseModel, EmailStr
from typing import Optional, List
#Register a User
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#Return user data
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # This allows Pydantic to read data as dictionaries

#Token data
class Token(BaseModel):
    access_token: str
    token_type: str

# Category Model 
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryOut(CategoryCreate):
    id: int

    class Config:
        orm_mode = True

# Income Model
class IncomeCreate(BaseModel):
    description: str
    amount: float
    date: str
    category_id: int

class IncomeOut(IncomeCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Expense Model
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: str
    category_id: int

class ExpenseOut(ExpenseCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Summary Model
from pydantic import BaseModel

class SummaryOut(BaseModel):
    total_expenses: float
    total_income: float

    class Config:
        orm_mode = True
