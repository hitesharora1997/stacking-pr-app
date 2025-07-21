import pytest
from fastapi.testclient import TestClient

from app.models.task import Task as TaskModel


def test_end_to_end_task_workflow(client: TestClient, db_session):
    """Test complete task workflow from API to database"""
    # Create task via API
    task_data = {"id": 1, "title": "Integration Test Task", "is_completed": False}

    response = client.post("/api/v1/tasks", json=task_data)
    assert response.status_code == 200

    # Verify task exists in database
    db_task = db_session.query(TaskModel).filter_by(id=1).first()
    assert db_task is not None
    assert db_task.title == "Integration Test Task"
    assert db_task.is_completed is False

    # Verify task appears in API response
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Integration Test Task"


def test_database_persistence_across_requests(client: TestClient):
    """Test that tasks persist across multiple API requests"""
    # Create multiple tasks
    tasks_data = [
        {"id": 1, "title": "Task 1", "is_completed": False},
        {"id": 2, "title": "Task 2", "is_completed": True},
    ]

    for task_data in tasks_data:
        response = client.post("/api/v1/tasks", json=task_data)
        assert response.status_code == 200

    # Make multiple GET requests to verify persistence
    for _ in range(3):
        response = client.get("/api/v1/tasks")
        assert response.status_code == 200

        tasks = response.json()
        assert len(tasks) == 2


def test_database_transaction_rollback_on_error(client: TestClient, db_session):
    """Test that database transactions are properly handled on errors"""
    # This would be more relevant with more complex business logic
    # For now, test that invalid requests don't affect database state

    # Create a valid task first
    valid_task = {"id": 1, "title": "Valid Task", "is_completed": False}
    response = client.post("/api/v1/tasks", json=valid_task)
    assert response.status_code == 200

    # Attempt to create invalid task
    invalid_task = {"title": "Invalid Task"}  # Missing 'id'
    response = client.post("/api/v1/tasks", json=invalid_task)
    assert response.status_code == 422

    # Verify original task still exists and no partial data was saved
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Valid Task"


def test_concurrent_task_creation(client: TestClient):
    """Test handling multiple concurrent task creations"""
    import concurrent.futures
    import threading

    def create_task(task_id):
        task_data = {
            "id": task_id,
            "title": f"Concurrent Task {task_id}",
            "is_completed": False,
        }
        return client.post("/api/v1/tasks", json=task_data)

    # Create tasks concurrently
    task_ids = range(1, 6)  # Create 5 tasks

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        responses = list(executor.map(create_task, task_ids))

    # Verify all tasks were created successfully
    for response in responses:
        assert response.status_code == 200

    # Verify all tasks exist
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 5
