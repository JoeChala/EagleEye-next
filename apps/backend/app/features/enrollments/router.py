from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.enrollments.model import Enrollment
from app.features.enrollments.schema import (
    EnrollmentCreate,
    EnrollmentListResponse,
    EnrollmentResponse,
)
from app.features.enrollments.service import EnrollmentService

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)


@router.post(
    "",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_enrollment(
    enrollment_data: EnrollmentCreate,
    session: AsyncSession = Depends(get_db),
) -> EnrollmentResponse:
    enrollment = Enrollment(**enrollment_data.model_dump())

    service = EnrollmentService(session)

    enrollment = await service.create_enrollment(
        enrollment.student_id, enrollment.course_id
    )

    await session.commit()

    return EnrollmentResponse.model_validate(enrollment)


@router.get(
    "/{enrollment_id}",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_enrollment(
    enrollment_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> EnrollmentResponse:
    service = EnrollmentService(session)

    course = await service.get_enrollment(enrollment_id)

    return EnrollmentResponse.model_validate(course)


@router.get(
    "/student/{student_id}",
    response_model=EnrollmentListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_student_enrollment(
    student_id: UUID,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> EnrollmentListResponse:
    service = EnrollmentService(session)

    enrollments, total = await service.list_student_enrollments(
        student_id,
        offset=offset,
        limit=limit,
    )

    return EnrollmentListResponse(
        records=[
            EnrollmentResponse.model_validate(enrollment) for enrollment in enrollments
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/course/{course_id}",
    response_model=EnrollmentListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_course_enrollment(
    course_id: UUID,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> EnrollmentListResponse:
    service = EnrollmentService(session)

    enrollments, total = await service.list_course_enrollments(
        course_id,
        offset=offset,
        limit=limit,
    )

    return EnrollmentListResponse(
        records=[
            EnrollmentResponse.model_validate(enrollment) for enrollment in enrollments
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.delete(
    "/{enrollment_id}",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_enrollment(
    enrollment_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> EnrollmentResponse:
    service = EnrollmentService(session)

    course = await service.deactivate_enrollment(enrollment_id)

    await session.commit()

    return EnrollmentResponse.model_validate(course)
