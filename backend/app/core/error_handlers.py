"""
app/core/error_handlers.py
Registers global exception → HTTP response mappings on the FastAPI app.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.exceptions import AppException
from app.core.constants import GenericErrorCode


def _error_body(code: str, message: str, extra: dict | None = None) -> dict:
    body: dict = {"success": False, "code": code, "message": message}
    if extra:
        body.update(extra)
    return body


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.code, exc.message),
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_error_body(
                GenericErrorCode.VALIDATION_ERROR,
                "Request validation failed.",
                {"details": exc.errors()},
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        # Never leak internals in production
        return JSONResponse(
            status_code=500,
            content=_error_body(
                GenericErrorCode.INTERNAL_SERVER_ERROR,
                "An unexpected error occurred. Please try again later.",
            ),
        )
