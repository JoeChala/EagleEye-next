import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_course(client: AsyncClient, department):
    response = await client.post(
        "/api/v1/courses",
        json={
            "code": "CS522",
            "name": "API Test Course",
            "department_id": str(department.id),
            "semester": 5,
            "credits": 4,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["code"] == "CS522"
    assert data["name"] == "API Test Course"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_course_duplicate_code(client: AsyncClient, department):
    course = {
        "code": "CS523",
        "name": "API Test Course",
        "department_id": str(department.id),
        "semester": 5,
        "credits": 4,
    }

    first_response = await client.post("/api/v1/courses", json=course)

    assert first_response.status_code == 201

    second_response = await client.post("/api/v1/courses", json=course)

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Course with code 'CS523' already exists"


@pytest.mark.asyncio
async def test_get_course(client: AsyncClient, department):
    create_response = await client.post(
        "/api/v1/courses",
        json={
            "code": "CS524",
            "name": "API Get Course",
            "department_id": str(department.id),
            "semester": 5,
            "credits": 4,
        },
    )

    assert create_response.status_code == 201

    course = create_response.json()

    response = await client.get(f"/api/v1/courses/{course['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == course["id"]
    assert data["code"] == "CS524"


@pytest.mark.asyncio
async def test_get_course_not_found(client: AsyncClient, department):
    course_id = uuid.uuid4()

    response = await client.get(f"/api/v1/courses/{course_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Course with id '{course_id}' was not found"}


@pytest.mark.asyncio
async def test_get_courses(client: AsyncClient, department):
    await client.post(
        "/api/v1/courses",
        json={
            "code": "CS525",
            "name": "Course One",
            "department_id": str(department.id),
            "semester": 5,
            "credits": 4,
        },
    )

    await client.post(
        "/api/v1/courses",
        json={
            "code": "CS526",
            "name": "Course Two",
            "department_id": str(department.id),
            "semester": 6,
            "credits": 3,
        },
    )

    response = await client.get("/api/v1/courses")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["offset"] == 0
    assert data["limit"] == 20


@pytest.mark.asyncio
async def test_get_courses_pagination(client: AsyncClient, department):
    for index in range(3):
        response = await client.post(
            "/api/v1/courses",
            json={
                "code": f"CS52{index + 7}",
                "name": f"Paged Course {index}",
                "department_id": str(department.id),
                "semester": 5,
                "credits": 4,
            },
        )

        assert response.status_code == 201

    response = await client.get("/api/v1/courses?offset=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert data["offset"] == 1
    assert data["limit"] == 1


@pytest.mark.asyncio
async def test_update_course(client: AsyncClient, department):
    create_response = await client.post(
        "/api/v1/courses",
        json={
            "code": "CS530",
            "name": "Before Update",
            "department_id": str(department.id),
            "semester": 5,
            "credits": 4,
        },
    )

    assert create_response.status_code == 201

    course = create_response.json()

    response = await client.patch(
        f"/api/v1/courses/{course['id']}",
        json={
            "name": "After Update",
            "credits": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == course["id"]
    assert data["name"] == "After Update"
    assert data["credits"] == 5
    assert data["code"] == "CS530"


@pytest.mark.asyncio
async def test_update_course_not_found(client: AsyncClient, department):
    course_id = uuid.uuid4()

    response = await client.patch(
        f"/api/v1/courses/{course_id}",
        json={
            "name": "Does Not Exist",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": f"Course with id '{course_id}' was not found"}


@pytest.mark.asyncio
async def test_deactivate_course(client: AsyncClient, department):
    create_response = await client.post(
        "/api/v1/courses",
        json={
            "code": "CS531",
            "name": "Deactivate Test",
            "department_id": str(department.id),
            "semester": 5,
            "credits": 4,
        },
    )

    assert create_response.status_code == 201

    course = create_response.json()

    assert course["is_active"] is True

    response = await client.delete(f"/api/v1/courses/{course['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == course["id"]
    assert data["code"] == "CS531"
    assert data["is_active"] is False


@pytest.mark.asyncio
async def test_deactivated_course_not_in_list(client: AsyncClient, department):
    create_response = await client.post(
        "/api/v1/courses",
        json={
            "code": "CS532",
            "name": "Inactive Course",
            "department_id": str(department.id),
            "semester": 5,
            "credits": 4,
        },
    )

    assert create_response.status_code == 201

    course = create_response.json()

    delete_response = await client.delete(f"/api/v1/courses/{course['id']}")

    assert delete_response.status_code == 200

    list_response = await client.get("/api/v1/courses")

    assert list_response.status_code == 200

    data = list_response.json()

    codes = [item["code"] for item in data["items"]]

    assert "CS532" not in codes


@pytest.mark.asyncio
async def test_deactivate_course_not_found(client: AsyncClient, department):
    course_id = uuid.uuid4()

    response = await client.delete(f"/api/v1/courses/{course_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Course with id '{course_id}' was not found"}


@pytest.mark.asyncio
async def test_create_course_invalid_payload_returns_validation_error(
    client: AsyncClient,
    department,
):
    response = await client.post(
        "/api/v1/courses",
        json={
            "code": "",
            "name": "",
            "department_id": "",
            "semester": "invalid",
            "credits": "invalid",
        },
    )

    assert response.status_code == 422
