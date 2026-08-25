from datetime import date, time
from uuid import uuid4

import pytest

from app.exceptions.errors import (
    AttendanceAlreadyExistsError,
    AttendanceSessionNotFoundError,
    CourseNotFoundError,
    StudentNotFoundError,
)
from app.features.attendance.model import (
    AttendanceRecord,
    AttendanceSession,
    AttendanceStatus,
)
from app.features.attendance.repository import (
    AttendanceRecordRepository,
    AttendanceSessionRepository,
)
from app.features.attendance.service import (
    AttendanceRecordService,
    AttendanceSessionService,
)
from app.features.courses.repository import CourseRepository
from app.features.departments.model import Department
from app.features.departments.repository import DepartmentRepository
from app.features.students.repository import StudentRepository


async def create_session(db_session, course, department):
    repository = AttendanceSessionRepository(db_session)
    course_repository = CourseRepository(db_session)
    department_repository = DepartmentRepository(db_session)

    session = AttendanceSession(
        course_id=course.id,
        session_date=date(2026, 8, 24),
        start_time=time(10, 0),
        end_time=time(11, 0),
        department_id=department.id,
        semester=5,
        section="A",
    )

    service = AttendanceSessionService(
        repository,
        course_repository,
        department_repository,
    )

    return await service.create_session(session)


async def create_student(db_session, department):
    from app.features.students.model import Student

    student = Student(
        roll_number=f"TEST-{uuid4().hex[:8]}",
        name="Service Test Student",
        email=f"{uuid4().hex[:8]}@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    db_session.add(student)
    await db_session.flush()
    await db_session.refresh(student)

    return student


@pytest.mark.asyncio
async def test_create_attendance_session(db_session, course, department):
    repository = AttendanceSessionRepository(db_session)
    course_repository = CourseRepository(db_session)
    department_repository = DepartmentRepository(db_session)
    service = AttendanceSessionService(
        repository,
        course_repository,
        department_repository,
    )

    session = AttendanceSession(
        course_id=course.id,
        session_date=date(2026, 8, 24),
        start_time=time(10, 0),
        end_time=time(11, 0),
        department_id=department.id,
        semester=5,
        section="A",
    )

    result = await service.create_session(session)

    assert result.id is not None
    assert result.course_id == course.id


@pytest.mark.asyncio
async def test_create_attendance_session_course_not_found(db_session, department):
    repository = AttendanceSessionRepository(db_session)
    course_repository = CourseRepository(db_session)
    department_repository = DepartmentRepository(db_session)
    service = AttendanceSessionService(
        repository,
        course_repository,
        department_repository,
    )

    session = AttendanceSession(
        course_id=uuid4(),
        session_date=date(2026, 8, 24),
        start_time=time(10, 0),
        end_time=time(11, 0),
        department_id=department.id,
        semester=5,
        section="A",
    )

    with pytest.raises(CourseNotFoundError):
        await service.create_session(session)


@pytest.mark.asyncio
async def test_get_attendance_session(db_session, course, department):
    repository = AttendanceSessionRepository(db_session)
    course_repository = CourseRepository(db_session)
    department_repository = DepartmentRepository(db_session)
    service = AttendanceSessionService(
        repository,
        course_repository,
        department_repository,
    )

    session = AttendanceSession(
        course_id=course.id,
        session_date=date(2026, 8, 24),
        start_time=time(11, 0),
        end_time=time(12, 0),
        department_id=department.id,
        semester=5,
        section="A",
    )

    created = await repository.create(session)

    result = await service.get_session(created.id)

    assert result is not None
    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_attendance_session_not_found(db_session, department):
    repository = AttendanceSessionRepository(db_session)
    course_repository = CourseRepository(db_session)
    department_repository = DepartmentRepository(db_session)
    service = AttendanceSessionService(
        repository,
        course_repository,
        department_repository,
    )

    result = await service.get_session(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_create_attendance_record(db_session, course, department):
    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)
    service = AttendanceRecordService(
        record_repository, session_repository, student_repository
    )

    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.PRESENT,
    )

    result = await service.create_record(record)

    assert result.id is not None
    assert result.session_id == session.id
    assert result.student_id == student.id
    assert result.status == AttendanceStatus.PRESENT


