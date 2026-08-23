from datetime import date as DateType
from datetime import time as TimeType

from sqlalchemy import Date, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class AttendanceSession(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "attendance_sessions"

    subject: Mapped[str] = mapped_column(
        String(100),
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
