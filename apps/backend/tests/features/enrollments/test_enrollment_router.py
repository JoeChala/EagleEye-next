from uuid import uuid4

import pytest
from httpx import AsyncClient

BASE_URL = "/api/v1/enrollments"


@pytest.mark.asyncio
async def test_create_enrollment(
    client: AsyncClient,
    student,
    course,
):
    response = await client.post(
        BASE_URL,
        json={
            "student_id": str(student.id),
            "course_id": str(course.id),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["student_id"] == str(student.id)
    assert data["course_id"] == str(course.id)
    assert data["is_active"] is True
    assert data["enrolled_at"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


@pytest.mark.asyncio
async def test_create_enrollment_student_not_found(
    client: AsyncClient,
    course,
):
    student_id = uuid4()

    response = await client.post(
        BASE_URL,
        json={
            "student_id": str(student_id),
            "course_id": str(course.id),
        },
    )

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == (f"Student with id '{student_id}' was not found")


@pytest.mark.asyncio
async def test_create_enrollment_course_not_found(
    client: AsyncClient,
    student,
):
    course_id = uuid4()

    response = await client.post(
        BASE_URL,
        json={
            "student_id": str(student.id),
            "course_id": str(course_id),
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == (f"Course with id '{course_id}' was not found")


@pytest.mark.asyncio
async def test_create_duplicate_enrollment(
    client: AsyncClient,
    student,
    course,
):
    payload = {
        "student_id": str(student.id),
        "course_id": str(course.id),
    }

    first_response = await client.post(
        BASE_URL,
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        BASE_URL,
        json=payload,
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["detail"] == (
        f"Student '{student.id}' is already enrolled in course '{course.id}'"
    )


@pytest.mark.asyncio
async def test_get_enrollment(
    client: AsyncClient,
    student,
    course,
):
    create_response = await client.post(
        BASE_URL,
        json={
            "student_id": str(student.id),
            "course_id": str(course.id),
        },
    )

    assert create_response.status_code == 201

    enrollment_id = create_response.json()["id"]

    response = await client.get(
        f"{BASE_URL}/{enrollment_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == enrollment_id
    assert data["student_id"] == str(student.id)
    assert data["course_id"] == str(course.id)
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_get_enrollment_not_found(
    client: AsyncClient,
):
    enrollment_id = uuid4()

    response = await client.get(
        f"{BASE_URL}/{enrollment_id}",
    )

    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == (f"Enrollment with id '{enrollment_id}' was not found")


@pytest.mark.asyncio
async def test_list_student_enrollments(
    client: AsyncClient,
    student,
    course,
):
    create_response = await client.post(
        BASE_URL,
        json={
            "student_id": str(student.id),
            "course_id": str(course.id),
        },
    )

    assert create_response.status_code == 201

    response = await client.get(
        f"{BASE_URL}/student/{student.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["records"]) == 1

    enrollment = data["records"][0]

    assert enrollment["student_id"] == str(student.id)
    assert enrollment["course_id"] == str(course.id)


@pytest.mark.asyncio
async def test_list_student_enrollments_student_not_found(
    client: AsyncClient,
):
    student_id = uuid4()

    response = await client.get(
        f"{BASE_URL}/student/{student_id}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == (f"Student with id '{student_id}' was not found")


@pytest.mark.asyncio
async def test_list_course_enrollments(
    client: AsyncClient,
    student,
    course,
):
    create_response = await client.post(
        BASE_URL,
        json={
            "student_id": str(student.id),
            "course_id": str(course.id),
        },
    )

    assert create_response.status_code == 201

    response = await client.get(
        f"{BASE_URL}/course/{course.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["records"]) == 1

    enrollment = data["records"][0]

    assert enrollment["student_id"] == str(student.id)
    assert enrollment["course_id"] == str(course.id)


@pytest.mark.asyncio
async def test_list_course_enrollments_course_not_found(
    client: AsyncClient,
):
    course_id = uuid4()

    response = await client.get(
        f"{BASE_URL}/course/{course_id}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == (f"Course with id '{course_id}' was not found")


@pytest.mark.asyncio
async def test_deactivate_enrollment(
    client: AsyncClient,
    student,
    course,
):
    create_response = await client.post(
        BASE_URL,
        json={
            "student_id": str(student.id),
            "course_id": str(course.id),
        },
    )

    assert create_response.status_code == 201

    enrollment_id = create_response.json()["id"]

    response = await client.delete(
        f"{BASE_URL}/{enrollment_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == enrollment_id
    assert data["student_id"] == str(student.id)
    assert data["course_id"] == str(course.id)
    assert data["is_active"] is False


@pytest.mark.asyncio
async def test_deactivate_enrollment_not_found(
    client: AsyncClient,
):
    enrollment_id = uuid4()

    response = await client.delete(
        f"{BASE_URL}/{enrollment_id}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == (f"Enrollment with id '{enrollment_id}' was not found")
