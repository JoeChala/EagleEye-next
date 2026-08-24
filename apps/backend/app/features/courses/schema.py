from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)
    department: str = Field(min_length=1, max_length=100)
    semester: int
    credits: int


class CourseUpdate(BaseModel):
    name: str | None = None
    department: str | None = None
    semester: int | None = None
    credits: int | None = None


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    department: str
    semester: int
    credits: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CourseListResponse(BaseModel):
    items: list[CourseResponse]
    total: int
    offset: int
    limit: int
