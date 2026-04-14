from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

def get_db():
    conn = sqlite3.connect("students.db")
    return conn

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

    conn.commit()
    conn.close()

init_db()


class Student(BaseModel):
    name: str
    age: int = Field(gt=0, lt=100)
    marks: float = Field(ge=0, lt=100)

def row_to_dict(row):
    return{
        "id" : row[0],
        "name" : row[1],
        "age" : row[2],
        "marks" : row[3]
    }

@app.get("/")
def home():
    return {"message": "Student API is running"}

@app.post("/students")
def add_student(student: Student):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students(name, age, marks) VALUES (?, ?, ?)",
        (student.name, student.age, student.marks)
    )
    conn.commit()
    conn.close()
    return {"message": "Student added successfully"}

@app.get("/students")
def get_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(row) for row in rows]

@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE id = ?",(student_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return row_to_dict(row)

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """ UPDATE students 
            SET name = ?, age = ?, marks = ? where id = ?
        """,(student.name, student.age, student.marks, student.id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    conn.close()
    
    return{"message": "Student updated successfully"}

@app.get("/search")
def search_student(name: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",(f"%{name}%",)
    )
    rows = cursor.fetchall()
    conn.close()

    return [row_to_dict(r) for r in rows]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE id = ?",(student_id,)
    )
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    
    conn.close()
    return{"message": "Student deleted successfully"}