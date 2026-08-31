from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.enrollments.model import Enrollment


class EnrollmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, enrollment: Enrollment) -> Enrollment:
        self.session.add(enrollment)
        await self.session.commit()
        await self.session.refresh(enrollment)

        return enrollment

    async def get_by_id(self, enrollment_id: UUID) -> Enrollment | None:
        result = await self.session.execute(
            select(Enrollment).where(Enrollment.id == enrollment_id)
        )

        return result.scalar_one_or_none()

    async def get_by_student_and_course(
        self,
        student_id: UUID,
        course_id: UUID,
    ) -> Enrollment | None:
        result = await self.session.execute(
            select(Enrollment).where(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_student(
        self,
        student_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Enrollment]:
        result = await self.session.execute(
            select(Enrollment)
            .where(Enrollment.student_id == student_id)
            .order_by(Enrollment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def list_by_course(
        self,
        course_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Enrollment]:
        result = await self.session.execute(
            select(Enrollment)
            .where(Enrollment.course_id == course_id)
            .order_by(Enrollment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count_by_student(self, student_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(Enrollment.student_id == student_id)
        )

        return result.scalar_one()

    async def count_by_course(
        self,
        course_id: UUID,
    ) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(Enrollment.course_id == course_id)
        )

        return result.scalar_one()

    async def update(
        self,
        enrollment_id: UUID,
        updates: dict,
    ) -> Enrollment | None:
        await self.session.execute(
            update(Enrollment).where(Enrollment.id == enrollment_id).values(**updates)
        )

        await self.session.commit()

        return await self.get_by_id(enrollment_id)

    async def deactivate(self, enrollment_id: UUID) -> Enrollment | None:
        return await self.update(
            enrollment_id,
            {"is_active": False},
        )
