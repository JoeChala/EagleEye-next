import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.features.departments.model import Department


@pytest.mark.asyncio
async def test_create_department(db_session):
    department = Department(
        code="CSE",
        name="Computer Science and Engineering",
    )

    db_session.add(department)
    await db_session.flush()

    result = await db_session.execute(
        select(Department).where(Department.code == "CSE")
    )

    saved_department = result.scalar_one()

    assert saved_department.id is not None
    assert saved_department.code == "CSE"
    assert saved_department.name == "Computer Science and Engineering"


@pytest.mark.asyncio
async def test_department_code_must_be_unique(db_session):
    department = Department(code="ECE", name="Electronics and Communication")
    db_session.add(department)
    await db_session.flush()

    duplicate_department = Department(
        code="ECE",
        name="Duplicate Electronics and Communication",
    )
    db_session.add(duplicate_department)

    with pytest.raises(IntegrityError):
        await db_session.flush()

    await db_session.rollback()


@pytest.mark.asyncio
async def test_department_is_active_defaults_to_true(db_session):
    department = Department(code="ISE", name="Information Science and Engineering")

    db_session.add(department)
    await db_session.flush()
    await db_session.refresh(department)

    assert department.is_active is True


@pytest.mark.asyncio
async def test_department_timestamps_are_populated(db_session):
    department = Department(code="MECH", name="Mechanical Engineering")

    db_session.add(department)
    await db_session.flush()
    await db_session.refresh(department)

    assert department.created_at is not None
    assert department.updated_at is not None
