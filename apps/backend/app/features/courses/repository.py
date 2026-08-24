from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.courses.model import Course


class CourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, course: Course) -> Course:
        self.session.add(course)
        await self.session.flush()
        await self.session.refresh(course)

        return course

    async def get_by_id(self, course_id: UUID) -> Course | None:
        result = await self.session.execute(
            select(Course).where(Course.id == course_id)
        )

        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Course | None:
        result = await self.session.execute(select(Course).where(Course.code == code))

        return result.scalar_one_or_none()

    async def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Course]:
        result = await self.session.execute(
            select(Course)
            .where(Course.is_active.is_(True))
            .order_by(Course.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(Course).where(Course.is_active.is_(True))
        )

        return result.scalar_one()

    async def update(self, course_id: UUID, updates: dict) -> Course | None:
        course = await self.get_by_id(course_id)

        if course is None:
            return None

        for field, value in updates.items():
            setattr(course, field, value)

        await self.session.flush()
        await self.session.refresh(course)

        return course

    async def deactivate(self, course_id: UUID) -> Course | None:
        course = await self.get_by_id(course_id)

        if course is None:
            return None

        course.is_active = False

        await self.session.flush()
        await self.session.refresh(course)

        return course
