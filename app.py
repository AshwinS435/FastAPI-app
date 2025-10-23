from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import mysql.connector

app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="fastapi_db"
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
)
""")

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

@app.post("/users/")
def create_user(user: User):
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (user.username, user.email, user.password))
        db.commit()
        return {"message": "User created"}

@app.get("/users/")
def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    cursor.execute("UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s",
                   (user.username, user.email, user.password, user_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
