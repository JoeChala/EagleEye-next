from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request_id import RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Stopping %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="EagleEye v2 FastAPI service",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(RequestIdMiddleware)
app.include_router(api_router)
register_exception_handlers(app)

