from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


async def transaction(session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session.begin():
        yield session


# transaction starts and yeilds a session if everything succceds then commit happens to
# DB else rollback so no data will get saved
