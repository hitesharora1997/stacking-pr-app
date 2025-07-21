from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.task import Task as TaskModel
from app.schemas.task import Task

router = APIRouter()


@router.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all tasks from the database.

    Returns:
        List[Task]: A list of all tasks
    """
    try:
        tasks = db.query(TaskModel).all()
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}",
        )


@router.post("/tasks", response_model=Task)
def create_task(task: Task, db: Session = Depends(get_db)):
    """
    Create a new task in the database.

    Args:
        task (Task): Task data to create
        db (Session): Database session

    Returns:
        Task: The created task

    Raises:
        HTTPException: 409 if task with same ID exists, 500 for other errors
    """
    try:
        # Check if task with same ID already exists
        existing_task = db.query(TaskModel).filter(TaskModel.id == task.id).first()
        if existing_task:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Task with ID {task.id} already exists",
            )

        db_task = TaskModel(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task with this ID already exists or constraint violation",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}",
        )


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID.

    Args:
        task_id (int): ID of the task to retrieve
        db (Session): Database session

    Returns:
        Task: The requested task

    Raises:
        HTTPException: 404 if task not found, 500 for other errors
    """
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found",
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}",
        )
