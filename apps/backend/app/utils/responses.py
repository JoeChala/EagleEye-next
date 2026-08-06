from collections.abc import Mapping, Sequence
from typing import Any

from fastapi.responses import JSONResponse


def success_response(
    *,
    message: str = "Success",
    data: Any | None = None,
    status_code: int = 200,
) -> JSONResponse:
    payload = {
        "success": True,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=payload)


def error_response(
    *,
    message: str,
    errors: Sequence[object] | Mapping[str, object] | None = None,
    status_code: int = 400,
) -> JSONResponse:
    normalized_errors: list[object]
    if errors is None:
        normalized_errors = []
    elif isinstance(errors, Mapping):
        normalized_errors = [dict(errors)]
    else:
        normalized_errors = list(errors)

    payload = {
        "success": False,
        "message": message,
        "errors": normalized_errors,
    }
    return JSONResponse(status_code=status_code, content=payload)
