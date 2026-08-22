from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    roll_number: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr | None = None
    department: str = Field(min_length=1, max_length=100)
    semester: int = Field(ge=1, le=8)
    section: str = Field(min_length=1, max_length=20)


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    roll_number: str
    name: str
    email: EmailStr | None
    department: str
    semester: int
    section: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class StudentListResponse(BaseModel):
    items: list[StudentResponse]
    total: int
    offset: int
    limit: int


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    department: str | None = None
    semester: int | None = Field(default=None, ge=1, le=8)
    section: str | None = None
