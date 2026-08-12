"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from hello_app.main import create_app


@pytest.fixture
def app():
    """Provide a fresh FastAPI application instance."""
    return create_app()


@pytest.fixture
def client(app):
    """Provide a synchronous TestClient for integration tests."""
    return TestClient(app)
