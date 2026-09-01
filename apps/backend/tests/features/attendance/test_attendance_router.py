from datetime import date
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.features.attendance.model import AttendanceRecord, AttendanceStatus
from app.features.enrollments.model import Enrollment


@pytest.mark.asyncio
async def test_create_attendance_session(client: AsyncClient, course, department):
    response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-24",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )
    assert response.status_code == 201

    data = response.json()

    assert data["course_id"] == str(course.id)
    assert data["session_date"] == "2026-08-24"
    assert data["department_id"] == str(department.id)
    assert data["semester"] == 5
    assert data["section"] == "A"


@pytest.mark.asyncio
async def test_get_attendance_session(client: AsyncClient, course, department):
    create_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-24",
            "start_time": "11:00:00",
            "end_time": "12:00:00",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )
    assert create_response.status_code == 201

    session_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/attendance/sessions/{session_id}")

    assert response.status_code == 200
    assert response.json()["id"] == session_id


@pytest.mark.asyncio
async def test_get_attendance_session_not_found(client: AsyncClient, department):
    session_id = uuid4()

    response = await client.get(f"/api/v1/attendance/sessions/{session_id}")

    assert response.status_code == 404

    assert response.json() == {
        "success": False,
        "message": f"Attendance session with id '{session_id}' was not found",
        "errors": [],
    }


@pytest.mark.asyncio
async def test_create_attendance_record(client: AsyncClient, course, department):
    # Create attendance session
    session_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-24",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )

    assert session_response.status_code == 201

    session_id = session_response.json()["id"]

    # Create student
    student_response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "ATT001",
            "name": "Attendance Student",
            "email": "attendance@example.com",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )

    assert student_response.status_code == 201

    student_id = student_response.json()["id"]

    enrollment_response = await client.post(
        "/api/v1/enrollments",
        json={
            "student_id": student_id,
            "course_id": str(course.id),
        },
    )

    assert enrollment_response.status_code == 201

    # Create attendance
    response = await client.post(
        "/api/v1/attendance/records",
        json={
            "session_id": session_id,
            "student_id": student_id,
            "status": "present",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["session_id"] == session_id
    assert data["student_id"] == student_id
    assert data["status"] == "present"


@pytest.mark.asyncio
async def test_get_attendance_record(client: AsyncClient, course, department):
    session_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-25",
            "start_time": "11:00:00",
            "end_time": "12:00:00",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )

    session_id = session_response.json()["id"]

    student_response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "ATT002",
            "name": "Get Attendance Student",
            "email": "getattendance@example.com",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )

    student_id = student_response.json()["id"]
    enrollment_response = await client.post(
        "/api/v1/enrollments",
        json={
            "student_id": student_id,
            "course_id": str(course.id),
        },
    )

    assert enrollment_response.status_code == 201

    create_response = await client.post(
        "/api/v1/attendance/records",
        json={
            "session_id": session_id,
            "student_id": student_id,
            "status": "absent",
        },
    )

    assert create_response.status_code == 201

    record_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/attendance/records/{record_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == record_id
    assert data["status"] == "absent"


@pytest.mark.asyncio
async def test_get_attendance_record_not_found(
    client: AsyncClient,
    department,
):
    record_id = uuid4()

    response = await client.get(f"/api/v1/attendance/records/{record_id}")

    assert response.status_code == 404

    assert response.json() == {
        "success": False,
        "message": (f"Attendance record with id '{record_id}' was not found"),
        "errors": [],
    }


@pytest.mark.asyncio
async def test_create_duplicate_attendance_record(
    client: AsyncClient,
    course,
    department,
):
    # Create session
    session_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-26",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )

    session_id = session_response.json()["id"]

    # Create student
    student_response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "ATT003",
            "name": "Duplicate Attendance Student",
            "email": "duplicate@example.com",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )

    student_id = student_response.json()["id"]
    enrollment_response = await client.post(
        "/api/v1/enrollments",
        json={
            "student_id": student_id,
            "course_id": str(course.id),
        },
    )

    assert enrollment_response.status_code == 201

    payload = {
        "session_id": session_id,
        "student_id": student_id,
        "status": "present",
    }

    first_response = await client.post(
        "/api/v1/attendance/records",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/attendance/records",
        json=payload,
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["success"] is False
    assert data["errors"] == []


@pytest.mark.asyncio
async def test_create_attendance_session_invalid_course(
    client: AsyncClient, department
):
    missing_course_id = uuid4()

    response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(missing_course_id),
            "session_date": "2026-08-24",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "department_id": str(department.id),
            "semester": 5,
            "section": "A",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Course with id '{missing_course_id}' was not found"
    }


