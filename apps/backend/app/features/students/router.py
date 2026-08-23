from uuid import UUID

from apps.backend.app.features.students.model import Student
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.students.schemas import (
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)
from app.features.students.service import StudentService

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
    response_model=StudentListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_students(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    department: str | None = Query(default=None),
    semester: int | None = Query(default=None, ge=1, le=8),
    section: str | None = Query(default=None),
    session: AsyncSession = Depends(get_db),
) -> StudentListResponse:

    service = StudentService(session)

    students, total = await service.get_students(
        offset=offset,
        limit=limit,
        department=department,
        semester=semester,
        section=section,
    )

    return StudentListResponse(
        items=[StudentResponse.model_validate(student) for student in students],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
)
async def update_student(
    student_id: UUID,
    student_data: StudentUpdate,
    session: AsyncSession = Depends(get_db),
) -> StudentResponse:
    service = StudentService(session)

    updates = student_data.model_dump(exclude_unset=True)

    student = await service.update_student(
        student_id,
        updates,
    )

    await session.commit()

    return StudentResponse.model_validate(student)


@router.delete(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_student(
    student_id: UUID, session: AsyncSession = Depends(get_db)
) -> StudentResponse:
    service = StudentService(session)

    student = await service.deactivate_student(student_id)

    await session.commit()

    return StudentResponse.model_validate(student)
