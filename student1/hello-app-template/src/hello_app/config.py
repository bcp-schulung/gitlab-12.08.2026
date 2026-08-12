"""Application configuration loaded from environment variables."""

import os


def get_app_name() -> str:
    """Return the application name."""
    return os.getenv("APP_NAME", "hello-app")


def get_app_version() -> str:
    """Return the application version."""
    return os.getenv("APP_VERSION", "0.1.0")


def get_environment() -> str:
    """Return the runtime environment (e.g. local, staging, production)."""
    return os.getenv("ENVIRONMENT", "local")


def get_port() -> int:
    """Return the port the HTTP server should bind to."""
    return int(os.getenv("PORT", "8000"))
