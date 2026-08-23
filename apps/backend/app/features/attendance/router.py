from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.attendance.model import AttendanceSession
from app.features.attendance.repository import AttendanceSessionRepository
from app.features.attendance.schema import (
    AttendanceSessionCreate,
    AttendanceSessionResponse,
)
from app.features.attendance.service import AttendanceSessionService

router = APIRouter(
    prefix="/attendance/sessions",
    tags=["Attendance"],
)


def get_attendance_service(
    db: AsyncSession = Depends(get_db),
) -> AttendanceSessionService:
    repository = AttendanceSessionRepository(db)
    return AttendanceSessionService(repository)


@router.post(
    "",
    response_model=AttendanceSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_attendance_session(
    data: AttendanceSessionCreate,
    service: AttendanceSessionService = Depends(get_attendance_service),
):
    session = AttendanceSession(**data.model_dump())

    return await service.create_session(session)


@router.get(
    "/{session_id}",
    response_model=AttendanceSessionResponse,
)
async def get_attendance_session(
    session_id: UUID,
    service: AttendanceSessionService = Depends(get_attendance_service),
):
    session = await service.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance session with id '{session_id}' was not found",
        )

    return session
