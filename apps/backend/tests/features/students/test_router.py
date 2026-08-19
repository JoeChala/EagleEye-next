import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_student(client: AsyncClient):
    response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "API001",
            "name": "API Test Student",
            "email": "api@example.com",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["roll_number"] == "API001"
    assert data["name"] == "API Test Student"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_student_duplicate_roll_number(client: AsyncClient):
    student = {
        "roll_number": "API002",
        "name": "API Test Student",
        "email": "api@example.com",
        "department": "CSE",
        "semester": 5,
        "section": "A",
    }

    first_response = await client.post(
        "/api/v1/students",
        json=student,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/students",
        json=student,
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "Student with roll number 'API002' already exists"
    )
