from fastapi import APIRouter

from app.core.config import settings
from app.utils.responses import success_response

api_router = APIRouter(prefix=settings.api_prefix)


@api_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@api_router.get("/version")
async def version():
    return success_response(
        message="Application version",
        data={"name": settings.app_name, "version": settings.app_version},
    )

