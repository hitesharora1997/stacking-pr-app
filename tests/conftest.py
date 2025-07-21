import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dependencies import get_db
from app.main import app
from app.models.task import Base

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create test client with overridden database dependency"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def db_session(test_db):
    """Create database session for direct database operations in tests"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def clear_database():
    """Clear database between tests to ensure isolation"""
    from sqlalchemy import text

    # Clear all tables before each test
    connection = engine.connect()
    transaction = connection.begin()
    try:
        # Delete all records from tasks table
        connection.execute(text("DELETE FROM tasks"))
        transaction.commit()
    except Exception:
        transaction.rollback()
    finally:
        connection.close()


@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {"id": 1, "title": "Test Task", "is_completed": False}
