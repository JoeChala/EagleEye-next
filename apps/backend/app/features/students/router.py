from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.students.model import Student
from app.features.students.schema import (
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
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    department_id: Annotated[UUID | None, Query()] = None,
    semester: Annotated[int | None, Query(ge=1, le=8)] = None,
    section: Annotated[str | None, Query()] = None,
    session: AsyncSession = Depends(get_db),
) -> StudentListResponse:

    service = StudentService(session)

    students, total = await service.get_students(
        offset=offset,
        limit=limit,
        department_id=department_id,
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
