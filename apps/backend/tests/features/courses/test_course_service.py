from uuid import uuid4

import pytest

from app.exceptions.errors import CourseAlreadyExistsError, CourseNotFoundError
from app.features.courses.model import Course
from app.features.courses.service import CourseService


@pytest.mark.asyncio
async def test_course_already_exists_error(db_session, department):
    service = CourseService(db_session)

    course1 = Course(
        code="CS515",
        name="Course Error Test 1",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    await service.create_course(course1)

    course2 = Course(
        code="CS515",
        name="Course Error Test 2",
        department_id=department.id,
        semester=6,
        credits=3,
    )

    with pytest.raises(CourseAlreadyExistsError):
        await service.create_course(course2)


@pytest.mark.asyncio
async def test_get_course(db_session, department):
    service = CourseService(db_session)

    course = Course(
        code="CS516",
        name="Service Get Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    await service.create_course(course)

    result = await service.get_course(course.id)

    assert result.id == course.id
    assert result.code == "CS516"


@pytest.mark.asyncio
async def test_course_not_found_error(db_session, department):
    service = CourseService(db_session)

    course_id = uuid4()

    with pytest.raises(CourseNotFoundError) as exc_info:
        await service.get_course(course_id)

    assert str(exc_info.value) == f"Course with id '{course_id}' was not found"


@pytest.mark.asyncio
async def test_list_courses(db_session, department):
    service = CourseService(db_session)

    await service.create_course(
        Course(
            code="CS517",
            name="CSE Course",
            department_id=department.id,
            semester=5,
            credits=4,
        )
    )

    await service.create_course(
        Course(
            code="CS518",
            name="ECE Course",
            department_id=department.id,
            semester=6,
            credits=3,
        )
    )

    courses, total = await service.list_courses()

    assert total == 2
    assert len(courses) == 2
    assert {course.code for course in courses} == {"CS517", "CS518"}


@pytest.mark.asyncio
async def test_update_course(db_session, department):
    service = CourseService(db_session)

    course = Course(
        code="CS519",
        name="Service Update Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    await service.create_course(course)

    updated_course = await service.update_course(
        course.id,
        {
            "name": "Updated Service Course",
            "credits": 5,
        },
    )

    assert updated_course.name == "Updated Service Course"
    assert updated_course.credits == 5
    assert updated_course.code == "CS519"


@pytest.mark.asyncio
async def test_update_course_not_found(db_session, department):
    service = CourseService(db_session)

    course_id = uuid4()

    with pytest.raises(CourseNotFoundError):
        await service.update_course(
            course_id,
            {"name": "Does Not Exist"},
        )


@pytest.mark.asyncio
async def test_deactivate_course(db_session, department):
    service = CourseService(db_session)

    course = Course(
        code="CS520",
        name="Deactivate Service Test",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    await service.create_course(course)

    result = await service.deactivate_course(course.id)

    assert result.id == course.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_deactivate_course_not_found(db_session, department):
    service = CourseService(db_session)

    course_id = uuid4()

    with pytest.raises(CourseNotFoundError):
        await service.deactivate_course(course_id)


@pytest.mark.asyncio
async def test_deactivate_already_inactive_course(db_session, department):
    service = CourseService(db_session)

    course = Course(
        code="CS521",
        name="Already Inactive",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    await service.create_course(course)
    await service.deactivate_course(course.id)

    result = await service.deactivate_course(course.id)

    assert result.id == course.id
    assert result.is_active is False
