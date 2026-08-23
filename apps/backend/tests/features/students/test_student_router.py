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


@pytest.mark.asyncio
async def test_update_student(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "API006",
            "name": "Before Update",
            "email": "update-api@example.com",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    assert create_response.status_code == 201

    student = create_response.json()

    response = await client.patch(
        f"/api/v1/students/{student['id']}",
        json={
            "name": "After Update",
            "semester": 6,
            "section": "B",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student["id"]
    assert data["name"] == "After Update"
    assert data["semester"] == 6
    assert data["section"] == "B"

    # roll number should remain unchanged
    assert data["roll_number"] == "API006"


@pytest.mark.asyncio
async def test_update_student_not_found(client: AsyncClient):
    student_id = uuid.uuid4()

    response = await client.patch(
        f"/api/v1/students/{student_id}",
        json={
            "name": "Does Not Exist",
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": f"Student with id '{student_id}' was not found"
    }


@pytest.mark.asyncio
async def test_deactivate_student(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "API007",
            "name": "Deactivate Test",
            "email": "deactivate@example.com",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    assert create_response.status_code == 201

    student = create_response.json()

    assert student["is_active"] is True

    response = await client.delete(f"/api/v1/students/{student['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student["id"]
    assert data["roll_number"] == "API007"
    assert data["is_active"] is False


@pytest.mark.asyncio
async def test_deactivated_student_not_in_list(
    client: AsyncClient,
):
    create_response = await client.post(
        "/api/v1/students",
        json={
            "roll_number": "API008",
            "name": "Inactive Student",
            "email": "inactive@example.com",
            "department": "CSE",
            "semester": 5,
            "section": "A",
        },
    )

    assert create_response.status_code == 201

    student = create_response.json()

    delete_response = await client.delete(f"/api/v1/students/{student['id']}")

    assert delete_response.status_code == 200

    list_response = await client.get("/api/v1/students")

    assert list_response.status_code == 200

    data = list_response.json()

    roll_numbers = [item["roll_number"] for item in data["items"]]

    assert "API008" not in roll_numbers


@pytest.mark.asyncio
async def test_deactivate_student_not_found(
    client: AsyncClient,
):
    student_id = uuid.uuid4()

    response = await client.delete(f"/api/v1/students/{student_id}")

    assert response.status_code == 404

    assert response.json() == {
        "detail": f"Student with id '{student_id}' was not found"
    }


@pytest.mark.asyncio
async def test_get_students_by_department(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?department=CSE")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data

    for student in data["items"]:
        assert student["department"] == "CSE"


@pytest.mark.asyncio
async def test_get_students_by_semester(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?semester=5")

    assert response.status_code == 200

    data = response.json()

    for student in data["items"]:
        assert student["semester"] == 5


@pytest.mark.asyncio
async def test_get_students_by_section(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?section=A")

    assert response.status_code == 200

    data = response.json()

    for student in data["items"]:
        assert student["section"] == "A"


@pytest.mark.asyncio
async def test_get_students_with_multiple_filters(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?department=CSE&semester=5&section=A")

    assert response.status_code == 200

    data = response.json()

    for student in data["items"]:
        assert student["department"] == "CSE"
        assert student["semester"] == 5
        assert student["section"] == "A"


@pytest.mark.asyncio
async def test_students_filter_with_pagination(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?department=CSE&offset=0&limit=5")

    assert response.status_code == 200

    data = response.json()

    assert data["offset"] == 0
    assert data["limit"] == 5
    assert len(data["items"]) <= 5

    for student in data["items"]:
        assert student["department"] == "CSE"


@pytest.mark.asyncio
async def test_get_students_with_no_matching_department(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?department=NONEXISTENT")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_students_invalid_semester(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?semester=0")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_students_semester_above_maximum(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?semester=9")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_students_negative_offset(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?offset=-1")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_students_invalid_limit(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?limit=0")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_students_limit_too_large(
    client: AsyncClient,
):
    response = await client.get("/api/v1/students?limit=101")

    assert response.status_code == 422
