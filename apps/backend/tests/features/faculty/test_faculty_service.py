from uuid import uuid4

import pytest

from app.exceptions.errors import FacultyAlreadyExistsError, FacultyNotFoundError
from app.features.departments.model import Department
from app.features.faculty.model import Faculty
from app.features.faculty.service import FacultyService


@pytest.mark.asyncio
async def test_faculty_already_exists_error(db_session, department):
    service = FacultyService(db_session)

    faculty1 = Faculty(
        employee_id="EMP013",
        name="Faculty Error Test 1",
        email="repository@example.com",
        department_id=department.id,
    )

    await service.create_faculty(faculty1)

    faculty2 = Faculty(
        employee_id="EMP013",
        name="Faculty Error Test 2",
        email="repository2@example.com",
        department_id=department.id,
    )

    with pytest.raises(FacultyAlreadyExistsError):
        await service.create_faculty(faculty2)


@pytest.mark.asyncio
async def test_get_faculty(db_session, department):
    service = FacultyService(db_session)

    faculty = Faculty(
        employee_id="EMP014",
        name="Service Get Test",
        email="service-get@example.com",
        department_id=department.id,
    )

    await service.create_faculty(faculty)

    result = await service.get_faculty(faculty.id)

    assert result.id == faculty.id
    assert result.employee_id == "EMP014"


@pytest.mark.asyncio
async def test_faculty_not_found_error(db_session, department):
    service = FacultyService(db_session)

    faculty_id = uuid4()

    with pytest.raises(FacultyNotFoundError) as exc_info:
        await service.get_faculty(faculty_id)

    assert str(exc_info.value) == f"Faculty with id '{faculty_id}' was not found"


@pytest.mark.asyncio
async def test_update_faculty(db_session, department):
    service = FacultyService(db_session)

    faculty = Faculty(
        employee_id="EMP015",
        name="Service Update Test",
        email="service-update@example.com",
        department_id=department.id,
    )

    await service.create_faculty(faculty)

    updated_faculty = await service.update_faculty(
        faculty.id,
        {
            "name": "Updated Service Faculty",
            "department_id": str(department.id),
        },
    )

    assert updated_faculty.name == "Updated Service Faculty"
    assert updated_faculty.department_id == department.id
    assert updated_faculty.employee_id == "EMP015"


@pytest.mark.asyncio
async def test_update_faculty_not_found(db_session, department):
    service = FacultyService(db_session)

    faculty_id = uuid4()

    with pytest.raises(FacultyNotFoundError):
        await service.update_faculty(
            faculty_id,
            {"name": "Does Not Exist"},
        )


@pytest.mark.asyncio
async def test_deactivate_faculty(db_session, department):
    service = FacultyService(db_session)

    faculty = Faculty(
        employee_id="EMP016",
        name="Deactivate Service Test",
        email="deactivate-service@example.com",
        department_id=department.id,
    )

    await service.create_faculty(faculty)

    result = await service.deactivate_faculty(faculty.id)

    assert result.id == faculty.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_deactivate_faculty_not_found(db_session, department):
    service = FacultyService(db_session)

    faculty_id = uuid4()

    with pytest.raises(FacultyNotFoundError):
        await service.deactivate_faculty(faculty_id)


@pytest.mark.asyncio
async def test_list_faculty(db_session, department):
    service = FacultyService(db_session)
    ece_department = Department(
        code="ECE",
        name="Electronics and Communication Engineering",
    )
    db_session.add(ece_department)
    await db_session.commit()
    await db_session.refresh(ece_department)

    await service.create_faculty(
        Faculty(
            employee_id="EMP017",
            name="CSE Faculty",
            email="servicefilter1@example.com",
            department_id=department.id,
        )
    )

    await service.create_faculty(
        Faculty(
            employee_id="EMP018",
            name="ECE Faculty",
            email="servicefilter2@example.com",
            department_id=ece_department.id,
        )
    )

    faculties, total = await service.list_faculty()

    assert total == 2
    assert len(faculties) == 2
    assert {faculty.department_id for faculty in faculties} == {
        department.id,
        ece_department.id,
    }
