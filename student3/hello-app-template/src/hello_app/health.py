"""Health check helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthStatus:
    """Immutable health status object."""

    status: str
    healthy: bool


def build_health_status() -> HealthStatus:
    """Build and return the current application health status."""
    return HealthStatus(status="ok", healthy=True)
