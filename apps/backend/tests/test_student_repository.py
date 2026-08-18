import pytest

from app.exceptions.student import StudentAlreadyExistsError
from app.features.students.repository import StudentRepository
from app.features.students.service import StudentService
from app.models.student import Student


@pytest.mark.asyncio
async def test_get_student_by_roll_number(db_session):
    student = Student(
        roll_number="TEST003",
        name="Repository Test",
        email="repository@example.com",
        department="CSE",
        semester=5,
        section="A",
    )

    db_session.add(student)
    await db_session.flush()

    repository = StudentRepository(db_session)

    result = await repository.get_by_roll_number("TEST003")

    assert result is not None
    assert result.roll_number == "TEST003"
    assert result.name == "Repository Test"


@pytest.mark.asyncio
async def test_get_student_by_roll_number_not_found(db_session):
    repository = StudentRepository(db_session)

    result = await repository.get_by_roll_number("DOES_NOT_EXIST")

    assert result is None


@pytest.mark.asyncio
async def test_create_student(db_session):
    repository = StudentRepository(db_session)
    student_details = Student(
        roll_number="TEST004",
        name="Student Creation Test",
        email="repository@example.com",
        department="CSE",
        semester=5,
        section="A",
    )
    student = await repository.create(student_details)

    assert student.id is not None
    assert student.roll_number == "TEST004"


@pytest.mark.asyncio
async def test_student_already_exists_error(db_session):
    service = StudentService(db_session)

    student1 = Student(
        roll_number="TEST005",
        name="Student Error Test 1",
        email="repository@example.com",
        department="CSE",
        semester=5,
        section="A",
    )

    await service.register_student(student1)

    student2 = Student(
        roll_number="TEST005",
        name="Student Error Test 2",
        email="repository2@example.com",
        department="CSE",
        semester=5,
        section="A",
    )

    with pytest.raises(StudentAlreadyExistsError):
        await service.register_student(student2)
