import pytest

from app.models.task import Task as TaskModel


def test_task_model_creation(db_session):
    """Test creating a Task model instance"""
    task = TaskModel(id=1, title="Test Task", is_completed=False)

    db_session.add(task)
    db_session.commit()

    # Verify task was created
    saved_task = db_session.query(TaskModel).filter_by(id=1).first()
    assert saved_task is not None
    assert saved_task.title == "Test Task"
    assert saved_task.is_completed is False


def test_task_model_default_values(db_session):
    """Test Task model default values"""
    task = TaskModel(id=2, title="Another Task")

    db_session.add(task)
    db_session.commit()

    saved_task = db_session.query(TaskModel).filter_by(id=2).first()
    assert saved_task.is_completed is False  # Default value


def test_task_model_query_all(db_session):
    """Test querying all tasks"""
    # Create multiple tasks
    tasks_data = [
        TaskModel(id=1, title="Task 1", is_completed=False),
        TaskModel(id=2, title="Task 2", is_completed=True),
        TaskModel(id=3, title="Task 3", is_completed=False),
    ]

    for task in tasks_data:
        db_session.add(task)
    db_session.commit()

    # Query all tasks
    all_tasks = db_session.query(TaskModel).all()
    assert len(all_tasks) == 3


def test_task_model_query_by_completion_status(db_session):
    """Test querying tasks by completion status"""
    # Create tasks with different completion statuses
    task1 = TaskModel(id=1, title="Completed Task", is_completed=True)
    task2 = TaskModel(id=2, title="Incomplete Task", is_completed=False)

    db_session.add(task1)
    db_session.add(task2)
    db_session.commit()

    # Query completed tasks
    completed_tasks = db_session.query(TaskModel).filter_by(is_completed=True).all()
    assert len(completed_tasks) == 1
    assert completed_tasks[0].title == "Completed Task"

    # Query incomplete tasks
    incomplete_tasks = db_session.query(TaskModel).filter_by(is_completed=False).all()
    assert len(incomplete_tasks) == 1
    assert incomplete_tasks[0].title == "Incomplete Task"
