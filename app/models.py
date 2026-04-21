from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str
    age: int = Field(gt=0, lt=100)
    marks: float = Field(ge=0, lt=100)

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    marks: float

class User(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str