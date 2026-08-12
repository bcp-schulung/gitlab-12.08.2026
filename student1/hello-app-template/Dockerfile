# syntax=docker/dockerfile:1

# Build stage
FROM python:3.12-alpine AS builder

WORKDIR /build

# Install build dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# Copy project files and install into a virtual environment
COPY pyproject.toml README.md ./
COPY src/ ./src
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir .

# Runtime stage
FROM python:3.12-alpine AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    APP_NAME=hello-app \
    APP_VERSION=0.1.0 \
    ENVIRONMENT=production

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source
COPY src/ ./src

# Remove pip from runtime image: it is not needed at runtime and its vendored
# dependencies trigger CVE scanners.
RUN rm -rf /usr/local/lib/python*/site-packages/pip* \
    /opt/venv/lib/python*/site-packages/pip* \
    /usr/local/bin/pip*

# Create a non-root user and switch to it
RUN adduser -D -s /bin/sh appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=5)" || exit 1

CMD ["uvicorn", "hello_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
