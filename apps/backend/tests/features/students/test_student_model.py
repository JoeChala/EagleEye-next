import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.student import Student


@pytest.mark.asyncio
async def test_create_student(db_session):
    student = Student(
        roll_number="TEST001",
        name="Test Student",
        email="test@example.com",
        department="CSE",
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
async def test_student_roll_number_must_be_unique(db_session):
    student = Student(
        roll_number="TEST002",
        name="Test Student",
        email="test@example.com",
        department="CSE",
        semester=7,
        section="A",
    )
    db_session.add(student)
    await db_session.flush()

    duplicate_student = Student(
        roll_number="TEST002",
        name="Test Student2",
        email="test2@example.com",
        department="ISE",
        semester=7,
        section="A",
    )
    db_session.add(duplicate_student)

    with pytest.raises(IntegrityError):
        await db_session.flush()

    await db_session.rollback()
