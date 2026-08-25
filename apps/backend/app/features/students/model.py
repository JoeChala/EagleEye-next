from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class Student(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint(
            "roll_number",
            name="uq_students_roll_number",
        ),
        Index("ix_students_is_active", "is_active"),
        Index("ix_students_department_id", "department_id"),
        Index("ix_students_semester", "semester"),
    )
    roll_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
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

    section: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, server_default="true"
    )
