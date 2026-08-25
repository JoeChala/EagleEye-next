from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import DepartmentAlreadyExistsError, DepartmentNotFoundError
from app.features.departments.model import Department
from app.features.departments.repository import DepartmentRepository


class DepartmentService:
    def __init__(self, session: AsyncSession):
        self.repository = DepartmentRepository(session)
        self.session = session

    async def create_department(self, department: Department) -> Department:
        existing_department = await self.repository.get_by_code(department.code)

        if existing_department is not None:
            raise DepartmentAlreadyExistsError(department.code)

        return await self.repository.create(department)

    async def get_department(self, department_id: UUID) -> Department:
        department = await self.repository.get_by_id(department_id)

        if department is None:
            raise DepartmentNotFoundError(department_id)

        return department

    async def list_departments(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Department], int]:
        departments = await self.repository.list(
            offset=offset,
            limit=limit,
        )

        total = await self.repository.count()

        return departments, total

    async def update_department(
        self,
        department_id: UUID,
        updates: dict,
    ) -> Department:
        department = await self.repository.update(department_id, updates)

        if department is None:
            raise DepartmentNotFoundError(department_id)

        return department

    async def deactivate_department(self, department_id: UUID) -> Department:
        department = await self.repository.deactivate(department_id)

        if department is None:
            raise DepartmentNotFoundError(department_id)

        return department
