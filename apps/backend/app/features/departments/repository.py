from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.departments.model import Department


class DepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, department: Department) -> Department:
        self.session.add(department)
        await self.session.flush()
        await self.session.refresh(department)

        return department

    async def get_by_id(self, department_id: UUID) -> Department | None:
        result = await self.session.execute(
            select(Department).where(Department.id == department_id)
        )

        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Department | None:
        result = await self.session.execute(
            select(Department).where(Department.code == code)
        )

        return result.scalar_one_or_none()

    async def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Department]:
        result = await self.session.execute(
            select(Department)
            .where(Department.is_active.is_(True))
            .order_by(Department.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(Department)
            .where(Department.is_active.is_(True))
        )

        return result.scalar_one()

    async def update(self, department_id: UUID, updates: dict) -> Department | None:
        department = await self.get_by_id(department_id)

        if department is None:
            return None

        for field, value in updates.items():
            setattr(department, field, value)

        await self.session.flush()
        await self.session.refresh(department)

        return department

    async def deactivate(self, department_id: UUID) -> Department | None:
        department = await self.get_by_id(department_id)

        if department is None:
            return None

        department.is_active = False

        await self.session.flush()
        await self.session.refresh(department)

        return department
