from contextvars import ContextVar, Token
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


REQUEST_ID_HEADER = "X-Request-ID"
request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    return request_id_context.get()


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid4())
        token: Token[str | None] = request_id_context.set(request_id)
        request.state.request_id = request_id
        try:
            response = await call_next(request)
        finally:
            request_id_context.reset(token)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response

