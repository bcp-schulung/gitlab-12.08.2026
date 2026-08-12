# Deployment Guide

This document explains how to build, run, and deploy the `hello-app` web application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker](#docker)
  - [Build the image](#build-the-image)
  - [Run the container](#run-the-container)
  - [Docker Compose](#docker-compose)
- [GitLab CI/CD](#gitlab-cicd)
- [Production Checklist](#production-checklist)

## Prerequisites

- Python 3.11 or newer
- `pip` and `venv` (or your preferred Python environment manager)
- Docker Engine 24.0+ and Docker Compose v2 (for containerized deployment)
- A GitLab runner with Docker-in-Docker support (for CI/CD builds)

## Local Development

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the package in editable mode with development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Run the application directly with Uvicorn:

   ```bash
   uvicorn hello_app.main:app --reload --port 8000
   ```

   The `--reload` flag is convenient for local development; do **not** use it in production.

4. Open your browser or use `curl` to verify the endpoints:

   ```bash
   curl http://localhost:8000/
   curl http://localhost:8000/health
   curl http://localhost:8000/docs
   ```

## Docker

### Build the image

From the project root:

```bash
docker build -t hello-app:latest .
```

The `Dockerfile` uses a multi-stage build to keep the runtime image small and avoids shipping build tools in the final image.

### Run the container

```bash
docker run -d \
  --name hello-app \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  hello-app:latest
```

Verify it is running:

```bash
curl http://localhost:8000/health
```

Stop and remove the container:

```bash
docker stop hello-app
docker rm hello-app
```

### Docker Compose

For local orchestration, use Docker Compose:

```bash
docker compose up -d --build
```

This builds the image if needed, starts the container, and exposes the service on `http://localhost:8000`. To tear it down:

```bash
docker compose down
```

## GitLab CI/CD

The included [`.gitlab-ci.yml`](../.gitlab-ci.yml) pipeline runs on every push and merge request:

1. **lint** — checks formatting, import order, and type safety with `ruff` and `mypy`.
2. **unit-tests** — runs the unit test suite.
3. **integration-tests** — runs the integration test suite.
4. **e2e-tests** — runs end-to-end tests against a live Uvicorn process.
5. **docker-build** — builds the Docker image and pushes it to the GitLab Container Registry.
6. **deploy** — placeholder manual job for production deployment.

To use the registry push step, ensure your GitLab project has a Container Registry and the runner has the `CI_REGISTRY_PASSWORD` variable available.

## Production Checklist

Before deploying to a real production environment:

- [ ] Set `ENVIRONMENT=production` and configure `APP_NAME` / `APP_VERSION` as needed.
- [ ] Remove `--reload` from the Uvicorn command and run with multiple workers if required:
  `uvicorn hello_app.main:app --host 0.0.0.0 --port 8000 --workers 4`
- [ ] Place the application behind a reverse proxy or load balancer (e.g., nginx, Traefik, or a cloud load balancer).
- [ ] Configure centralized logging and health-check monitoring for `/health`.
- [ ] Replace the placeholder `deploy` job in `.gitlab-ci.yml` with your actual deployment target (Kubernetes, VM, PaaS, etc.).
