from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import FacultyAlreadyExistsError, FacultyNotFoundError
from app.features.faculty.model import Faculty
from app.features.faculty.repository import FacultyRepository


class FacultyService:
    def __init__(self, session: AsyncSession):
        self.repository = FacultyRepository(session)
        self.session = session

    async def create_faculty(self, faculty: Faculty) -> Faculty:
        existing_faculty = await self.repository.get_by_employee_id(faculty.employee_id)

        if existing_faculty is not None:
            raise FacultyAlreadyExistsError(faculty.employee_id)

        return await self.repository.create(faculty)

    async def get_faculty(self, faculty_id: UUID) -> Faculty:
        faculty = await self.repository.get_by_id(faculty_id)

        if faculty is None:
            raise FacultyNotFoundError(faculty_id)

        return faculty

    async def list_faculty(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Faculty], int]:
        faculties = await self.repository.list(
            offset=offset,
            limit=limit,
        )

        total = await self.repository.count()

        return faculties, total

    async def update_faculty(
        self,
        faculty_id: UUID,
        updates: dict,
    ) -> Faculty:
        faculty = await self.repository.update(
            faculty_id,
            updates,
        )

        if faculty is None:
            raise FacultyNotFoundError(faculty_id)

        return faculty

    async def deactivate_faculty(self, faculty_id: UUID) -> Faculty:
        faculty = await self.repository.deactivate(faculty_id)

        if faculty is None:
            raise FacultyNotFoundError(faculty_id)

        return faculty
