import uuid

import pytest

from app.features.faculty.model import Faculty
from app.features.faculty.repository import FacultyRepository


@pytest.mark.asyncio
async def test_get_faculty_by_employee_id(db_session):
    faculty = Faculty(
        employee_id="EMP004",
        name="Repository Test",
        email="repository@example.com",
        department="CSE",
    )

    db_session.add(faculty)
    await db_session.flush()

    repository = FacultyRepository(db_session)

    result = await repository.get_by_employee_id("EMP004")

    assert result is not None
    assert result.employee_id == "EMP004"
    assert result.name == "Repository Test"


@pytest.mark.asyncio
async def test_get_faculty_by_employee_id_not_found(db_session):
    repository = FacultyRepository(db_session)

    result = await repository.get_by_employee_id("DOES_NOT_EXIST")

    assert result is None


@pytest.mark.asyncio
async def test_create_faculty(db_session):
    repository = FacultyRepository(db_session)
    faculty_details = Faculty(
        employee_id="EMP005",
        name="Faculty Creation Test",
        email="repository@example.com",
        department="CSE",
    )
    faculty = await repository.create(faculty_details)

    assert faculty.id is not None
    assert faculty.employee_id == "EMP005"


@pytest.mark.asyncio
async def test_get_faculty_by_id(db_session):
    repository = FacultyRepository(db_session)
    faculty_details = Faculty(
        employee_id="EMP006",
        name="Faculty Get Test",
        email="repository@example.com",
        department="CSE",
    )
    faculty = await repository.create(faculty_details)

    test_faculty = await repository.get_by_id(faculty.id)

    assert test_faculty is not None
    assert test_faculty.id == faculty.id


@pytest.mark.asyncio
async def test_get_faculty_by_random_id(db_session):
    repository = FacultyRepository(db_session)
    faculty = await repository.get_by_id(uuid.uuid4())

    assert faculty is None


@pytest.mark.asyncio
async def test_list_faculty(db_session):
    repository = FacultyRepository(db_session)

    faculty1 = Faculty(
        employee_id="EMP007",
        name="Faculty One",
        email="faculty1@example.com",
        department="CSE",
    )

    faculty2 = Faculty(
        employee_id="EMP008",
        name="Faculty Two",
        email="faculty2@example.com",
        department="ECE",
    )

    await repository.create(faculty1)
    await repository.create(faculty2)

    faculties = await repository.list()

    employee_ids = {faculty.employee_id for faculty in faculties}

    assert "EMP007" in employee_ids
    assert "EMP008" in employee_ids


@pytest.mark.asyncio
async def test_update_faculty(db_session):
    repository = FacultyRepository(db_session)

    faculty = Faculty(
        employee_id="EMP009",
        name="Update Test",
        email="update@example.com",
        department="CSE",
    )

    await repository.create(faculty)

    updated_faculty = await repository.update(
        faculty.id,
        {
            "name": "Updated Faculty",
            "department": "ECE",
        },
    )

    assert updated_faculty is not None
    assert updated_faculty.id == faculty.id
    assert updated_faculty.name == "Updated Faculty"
    assert updated_faculty.department == "ECE"
    assert updated_faculty.employee_id == "EMP009"


@pytest.mark.asyncio
async def test_update_faculty_not_found(db_session):
    repository = FacultyRepository(db_session)

    faculty = await repository.update(
        uuid.uuid4(),
        {"name": "Does Not Exist"},
    )

    assert faculty is None


@pytest.mark.asyncio
async def test_deactivate_faculty(db_session):
    repository = FacultyRepository(db_session)

    faculty = Faculty(
        employee_id="EMP010",
        name="Deactivate Repository Test",
        email="deactivate-repo@example.com",
        department="CSE",
    )

    await repository.create(faculty)

    result = await repository.deactivate(faculty.id)

    assert result is not None
    assert result.id == faculty.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_deactivate_faculty_not_found(db_session):
    repository = FacultyRepository(db_session)

    result = await repository.deactivate(uuid.uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_excludes_inactive_faculty(db_session):
    repository = FacultyRepository(db_session)

    active_faculty = Faculty(
        employee_id="EMP011",
        name="Active Faculty",
        email="active@example.com",
        department="CSE",
    )

    inactive_faculty = Faculty(
        employee_id="EMP012",
        name="Inactive Faculty",
        email="inactive@example.com",
        department="ECE",
    )

    await repository.create(active_faculty)
    await repository.create(inactive_faculty)
    await repository.deactivate(inactive_faculty.id)

    faculties = await repository.list()

    employee_ids = {faculty.employee_id for faculty in faculties}

    assert "EMP011" in employee_ids
    assert "EMP012" not in employee_ids
