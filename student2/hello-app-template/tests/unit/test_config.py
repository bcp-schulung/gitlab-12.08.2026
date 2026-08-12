"""Unit tests for the configuration module."""

import pytest

from hello_app.config import get_app_name, get_app_version, get_environment, get_port


class TestGetAppName:
    """Tests for get_app_name."""

    def test_default_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the default app name when the env var is unset."""
        monkeypatch.delenv("APP_NAME", raising=False)

        assert get_app_name() == "hello-app"

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the value from the APP_NAME environment variable."""
        monkeypatch.setenv("APP_NAME", "custom-app")

        assert get_app_name() == "custom-app"


class TestGetPort:
    """Tests for get_port."""

    def test_default_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the default port when the env var is unset."""
        monkeypatch.delenv("PORT", raising=False)

        assert get_port() == 8000

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the integer value from the PORT environment variable."""
        monkeypatch.setenv("PORT", "8080")

        assert get_port() == 8080


class TestGetEnvironment:
    """Tests for get_environment."""

    def test_default_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the default environment when the env var is unset."""
        monkeypatch.delenv("ENVIRONMENT", raising=False)

        assert get_environment() == "local"

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the value from the ENVIRONMENT environment variable."""
        monkeypatch.setenv("ENVIRONMENT", "staging")

        assert get_environment() == "staging"


class TestGetAppVersion:
    """Tests for get_app_version."""

    def test_default_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the default version when the env var is unset."""
        monkeypatch.delenv("APP_VERSION", raising=False)

        assert get_app_version() == "0.1.0"

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns the value from the APP_VERSION environment variable."""
        monkeypatch.setenv("APP_VERSION", "1.2.3")

        assert get_app_version() == "1.2.3"
