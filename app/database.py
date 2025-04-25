from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Database URL
DATABASE_URL = "sqlite:///./expenses.db"

#Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread": False}  # Allow multiple threads to use the same connection
)

#Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create a base class for the models
Base = declarative_base()

#Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
