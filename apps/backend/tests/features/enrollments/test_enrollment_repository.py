from uuid import uuid4

import pytest

from app.features.enrollments.model import Enrollment
from app.features.enrollments.repository import EnrollmentRepository


@pytest.mark.asyncio
async def test_create_enrollment(db_session, student, course):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(student_id=student.id, course_id=course.id)

    result = await repository.create(enrollment)

    assert result.id is not None
    assert result.student_id == student.id
    assert result.course_id == course.id
    assert result.is_active is True


@pytest.mark.asyncio
async def test_get_enrollment_by_id(db_session, student, course):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    created = await repository.create(enrollment)

    result = await repository.get_by_id(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.student_id == student.id
    assert result.course_id == course.id


@pytest.mark.asyncio
async def test_get_enrollment_by_id_not_found(db_session):
    repository = EnrollmentRepository(db_session)

    result = await repository.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_get_by_student_and_course(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    created = await repository.create(enrollment)

    result = await repository.get_by_student_and_course(
        student.id,
        course.id,
    )

    assert result is not None
    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_by_student_and_course_not_found(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    result = await repository.get_by_student_and_course(
        student.id,
        course.id,
    )

    assert result is None


@pytest.mark.asyncio
async def test_list_by_student(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    await repository.create(enrollment)

    results = await repository.list_by_student(student.id)

    assert len(results) == 1
    assert results[0].student_id == student.id
    assert results[0].course_id == course.id


@pytest.mark.asyncio
async def test_list_by_course(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    await repository.create(enrollment)

    results = await repository.list_by_course(course.id)

    assert len(results) == 1
    assert results[0].student_id == student.id
    assert results[0].course_id == course.id


@pytest.mark.asyncio
async def test_count_by_student(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    await repository.create(enrollment)

    count = await repository.count_by_student(student.id)

    assert count == 1


@pytest.mark.asyncio
async def test_count_by_course(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    await repository.create(enrollment)

    count = await repository.count_by_course(course.id)

    assert count == 1


@pytest.mark.asyncio
async def test_update_enrollment(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    created = await repository.create(enrollment)

    result = await repository.update(
        created.id,
        {"is_active": False},
    )

    assert result is not None
    assert result.id == created.id
    assert result.is_active is False


@pytest.mark.asyncio
async def test_update_enrollment_not_found(
    db_session,
):
    repository = EnrollmentRepository(db_session)

    result = await repository.update(
        uuid4(),
        {"is_active": False},
    )

    assert result is None


@pytest.mark.asyncio
async def test_deactivate_enrollment(
    db_session,
    student,
    course,
):
    repository = EnrollmentRepository(db_session)

    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id,
    )

    created = await repository.create(enrollment)

    result = await repository.deactivate(created.id)

    assert result is not None
    assert result.is_active is False
