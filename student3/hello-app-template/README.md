# Hello App

A small, production-ready **Hello World** web application written in Python using [FastAPI](https://fastapi.tiangolo.com/). It is packaged for Docker deployment and includes a complete layered test suite: unit, integration, and end-to-end tests.

## Features

- **FastAPI** HTTP API with automatic OpenAPI documentation
- `/` — returns a friendly `Hello, World!` JSON message
- `/health` — liveness/readiness health check
- **Docker** multi-stage build with a non-root runtime user
- **Docker Compose** support for local development
- **Layered testing**:
  - Unit tests for isolated business logic
  - Integration tests using FastAPI's `TestClient`
  - End-to-end tests against a live Uvicorn server
- **GitLab CI/CD** pipeline with lint, test, build, and deploy stages

## Project Structure

```text
.
├── .gitlab-ci.yml          # GitLab CI/CD pipeline
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Local Docker Compose setup
├── docs/
│   └── DEPLOYMENT.md       # Detailed deployment guide
├── pyproject.toml          # Project metadata, dependencies, tool config
├── README.md               # This file
├── scripts/
│   └── run_e2e.sh          # Helper to run end-to-end tests locally
├── src/hello_app/          # Application source code
│   ├── __init__.py
│   ├── config.py           # Environment-based configuration
│   ├── health.py           # Health status helpers
│   └── main.py             # FastAPI application factory
└── tests/                  # Test suites
    ├── conftest.py         # Shared pytest fixtures
    ├── e2e/                # End-to-end tests
    ├── integration/        # Integration tests
    └── unit/               # Unit tests
```

## Quick Start

### Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn hello_app.main:app --reload --port 8000
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to explore the interactive API documentation.

### Docker

```bash
docker build -t hello-app:latest .
docker run -d -p 8000:8000 hello-app:latest
```

Or with Docker Compose:

```bash
docker compose up -d --build
```

## Running Tests

All test commands should be run from the repository root with the development dependencies installed.

### Run everything

```bash
pytest
```

### Run individual suites

```bash
pytest tests/unit        # Unit tests
pytest tests/integration # Integration tests
pytest tests/e2e         # End-to-end tests
```

You can also run the E2E suite using the helper script:

```bash
./scripts/run_e2e.sh
```

### Linting and type checking

```bash
ruff check src tests
ruff format --check src tests
mypy src
```

## Configuration

The application reads the following environment variables:

| Variable      | Default       | Description                          |
|---------------|---------------|--------------------------------------|
| `APP_NAME`    | `hello-app`   | Application name used in FastAPI     |
| `APP_VERSION` | `0.1.0`       | Application version                  |
| `ENVIRONMENT` | `local`       | Runtime environment label            |
| `PORT`        | `8000`        | HTTP server port                     |

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions on building, running, and deploying the Docker image, as well as the GitLab CI/CD pipeline overview.

## License

MIT
