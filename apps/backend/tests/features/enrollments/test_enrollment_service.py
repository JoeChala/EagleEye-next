from uuid import uuid4

import pytest

from app.exceptions.errors import (
    CourseNotFoundError,
    EnrollmentAlreadyExistsError,
    EnrollmentNotFoundError,
    InvalidEnrollmentError,
    StudentNotFoundError,
)
from app.features.courses.model import Course
from app.features.enrollments.service import EnrollmentService


@pytest.mark.asyncio
async def test_create_enrollment(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    result = await service.create_enrollment(
        student.id,
        course.id,
    )

    assert result.id is not None
    assert result.student_id == student.id
    assert result.course_id == course.id
    assert result.is_active is True


@pytest.mark.asyncio
async def test_create_enrollment_student_not_found(
    db_session,
    course,
):
    service = EnrollmentService(db_session)

    with pytest.raises(StudentNotFoundError):
        await service.create_enrollment(
            uuid4(),
            course.id,
        )


@pytest.mark.asyncio
async def test_create_enrollment_course_not_found(
    db_session,
    student,
):
    service = EnrollmentService(db_session)

    with pytest.raises(CourseNotFoundError):
        await service.create_enrollment(
            student.id,
            uuid4(),
        )


@pytest.mark.asyncio
async def test_create_duplicate_enrollment(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    await service.create_enrollment(
        student.id,
        course.id,
    )

    with pytest.raises(EnrollmentAlreadyExistsError):
        await service.create_enrollment(
            student.id,
            course.id,
        )


@pytest.mark.asyncio
async def test_get_enrollment(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    created = await service.create_enrollment(
        student.id,
        course.id,
    )

    result = await service.get_enrollment(created.id)

    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_enrollment_not_found(
    db_session,
):
    service = EnrollmentService(db_session)

    with pytest.raises(EnrollmentNotFoundError):
        await service.get_enrollment(uuid4())


@pytest.mark.asyncio
async def test_get_student_enrollment(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    created = await service.create_enrollment(
        student.id,
        course.id,
    )

    result = await service.get_student_enrollment(
        student.id,
        course.id,
    )

    assert result.id == created.id


@pytest.mark.asyncio
async def test_list_student_enrollments(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    await service.create_enrollment(
        student.id,
        course.id,
    )

    enrollments, total = await service.list_student_enrollments(
        student.id,
    )

    assert total == 1
    assert len(enrollments) == 1
    assert enrollments[0].student_id == student.id


@pytest.mark.asyncio
async def test_list_course_enrollments(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    await service.create_enrollment(
        student.id,
        course.id,
    )

    enrollments, total = await service.list_course_enrollments(
        course.id,
    )

    assert total == 1
    assert len(enrollments) == 1
    assert enrollments[0].course_id == course.id


@pytest.mark.asyncio
async def test_deactivate_enrollment(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    created = await service.create_enrollment(
        student.id,
        course.id,
    )

    result = await service.deactivate_enrollment(
        created.id,
    )

    assert result.is_active is False


@pytest.mark.asyncio
async def test_create_enrollment_department_mismatch(
    db_session,
    student,
    department_factory,
):
    ece = await department_factory(
        code="ECE",
        name="Electronics and Communication Engineering",
    )

    course = Course(
        code="EC501",
        name="Digital Electronics",
        department_id=ece.id,
        semester=5,
        credits=4,
    )

    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    service = EnrollmentService(db_session)

    with pytest.raises(InvalidEnrollmentError):
        await service.create_enrollment(
            student.id,
            course.id,
        )


@pytest.mark.asyncio
async def test_create_enrollment_semester_mismatch(
    db_session,
    student,
    department,
):
    course = Course(
        code="CS701",
        name="Advanced Databases",
        department_id=department.id,
        semester=7,
        credits=4,
    )

    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    service = EnrollmentService(db_session)

    with pytest.raises(InvalidEnrollmentError):
        await service.create_enrollment(
            student.id,
            course.id,
        )


@pytest.mark.asyncio
async def test_create_enrollment_reactivates_inactive_enrollment(
    db_session,
    student,
    course,
):
    service = EnrollmentService(db_session)

    created = await service.create_enrollment(
        student.id,
        course.id,
    )

    await service.deactivate_enrollment(created.id)

    result = await service.create_enrollment(
        student.id,
        course.id,
    )

    assert result.id == created.id
    assert result.is_active is True
