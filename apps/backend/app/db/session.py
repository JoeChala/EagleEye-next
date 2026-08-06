from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.db.engine import async_engine

SessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """
    FastAPI dependency that provides a database session.
    """

    async with SessionLocal() as session:
        yield session


async def check_database_connection() -> dict[str, object]:
    """
    Check whether the database is reachable.

    Used by the health endpoint.
    """

    try:
        async with async_engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return {
            "connected": True,
            "status": "healthy",
            "driver": async_engine.name,
        }

    except SQLAlchemyError as exc:
        return {
            "connected": False,
            "status": "unhealthy",
            "driver": async_engine.name,
            "error": str(exc),
        }
