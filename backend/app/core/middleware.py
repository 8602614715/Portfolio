"""Pure-ASGI middleware: body size limit, request logging, security headers."""

import logging
import time
import uuid

from fastapi import HTTPException
from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.errors import PayloadTooLargeError, error_response, internal_error_response

logger = logging.getLogger("app.request")


class BodySizeLimitMiddleware:
    """Reject bodies over ``max_bytes`` (checks Content-Length and streamed chunks)."""

    def __init__(self, app: ASGIApp, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        declared = Headers(scope=scope).get("content-length")
        if declared is not None and declared.isdigit() and int(declared) > self.max_bytes:
            exc = PayloadTooLargeError()
            await error_response(exc.status_code, exc.code, exc.message)(scope, receive, send)
            return

        received = 0

        async def limited_receive() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_bytes:
                    # FastAPI re-raises HTTPException from body parsing (anything else becomes a 400);
                    # the central handler maps 413 to PAYLOAD_TOO_LARGE.
                    raise HTTPException(status_code=413)
            return message

        await self.app(scope, limited_receive, send)


class RequestLoggingMiddleware:
    """Logs method, path, status and duration. Never logs query strings, headers or bodies.

    Also converts unexpected exceptions into a safe 500 response here, so the
    outer CORS/security-header middleware still decorates it.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.perf_counter()
        request_id = uuid.uuid4().hex[:12]
        status_code = 500
        response_started = False

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code, response_started
            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_started = True
                MutableHeaders(scope=message)["X-Request-ID"] = request_id
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception:
            # Traceback goes to the server log only, never to the client.
            logger.exception("unhandled exception", extra={"request_id": request_id})
            if response_started:
                raise
            status_code = 500
            await internal_error_response()(scope, receive, send_wrapper)
        finally:
            logger.info(
                "request",
                extra={
                    "request_id": request_id,
                    "method": scope["method"],
                    "path": scope["path"],
                    "status_code": status_code,
                    "duration_ms": round((time.perf_counter() - start) * 1000, 2),
                },
            )


class SecurityHeadersMiddleware:
    """Adds defensive response headers. A strict CSP is skipped for the Swagger/ReDoc pages."""

    DOCS_PATHS = ("/docs", "/redoc")

    def __init__(self, app: ASGIApp, hsts: bool) -> None:
        self.app = app
        self.hsts = hsts

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        is_docs = scope["path"].startswith(self.DOCS_PATHS)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["X-Content-Type-Options"] = "nosniff"
                headers["X-Frame-Options"] = "DENY"
                headers["Referrer-Policy"] = "no-referrer"
                headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
                if not is_docs:
                    headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
                if self.hsts:
                    headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            await send(message)

        await self.app(scope, receive, send_wrapper)
