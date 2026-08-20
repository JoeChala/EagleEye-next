import uuid

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


@pytest.mark.asyncio
async def test_get_student(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "API003",
            "name": "API Get Student",
            "email": "api-get@example.com",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    assert create_response.status_code == 201

    student = create_response.json()

    response = await client.get(f"/api/v1/students/{student['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student["id"]
    assert data["roll_number"] == "API003"


@pytest.mark.asyncio
async def test_get_student_not_found(client: AsyncClient):
    student_id = uuid.uuid4()

    response = await client.get(f"/api/v1/students/{student_id}")

    assert response.status_code == 404

    assert response.json() == {
        "detail": f"Student with id '{student_id}' was not found"
    }


@pytest.mark.asyncio
async def test_get_students(client: AsyncClient):
    await client.post(
        "/api/v1/students",
        json={
            "roll_number": "API004",
            "name": "API Student One",
            "email": "api4@example.com",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    await client.post(
        "/api/v1/students",
        json={
            "roll_number": "API005",
            "name": "API Student Two",
            "email": "api5@example.com",
            "department": "CSE",
            "semester": 6,
            "section": "B",
        },
    )

    response = await client.get("/api/v1/students")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["offset"] == 0
    assert data["limit"] == 20

    assert data["items"][0]["roll_number"] == "API005"
    assert data["items"][1]["roll_number"] == "API004"


@pytest.mark.asyncio
async def test_get_students_pagination(client: AsyncClient):
    for i in range(3):
        response = await client.post(
            "/api/v1/students",
            json={
                "roll_number": f"PAGE00{i}",
                "name": f"Page Student {i}",
                "email": f"page{i}@example.com",
                "department": "CSE",
                "semester": 5,
                "section": "A",
            },
        )

        assert response.status_code == 201

    response = await client.get("/api/v1/students?offset=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert data["offset"] == 1
    assert data["limit"] == 1
