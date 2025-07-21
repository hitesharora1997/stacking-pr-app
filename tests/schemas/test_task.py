import pytest
from pydantic import ValidationError

from app.schemas.task import Task


def test_task_schema_valid_data():
    """Test Task schema with valid data"""
    task_data = {"id": 1, "title": "Test Task", "is_completed": False}

    task = Task(**task_data)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.is_completed is False


def test_task_schema_required_fields():
    """Test Task schema with all required fields"""
    task_data = {"id": 1, "title": "Test Task", "is_completed": False}
    task = Task(**task_data)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.is_completed is False


def test_task_schema_missing_required_fields():
    """Test Task schema validation with missing required fields"""
    # Missing 'id' field
    with pytest.raises(ValidationError) as exc_info:
        Task(title="Test Task", is_completed=False)

    assert "id" in str(exc_info.value)

    # Missing 'title' field
    with pytest.raises(ValidationError) as exc_info:
        Task(id=1, is_completed=False)

    assert "title" in str(exc_info.value)


def test_task_schema_type_validation():
    """Test Task schema type validation"""
    # Invalid id type (string instead of int)
    with pytest.raises(ValidationError) as exc_info:
        Task(id="invalid", title="Test Task", is_completed=False)

    assert "id" in str(exc_info.value)

    # Invalid title type (int instead of string)
    with pytest.raises(ValidationError) as exc_info:
        Task(id=1, title=123, is_completed=False)

    assert "title" in str(exc_info.value)

    # Invalid is_completed type (string instead of bool)
    with pytest.raises(ValidationError) as exc_info:
        Task(id=1, title="Test Task", is_completed="invalid")

    assert "is_completed" in str(exc_info.value)


def test_task_schema_json_serialization():
    """Test Task schema JSON serialization"""
    task = Task(id=1, title="Test Task", is_completed=True)
    task_dict = task.dict()

    expected = {"id": 1, "title": "Test Task", "is_completed": True}

    assert task_dict == expected


def test_task_schema_json_deserialization():
    """Test Task schema JSON deserialization"""
    json_data = '{"id": 1, "title": "Test Task", "is_completed": true}'
    task = Task.parse_raw(json_data)

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.is_completed is True
