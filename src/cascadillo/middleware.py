import time
import uuid

from collections.abc import Awaitable, Callable

from fastapi import Request, Response


class RequestIDMiddleware:
    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def add_request_id_send(event) -> None:
            if event["type"] == "http.response.start":
                headers = event.get("headers", [])
                # Keep incoming x-request-id or generate a new one
                req_id = None
                for (k, v) in scope.get("headers", []):
                    if k == b"x-request-id":
                        req_id = v
                        break
                if req_id is None:
                    req_id = str(uuid.uuid4()).encode()
                headers.append((b"x-request-id", req_id))
                event["headers"] = headers
            await send(event)

        await self.app(scope, receive, add_request_id_send)


def _header(headers, name: str) -> str | None:
    name_b = name.lower().encode()
    for k, v in headers:
        if k.lower() == name_b:
            try:
                return v.decode()
            except Exception:
                return None
    return None


async def request_logger_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    t0 = time.perf_counter()
    request.headers.get("x-request-id") or str(uuid.uuid4())
    response: Response | None = None
    try:
        return await call_next(request)
    finally:
        int((time.perf_counter() - t0) * 1000)
        getattr(response, "status_code", 0) if response is not None else 0
