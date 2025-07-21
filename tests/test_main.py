from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app, main


@pytest.fixture
def client():
    """Create test client"""
    with TestClient(app) as test_client:
        yield test_client


def test_read_root(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI", "status": "healthy"}


def test_app_startup():
    """Test app can be imported and initialized"""
    assert app.title == "Stacking PR Task API"
    assert hasattr(app, "router")


def test_health_check(client: TestClient):
    """Test that the app is healthy"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert isinstance(data["message"], str)


def test_invalid_endpoint(client: TestClient):
    """Test accessing non-existent endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_api_docs(client: TestClient):
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client: TestClient):
    """Test OpenAPI schema is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema


def test_health_endpoint(client: TestClient):
    """Test dedicated health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "stacking-pr-api"
    assert data["version"] == "0.1.0"


@patch("app.main.uvicorn")
def test_main_function(mock_uvicorn):
    """Test main function calls uvicorn.run with correct parameters"""
    main()
    mock_uvicorn.run.assert_called_once_with(
        "app.main:app", host="0.0.0.0", port=8000, reload=True
    )
