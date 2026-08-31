from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EnrollmentCreate(BaseModel):
    student_id: UUID
    course_id: UUID


class EnrollmentUpdate(BaseModel):
    is_active: bool


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    course_id: UUID
    enrolled_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime


class EnrollmentListResponse(BaseModel):
    records: list[EnrollmentResponse]
    total: int
    offset: int
    limit: int
