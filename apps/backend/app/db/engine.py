from __future__ import annotations

from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings


def _normalize_database_url(database_url: str) -> str:
    # Normalize PostgreSQL URLs for SQLAlchemy async support.
    
    database_url = database_url.strip()

    if database_url.startswith("postgres://"):
        return "postgresql+asyncpg://" + database_url.removeprefix("postgres://")

    if database_url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + database_url.removeprefix("postgresql://")

    if database_url.startswith("postgresql+psycopg://"):
        return "postgresql+asyncpg://" + database_url.removeprefix(
            "postgresql+psycopg://"
        )

    return database_url


@lru_cache(maxsize=1)
def get_database_url() -> str:
    database_url = _normalize_database_url(settings.database_url)

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    return database_url


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    # Create a singleton SQLAlchemy AsyncEngine.

    return create_async_engine(
        get_database_url(),
        echo=settings.debug,
        future=True,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
    )


async_engine = get_engine()
