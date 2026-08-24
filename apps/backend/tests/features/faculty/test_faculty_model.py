import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.features.faculty.model import Faculty


@pytest.mark.asyncio
async def test_create_faculty(db_session):
    faculty = Faculty(
        employee_id="EMP001",
        name="Test Faculty",
        email="faculty@example.com",
        department="CSE",
    )

    db_session.add(faculty)
    await db_session.flush()

    result = await db_session.execute(
        select(Faculty).where(Faculty.employee_id == "EMP001")
    )

    saved_faculty = result.scalar_one()

    assert saved_faculty.name == "Test Faculty"
    assert saved_faculty.employee_id == "EMP001"


@pytest.mark.asyncio
async def test_faculty_employee_id_must_be_unique(db_session):
    faculty = Faculty(
        employee_id="EMP002",
        name="Test Faculty",
        email="faculty@example.com",
        department="CSE",
    )
    db_session.add(faculty)
    await db_session.flush()

    duplicate_faculty = Faculty(
        employee_id="EMP002",
        name="Test Faculty 2",
        email="faculty2@example.com",
        department="ECE",
    )
    db_session.add(duplicate_faculty)

    with pytest.raises(IntegrityError):
        await db_session.flush()

    await db_session.rollback()


@pytest.mark.asyncio
async def test_faculty_is_active_defaults_to_true(db_session):
    faculty = Faculty(
        employee_id="EMP003",
        name="Active Faculty",
        email="active@example.com",
        department="CSE",
    )

    db_session.add(faculty)
    await db_session.flush()
    await db_session.refresh(faculty)

    assert faculty.is_active is True
