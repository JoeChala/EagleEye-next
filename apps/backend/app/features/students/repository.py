from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.students.model import Student


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_roll_number(self, roll_number: str) -> Student | None:
        result = await self.session.execute(
            select(Student).where(Student.roll_number == roll_number)
        )

        return result.scalar_one_or_none()

    async def create(self, student: Student) -> Student:
        self.session.add(student)
        await self.session.flush()  # only the service commits transaction

        return student

    async def get_by_id(self, student_id: UUID) -> Student | None:
        result = await self.session.execute(
            select(Student).where(Student.id == student_id)
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
        department: str | None = None,
        semester: int | None = None,
        section: str | None = None,
    ) -> list[Student]:
        query = (
            select(Student)
            .where(Student.is_active.is_(True))
            .order_by(Student.created_at.desc())
        )

        if department is not None:
            query = query.where(Student.department == department)

        if semester is not None:
            query = query.where(Student.semester == semester)

        if section is not None:
            query = query.where(Student.section == section)

        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def count(
        self,
        department: str | None = None,
        semester: int | None = None,
        section: str | None = None,
    ) -> int:

        query = (
            select(func.count()).select_from(Student).where(Student.is_active.is_(True))
        )

        if department is not None:
            query = query.where(Student.department == department)

        if semester is not None:
            query = query.where(Student.semester == semester)

        if section is not None:
            query = query.where(Student.section == section)

        result = await self.session.execute(query)

        return result.scalar_one()

    async def update_by_id(self, student_id: UUID, updates: dict) -> Student | None:
        student = await self.get_by_id(student_id)

        if student is None:
            return None

        for field, value in updates.items():
            setattr(student, field, value)

        await self.session.flush()
        await self.session.refresh(student)  # refresh before flushing
        # after SQL execution Python obj may not have new value

        return student

    async def deactivate(self, student_id: UUID) -> Student | None:
        # soft deletion
        student = await self.get_by_id(student_id)

        if student is None:
            return None

        student.is_active = False

        await self.session.flush()
        await self.session.refresh(student)

        return student
