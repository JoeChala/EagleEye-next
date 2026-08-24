"""replace attendance subject with course id

Revision ID: 5f6c1f8d2d3a
Revises: 8d8b5d2e6b11
Create Date: 2026-08-24 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5f6c1f8d2d3a"
down_revision = "8d8b5d2e6b11"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "attendance_sessions",
        sa.Column("course_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_attendance_sessions_course_id_courses",
        "attendance_sessions",
        "courses",
        ["course_id"],
        ["id"],
    )
    op.drop_column("attendance_sessions", "subject")


def downgrade() -> None:
    op.add_column(
        "attendance_sessions",
        sa.Column("subject", sa.String(length=100), nullable=True),
    )
    op.drop_constraint(
        "fk_attendance_sessions_course_id_courses",
        "attendance_sessions",
        type_="foreignkey",
    )
    op.drop_column("attendance_sessions", "course_id")
