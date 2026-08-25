from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class Course(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint(
            "code",
            name="uq_courses_code",
        ),
        Index("ix_courses_is_active", "is_active"),
        Index("ix_courses_department_id", "department_id"),
        Index("ix_courses_semester", "semester"),
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    department_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("departments.id"),
        nullable=False,
    )
    semester: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        server_default="true",
    )
