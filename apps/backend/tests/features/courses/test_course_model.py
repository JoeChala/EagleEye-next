import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.features.courses.model import Course


@pytest.mark.asyncio
async def test_create_course(db_session, department):
    course = Course(
        code="CS501",
        name="Database Management Systems",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    db_session.add(course)
    await db_session.flush()

    result = await db_session.execute(select(Course).where(Course.code == "CS501"))

    saved_course = result.scalar_one()

    assert saved_course.id is not None
    assert saved_course.code == "CS501"
    assert saved_course.name == "Database Management Systems"


@pytest.mark.asyncio
async def test_course_code_must_be_unique(db_session, department):
    course = Course(
        code="CS502",
        name="Operating Systems",
        department_id=department.id,
        semester=5,
        credits=4,
    )
    db_session.add(course)
    await db_session.flush()

    duplicate_course = Course(
        code="CS502",
        name="Computer Networks",
        department_id=department.id,
        semester=6,
        credits=3,
    )
    db_session.add(duplicate_course)

    with pytest.raises(IntegrityError):
        await db_session.flush()

    await db_session.rollback()


@pytest.mark.asyncio
async def test_course_is_active_defaults_to_true(db_session, department):
    course = Course(
        code="CS503",
        name="Algorithms",
        department_id=department.id,
        semester=5,
        credits=3,
    )

    db_session.add(course)
    await db_session.flush()
    await db_session.refresh(course)

    assert course.is_active is True


@pytest.mark.asyncio
async def test_course_timestamps_are_populated(db_session, department):
    course = Course(
        code="CS504",
        name="Software Engineering",
        department_id=department.id,
        semester=6,
        credits=3,
    )

    db_session.add(course)
    await db_session.flush()
    await db_session.refresh(course)

    assert course.created_at is not None
    assert course.updated_at is not None
