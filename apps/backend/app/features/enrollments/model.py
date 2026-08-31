from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class Enrollment(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "enrollments"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_id",
            name="uq_enrollments_student_course",
        ),
        Index("ix_enrollments_student_id", "student_id"),
        Index("ix_enrollments_course_id", "course_id"),
        Index("ix_enrollments_is_active", "is_active"),
    )

    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("students.id"),
        nullable=False,
    )

    course_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("courses.id"),
        nullable=False,
    )

    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        server_default="true",
    )
