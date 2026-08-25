from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.features.attendance.model import AttendanceStatus


class AttendanceSessionCreate(BaseModel):
    course_id: UUID
    department_id: UUID
    session_date: date
    start_time: time
    end_time: time
    semester: int
    section: str


class AttendanceSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    department_id: UUID
    session_date: date
    start_time: time
    end_time: time
    semester: int
    section: str


class AttendanceRecordCreate(BaseModel):
    session_id: UUID
    student_id: UUID
    status: AttendanceStatus


class AttendanceRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
    student_id: UUID
    status: AttendanceStatus


class BulkAttendanceRecordCreate(BaseModel):
    student_id: UUID
    status: AttendanceStatus


class BulkAttendanceCreate(BaseModel):
    records: list[BulkAttendanceRecordCreate]


class BulkAttendanceResponse(BaseModel):
    session_id: UUID
    records: list[AttendanceRecordResponse]
