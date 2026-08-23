from uuid import UUID

from app.features.attendance.model import AttendanceSession
from app.features.attendance.repository import (
    AttendanceSessionRepository,
)


class AttendanceSessionService:
    def __init__(self, repository: AttendanceSessionRepository):
        self.repository = repository

    async def create_session(
        self,
        attendance_session: AttendanceSession,
    ) -> AttendanceSession:
        return await self.repository.create(attendance_session)

    async def get_session(
        self,
        session_id: UUID,
    ) -> AttendanceSession | None:
        return await self.repository.get_by_id(session_id)
