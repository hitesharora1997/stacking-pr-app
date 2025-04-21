from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.task import Task as TaskModel
from app.schemas.task import Task
from app.dependencies import get_db

router = APIRouter()

# In-memory task list
tasks = []

@router.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

@router.post("/tasks", response_model=Task)
def create_task(task: Task, db: Session = Depends(get_db)):
    db_task = TaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task