@pytest.mark.asyncio
async def test_get_student_course_attendance_summary(
    client: AsyncClient,
    db_session,
    student,
    course,
    department,
    attendance_session_factory,
):
    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    db_session.add(enrollment)
    await db_session.commit()

    session_one = await attendance_session_factory(
        course=course,
        department=department,
        session_date=date(2026, 8, 24),
    )

    session_two = await attendance_session_factory(
        course=course,
        department=department,
        session_date=date(2026, 8, 25),
    )

    session_three = await attendance_session_factory(
        course=course,
        department=department,
        session_date=date(2026, 8, 26),
    )

    db_session.add_all(
        [
            AttendanceRecord(
                session_id=session_one.id,
                student_id=student.id,
                status=AttendanceStatus.PRESENT,
            ),
            AttendanceRecord(
                session_id=session_two.id,
                student_id=student.id,
                status=AttendanceStatus.PRESENT,
            ),
            AttendanceRecord(
                session_id=session_three.id,
                student_id=student.id,
                status=AttendanceStatus.ABSENT,
            ),
        ]
    )

    await db_session.commit()

    response = await client.get(
        "/api/v1/attendance",
        params={
            "student": str(student.id),
            "course": str(course.id),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == str(student.id)
    assert data["course_id"] == str(course.id)
    assert data["total_sessions"] == 3
    assert data["present"] == 2
    assert data["absent"] == 1
    assert data["attendance_percentage"] == 66.67


@pytest.mark.asyncio
async def test_get_student_course_attendance_student_not_found(
    client: AsyncClient,
    course,
):
    student_id = uuid4()

    response = await client.get(
        "/api/v1/attendance",
        params={
            "student": str(student_id),
            "course": str(course.id),
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": f"Student with id '{student_id}' was not found"
    }


@pytest.mark.asyncio
async def test_get_student_course_attendance_no_records(
    client: AsyncClient,
    student,
    course,
):
    enrollment_response = await client.post(
        "/api/v1/enrollments",
        json={
            "student_id": str(student.id),
            "course_id": str(course.id),
        },
    )

    assert enrollment_response.status_code == 201
    response = await client.get(
        "/api/v1/attendance",
        params={
            "student": str(student.id),
            "course": str(course.id),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == str(student.id)
    assert data["course_id"] == str(course.id)
    assert data["total_sessions"] == 0
    assert data["present"] == 0
    assert data["absent"] == 0
    assert data["attendance_percentage"] == 0.0


@pytest.mark.asyncio
async def test_get_student_course_attendance_missing_student(
    client: AsyncClient,
    course,
):
    response = await client.get(
        "/api/v1/attendance",
        params={
            "course": str(course.id),
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Validation failed"
    assert data["errors"]


@pytest.mark.asyncio
async def test_get_student_course_attendance_missing_course(
    client: AsyncClient,
    student,
):
    response = await client.get(
        "/api/v1/attendance",
        params={
            "student": str(student.id),
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Validation failed"
    assert data["errors"]


@pytest.mark.asyncio
async def test_get_student_course_attendance_invalid_student_id(
    client: AsyncClient,
    course,
):
    response = await client.get(
        "/api/v1/attendance",
        params={
            "student": "not-a-uuid",
            "course": str(course.id),
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Validation failed"
    assert data["errors"]
