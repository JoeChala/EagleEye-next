from collections.abc import AsyncIterator, Iterator

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine: Engine | None = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None
session_factory: sessionmaker[Session] | None = None


def init_db() -> None:
    # TODO: Initialize SQLAlchemy engines when persistence is added.
    _ = settings.database_url


async def get_async_session() -> AsyncIterator[AsyncSession]:
    # TODO: Yield an async session when the database layer is enabled.
    raise NotImplementedError


def get_session() -> Iterator[Session]:
    # TODO: Yield a sync session when the database layer is enabled.
    raise NotImplementedError
