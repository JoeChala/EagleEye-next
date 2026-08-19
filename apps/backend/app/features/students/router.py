from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.students.schemas import StudentCreate, StudentResponse
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
