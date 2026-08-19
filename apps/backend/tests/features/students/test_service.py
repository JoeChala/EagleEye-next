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
async def test_student_not_found_error(db_session):
    service = StudentService(db_session)
    with pytest.raises(StudentNotFoundError):
        await service.get_student(uuid4())
