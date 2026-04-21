from fastapi import FastAPI
from app.routes.student import router
from app.database import get_db

app = FastAPI()

app.include_router(router)

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            marks REAL    
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return {"message": "Student API is running"}

