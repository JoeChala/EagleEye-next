from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.student import StudentAlreadyExistsError, StudentNotFoundError
from app.features.students.repository import StudentRepository
from app.models.student import Student


class StudentService:
    def __init__(self, session: AsyncSession):
        self.repository = StudentRepository(session)
        self.session = session

    async def register_student(self, student: Student) -> Student:
        existing_student = await self.repository.get_by_roll_number(student.roll_number)

        if existing_student is not None:
            raise StudentAlreadyExistsError(student.roll_number)

        return await self.repository.create(student)

    async def get_student(self, student_id: UUID) -> Student:
        student = await self.repository.get_by_id(student_id)

        if student is None:
            raise StudentNotFoundError(student_id)

        return student

    async def get_students(
        self,
        offset: int = 0,
        limit: int = 20,
        department: str | None = None,
        semester: int | None = None,
        section: str | None = None,
    ) -> tuple[list[Student], int]:

        students = await self.repository.get_all(
            offset=offset,
            limit=limit,
            department=department,
            semester=semester,
            section=section,
        )

        total = await self.repository.count(
            department=department,
            semester=semester,
            section=section,
        )

        return students, total

    async def update_student(
        self,
        student_id: UUID,
        updates: dict,
    ) -> Student:
        student = await self.repository.update_by_id(
            student_id,
            updates,
        )

        if student is None:
            raise StudentNotFoundError(student_id)

        return student

    async def deactivate_student(self, student_id: UUID) -> Student:
        student = await self.repository.deactivate(student_id)

        if student is None:
            raise StudentNotFoundError(student_id)

        return student
