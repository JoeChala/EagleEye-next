from uuid import uuid4

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_attendance_session(client: AsyncClient, course):
    response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-24",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )
    assert response.status_code == 201

    data = response.json()

    assert data["course_id"] == str(course.id)
    assert data["session_date"] == "2026-08-24"
    assert data["department"] == "CSE"
    assert data["semester"] == 5
    assert data["section"] == "A"


@pytest.mark.asyncio
async def test_get_attendance_session(client: AsyncClient, course):
    create_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-24",
            "start_time": "11:00:00",
            "end_time": "12:00:00",
            "department": "CSE",
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
async def test_get_attendance_session_not_found(client: AsyncClient):
    session_id = uuid4()

    response = await client.get(f"/api/v1/attendance/sessions/{session_id}")

    assert response.status_code == 404

    assert response.json() == {
        "success": False,
        "message": f"Attendance session with id '{session_id}' was not found",
        "errors": [],
    }


@pytest.mark.asyncio
async def test_create_attendance_record(client: AsyncClient, course):
    # Create attendance session
    session_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-24",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "department": "CSE",
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
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    assert student_response.status_code == 201

    student_id = student_response.json()["id"]

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
async def test_get_attendance_record(client: AsyncClient, course):
    session_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-25",
            "start_time": "11:00:00",
            "end_time": "12:00:00",
            "department": "CSE",
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
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    student_id = student_response.json()["id"]

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
):
    # Create session
    session_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(course.id),
            "session_date": "2026-08-26",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "department": "CSE",
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
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    student_id = student_response.json()["id"]

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
async def test_create_attendance_session_invalid_course(client: AsyncClient):
    missing_course_id = uuid4()

    response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "course_id": str(missing_course_id),
            "session_date": "2026-08-24",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Course with id '{missing_course_id}' was not found"
    }
