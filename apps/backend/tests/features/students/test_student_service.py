from uuid import uuid4

import pytest

from app.exceptions.errors import StudentAlreadyExistsError, StudentNotFoundError
from app.features.students.model import Student
from app.features.students.service import StudentService


@pytest.mark.asyncio
async def test_student_already_exists_error(db_session, department):
    service = StudentService(db_session)

    student1 = Student(
        roll_number="TEST005",
        name="Student Error Test 1",
        email="repository@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    await service.register_student(student1)

    student2 = Student(
        roll_number="TEST005",
        name="Student Error Test 2",
        email="repository2@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    with pytest.raises(StudentAlreadyExistsError):
        await service.register_student(student2)


@pytest.mark.asyncio
async def test_get_student(db_session, department):
    service = StudentService(db_session)

    student = Student(
        roll_number="TEST006",
        name="Service Get Test",
        email="service-get@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    await service.register_student(student)

    result = await service.get_student(student.id)

    assert result.id == student.id
    assert result.roll_number == "TEST006"


@pytest.mark.asyncio
async def test_student_not_found_error(db_session, department):
    service = StudentService(db_session)

    student_id = uuid4()

    with pytest.raises(StudentNotFoundError) as exc_info:
        await service.get_student(student_id)

    assert str(exc_info.value) == (f"Student with id '{student_id}' was not found")


@pytest.mark.asyncio
async def test_update_student(db_session, department):
    service = StudentService(db_session)

    student = Student(
        roll_number="TEST009",
        name="Service Update Test",
        email="service-update@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    await service.register_student(student)

    updated_student = await service.update_student(
        student.id,
        {
            "name": "Updated Service Student",
            "section": "B",
        },
    )

    assert updated_student.name == "Updated Service Student"
    assert updated_student.section == "B"
    assert updated_student.roll_number == "TEST009"


@pytest.mark.asyncio
async def test_update_student_not_found(db_session, department):
    service = StudentService(db_session)

    student_id = uuid4()

    with pytest.raises(StudentNotFoundError):
        await service.update_student(
            student_id,
            {"name": "Does Not Exist"},
        )


@pytest.mark.asyncio
async def test_deactivate_student(db_session, department):
    service = StudentService(db_session)

    student = Student(
        roll_number="TEST011",
        name="Deactivate Service Test",
        email="deactivate-service@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    await service.register_student(student)

    result = await service.deactivate_student(student.id)

    assert result.id == student.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_deactivate_student_not_found(db_session, department):
    service = StudentService(db_session)

    student_id = uuid4()

    with pytest.raises(StudentNotFoundError):
        await service.deactivate_student(student_id)


@pytest.mark.asyncio
async def test_get_students_with_filters(
    db_session,
    department,
    department_factory,
):
    service = StudentService(db_session)
    ece_department = await department_factory(
        code="ECE",
        name="Electronics and Communication Engineering",
    )

    await service.register_student(
        Student(
            roll_number="SERVICEFILTER001",
            name="CSE Student",
            email="servicefilter1@example.com",
            department_id=department.id,
            semester=5,
            section="A",
        )
    )

    await service.register_student(
        Student(
            roll_number="SERVICEFILTER002",
            name="ECE Student",
            email="servicefilter2@example.com",
            department_id=ece_department.id,
            semester=5,
            section="A",
        )
    )

    students, total = await service.get_students(
        department_id=department.id,
    )

    assert total == 1
    assert len(students) == 1
    assert students[0].department_id == department.id
