import uuid

import pytest

from app.features.students.repository import StudentRepository
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
async def test_get_student_by_id(db_session):
    repository = StudentRepository(db_session)
    student_details = Student(
        roll_number="TEST005",
        name="Student Creation Test",
        email="repository@example.com",
        department="CSE",
        semester=5,
        section="A",
    )
    student = await repository.create(student_details)

    test_student = await repository.get_by_id(student.id)

    assert test_student is not None
    assert test_student.id == student.id


@pytest.mark.asyncio
async def test_get_student_by_random_id(db_session):
    repository = StudentRepository(db_session)
    student = await repository.get_by_id(uuid.uuid4())

    assert student is None


@pytest.mark.asyncio
async def test_get_all_students(db_session):
    repository = StudentRepository(db_session)

    student1 = Student(
        roll_number="TEST006",
        name="Student One",
        email="student1@example.com",
        department="CSE",
        semester=5,
        section="A",
    )

    student2 = Student(
        roll_number="TEST007",
        name="Student Two",
        email="student2@example.com",
        department="CSE",
        semester=6,
        section="B",
    )

    await repository.create(student1)
    await repository.create(student2)

    students = await repository.get_all()

    roll_numbers = {student.roll_number for student in students}

    assert "TEST006" in roll_numbers
    assert "TEST007" in roll_numbers


@pytest.mark.asyncio
async def test_update_student(db_session):
    repository = StudentRepository(db_session)

    student = Student(
        roll_number="TEST008",
        name="Update Test",
        email="update@example.com",
        department="CSE",
        semester=5,
        section="A",
    )

    await repository.create(student)

    updated_student = await repository.update_by_id(
        student.id,
        {
            "name": "Updated Student",
            "semester": 6,
            "section": "B",
        },
    )

    assert updated_student is not None
    assert updated_student.id == student.id
    assert updated_student.name == "Updated Student"
    assert updated_student.semester == 6
    assert updated_student.section == "B"
    assert updated_student.roll_number == "TEST008"


@pytest.mark.asyncio
async def test_update_student_not_found(db_session):
    repository = StudentRepository(db_session)

    student = await repository.update_by_id(
        uuid.uuid4(),
        {"name": "Does Not Exist"},
    )

    assert student is None


@pytest.mark.asyncio
async def test_deactivate_student(db_session):
    repository = StudentRepository(db_session)

    student = Student(
        roll_number="TEST010",
        name="Deactivate Repository Test",
        email="deactivate-repo@example.com",
        department="CSE",
        semester=5,
        section="A",
    )

    await repository.create(student)

    result = await repository.deactivate(student.id)

    assert result is not None
    assert result.id == student.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_deactivate_student_not_found(db_session):
    repository = StudentRepository(db_session)

    result = await repository.deactivate(uuid.uuid4())

    assert result is None
