from fastapi import APIRouter, HTTPException, Depends
from app.auth import create_access_token, get_current_user
from app.database import get_db
from app.models import Student,StudentResponse,User, UserLogin
from app.utils import row_to_dict
from passlib.context import CryptContext

router = APIRouter()

pwd_context= CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

@router.post("/students")
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

@router.post("/signup")
def signup(user: User):
    conn = get_db()
    cursor = conn.cursor()

    hashed = hash_password(user.password)

    try:
        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)", 
            (user.username, hashed, user.role)
        )
        conn.commit()
    except:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    conn.close()
    return {"message" : "User created"}

@router.post("/login")
def login(user: UserLogin):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password, role FROM users WHERE username = ? AND password = ?"
        , (user.username, user.password)
    )
    data = cursor.fetchone()
    conn.close()
    if not data or not verify_password(user.password, data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({
        "username" : user.username,
        "role" : data["role"]
    })

    return {"access_token": token,
            "token_type": "bearer"}

@router.get("/students", response_model= list[StudentResponse])
def get_students(limit: int= 5, offset: int= 0):
    if limit > 50:
        limit = 50
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No students found")
    
    return [row_to_dict(row) for row in rows]

@router.delete("/students")
def delete_all_students(confirm: bool = False, user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins allowed")
    
    if not confirm:
        raise HTTPException(status_code=400, detail="Set confirm=true to delete all students")
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students")
    conn.commit()
    conn.close()

    return {"message": "All students deleted"}

@router.get("/students/search", response_model= list[StudentResponse])
def search_student(name: str= "", min_marks: int= 0, max_marks: int= 100):
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT * FROM students WHERE name LIKE ?
        AND marks BETWEEN ? AND ?
    """
    cursor.execute(
        query, ('%' + name + '%', min_marks, max_marks)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail= "Student not found")

    return [row_to_dict(r) for r in rows]

@router.get("/students/topper", response_model=list[StudentResponse])
def topper_students():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students ORDER BY marks DESC LIMIT 3"
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [row_to_dict(r) for r in rows]
        

@router.get("/students/fail",response_model=list[StudentResponse])
def fail_students():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE marks < 40 ORDER BY marks DESC"
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return [row_to_dict(r) for r in rows]
    
@router.get("/students/average")
def average_students():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT AVG(marks) from students"
    )
    avg = cursor.fetchone()[0]
    conn.close()

    if avg is None:
        raise HTTPException(status_code=404, detail="Student not found")
            
    return {"average_marks" : round(avg,2)}

@router.get("/students/{student_id}",response_model=StudentResponse)
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

@router.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """ UPDATE students 
            SET name = ?, age = ?, marks = ? where id = ?
        """,(student.name, student.age, student.marks, student_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    conn.close()
    
    return{"message": "Student updated successfully"}

@router.delete("/students/{student_id}")
def delete_student(student_id: int, user= Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code= 403, detail="Only admins allowed")
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
