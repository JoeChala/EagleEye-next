import uuid

import pytest

from app.features.students.model import Student
from app.features.students.repository import StudentRepository


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


@pytest.mark.asyncio
async def test_get_students_by_department(db_session):
    repository = StudentRepository(db_session)

    await repository.create(
        Student(
            roll_number="FILTER001",
            name="CSE Student",
            email="filter1@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.create(
        Student(
            roll_number="FILTER002",
            name="ECE Student",
            email="filter2@example.com",
            department="ECE",
            semester=5,
            section="A",
        )
    )

    students = await repository.get_all(
        department="CSE",
    )

    assert len(students) == 1
    assert students[0].roll_number == "FILTER001"


@pytest.mark.asyncio
async def test_get_students_by_semester(db_session):
    repository = StudentRepository(db_session)

    await repository.create(
        Student(
            roll_number="FILTER003",
            name="Semester Five",
            email="filter3@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.create(
        Student(
            roll_number="FILTER004",
            name="Semester Six",
            email="filter4@example.com",
            department="CSE",
            semester=6,
            section="A",
        )
    )

    students = await repository.get_all(
        semester=5,
    )

    assert len(students) == 1
    assert students[0].semester == 5


@pytest.mark.asyncio
async def test_get_students_by_section(db_session):
    repository = StudentRepository(db_session)

    await repository.create(
        Student(
            roll_number="FILTER005",
            name="Section A",
            email="filter5@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.create(
        Student(
            roll_number="FILTER006",
            name="Section B",
            email="filter6@example.com",
            department="CSE",
            semester=5,
            section="B",
        )
    )

    students = await repository.get_all(
        section="A",
    )

    assert len(students) == 1
    assert students[0].roll_number == "FILTER005"


@pytest.mark.asyncio
async def test_get_students_with_multiple_filters(db_session):
    repository = StudentRepository(db_session)

    await repository.create(
        Student(
            roll_number="FILTER007",
            name="Matching Student",
            email="filter7@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.create(
        Student(
            roll_number="FILTER008",
            name="Wrong Semester",
            email="filter8@example.com",
            department="CSE",
            semester=6,
            section="A",
        )
    )

    await repository.create(
        Student(
            roll_number="FILTER009",
            name="Wrong Department",
            email="filter9@example.com",
            department="ECE",
            semester=5,
            section="A",
        )
    )

    students = await repository.get_all(
        department="CSE",
        semester=5,
        section="A",
    )

    assert len(students) == 1
    assert students[0].roll_number == "FILTER007"


@pytest.mark.asyncio
async def test_get_students_with_no_matches(db_session):
    repository = StudentRepository(db_session)

    await repository.create(
        Student(
            roll_number="FILTER010",
            name="CSE Student",
            email="filter10@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    students = await repository.get_all(
        department="MECH",
    )

    assert students == []


@pytest.mark.asyncio
async def test_get_students_excludes_inactive_students(
    db_session,
):
    repository = StudentRepository(db_session)

    student = await repository.create(
        Student(
            roll_number="FILTER011",
            name="Inactive Student",
            email="filter11@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.deactivate(student.id)

    students = await repository.get_all(
        department="CSE",
    )

    assert all(student.roll_number != "FILTER011" for student in students)


@pytest.mark.asyncio
async def test_count_students_by_department(db_session):
    repository = StudentRepository(db_session)

    await repository.create(
        Student(
            roll_number="COUNT001",
            name="CSE Student 1",
            email="count1@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.create(
        Student(
            roll_number="COUNT002",
            name="CSE Student 2",
            email="count2@example.com",
            department="CSE",
            semester=6,
            section="B",
        )
    )

    await repository.create(
        Student(
            roll_number="COUNT003",
            name="ECE Student",
            email="count3@example.com",
            department="ECE",
            semester=5,
            section="A",
        )
    )

    count = await repository.count(
        department="CSE",
    )

    assert count == 2


@pytest.mark.asyncio
async def test_count_students_with_multiple_filters(
    db_session,
):
    repository = StudentRepository(db_session)

    await repository.create(
        Student(
            roll_number="COUNT004",
            name="Matching",
            email="count4@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.create(
        Student(
            roll_number="COUNT005",
            name="Wrong Section",
            email="count5@example.com",
            department="CSE",
            semester=5,
            section="B",
        )
    )

    count = await repository.count(
        department="CSE",
        semester=5,
        section="A",
    )

    assert count == 1


@pytest.mark.asyncio
async def test_count_excludes_inactive_students(
    db_session,
):
    repository = StudentRepository(db_session)

    student = await repository.create(
        Student(
            roll_number="COUNT006",
            name="Inactive",
            email="count6@example.com",
            department="CSE",
            semester=5,
            section="A",
        )
    )

    await repository.deactivate(student.id)

    count = await repository.count(
        department="CSE",
    )

    assert count == 0
