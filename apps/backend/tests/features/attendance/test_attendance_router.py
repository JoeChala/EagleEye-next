from uuid import uuid4

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_attendance_session(client: AsyncClient):
    response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "subject": "DBMS",
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

    assert data["subject"] == "DBMS"
    assert data["session_date"] == "2026-08-24"
    assert data["department"] == "CSE"
    assert data["semester"] == 5
    assert data["section"] == "A"


@pytest.mark.asyncio
async def test_get_attendance_session(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/attendance/sessions",
        json={
            "subject": "OS",
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
