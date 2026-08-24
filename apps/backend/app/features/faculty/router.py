from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.faculty.model import Faculty
from app.features.faculty.schema import (
    FacultyCreate,
    FacultyListResponse,
    FacultyResponse,
    FacultyUpdate,
)
from app.features.faculty.service import FacultyService

router = APIRouter(
    prefix="/faculty",
    tags=["Faculty"],
)


@router.post(
    "",
    response_model=FacultyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_faculty(
    faculty_data: FacultyCreate,
    session: AsyncSession = Depends(get_db),
) -> FacultyResponse:
    faculty = Faculty(**faculty_data.model_dump())

    service = FacultyService(session)

    faculty = await service.create_faculty(faculty)

    await session.commit()

    return FacultyResponse.model_validate(faculty)


@router.get(
    "/{faculty_id}",
    response_model=FacultyResponse,
    status_code=status.HTTP_200_OK,
)
async def get_faculty(
    faculty_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> FacultyResponse:
    service = FacultyService(session)

    faculty = await service.get_faculty(faculty_id)

    return FacultyResponse.model_validate(faculty)


@router.get(
    "",
    response_model=FacultyListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_faculty(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> FacultyListResponse:
    service = FacultyService(session)

    faculties, total = await service.list_faculty(
        offset=offset,
        limit=limit,
    )

    return FacultyListResponse(
        items=[FacultyResponse.model_validate(faculty) for faculty in faculties],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.patch(
    "/{faculty_id}",
    response_model=FacultyResponse,
    status_code=status.HTTP_200_OK,
)
async def update_faculty(
    faculty_id: UUID,
    faculty_data: FacultyUpdate,
    session: AsyncSession = Depends(get_db),
) -> FacultyResponse:
    service = FacultyService(session)

    updates = faculty_data.model_dump(exclude_unset=True)

    faculty = await service.update_faculty(
        faculty_id,
        updates,
    )

    await session.commit()

    return FacultyResponse.model_validate(faculty)


@router.delete(
    "/{faculty_id}",
    response_model=FacultyResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_faculty(
    faculty_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> FacultyResponse:
    service = FacultyService(session)

    faculty = await service.deactivate_faculty(faculty_id)

    await session.commit()

    return FacultyResponse.model_validate(faculty)
