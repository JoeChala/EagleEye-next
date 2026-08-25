from uuid import uuid4

import pytest

from app.exceptions.errors import DepartmentAlreadyExistsError, DepartmentNotFoundError
from app.features.departments.model import Department
from app.features.departments.service import DepartmentService


@pytest.mark.asyncio
async def test_create_department(db_session):
    service = DepartmentService(db_session)

    department = Department(
        code="CSE",
        name="Computer Science and Engineering",
    )

    result = await service.create_department(department)

    assert result.id is not None
    assert result.code == "CSE"


@pytest.mark.asyncio
async def test_duplicate_department_code(db_session):
    service = DepartmentService(db_session)

    await service.create_department(
        Department(code="ECE", name="Electronics and Communication Engineering")
    )

    with pytest.raises(DepartmentAlreadyExistsError):
        await service.create_department(
            Department(
                code="ECE",
                name="Duplicate Electronics and Communication Engineering",
            )
        )


@pytest.mark.asyncio
async def test_get_department(db_session):
    service = DepartmentService(db_session)

    department = await service.create_department(
        Department(code="ISE", name="Information Science and Engineering")
    )

    result = await service.get_department(department.id)

    assert result.id == department.id


@pytest.mark.asyncio
async def test_get_department_not_found(db_session):
    service = DepartmentService(db_session)

    department_id = uuid4()

    with pytest.raises(DepartmentNotFoundError):
        await service.get_department(department_id)


@pytest.mark.asyncio
async def test_list_departments(db_session):
    service = DepartmentService(db_session)

    await service.create_department(Department(code="CIV", name="Civil Engineering"))
    await service.create_department(Department(code="BIO", name="Biotechnology"))

    departments, total = await service.list_departments()

    assert total == 2
    assert len(departments) == 2


@pytest.mark.asyncio
async def test_update_department(db_session):
    service = DepartmentService(db_session)

    department = await service.create_department(
        Department(code="CHE", name="Chemical Engineering")
    )

    updated_department = await service.update_department(
        department.id,
        {"name": "Chemical and Electrochemical Engineering"},
    )

    assert updated_department.id == department.id
    assert updated_department.name == "Chemical and Electrochemical Engineering"


@pytest.mark.asyncio
async def test_update_department_not_found(db_session):
    service = DepartmentService(db_session)

    with pytest.raises(DepartmentNotFoundError):
        await service.update_department(uuid4(), {"name": "Missing"})


@pytest.mark.asyncio
async def test_deactivate_department(db_session):
    service = DepartmentService(db_session)

    department = await service.create_department(
        Department(code="MAT", name="Mathematics")
    )

    result = await service.deactivate_department(department.id)

    assert result.id == department.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_deactivate_department_not_found(db_session):
    service = DepartmentService(db_session)

    with pytest.raises(DepartmentNotFoundError):
        await service.deactivate_department(uuid4())


@pytest.mark.asyncio
async def test_deactivate_already_inactive_department(db_session):
    service = DepartmentService(db_session)

    department = await service.create_department(Department(code="PHY", name="Physics"))

    await service.deactivate_department(department.id)
    result = await service.deactivate_department(department.id)

    assert result.id == department.id
    assert result.is_active is False
