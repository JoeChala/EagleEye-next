from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student


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

    async def get_all(self, offset: int = 0, limit: int = 20) -> list[Student]:
        result = await self.session.execute(
            select(Student)
            .order_by(Student.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Student))

        return result.scalar_one()
