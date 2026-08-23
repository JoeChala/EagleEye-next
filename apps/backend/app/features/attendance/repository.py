from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.attendance.model import AttendanceSession


class AttendanceSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        attendance_session: AttendanceSession,
    ) -> AttendanceSession:
        self.session.add(attendance_session)

        await self.session.flush()
        await self.session.refresh(attendance_session)

        return attendance_session

    async def get_by_id(
        self,
        session_id: UUID,
    ) -> AttendanceSession | None:
        result = await self.session.execute(
            select(AttendanceSession).where(AttendanceSession.id == session_id)
        )

        return result.scalar_one_or_none()
