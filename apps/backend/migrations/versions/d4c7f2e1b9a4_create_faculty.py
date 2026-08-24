"""create faculty

Revision ID: d4c7f2e1b9a4
Revises: e1145f9b7ba1
Create Date: 2026-08-24 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d4c7f2e1b9a4"
down_revision = "e1145f9b7ba1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "faculty",
        sa.Column("employee_id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("department", sa.String(length=100), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_faculty")),
        sa.UniqueConstraint("employee_id", name="uq_faculty_employee_id"),
    )
    op.create_index("ix_faculty_department", "faculty", ["department"], unique=False)
    op.create_index("ix_faculty_is_active", "faculty", ["is_active"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_faculty_is_active", table_name="faculty")
    op.drop_index("ix_faculty_department", table_name="faculty")
    op.drop_table("faculty")
