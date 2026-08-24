"""create courses

Revision ID: 8d8b5d2e6b11
Revises: d4c7f2e1b9a4
Create Date: 2026-08-24 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8d8b5d2e6b11"
down_revision = "d4c7f2e1b9a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("semester", sa.Integer(), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_courses")),
        sa.UniqueConstraint("code", name="uq_courses_code"),
    )
    op.create_index("ix_courses_department", "courses", ["department"], unique=False)
    op.create_index("ix_courses_is_active", "courses", ["is_active"], unique=False)
    op.create_index("ix_courses_semester", "courses", ["semester"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_courses_semester", table_name="courses")
    op.drop_index("ix_courses_is_active", table_name="courses")
    op.drop_index("ix_courses_department", table_name="courses")
    op.drop_table("courses")
