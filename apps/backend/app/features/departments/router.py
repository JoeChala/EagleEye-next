from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.departments.model import Department
from app.features.departments.schema import (
    DepartmentCreate,
    DepartmentListResponse,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.features.departments.service import DepartmentService

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    department_data: DepartmentCreate,
    session: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    department = Department(**department_data.model_dump())

    service = DepartmentService(session)
    department = await service.create_department(department)

    await session.commit()

    return DepartmentResponse.model_validate(department)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_department(
    department_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    service = DepartmentService(session)
    department = await service.get_department(department_id)

    return DepartmentResponse.model_validate(department)


@router.get(
    "",
    response_model=DepartmentListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_departments(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> DepartmentListResponse:
    service = DepartmentService(session)
    departments, total = await service.list_departments(
        offset=offset,
        limit=limit,
    )

    return DepartmentListResponse(
        items=[
            DepartmentResponse.model_validate(department) for department in departments
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
)
async def update_department(
    department_id: UUID,
    department_data: DepartmentUpdate,
    session: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    service = DepartmentService(session)
    updates = department_data.model_dump(exclude_unset=True)

    department = await service.update_department(department_id, updates)

    await session.commit()

    return DepartmentResponse.model_validate(department)


@router.delete(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_department(
    department_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    service = DepartmentService(session)
    department = await service.deactivate_department(department_id)

    await session.commit()

    return DepartmentResponse.model_validate(department)
