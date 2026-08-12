"""Unit tests for the health module."""

import pytest

from hello_app.health import HealthStatus, build_health_status


class TestBuildHealthStatus:
    """Tests for build_health_status."""

    def test_returns_healthy_status(self) -> None:
        """The health status should report the app as healthy."""
        result = build_health_status()

        assert isinstance(result, HealthStatus)
        assert result.status == "ok"
        assert result.healthy is True

    def test_status_is_immutable(self) -> None:
        """The dataclass should be frozen and not allow mutation."""
        result = build_health_status()

        with pytest.raises(expected_exception=AttributeError):
            result.healthy = False  # type: ignore[misc]
