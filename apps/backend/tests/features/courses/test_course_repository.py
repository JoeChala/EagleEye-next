import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.features.courses.model import Course
from app.features.courses.repository import CourseRepository


@pytest.mark.asyncio
async def test_get_course_by_code(db_session, department):
    course = Course(
        code="CS505",
        name="Repository Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    db_session.add(course)
    await db_session.flush()

    repository = CourseRepository(db_session)

    result = await repository.get_by_code("CS505")

    assert result is not None
    assert result.code == "CS505"
    assert result.name == "Repository Test"


@pytest.mark.asyncio
async def test_get_course_by_code_not_found(db_session, department):
    repository = CourseRepository(db_session)

    result = await repository.get_by_code("DOES_NOT_EXIST")

    assert result is None


@pytest.mark.asyncio
async def test_create_course(db_session, department):
    repository = CourseRepository(db_session)
    course_details = Course(
        code="CS506",
        name="Course Creation Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )
    course = await repository.create(course_details)

    assert course.id is not None
    assert course.code == "CS506"


@pytest.mark.asyncio
async def test_get_course_by_id(db_session, department):
    repository = CourseRepository(db_session)
    course_details = Course(
        code="CS507",
        name="Course Get Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )
    course = await repository.create(course_details)

    test_course = await repository.get_by_id(course.id)

    assert test_course is not None
    assert test_course.id == course.id


@pytest.mark.asyncio
async def test_get_course_by_random_id(db_session, department):
    repository = CourseRepository(db_session)
    course = await repository.get_by_id(uuid.uuid4())

    assert course is None


@pytest.mark.asyncio
async def test_list_courses(db_session, department):
    repository = CourseRepository(db_session)

    course1 = Course(
        code="CS508",
        name="Course One",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    course2 = Course(
        code="CS509",
        name="Course Two",
        department_id=department.id,
        semester=6,
        credits=3,
    )

    await repository.create(course1)
    await repository.create(course2)

    courses = await repository.list()

    codes = {course.code for course in courses}

    assert "CS508" in codes
    assert "CS509" in codes


@pytest.mark.asyncio
async def test_list_courses_pagination(db_session, department):
    repository = CourseRepository(db_session)

    for index in range(3):
        await repository.create(
            Course(
                code=f"CS51{index}",
                name=f"Paged Course {index}",
                department_id=department.id,
                semester=5,
                credits=4,
            )
        )

    courses = await repository.list(offset=1, limit=1)

    assert len(courses) == 1


@pytest.mark.asyncio
async def test_update_course(db_session, department):
    repository = CourseRepository(db_session)

    course = Course(
        code="CS510",
        name="Update Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    await repository.create(course)

    updated_course = await repository.update(
        course.id,
        {
            "name": "Updated Course",
            "semester": 6,
            "credits": 5,
        },
    )

    assert updated_course is not None
    assert updated_course.id == course.id
    assert updated_course.name == "Updated Course"
    assert updated_course.semester == 6
    assert updated_course.credits == 5
    assert updated_course.code == "CS510"


@pytest.mark.asyncio
async def test_update_course_not_found(db_session, department):
    repository = CourseRepository(db_session)

    course = await repository.update(
        uuid.uuid4(),
        {"name": "Does Not Exist"},
    )

    assert course is None


@pytest.mark.asyncio
async def test_deactivate_course(db_session, department):
    repository = CourseRepository(db_session)

    course = Course(
        code="CS511",
        name="Deactivate Repository Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    await repository.create(course)

    result = await repository.deactivate(course.id)

    assert result is not None
    assert result.id == course.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_deactivate_course_not_found(db_session, department):
    repository = CourseRepository(db_session)

    result = await repository.deactivate(uuid.uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_excludes_inactive_courses(db_session, department):
    repository = CourseRepository(db_session)

    active_course = Course(
        code="CS512",
        name="Active Course",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    inactive_course = Course(
        code="CS513",
        name="Inactive Course",
        department_id=department.id,
        semester=6,
        credits=3,
    )

    await repository.create(active_course)
    await repository.create(inactive_course)
    await repository.deactivate(inactive_course.id)

    courses = await repository.list()

    codes = {course.code for course in courses}

    assert "CS512" in codes
    assert "CS513" not in codes


@pytest.mark.asyncio
async def test_duplicate_course_code_is_rejected_at_persistence_layer(
    db_session, department
):
    repository = CourseRepository(db_session)

    await repository.create(
        Course(
            code="CS514",
            name="First",
            department_id=department.id,
            semester=5,
            credits=4,
        )
    )

    with pytest.raises(IntegrityError):
        await repository.create(
            Course(
                code="CS514",
                name="Duplicate",
                department_id=department.id,
                semester=6,
                credits=3,
            )
        )

    await db_session.rollback()
