from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.courses.model import Course
from app.features.courses.schema import (
    CourseCreate,
    CourseListResponse,
    CourseResponse,
    CourseUpdate,
)
from app.features.courses.service import CourseService

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    course_data: CourseCreate,
    session: AsyncSession = Depends(get_db),
) -> CourseResponse:
    course = Course(**course_data.model_dump())

    service = CourseService(session)

    course = await service.create_course(course)

    await session.commit()

    return CourseResponse.model_validate(course)


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
async def get_course(
    course_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> CourseResponse:
    service = CourseService(session)

    course = await service.get_course(course_id)

    return CourseResponse.model_validate(course)


@router.get(
    "",
    response_model=CourseListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_courses(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> CourseListResponse:
    service = CourseService(session)

    courses, total = await service.list_courses(
        offset=offset,
        limit=limit,
    )

    return CourseListResponse(
        items=[CourseResponse.model_validate(course) for course in courses],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.patch(
    "/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
async def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    session: AsyncSession = Depends(get_db),
) -> CourseResponse:
    service = CourseService(session)

    updates = course_data.model_dump(exclude_unset=True)

    course = await service.update_course(
        course_id,
        updates,
    )

    await session.commit()

    return CourseResponse.model_validate(course)


@router.delete(
    "/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_course(
    course_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> CourseResponse:
    service = CourseService(session)

    course = await service.deactivate_course(course_id)

    await session.commit()

    return CourseResponse.model_validate(course)
