from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.attendance.model import AttendanceRecord, AttendanceSession


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


class AttendanceRecordRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        record: AttendanceRecord,
    ) -> AttendanceRecord:
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)

        return record

    async def get_by_id(
        self,
        record_id: UUID,
    ) -> AttendanceRecord | None:
        result = await self.session.execute(
            select(AttendanceRecord).where(AttendanceRecord.id == record_id)
        )

        return result.scalar_one_or_none()

    async def get_by_session_and_student(
        self,
        session_id: UUID,
        student_id: UUID,
    ) -> AttendanceRecord | None:
        result = await self.session.execute(
            select(AttendanceRecord).where(
                AttendanceRecord.session_id == session_id,
                AttendanceRecord.student_id == student_id,
            )
        )

        return result.scalar_one_or_none()
