**from fastapi import FastAPI, HTTPException  *# Import FastAPI (to create API) and HTTPException (to handle errors)***

**from pydantic import BaseModel, Field       *# Import BaseModel (for data structure) and Field (for validation rules)***

**import sqlite3                              *# Import SQLite (database)***



**app = FastAPI()  # Create FastAPI app (this becomes our server)**



\# ---------------- DATABASE ----------------



**def get\_db():  *# Function to create a new database connection every time***

&#x20;   **conn = sqlite3.connect("students.db")  *# Connect to database file (creates if not exists)***

&#x20;   **return conn  *# Return connection so we can use it***



\# ---------------- CREATE TABLE ----------------



**def init\_db():  *# Function to initialize database (run once at start)***

&#x20;   **conn = get\_db()  *# Get database connection***

&#x20;   **cursor = conn.cursor()  *# Create cursor (used to run SQL queries)***



&#x20;   cursor.execute("""  

&#x20;   CREATE TABLE IF NOT EXISTS students (  # Create table only if it doesn't exist

&#x20;       id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique ID (auto increases)

&#x20;       name TEXT,  # Name column (text)

&#x20;       age INTEGER,  # Age column (integer)

&#x20;       marks REAL  # Marks column (decimal values allowed)

&#x20;   )

&#x20;   """)



&#x20;   **conn.commit()  *# Save changes to database***

&#x20;   **conn.close()  *# Close connection (good pract*ice)**



**init\_db()  *# Call function to ensure table is created before API starts***



\# ---------------- DATA MODEL ----------------



**class Student(BaseModel):  *# Define structure of incoming data using Pydantic***

&#x20;   **name: str  *# Name must be string***

&#x20;   **age: int = Field(gt=0, lt=100)  *# Age must be >0 and <100***

&#x20;   **marks: float = Field(ge=0, le=100)  *# Marks must be between 0 and 100***



\# ---------------- HELPER FUNCTION ----------------



def row\_to\_dict(row):  # Function to convert database row (tuple) to dictionary

&#x20;   return {

&#x20;       "id": row\[0],  # First column = id

&#x20;       "name": row\[1],  # Second column = name

&#x20;       "age": row\[2],  # Third column = age

&#x20;       "marks": row\[3]  # Fourth column = marks

&#x20;   }



\# ---------------- ROUTES ----------------



**@app.get("/")  *# Define GET API for home route "/"***

**def home():  *# Function that runs when "/" is accessed***

&#x20;   **return {"message": "Student API running"}  *# Return simple JSON response***



\# ---------------- ADD STUDENT ----------------



**@app.post("/students")  *# Define POST API to add new student***

**def add\_student(student: Student):  *# Receive data as Student object (validated automatically)***

&#x20;   conn = get\_db()  # Open database connection

&#x20;   cursor = conn.cursor()  # Create cursor



&#x20;   cursor.execute(

&#x20;       "INSERT INTO students (name, age, marks) VALUES (?, ?, ?)",  # SQL query to insert data

&#x20;       (student.name, student.age, student.marks)  # Values passed safely using placeholders

&#x20;   )



&#x20;   conn.commit()  # Save changes

&#x20;   conn.close()  # Close connection



&#x20;   return {  # Return response

&#x20;       "message": "Student added",

&#x20;       "student": student  # Return added student data

&#x20;   }



\# ---------------- GET ALL STUDENTS ----------------



**@app.get("/students")  *# Define GET API to fetch all students***

**def get\_students():  *# Function to get all students***

&#x20;   conn = get\_db()  # Open DB connection

&#x20;   cursor = conn.cursor()  # Create cursor



&#x20;   cursor.execute("SELECT \* FROM students")  # SQL query to get all records

&#x20;   rows = cursor.fetchall()  # Fetch all rows from database



&#x20;   conn.close()  # Close connection



&#x20;   return \[row\_to\_dict(r) for r in rows]  # Convert each row to dict and return list



\# ---------------- GET SINGLE STUDENT ----------------



**@app.get("/students/{student\_id}")  *# Dynamic route (student\_id comes from URL)***

**def get\_student(student\_id: int):  *# Function receives student\_id from URL***

&#x20;   conn = get\_db()  # Open DB connection

&#x20;   cursor = conn.cursor()  # Create cursor



&#x20;   cursor.execute("SELECT \* FROM students WHERE id = ?", (student\_id,))  # SQL query to get specific student

&#x20;   row = cursor.fetchone()  # Fetch one result



&#x20;   conn.close()  # Close connection



&#x20;   if not row:  # If no data found

&#x20;       raise HTTPException(status\_code=404, detail="Student not found")  # Raise error



&#x20;   return row\_to\_dict(row)  # Return student data as dictionary



\# ---------------- UPDATE STUDENT ----------------



**@app.put("/students/{student\_id}")  *# Define PUT API to update student***

**def update\_student(student\_id: int, student: Student):  *# Receive ID from URL and data from body***

&#x20;   conn = get\_db()  # Open DB connection

&#x20;   cursor = conn.cursor()  # Create cursor



&#x20;   cursor.execute("""

&#x20;       UPDATE students

&#x20;       SET name = ?, age = ?, marks = ?  # Update columns

&#x20;       WHERE id = ?  # Condition to match student

&#x20;   """, (student.name, student.age, student.marks, student\_id))



&#x20;   conn.commit()  # Save changes



&#x20;   if cursor.rowcount == 0:  # If no row updated

&#x20;       conn.close()

&#x20;       **raise HTTPException(status\_code=404, detail="Student not found")  *# Raise error***



&#x20;   conn.close()  # Close connection



&#x20;   return {

&#x20;       "message": "Student updated",

&#x20;       "student": student

&#x20;   }



\# ---------------- DELETE STUDENT ----------------



@app.delete("/students/{student\_id}")  # Define DELETE API

def delete\_student(student\_id: int):  # Receive ID from URL

&#x20;   conn = get\_db()  # Open DB connection

&#x20;   cursor = conn.cursor()  # Create cursor



&#x20;   cursor.execute("DELETE FROM students WHERE id = ?", (student\_id,))  # SQL query to delete student

&#x20;   conn.commit()  # Save changes



&#x20;   if cursor.rowcount == 0:  # If no row deleted

&#x20;       conn.close()

&#x20;       **raise HTTPException(status\_code=404, detail="Student not found")  *# Raise error***



&#x20;   conn.close()  # Close connection



&#x20;   return {"message": "Student deleted"}  # Return success message



\# ---------------- SEARCH STUDENT ----------------



**@app.get("/search")  *# Define GET API for search***

**def search\_student(name: str):  *# Receive name from query parameter (?name=...)***

&#x20;   conn = get\_db()  # Open DB connection

&#x20;   cursor = conn.cursor()  # Create cursor



&#x20;   cursor.execute(

&#x20;       "SELECT \* FROM students WHERE name LIKE ?",  # SQL query for search

&#x20;       (f"%{name}%",)  # % allows partial matching

&#x20;   )



&#x20;   rows = cursor.fetchall()  # Fetch all matching rows

&#x20;   conn.close()  # Close connection



&#x20;   return \[row\_to\_dict(r) for r in rows]  # Return list of matching students

