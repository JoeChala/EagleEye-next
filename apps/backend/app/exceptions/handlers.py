from typing import cast

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import logger
from app.exceptions.errors import (
    AttendanceAlreadyExistsError,
    StudentAlreadyExistsError,
    StudentNotFoundError,
)
from app.utils.responses import error_response


def _http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    error = cast(HTTPException, exc)
    message = str(error.detail) if error.detail else "Request failed"
    errors: list[object] = []
    if isinstance(error.detail, list):
        errors = error.detail
        message = "Request failed"
    return error_response(message=message, errors=errors, status_code=error.status_code)


def _validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    error = cast(RequestValidationError, exc)
    return error_response(
        message="Validation failed",
        errors=error.errors(),
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


def _generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled application error", exc_info=exc)
    return error_response(
        message="Internal server error",
        errors=[],
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _student_already_exists_handler(request: Request, exc: Exception) -> JSONResponse:
    error = cast(StudentAlreadyExistsError, exc)
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(error),
        },
    )


def _student_not_found(request: Request, exc: Exception) -> JSONResponse:
    error = cast(StudentNotFoundError, exc)
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(error),
        },
    )


def _attendance_already_exists_handler(
    _: Request,
    exc: Exception,
) -> JSONResponse:
    error = cast(AttendanceAlreadyExistsError, exc)

    return error_response(
        message=str(error),
        status_code=status.HTTP_409_CONFLICT,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)
    app.add_exception_handler(Exception, _generic_exception_handler)
    app.add_exception_handler(
        StudentAlreadyExistsError, _student_already_exists_handler
    )
    app.add_exception_handler(StudentNotFoundError, _student_not_found)
    app.add_exception_handler(
        AttendanceAlreadyExistsError,
        _attendance_already_exists_handler,
    )
