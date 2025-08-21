from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from .middleware import RequestIDMiddleware, request_logger_middleware


def create_app() -> FastAPI:
    app = FastAPI(title="cascadillo", version="0.0.1")

    # Middlewares: request id + structured request logs
    app.add_middleware(RequestIDMiddleware)
    app.middleware("http")(request_logger_middleware)

    @app.get("/healthz", summary="Liveness", tags=["health"])  # k8s style
    async def healthz() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    @app.get("/livez", summary="Liveness (alias)", tags=["health"])  # alias
    async def livez() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    @app.get("/readyz", summary="Readiness", tags=["health"])  # future: check deps
    async def readyz() -> JSONResponse:
        # In milestone 0, we always report ready. Wire DB/Redis checks later.
        return JSONResponse({"status": "ready"})

    @app.get("/", summary="Root")
    async def root(request: Request) -> Response:
        return JSONResponse(
            {
                "app": "cascadillo",
                "version": app.version,
                "message": "Milestone 0 running",
                "request_id": request.headers.get("x-request-id"),
            },
        )

    return app
