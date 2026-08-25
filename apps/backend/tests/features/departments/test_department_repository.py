import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.features.departments.model import Department
from app.features.departments.repository import DepartmentRepository


@pytest.mark.asyncio
async def test_create_department(db_session):
    repository = DepartmentRepository(db_session)

    department = Department(
        code="CSE",
        name="Computer Science and Engineering",
    )

    result = await repository.create(department)

    assert result.id is not None
    assert result.code == "CSE"


@pytest.mark.asyncio
async def test_get_department_by_id(db_session):
    repository = DepartmentRepository(db_session)

    department = await repository.create(
        Department(code="ECE", name="Electronics and Communication Engineering")
    )

    result = await repository.get_by_id(department.id)

    assert result is not None
    assert result.id == department.id


@pytest.mark.asyncio
async def test_get_department_by_id_not_found(db_session):
    repository = DepartmentRepository(db_session)

    result = await repository.get_by_id(uuid.uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_get_department_by_code(db_session):
    repository = DepartmentRepository(db_session)

    department = await repository.create(
        Department(code="ISE", name="Information Science and Engineering")
    )

    result = await repository.get_by_code("ISE")

    assert result is not None
    assert result.id == department.id


@pytest.mark.asyncio
async def test_get_department_by_code_not_found(db_session):
    repository = DepartmentRepository(db_session)

    result = await repository.get_by_code("UNKNOWN")

    assert result is None


@pytest.mark.asyncio
async def test_list_departments(db_session):
    repository = DepartmentRepository(db_session)

    await repository.create(
        Department(code="CSE", name="Computer Science and Engineering")
    )
    await repository.create(
        Department(code="ECE", name="Electronics and Communication Engineering")
    )

    departments = await repository.list()

    assert len(departments) == 2
    assert {department.code for department in departments} == {"CSE", "ECE"}


@pytest.mark.asyncio
async def test_list_departments_pagination(db_session):
    repository = DepartmentRepository(db_session)

    for index in range(3):
        await repository.create(
            Department(
                code=f"DPT{index}",
                name=f"Department {index}",
            )
        )

    departments = await repository.list(offset=1, limit=1)

    assert len(departments) == 1


@pytest.mark.asyncio
async def test_update_department(db_session):
    repository = DepartmentRepository(db_session)

    department = await repository.create(
        Department(code="MECH", name="Mechanical Engineering")
    )

    updated_department = await repository.update(
        department.id,
        {"name": "Mechanical and Manufacturing Engineering"},
    )

    assert updated_department is not None
    assert updated_department.id == department.id
    assert updated_department.name == "Mechanical and Manufacturing Engineering"


@pytest.mark.asyncio
async def test_deactivate_department(db_session):
    repository = DepartmentRepository(db_session)

    department = await repository.create(
        Department(code="CIV", name="Civil Engineering")
    )

    result = await repository.deactivate(department.id)

    assert result is not None
    assert result.id == department.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_list_excludes_inactive_departments(db_session):
    repository = DepartmentRepository(db_session)

    active_department = await repository.create(
        Department(code="BIO", name="Biotechnology")
    )
    inactive_department = await repository.create(
        Department(code="CHE", name="Chemical Engineering")
    )

    await repository.deactivate(inactive_department.id)

    departments = await repository.list()

    assert active_department.id in {department.id for department in departments}
    assert inactive_department.id not in {department.id for department in departments}


@pytest.mark.asyncio
async def test_duplicate_department_code_is_rejected_at_persistence_layer(db_session):
    repository = DepartmentRepository(db_session)

    await repository.create(Department(code="PHY", name="Physics"))

    with pytest.raises(IntegrityError):
        await repository.create(Department(code="PHY", name="Duplicate Physics"))

    await db_session.rollback()
