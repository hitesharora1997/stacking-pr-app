from unittest.mock import MagicMock, patch

import pytest

from app.dependencies import get_db


def test_get_db_success():
    """Test successful database session creation and cleanup"""
    with patch("app.dependencies.SessionLocal") as mock_session_local:
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db

        # Get the generator
        db_gen = get_db()

        # Get the session
        db_session = next(db_gen)
        assert db_session == mock_db

        # Cleanup should close the session
        try:
            next(db_gen)
        except StopIteration:
            pass

        mock_db.close.assert_called_once()


def test_get_db_exception_handling():
    """Test database session cleanup when exception occurs"""
    with patch("app.dependencies.SessionLocal") as mock_session_local:
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db

        db_gen = get_db()
        db_session = next(db_gen)

        # Simulate exception during database operations
        try:
            db_gen.throw(Exception("Database error"))
        except Exception:
            pass

        # Session should still be closed
        mock_db.close.assert_called_once()
