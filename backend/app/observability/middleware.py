import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))

        response = await call_next(request)

        elapsed = time.perf_counter() - start
        path = request.url.path
        status_code = str(response.status_code)

        REQUEST_COUNT.labels(request.method, path, status_code).inc()
        REQUEST_LATENCY.labels(request.method, path).observe(elapsed)

        response.headers["x-request-id"] = request_id

        logging.getLogger("smart-resume-builder").info(
            "request_complete",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": path,
                "status_code": response.status_code,
                "duration_ms": round(elapsed * 1000, 2),
            },
        )
        return response
