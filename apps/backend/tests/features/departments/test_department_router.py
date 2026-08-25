import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_department(client: AsyncClient):
    response = await client.post(
        "/api/v1/departments",
        json={
            "code": "CSE",
            "name": "Computer Science and Engineering",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["code"] == "CSE"
    assert data["name"] == "Computer Science and Engineering"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_department_duplicate_code(client: AsyncClient):
    department = {
        "code": "ECE",
        "name": "Electronics and Communication Engineering",
    }

    first_response = await client.post("/api/v1/departments", json=department)

    assert first_response.status_code == 201

    second_response = await client.post("/api/v1/departments", json=department)

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"] == "Department with code 'ECE' already exists"
    )


@pytest.mark.asyncio
async def test_get_department_list(client: AsyncClient):
    await client.post(
        "/api/v1/departments",
        json={
            "code": "CIV",
            "name": "Civil Engineering",
        },
    )
    await client.post(
        "/api/v1/departments",
        json={
            "code": "BIO",
            "name": "Biotechnology",
        },
    )

    response = await client.get("/api/v1/departments")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["offset"] == 0
    assert data["limit"] == 20


@pytest.mark.asyncio
async def test_get_department_by_id(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/departments",
        json={
            "code": "MAT",
            "name": "Mathematics",
        },
    )

    assert create_response.status_code == 201

    department = create_response.json()

    response = await client.get(f"/api/v1/departments/{department['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == department["id"]


@pytest.mark.asyncio
async def test_get_department_not_found(client: AsyncClient):
    department_id = uuid.uuid4()

    response = await client.get(f"/api/v1/departments/{department_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Department with id '{department_id}' was not found"
    }


@pytest.mark.asyncio
async def test_update_department(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/departments",
        json={
            "code": "PHY",
            "name": "Physics",
        },
    )

    department = create_response.json()

    response = await client.patch(
        f"/api/v1/departments/{department['id']}",
        json={
            "name": "Applied Physics",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == department["id"]
    assert data["name"] == "Applied Physics"


@pytest.mark.asyncio
async def test_update_department_not_found(client: AsyncClient):
    department_id = uuid.uuid4()

    response = await client.patch(
        f"/api/v1/departments/{department_id}",
        json={
            "name": "Missing",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Department with id '{department_id}' was not found"
    }


@pytest.mark.asyncio
async def test_deactivate_department(client: AsyncClient):
    create_response = await client.post(
        "/api/v1/departments",
        json={
            "code": "CHE",
            "name": "Chemical Engineering",
        },
    )

    department = create_response.json()

    response = await client.delete(f"/api/v1/departments/{department['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == department["id"]
    assert data["is_active"] is False


@pytest.mark.asyncio
async def test_deactivate_department_not_found(client: AsyncClient):
    department_id = uuid.uuid4()

    response = await client.delete(f"/api/v1/departments/{department_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Department with id '{department_id}' was not found"
    }


@pytest.mark.asyncio
async def test_create_department_validation_error(client: AsyncClient):
    response = await client.post(
        "/api/v1/departments",
        json={
            "code": "",
            "name": "",
        },
    )

    assert response.status_code == 422
