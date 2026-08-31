import pytest
from sqlalchemy.exc import IntegrityError

from app.features.enrollments.model import Enrollment


@pytest.mark.asyncio
async def test_create_enrollment(db_session, student, course):
    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    db_session.add(enrollment)
    await db_session.commit()
    await db_session.refresh(enrollment)

    assert enrollment.id is not None
    assert enrollment.student_id == student.id
    assert enrollment.course_id == course.id
    assert enrollment.is_active is True
    assert enrollment.enrolled_at is not None
    assert enrollment.created_at is not None
    assert enrollment.updated_at is not None


@pytest.mark.asyncio
async def test_duplicate_student_course_enrollment_is_rejected(
    db_session, student, course
):
    first = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    second = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    db_session.add(first)
    await db_session.commit()

    db_session.add(second)

    with pytest.raises(IntegrityError):
        await db_session.commit()

    await db_session.rollback()
