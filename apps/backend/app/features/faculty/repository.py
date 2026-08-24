from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.faculty.model import Faculty


class FacultyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, faculty: Faculty) -> Faculty:
        self.session.add(faculty)
        await self.session.flush()
        await self.session.refresh(faculty)

        return faculty

    async def get_by_id(self, faculty_id: UUID) -> Faculty | None:
        result = await self.session.execute(
            select(Faculty).where(Faculty.id == faculty_id)
        )

        return result.scalar_one_or_none()

    async def get_by_employee_id(self, employee_id: str) -> Faculty | None:
        result = await self.session.execute(
            select(Faculty).where(Faculty.employee_id == employee_id)
        )

        return result.scalar_one_or_none()

    async def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Faculty]:
        result = await self.session.execute(
            select(Faculty)
            .where(Faculty.is_active.is_(True))
            .order_by(Faculty.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(Faculty).where(Faculty.is_active.is_(True))
        )

        return result.scalar_one()

    async def update(self, faculty_id: UUID, updates: dict) -> Faculty | None:
        faculty = await self.get_by_id(faculty_id)

        if faculty is None:
            return None

        for field, value in updates.items():
            setattr(faculty, field, value)

        await self.session.flush()
        await self.session.refresh(faculty)

        return faculty

    async def deactivate(self, faculty_id: UUID) -> Faculty | None:
        faculty = await self.get_by_id(faculty_id)

        if faculty is None:
            return None

        faculty.is_active = False

        await self.session.flush()
        await self.session.refresh(faculty)

        return faculty
