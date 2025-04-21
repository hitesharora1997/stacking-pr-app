from fastapi import APIRouter
from app.schemas.task import Task

router = APIRouter()

# In-memory task list
tasks = []

@router.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks

@router.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task
