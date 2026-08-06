from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import logger
from app.utils.responses import error_response


def _http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    message = str(exc.detail) if exc.detail else "Request failed"
    errors: list[object] = []
    if isinstance(exc.detail, list):
        errors = exc.detail
        message = "Request failed"
    return error_response(message=message, errors=errors, status_code=exc.status_code)


def _validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return error_response(
        message="Validation failed",
        errors=exc.errors(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def _generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled application error", exc_info=exc)
    return error_response(
        message="Internal server error",
        errors=[],
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)
    app.add_exception_handler(Exception, _generic_exception_handler)
