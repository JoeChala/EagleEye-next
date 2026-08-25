import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.features.students.model import Student


@pytest.mark.asyncio
async def test_create_student(db_session, department):
    student = Student(
        roll_number="TEST001",
        name="Test Student",
        email="test@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    db_session.add(student)
    await db_session.flush()

    result = await db_session.execute(
        select(Student).where(Student.roll_number == "TEST001")
    )

    saved_student = result.scalar_one()

    assert saved_student.name == "Test Student"
    assert saved_student.roll_number == "TEST001"


@pytest.mark.asyncio
async def test_student_roll_number_must_be_unique(db_session, department):
    student = Student(
        roll_number="TEST002",
        name="Test Student",
        email="test@example.com",
        department_id=department.id,
        semester=7,
        section="A",
    )
    db_session.add(student)
    await db_session.flush()

    duplicate_student = Student(
        roll_number="TEST002",
        name="Test Student2",
        email="test2@example.com",
        department_id=department.id,
        semester=7,
        section="A",
    )
    db_session.add(duplicate_student)

    with pytest.raises(IntegrityError):
        await db_session.flush()

    await db_session.rollback()


@pytest.mark.asyncio
async def test_student_is_active_defaults_to_true(db_session, department):
    student = Student(
        roll_number="MODEL001",
        name="Default Active Test",
        email="model@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    db_session.add(student)
    await db_session.flush()
    await db_session.refresh(student)

    assert student.is_active is True
