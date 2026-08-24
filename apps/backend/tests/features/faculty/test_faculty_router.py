import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_faculty(client: AsyncClient):
    response = await client.post(
        "/api/v1/faculty",
        json={
            "employee_id": "EMP019",
            "name": "API Test Faculty",
            "email": "faculty@example.com",
            "department": "CSE",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["employee_id"] == "EMP019"
    assert data["name"] == "API Test Faculty"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_faculty_duplicate_employee_id(client: AsyncClient):
    faculty = {
        "employee_id": "EMP020",
        "name": "API Test Faculty",
        "email": "faculty@example.com",
        "department": "CSE",
    }

    first_response = await client.post("/api/v1/faculty", json=faculty)

    assert first_response.status_code == 201

    second_response = await client.post("/api/v1/faculty", json=faculty)

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "Faculty with employee id 'EMP020' already exists"
    )


@pytest.mark.asyncio
async def test_get_faculty(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/faculty",
        json={
            "employee_id": "EMP021",
            "name": "API Get Faculty",
            "email": "api-get@example.com",
            "department": "CSE",
        },
    )

    assert create_response.status_code == 201

    faculty = create_response.json()

    response = await client.get(f"/api/v1/faculty/{faculty['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == faculty["id"]
    assert data["employee_id"] == "EMP021"


@pytest.mark.asyncio
async def test_get_faculty_not_found(client: AsyncClient):
    faculty_id = uuid.uuid4()

    response = await client.get(f"/api/v1/faculty/{faculty_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Faculty with id '{faculty_id}' was not found"
    }


@pytest.mark.asyncio
async def test_get_faculty_list(client: AsyncClient):
    await client.post(
        "/api/v1/faculty",
        json={
            "employee_id": "EMP022",
            "name": "Faculty One",
            "email": "faculty1@example.com",
            "department": "CSE",
        },
    )

    await client.post(
        "/api/v1/faculty",
        json={
            "employee_id": "EMP023",
            "name": "Faculty Two",
            "email": "faculty2@example.com",
            "department": "ECE",
        },
    )

    response = await client.get("/api/v1/faculty")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["offset"] == 0
    assert data["limit"] == 20


@pytest.mark.asyncio
async def test_get_faculty_pagination(client: AsyncClient):
    for index in range(3):
        response = await client.post(
            "/api/v1/faculty",
            json={
                "employee_id": f"EMP02{index + 4}",
                "name": f"Paginated Faculty {index}",
                "email": f"faculty{index}@example.com",
                "department": "CSE",
            },
        )

        assert response.status_code == 201

    response = await client.get("/api/v1/faculty?offset=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert data["offset"] == 1
    assert data["limit"] == 1


@pytest.mark.asyncio
async def test_update_faculty(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/faculty",
        json={
            "employee_id": "EMP027",
            "name": "Before Update",
            "email": "update-api@example.com",
            "department": "CSE",
        },
    )

    assert create_response.status_code == 201

    faculty = create_response.json()

    response = await client.patch(
        f"/api/v1/faculty/{faculty['id']}",
        json={
            "name": "After Update",
            "department": "ECE",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == faculty["id"]
    assert data["name"] == "After Update"
    assert data["department"] == "ECE"
    assert data["employee_id"] == "EMP027"


@pytest.mark.asyncio
async def test_update_faculty_not_found(client: AsyncClient):
    faculty_id = uuid.uuid4()

    response = await client.patch(
        f"/api/v1/faculty/{faculty_id}",
        json={
            "name": "Does Not Exist",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Faculty with id '{faculty_id}' was not found"
    }


@pytest.mark.asyncio
async def test_deactivate_faculty(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/faculty",
        json={
            "employee_id": "EMP028",
            "name": "Deactivate Test",
            "email": "deactivate@example.com",
            "department": "CSE",
        },
    )

    assert create_response.status_code == 201

    faculty = create_response.json()

    assert faculty["is_active"] is True

    response = await client.delete(f"/api/v1/faculty/{faculty['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == faculty["id"]
    assert data["employee_id"] == "EMP028"
    assert data["is_active"] is False


@pytest.mark.asyncio
async def test_deactivated_faculty_not_in_list(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/faculty",
        json={
            "employee_id": "EMP029",
            "name": "Inactive Faculty",
            "email": "inactive@example.com",
            "department": "CSE",
        },
    )

    assert create_response.status_code == 201

    faculty = create_response.json()

    delete_response = await client.delete(f"/api/v1/faculty/{faculty['id']}")

    assert delete_response.status_code == 200

    list_response = await client.get("/api/v1/faculty")

    assert list_response.status_code == 200

    data = list_response.json()

    employee_ids = [item["employee_id"] for item in data["items"]]

    assert "EMP029" not in employee_ids


@pytest.mark.asyncio
async def test_deactivate_faculty_not_found(client: AsyncClient):
    faculty_id = uuid.uuid4()

    response = await client.delete(f"/api/v1/faculty/{faculty_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Faculty with id '{faculty_id}' was not found"
    }