@pytest.mark.asyncio
async def test_get_attendance_record(db_session, course, department):
    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)
    service = AttendanceRecordService(
        record_repository, session_repository, student_repository
    )

    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.ABSENT,
    )

    created = await record_repository.create(record)

    result = await service.get_record(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.status == AttendanceStatus.ABSENT


@pytest.mark.asyncio
async def test_get_attendance_record_not_found(db_session, department):
    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)
    service = AttendanceRecordService(
        record_repository, session_repository, student_repository
    )

    result = await service.get_record(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_create_duplicate_attendance_record(db_session, course, department):
    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)
    service = AttendanceRecordService(
        record_repository, session_repository, student_repository
    )

    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    first_record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.PRESENT,
    )

    await service.create_record(first_record)

    duplicate_record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.ABSENT,
    )

    with pytest.raises(AttendanceAlreadyExistsError):
        await service.create_record(duplicate_record)


@pytest.mark.asyncio
async def test_create_bulk_attendance(db_session, course, department):
    session = await create_session(db_session, course, department)

    student_one = await create_student(db_session, department)
    student_two = await create_student(db_session, department)

    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)
    service = AttendanceRecordService(
        record_repository, session_repository, student_repository
    )

    records = [
        AttendanceRecord(
            session_id=session.id,
            student_id=student_one.id,
            status=AttendanceStatus.PRESENT,
        ),
        AttendanceRecord(
            session_id=session.id,
            student_id=student_two.id,
            status=AttendanceStatus.ABSENT,
        ),
    ]

    result = await service.create_bulk_records(
        session.id,
        records,
    )

    assert len(result) == 2
    assert result[0].student_id == student_one.id
    assert result[0].status == AttendanceStatus.PRESENT
    assert result[1].student_id == student_two.id
    assert result[1].status == AttendanceStatus.ABSENT


@pytest.mark.asyncio
async def test_create_bulk_attendance_duplicate_student(
    db_session,
    course,
    department,
):
    session = await create_session(db_session, course, department)
    student = await create_student(db_session, department)

    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)
    service = AttendanceRecordService(
        record_repository, session_repository, student_repository
    )

    records = [
        AttendanceRecord(
            session_id=session.id,
            student_id=student.id,
            status=AttendanceStatus.PRESENT,
        ),
        AttendanceRecord(
            session_id=session.id,
            student_id=student.id,
            status=AttendanceStatus.ABSENT,
        ),
    ]

    with pytest.raises(AttendanceAlreadyExistsError):
        await service.create_bulk_records(
            session.id,
            records,
        )


@pytest.mark.asyncio
async def test_create_bulk_attendance_session_not_found(
    db_session,
    department,
):
    repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)

    service = AttendanceRecordService(
        repository, session_repository, student_repository
    )

    fake_session_id = uuid4()

    record = AttendanceRecord(
        session_id=fake_session_id,
        student_id=uuid4(),
        status=AttendanceStatus.PRESENT,
    )

    with pytest.raises(AttendanceSessionNotFoundError):
        await service.create_bulk_records(
            fake_session_id,
            [record],
        )


@pytest.mark.asyncio
async def test_create_bulk_attendance_student_not_found(
    db_session,
    course,
    department,
):
    session = await create_session(db_session, course, department)

    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)

    service = AttendanceRecordService(
        record_repository,
        session_repository,
        student_repository,
    )

    fake_student_id = uuid4()

    record = AttendanceRecord(
        session_id=session.id,
        student_id=fake_student_id,
        status=AttendanceStatus.PRESENT,
    )

    with pytest.raises(StudentNotFoundError):
        await service.create_bulk_records(
            session.id,
            [record],
        )


@pytest.mark.asyncio
async def test_create_bulk_attendance_student_wrong_class(
    db_session,
    course,
    department,
):
    session = await create_session(db_session, course, department)

    student = await create_student(db_session, department)

    # Change the student so it doesn't belong to the session.
    ece_department = Department(
        code="ECE",
        name="Electronics and Communication Engineering",
    )
    db_session.add(ece_department)
    await db_session.commit()
    await db_session.refresh(ece_department)

    student.department_id = ece_department.id

    await db_session.flush()

    record_repository = AttendanceRecordRepository(db_session)
    session_repository = AttendanceSessionRepository(db_session)
    student_repository = StudentRepository(db_session)

    service = AttendanceRecordService(
        record_repository,
        session_repository,
        student_repository,
    )

    record = AttendanceRecord(
        session_id=session.id,
        student_id=student.id,
        status=AttendanceStatus.PRESENT,
    )

    with pytest.raises(ValueError):
        await service.create_bulk_records(
            session.id,
            [record],
        )
