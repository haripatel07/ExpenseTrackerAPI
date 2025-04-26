# Expense Tracker API

A simple **Backend API** for tracking your **expenses**, **incomes**, and **categories** with **user authentication**. Built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

---

## 💡 Features

- User Registration and Authentication (JWT based)
- CRUD operations for:
  - Categories
  - Expenses
  - Incomes
- Summarized dashboard for tracking financial status
- Secure password hashing
- Clean project structure with routers, models, schemas
- Fully documented API (Swagger UI: `/docs`)

---

## 📚 Project Structure

```
app/
├── routes/
│   ├── auth_router.py
│   ├── category.py
│   ├── expenses.py
│   ├── income.py
│   ├── summary.py
│   └── users.py
├── auth.py
├── crud.py
├── database.py
├── main.py
├── models.py
└── schema.py

.venv/            # Virtual environment
.env               # Environment variables
.gitignore         # Files to ignore in git
expenses.db        # SQLite Database file
LICENSE            # Project license
README.md          # Project documentation
requirements.txt   # Project dependencies
```

---

## 💡 Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT Tokens (OAuth2PasswordBearer)
- **Password Hashing:** Passlib

---

## ✨ Installation

```bash
# Clone the repository
git clone https://github.com/haripatel07/ExpenseTrackerAPI.git
cd ExpenseTrackerAPI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running the Server

```bash
# Run the FastAPI server
uvicorn app.main:app --reload
```

- Visit **http://localhost:8000/docs** to view Swagger API documentation.
- Visit **http://localhost:8000/redoc** for ReDoc API documentation.

---

## 👤 API Endpoints

| Functionality | Endpoint | Method |
| :--- | :--- | :--- |
| User Registration | `/register` | POST |
| User Login | `/login` | POST |
| Create Category | `/categories/` | POST |
| Get All Categories | `/categories/` | GET |
| Create Expense | `/expenses/` | POST |
| Get Expenses | `/expenses/` | GET |
| Create Income | `/incomes/` | POST |
| Get Incomes | `/incomes/` | GET |
| Get Financial Summary | `/summary/` | GET |

---

## 📚 To Do

- ✅ Fix minor validation errors (date formats, etc.)
- ✅ Add pagination and filtering
- ✅ Add user-specific data protection
- ✅ Add test cases

---

## 📖 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌟 Author

- Hari Patel  
[GitHub Profile](https://github.com/haripatel07)

---


