# 🎓 Student Management API (FastAPI)

A backend API built using **FastAPI** that allows managing student records with secure authentication using **JWT** and **password hashing (bcrypt)**.

---

## 🚀 Features

* 🔐 User Authentication (Signup & Login)
* 🔑 JWT-based Authorization
* 🛡 Password Hashing using bcrypt
* 👨‍🎓 Student CRUD Operations
* 🏆 Topper & Fail Student APIs
* 📊 Average Marks Calculation
* 🔍 Search Students with filters
* 🔒 Role-based access (Admin/User)

---

## 🧠 Tech Stack

* Python
* FastAPI
* SQLite
* JWT (python-jose)
* Passlib (bcrypt)

---

## 📂 Project Structure

```
StudentAPI/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── utils.py
│   └── routes/
│       └── student.py
│
│── venv/
│── students.db
│── README.md
```

---

## ⚙️ Setup & Run

### 1️⃣ Clone the repo

```
git clone <your-repo-link>
cd StudentAPI
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install fastapi uvicorn python-jose passlib[bcrypt] bcrypt==4.0.1
```

---

### 4️⃣ Run Server

```
uvicorn app.main:app --reload
```

---

### 5️⃣ Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

1. Signup → Create user
2. Login → Get JWT token
3. Use token in headers:

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

### 👤 Auth

* `POST /signup` → Create user
* `POST /login` → Get JWT token

---

### 🎓 Students

* `POST /students` → Add student
* `GET /students` → Get all students
* `GET /students/{id}` → Get student by ID
* `PUT /students/{id}` → Update student
* `DELETE /students/{id}` → Delete student (Admin only)
* `DELETE /students?confirm=true` → Delete all (Admin only)

---

### 📊 Extra Features

* `GET /students/topper` → Top 3 students
* `GET /students/fail` → Failed students
* `GET /students/average` → Average marks
* `GET /students/search` → Filter students

---

## 🔒 Security

* Passwords are hashed using **bcrypt**
* JWT tokens used for authentication
* Role-based access control implemented

---

## 📈 Future Improvements

* Password reset system
* Email verification
* Deployment (Render / Railway)
* Frontend integration

---

## 👨‍💻 Author

Krishna Patil

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
