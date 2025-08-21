# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UVICORN_WORKERS=1 \
    PORT=8000

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

# Install runtime deps
RUN pip install --upgrade pip && \
        pip install \
            "fastapi>=0.112" \
            "uvicorn[standard]>=0.30" && \
        pip install -e .

EXPOSE 8000

CMD ["uvicorn", "cascadillo.main:app", "--host", "0.0.0.0", "--port", "8000"]
