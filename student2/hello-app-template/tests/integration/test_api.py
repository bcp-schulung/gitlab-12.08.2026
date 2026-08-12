"""Integration tests for the HTTP API."""

import pytest
from fastapi.testclient import TestClient


class TestHelloEndpoint:
    """Tests for GET /."""

    def test_returns_hello_message(self, client: TestClient) -> None:
        """The root endpoint returns a hello message and environment info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Beep boop, I'm alive!"
        assert "environment" in data

    def test_is_json(self, client: TestClient) -> None:
        """The response content type is application/json."""
        response = client.get("/")

        assert response.headers["content-type"] == "application/json"


class TestHealthEndpoint:
    """Tests for GET /health."""

    def test_returns_healthy_status(self, client: TestClient) -> None:
        """The health endpoint reports the application as healthy."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["healthy"] is True

    @pytest.mark.parametrize("method", ["POST", "PUT", "DELETE"])
    def test_rejects_non_get_methods(self, client: TestClient, method: str) -> None:
        """The health endpoint only accepts GET requests."""
        response = client.request(method, "/health")

        assert response.status_code == 405
