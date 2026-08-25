from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import (
    DepartmentNotFoundError,
    StudentAlreadyExistsError,
    StudentNotFoundError,
)
from app.features.departments.repository import DepartmentRepository
from app.features.students.model import Student
from app.features.students.repository import StudentRepository


class StudentService:
    def __init__(self, session: AsyncSession):
        self.repository = StudentRepository(session)
        self.department_repository = DepartmentRepository(session)
        self.session = session

    async def register_student(self, student: Student) -> Student:
        department = await self.department_repository.get_by_id(student.department_id)

        if department is None:
            raise DepartmentNotFoundError(student.department_id)

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
        department_id: UUID | None = None,
        semester: int | None = None,
        section: str | None = None,
    ) -> tuple[list[Student], int]:

        students = await self.repository.get_all(
            offset=offset,
            limit=limit,
            department_id=department_id,
            semester=semester,
            section=section,
        )

        total = await self.repository.count(
            department_id=department_id,
            semester=semester,
            section=section,
        )

        return students, total

    async def update_student(
        self,
        student_id: UUID,
        updates: dict,
    ) -> Student:
        if "department_id" in updates:
            department = await self.department_repository.get_by_id(
                updates["department_id"]
            )

            if department is None:
                raise DepartmentNotFoundError(updates["department_id"])

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
