from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.students.schemas import (
    StudentCreate,
    StudentListResponse,
    StudentResponse,
)
from app.features.students.service import StudentService
from app.models.student import Student

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    student_data: StudentCreate,
    session: AsyncSession = Depends(get_db),
) -> StudentResponse:
    student = Student(**student_data.model_dump())

    service = StudentService(session)

    student = await service.register_student(student)

    await session.commit()

    return StudentResponse.model_validate(student)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_student(
    student_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> StudentResponse:
    service = StudentService(session)

    student = await service.get_student(student_id)

    return StudentResponse.model_validate(student)


@router.get(
    "",
    response_model=list[StudentResponse],
    status_code=status.HTTP_200_OK,
)
@router.get(
    "",
    response_model=StudentListResponse,
)
async def get_students(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> StudentListResponse:
    service = StudentService(session)

    students, total = await service.get_students(
        offset=offset,
        limit=limit,
    )

    return StudentListResponse(
        items=[StudentResponse.model_validate(student) for student in students],
        total=total,
        offset=offset,
        limit=limit,
    )
