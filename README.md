# cascadillo

Milestone 0 — Bootstrap & scaffolding

What’s included:
 - FastAPI app with health endpoints: `/healthz`, `/livez`, `/readyz`, and root `/`.
 - Request ID header passthrough/generation and simple request logging.
 - Test for health endpoints.
 - Dockerfile and docker-compose with Redis and Postgres (for later milestones).

Prereqs
 - Python 3.12 or newer (3.12.x recommended)
 - uv (fast Python package manager by Astral)
 - Docker (optional) if you want to use compose services

Install uv (Windows PowerShell)
You can install/upgrade uv with:

```powershell
 iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex
```

Create a virtual environment with uv, install deps, then run the app (no activation needed)

```powershell
# Create venv in .venv (Python 3.12)
uv venv --python 3.12

# Install deps from pyproject.toml (latest compatible versions)
uv pip install -e .[dev]

# Run tests (optional)
uv run -m pytest -q

# Run the API locally
uv run uvicorn cascadillo.main:app --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/healthz to verify it’s green.

Note (Windows): 0.0.0.0 is the bind address, not a URL you can open in a browser. Use one of these in your browser or API client:
- http://localhost:8000
- http://127.0.0.1:8000

Quick health check from PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/healthz
```

Run with Docker (optional)

```powershell
 docker compose up --build
```

This starts:
 - app on http://localhost:8000
 - redis on port 6379
 - postgres on port 5432

Project layout

```
 src/cascadillo/
	app.py           # FastAPI app factory + health endpoints
	main.py          # ASGI entrypoint (uvicorn target)
	middleware.py    # Request ID + request logger
tests/
	test_health.py   # Health endpoints test
```

Next milestones
 - Wire readiness checks to Redis/Postgres.
 - Add structured logging (JSON) and a request ID context.
 - Add OpenAI-compatible endpoint skeleton.
# cascadillo