"""Centralised error handling.

Every error leaves the API in the same shape::

    {"success": false, "error": {"code": "...", "message": "..."}}

Handlers never echo SQL, stack traces, request bodies or file paths.
"""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("app.errors")


class AppError(Exception):
    """Base class for expected, client-safe errors."""

    status_code = 400
    code = "BAD_REQUEST"
    message = "Bad request"

    def __init__(self, message: str | None = None, headers: dict[str, str] | None = None):
        super().__init__(message or self.message)
        self.message = message or self.message
        self.headers = headers


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"
    message = "Resource not found"


class ProjectNotFoundError(NotFoundError):
    code = "PROJECT_NOT_FOUND"
    message = "Project not found"


class ProfileNotFoundError(NotFoundError):
    code = "PROFILE_NOT_FOUND"
    message = "Profile not found"


class PayloadTooLargeError(AppError):
    status_code = 413
    code = "PAYLOAD_TOO_LARGE"
    message = "Request body is too large"


class RateLimitExceededError(AppError):
    status_code = 429
    code = "RATE_LIMIT_EXCEEDED"
    message = "Too many requests. Please try again later."


def error_body(code: str, message: str, details: list[dict[str, str]] | None = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if details:
        error["details"] = details
    return {"success": False, "error": error}


def error_response(
    status_code: int,
    code: str,
    message: str,
    *,
    details: list[dict[str, str]] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content=error_body(code, message, details), headers=headers
    )


def internal_error_response() -> JSONResponse:
    return error_response(500, "INTERNAL_ERROR", "An unexpected error occurred")


_HTTP_CODES = {
    404: ("NOT_FOUND", "Resource not found"),
    413: (PayloadTooLargeError.code, PayloadTooLargeError.message),
    405: ("METHOD_NOT_ALLOWED", "Method not allowed"),
}


async def _app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return error_response(exc.status_code, exc.code, exc.message, headers=exc.headers)


async def _http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    code, message = _HTTP_CODES.get(exc.status_code, ("HTTP_ERROR", "Request failed"))
    return error_response(exc.status_code, code, message, headers=getattr(exc, "headers", None))


async def _validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    # Only field location + message are returned; the submitted value is never echoed.
    details = [
        {
            "field": ".".join(str(part) for part in err["loc"] if part not in ("body", "query", "path")),
            "message": str(err["msg"]).removeprefix("Value error, "),
        }
        for err in exc.errors()
    ]
    return error_response(422, "VALIDATION_ERROR", "Request validation failed", details=details)


async def _database_error_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    # Log only the exception class: statements and parameters may hold sensitive data.
    logger.error("database error", extra={"error_type": type(exc).__name__})
    return error_response(503, "SERVICE_UNAVAILABLE", "Service temporarily unavailable")


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, _validation_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(SQLAlchemyError, _database_error_handler)  # type: ignore[arg-type]
