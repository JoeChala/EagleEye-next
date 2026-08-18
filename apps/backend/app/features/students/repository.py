from sqlalchemy import select
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
