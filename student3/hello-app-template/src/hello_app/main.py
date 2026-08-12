"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from hello_app.config import get_app_name, get_app_version, get_environment
from hello_app.health import build_health_status


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        A configured FastAPI application instance.
    """
    app = FastAPI(
        title=get_app_name(),
        version=get_app_version(),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        """Return a friendly hello world message."""
        return {
            "message": "Student 3 App",
            "environment": get_environment(),
        }

    @app.get("/health")
    async def health_check() -> JSONResponse:
        """Return the application health status."""
        health = build_health_status()
        status_code = 200 if health.healthy else 503
        return JSONResponse(
            content={"status": health.status, "healthy": health.healthy},
            status_code=status_code,
        )

    return app


app = create_app()
