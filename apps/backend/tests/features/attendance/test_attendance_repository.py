import uuid
from datetime import date as DateType
from datetime import time as TimeType

import pytest

from app.features.attendance.model import AttendanceSession
from app.features.attendance.repository import (
    AttendanceSessionRepository,
)


@pytest.mark.asyncio
async def test_create_attendance_session(db_session):
    repository = AttendanceSessionRepository(db_session)

    attendance_session = AttendanceSession(
        subject="Database Management Systems",
        session_date=DateType(2026, 8, 24),
        start_time=TimeType(10, 0),
        end_time=TimeType(11, 0),
        department="CSE",
        semester=5,
        section="A",
    )

    result = await repository.create(attendance_session)

    assert result.id is not None
    assert result.subject == "Database Management Systems"


@pytest.mark.asyncio
async def test_get_attendance_session_by_id(db_session):
    repository = AttendanceSessionRepository(db_session)

    attendance_session = AttendanceSession(
        subject="Operating Systems",
        session_date=DateType(2026, 8, 24),
        start_time=TimeType(11, 0),
        end_time=TimeType(12, 0),
        department="CSE",
        semester=5,
        section="A",
    )

    created = await repository.create(attendance_session)

    result = await repository.get_by_id(created.id)

    assert result is not None
    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_attendance_session_not_found(db_session):
    repository = AttendanceSessionRepository(db_session)

    result = await repository.get_by_id(uuid.uuid4())

    assert result is None
