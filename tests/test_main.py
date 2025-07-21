import pytest
from fastapi.testclient import TestClient

from app.main import app


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
