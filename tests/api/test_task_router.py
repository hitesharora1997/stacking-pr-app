import pytest
from fastapi.testclient import TestClient

from app.models.task import Task as TaskModel


def test_get_tasks_empty(client: TestClient):
    """Test getting tasks when database is empty"""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client: TestClient, sample_task_data):
    """Test creating a new task"""
    response = client.post("/api/v1/tasks", json=sample_task_data)
    assert response.status_code == 200

    created_task = response.json()
    assert created_task["id"] == sample_task_data["id"]
    assert created_task["title"] == sample_task_data["title"]
    assert created_task["is_completed"] == sample_task_data["is_completed"]


def test_get_tasks_with_data(client: TestClient, sample_task_data):
    """Test getting tasks after creating one"""
    # Create a task first
    client.post("/api/v1/tasks", json=sample_task_data)

    # Get all tasks
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == sample_task_data["title"]


def test_create_task_invalid_data(client: TestClient):
    """Test creating task with invalid data"""
    invalid_data = {
        "title": "Test Task"
        # Missing required 'id' field
    }

    response = client.post("/api/v1/tasks", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_create_multiple_tasks(client: TestClient):
    """Test creating multiple tasks"""
    tasks_data = [
        {"id": 1, "title": "Task 1", "is_completed": False},
        {"id": 2, "title": "Task 2", "is_completed": True},
        {"id": 3, "title": "Task 3", "is_completed": False},
    ]

    # Create multiple tasks
    for task_data in tasks_data:
        response = client.post("/api/v1/tasks", json=task_data)
        assert response.status_code == 200

    # Verify all tasks exist
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 3
