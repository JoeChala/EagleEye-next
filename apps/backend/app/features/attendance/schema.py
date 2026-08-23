from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AttendanceSessionCreate(BaseModel):
    subject: str
    session_date: date
    start_time: time
    end_time: time
    department: str
    semester: int
    section: str


class AttendanceSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    subject: str
    session_date: date
    start_time: time
    end_time: time
    department: str
    semester: int
    section: str
