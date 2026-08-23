from datetime import date, time
from uuid import uuid4

import pytest

from app.features.attendance.model import AttendanceSession
from app.features.attendance.repository import AttendanceSessionRepository
from app.features.attendance.service import AttendanceSessionService


@pytest.mark.asyncio
async def test_create_attendance_session(db_session):
    repository = AttendanceSessionRepository(db_session)
    service = AttendanceSessionService(repository)

    session = AttendanceSession(
        subject="DBMS",
        session_date=date(2026, 8, 24),
        start_time=time(10, 0),
        end_time=time(11, 0),
        department="CSE",
        semester=5,
        section="A",
    )

    result = await service.create_session(session)

    assert result.id is not None
    assert result.subject == "DBMS"


@pytest.mark.asyncio
async def test_get_attendance_session(db_session):
    repository = AttendanceSessionRepository(db_session)
    service = AttendanceSessionService(repository)

    session = AttendanceSession(
        subject="OS",
        session_date=date(2026, 8, 24),
        start_time=time(11, 0),
        end_time=time(12, 0),
        department="CSE",
        semester=5,
        section="A",
    )

    created = await repository.create(session)

    result = await service.get_session(created.id)

    assert result is not None
    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_attendance_session_not_found(db_session):
    repository = AttendanceSessionRepository(db_session)
    service = AttendanceSessionService(repository)

    result = await service.get_session(uuid4())

    assert result is None
