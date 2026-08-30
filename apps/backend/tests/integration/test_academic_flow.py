from datetime import date, time
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.attendance.model import (
    AttendanceRecord,
    AttendanceSession,
    AttendanceStatus,
)
from app.features.courses.model import Course
from app.features.departments.model import Department
from app.features.faculty.model import Faculty
from app.features.students.model import Student


@pytest.mark.asyncio
async def test_complete_academic_attendance_flow(db_session: AsyncSession):
    # Department

    department = Department(
        code="CSE",
        name="Computer Science and Engineering",
    )

    db_session.add(department)
    await db_session.flush()

    # Student

    student = Student(
        roll_number="INT001",
        name="Integration Student",
        email="integration@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    # Faculty

    faculty = Faculty(
        employee_id="FAC001",
        name="Integration Faculty",
        email="faculty@example.com",
        department_id=department.id,
    )

    # Course

    course = Course(
        code="CS501",
        name="Database Management Systems",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    db_session.add_all(
        [
            student,
            faculty,
            course,
        ]
    )

    await db_session.flush()

    # Attendance Session

    attendance_session = AttendanceSession(
        course_id=course.id,
        department_id=department.id,
        session_date=date(2026, 8, 24),
        start_time=time(10, 0),
        end_time=time(11, 0),
        semester=5,
        section="A",
    )

    db_session.add(attendance_session)
    await db_session.flush()

    # Attendance Record

    attendance_record = AttendanceRecord(
        session_id=attendance_session.id,
        student_id=student.id,
        status=AttendanceStatus.PRESENT,
    )

    db_session.add(attendance_record)

    await db_session.commit()
    await db_session.refresh(attendance_record)

    # Verify the complete chain

    assert department.id is not None
    assert course.department_id == department.id
    assert student.department_id == department.id
    assert faculty.department_id == department.id

    assert attendance_session.course_id == course.id
    assert attendance_session.department_id == department.id

    assert attendance_record.session_id == attendance_session.id
    assert attendance_record.student_id == student.id
    assert attendance_record.status == AttendanceStatus.PRESENT


@pytest.mark.asyncio
async def test_course_rejects_nonexistent_department(db_session: AsyncSession):
    course = Course(
        code="CS999",
        name="Invalid Department Course",
        department_id=uuid4(),
        semester=5,
        credits=4,
    )

    db_session.add(course)

    with pytest.raises(IntegrityError):
        await db_session.commit()

    await db_session.rollback()


@pytest.mark.asyncio
async def test_attendance_session_rejects_nonexistent_course(db_session: AsyncSession):
    department = Department(
        code="CSE",
        name="Computer Science and Engineering",
    )

    db_session.add(department)
    await db_session.flush()

    attendance_session = AttendanceSession(
        course_id=uuid4(),
        department_id=department.id,
        session_date=date(2026, 8, 24),
        start_time=time(10, 0),
        end_time=time(11, 0),
        semester=5,
        section="A",
    )

    db_session.add(attendance_session)

    with pytest.raises(IntegrityError):
        await db_session.commit()

    await db_session.rollback()
