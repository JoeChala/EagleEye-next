from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class FacultyCreate(BaseModel):
    employee_id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr | None = None
    department: str = Field(min_length=1, max_length=100)


class FacultyUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    department: str | None = None


class FacultyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    employee_id: str
    name: str
    email: EmailStr | None
    department: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class FacultyListResponse(BaseModel):
    items: list[FacultyResponse]
    total: int
    offset: int
    limit: int
