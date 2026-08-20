from uuid import uuid4

import pytest

from app.exceptions.student import StudentAlreadyExistsError, StudentNotFoundError
from app.features.students.service import StudentService
from app.models.student import Student


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


@pytest.mark.asyncio
async def test_get_student(db_session):
    service = StudentService(db_session)

    student = Student(
        roll_number="TEST006",
        name="Service Get Test",
        email="service-get@example.com",
        department="CSE",
        semester=5,
        section="A",
    )

    await service.register_student(student)

    result = await service.get_student(student.id)

    assert result.id == student.id
    assert result.roll_number == "TEST006"


@pytest.mark.asyncio
async def test_student_not_found_error(db_session):
    service = StudentService(db_session)

    student_id = uuid4()

    with pytest.raises(StudentNotFoundError) as exc_info:
        await service.get_student(student_id)

    assert str(exc_info.value) == (f"Student with id '{student_id}' was not found")
