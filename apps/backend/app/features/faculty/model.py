from sqlalchemy import Boolean, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class Faculty(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "faculty"
    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            name="uq_faculty_employee_id",
        ),
        Index("ix_faculty_is_active", "is_active"),
        Index("ix_faculty_department", "department"),
    )

    employee_id: Mapped[str] = mapped_column(
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
    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        server_default="true",
    )
