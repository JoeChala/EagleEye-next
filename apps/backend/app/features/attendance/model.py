from datetime import date as DateType
from datetime import time as TimeType
from enum import Enum
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String, Time, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class AttendanceStatus(Enum):
    PRESENT = "present"
    ABSENT = "absent"


class AttendanceSession(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "attendance_sessions"

    course_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("courses.id"),
        nullable=False,
    )

    session_date: Mapped[DateType] = mapped_column(
        Date,
        nullable=False,
    )

    start_time: Mapped[TimeType] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[TimeType] = mapped_column(
        Time,
        nullable=False,
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    semester: Mapped[int] = mapped_column(
        nullable=False,
    )

    section: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )


class AttendanceRecord(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "student_id",
            name="uq_attendance_session_student",
        ),
    )
    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("attendance_sessions.id"),
        nullable=False,
    )

    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("students.id"),
        nullable=False,
    )

    status: Mapped[AttendanceStatus] = mapped_column(
        SQLEnum(AttendanceStatus),
        nullable=False,
    )
