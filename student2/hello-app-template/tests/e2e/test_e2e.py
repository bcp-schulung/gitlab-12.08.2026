"""End-to-end tests against a live server process.

These tests launch a real Uvicorn server in a subprocess and exercise the
application over HTTP. They are slower and more brittle than integration tests,
but they verify the actual deployment artifact behaves correctly.
"""

import os
import socket
import subprocess
import sys
import time
from contextlib import closing
from pathlib import Path

import httpx
import pytest


@pytest.fixture(scope="module")
def server_url() -> str:
    """Start uvicorn on a free port, wait for readiness, yield base URL."""
    port = _find_free_port()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2] / "src")

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "hello_app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    url = f"http://127.0.0.1:{port}"
    try:
        _wait_for_server(url, timeout=30)
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


class TestLiveServer:
    """End-to-end tests for the running server."""

    def test_hello_endpoint(self, server_url: str) -> None:
        """The live root endpoint returns the expected hello payload."""
        response = _http_get(f"{server_url}/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Beep boop, I'm alive!"
        assert data["environment"] == "local"

    def test_health_endpoint(self, server_url: str) -> None:
        """The live health endpoint reports the application as healthy."""
        response = _http_get(f"{server_url}/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["healthy"] is True


def _find_free_port() -> int:
    """Return a free TCP port on localhost."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_server(url: str, timeout: float) -> None:
    """Poll the health endpoint until the server responds or timeout elapses."""
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            with httpx.Client(timeout=httpx.Timeout(2.0)) as client:
                response = client.get(f"{url}/health")
            if response.status_code == 200:
                return
        except httpx.HTTPError as exc:
            last_error = exc
        time.sleep(0.25)

    raise RuntimeError(
        f"Server at {url} did not become ready in {timeout}s"
    ) from last_error


def _http_get(url: str) -> httpx.Response:
    """Perform a GET request and return the response."""
    with httpx.Client(timeout=httpx.Timeout(5.0)) as client:
        return client.get(url, headers={"Accept": "application/json"})
