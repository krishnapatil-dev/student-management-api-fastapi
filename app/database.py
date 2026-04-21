import sqlite3

def get_db():
    conn = sqlite3.connect("students.db")
    return conn