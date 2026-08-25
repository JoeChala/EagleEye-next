import uuid
from datetime import date as DateType
from datetime import time as TimeType

import pytest
from sqlalchemy.exc import IntegrityError

from app.features.attendance.model import (
    AttendanceRecord,
    AttendanceSession,
    AttendanceStatus,
)
from app.features.attendance.repository import (
    AttendanceRecordRepository,
    AttendanceSessionRepository,
)


@pytest.mark.asyncio
async def test_create_attendance_session(db_session, course, department):
    repository = AttendanceSessionRepository(db_session)

    attendance_session = AttendanceSession(
        course_id=course.id,
        session_date=DateType(2026, 8, 24),
        start_time=TimeType(10, 0),
        end_time=TimeType(11, 0),
        department_id=department.id,
        semester=5,
        section="A",
    )

    result = await repository.create(attendance_session)

    assert result.id is not None
    assert result.course_id == course.id


@pytest.mark.asyncio
async def test_get_attendance_session_by_id(db_session, course, department):
    repository = AttendanceSessionRepository(db_session)

    attendance_session = AttendanceSession(
        course_id=course.id,
        session_date=DateType(2026, 8, 24),
        start_time=TimeType(11, 0),
        end_time=TimeType(12, 0),
        department_id=department.id,
        semester=5,
        section="A",
    )

    created = await repository.create(attendance_session)

    result = await repository.get_by_id(created.id)

    assert result is not None
    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_attendance_session_not_found(db_session, department):
    repository = AttendanceSessionRepository(db_session)

    result = await repository.get_by_id(uuid.uuid4())

    assert result is None


async def create_session(db_session, course, department):
    session = AttendanceSession(
        course_id=course.id,
        session_date=DateType(2026, 8, 24),
        start_time=TimeType(10, 0),
        end_time=TimeType(11, 0),
        department_id=department.id,
        semester=5,
        section="A",
    )

    db_session.add(session)
    await db_session.flush()
    await db_session.refresh(session)

    return session


async def create_student(db_session, department):
    from app.features.students.model import Student

    student = Student(
        roll_number=f"TEST-{uuid.uuid4().hex[:8]}",
        name="Test Student",
        email=f"{uuid.uuid4().hex[:8]}@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    db_session.add(student)
    await db_session.flush()
    await db_session.refresh(student)

    return student


@pytest.mark.asyncio
async def test_create_attendance_record(db_session, course, department):
    repository = AttendanceRecordRepository(db_session)

    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.PRESENT,
    )

    result = await repository.create(record)

    assert result.id is not None
    assert result.session_id == session.id
    assert result.student_id == student.id
    assert result.status == AttendanceStatus.PRESENT


@pytest.mark.asyncio
async def test_get_attendance_record_by_id(db_session, course, department):
    repository = AttendanceRecordRepository(db_session)

    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.PRESENT,
    )

    created = await repository.create(record)

    result = await repository.get_by_id(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.session_id == session.id
    assert result.student_id == student.id


@pytest.mark.asyncio
async def test_get_attendance_record_not_found(db_session, department):
    repository = AttendanceRecordRepository(db_session)

    result = await repository.get_by_id(uuid.uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_get_by_session_and_student(db_session, course, department):
    repository = AttendanceRecordRepository(db_session)

    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.ABSENT,
    )

    created = await repository.create(record)

    result = await repository.get_by_session_and_student(
        session.id,
        student.id,
    )

    assert result is not None
    assert result.id == created.id
    assert result.status == AttendanceStatus.ABSENT


@pytest.mark.asyncio
async def test_get_by_session_and_student_not_found(db_session, department):
    repository = AttendanceRecordRepository(db_session)

    result = await repository.get_by_session_and_student(
        uuid.uuid4(),
        uuid.uuid4(),
    )

    assert result is None


@pytest.mark.asyncio
async def test_duplicate_attendance_record_is_rejected(db_session, course, department):
    repository = AttendanceRecordRepository(db_session)

    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    first_record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.PRESENT,
    )

    await repository.create(first_record)

    duplicate_record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.ABSENT,
    )

    with pytest.raises(IntegrityError):
        await repository.create(duplicate_record)

    await db_session.rollback()
