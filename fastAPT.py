from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional

# Create a FastAPI app
app = FastAPI()

# Define a user model for authentication
class User(BaseModel):
    username: str
    email: str

# Sample user data (in-memory database)
users_db = {
    "testuser": {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
}

# Define an OAuth2 password flow for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to verify user credentials
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user is None or user["password"] != password:
        return False
    return True

# Function to get the current user based on the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = token  # In this simplified example, the token is assumed to be the username
    user = users_db.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# Define a task model
class Task(BaseModel):
    title: str
    description: Optional[str] = None

# Sample task data (in-memory database)
tasks_db = []

# Create a task
@app.post("/tasks/", response_model=Task)
def create_task(task: Task, current_user: User = Depends(get_current_user)):
    tasks_db.append(task)
    return task

# Get all tasks
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks_db

# Update a task by ID
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, current_user: User = Depends(get_current_user)):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_id] = task
    return task

# Delete a task by ID
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = tasks_db.pop(task_id)
    return deleted_task
