from fastapi import FastAPI
from app.database import Base, engine
from app.routes import users
from app.routes import auth_router, category, expenses, income, summary
#Create the database tables
Base.metadata.create_all(bind=engine)

#Create an instance of FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "Welcome to Expense Tracker API"}

#Include the router for user routes
app.include_router(users.router)

app.include_router(auth_router.router)

app.include_router(category.router)
app.include_router(expenses.router)
app.include_router(income.router)
app.include_router(summary.router)




