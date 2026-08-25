from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)


class DepartmentUpdate(BaseModel):
    name: str | None = None


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class DepartmentListResponse(BaseModel):
    items: list[DepartmentResponse]
    total: int
    offset: int
    limit: int
