from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.student import StudentAlreadyExistsError
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
