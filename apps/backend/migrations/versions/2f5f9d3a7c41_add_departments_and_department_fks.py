"""add departments and department foreign keys

Revision ID: 2f5f9d3a7c41
Revises: 5f6c1f8d2d3a
Create Date: 2026-08-24 00:00:00.000000
"""

from uuid import uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2f5f9d3a7c41"
down_revision = "5f6c1f8d2d3a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_departments")),
        sa.UniqueConstraint("code", name="uq_departments_code"),
    )

    op.add_column(
        "students",
        sa.Column("department_id", sa.UUID(), nullable=True),
    )
    op.add_column(
        "faculty",
        sa.Column("department_id", sa.UUID(), nullable=True),
    )
    op.add_column(
        "courses",
        sa.Column("department_id", sa.UUID(), nullable=True),
    )
    op.add_column(
        "attendance_sessions",
        sa.Column("department_id", sa.UUID(), nullable=True),
    )

    connection = op.get_bind()

    distinct_departments = (
        connection.execute(
            sa.text(
                """
                SELECT DISTINCT department AS code
                FROM students
                WHERE department IS NOT NULL
                UNION
                SELECT DISTINCT department AS code
                FROM faculty
                WHERE department IS NOT NULL
                UNION
                SELECT DISTINCT department AS code
                FROM courses
                WHERE department IS NOT NULL
                UNION
                SELECT DISTINCT department AS code
                FROM attendance_sessions
                WHERE department IS NOT NULL
                ORDER BY code
                """
            )
        )
        .scalars()
        .all()
    )

    department_table = sa.table(
        "departments",
        sa.column("id", sa.UUID()),
        sa.column("code", sa.String()),
        sa.column("name", sa.String()),
        sa.column("is_active", sa.Boolean()),
    )

    for code in distinct_departments:
        connection.execute(
            sa.insert(department_table).values(
                id=uuid4(),
                code=code,
                name=code,
                is_active=True,
            )
        )

    op.execute(
        sa.text(
            """
            UPDATE students
            SET department_id = departments.id
            FROM departments
            WHERE students.department = departments.code
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE faculty
            SET department_id = departments.id
            FROM departments
            WHERE faculty.department = departments.code
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE courses
            SET department_id = departments.id
            FROM departments
            WHERE courses.department = departments.code
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE attendance_sessions
            SET department_id = departments.id
            FROM departments
            WHERE attendance_sessions.department = departments.code
            """
        )
    )

    op.alter_column(
        "students",
        "department_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.alter_column(
        "faculty",
        "department_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.alter_column(
        "courses",
        "department_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.alter_column(
        "attendance_sessions",
        "department_id",
        existing_type=sa.UUID(),
        nullable=False,
    )

    op.create_foreign_key(
        "fk_students_department_id_departments",
        "students",
        "departments",
        ["department_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_faculty_department_id_departments",
        "faculty",
        "departments",
        ["department_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_courses_department_id_departments",
        "courses",
        "departments",
        ["department_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_attendance_sessions_department_id_departments",
        "attendance_sessions",
        "departments",
        ["department_id"],
        ["id"],
    )

    op.drop_index("ix_students_department", table_name="students")
    op.drop_index("ix_faculty_department", table_name="faculty")
    op.drop_index("ix_courses_department", table_name="courses")

    op.create_index(
        "ix_students_department_id",
        "students",
        ["department_id"],
        unique=False,
    )
    op.create_index(
        "ix_faculty_department_id",
        "faculty",
        ["department_id"],
        unique=False,
    )
    op.create_index(
        "ix_courses_department_id",
        "courses",
        ["department_id"],
        unique=False,
    )

    op.drop_column("students", "department")
    op.drop_column("faculty", "department")
    op.drop_column("courses", "department")
    op.drop_column("attendance_sessions", "department")


def downgrade() -> None:
    op.add_column(
        "students",
        sa.Column("department", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "faculty",
        sa.Column("department", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "courses",
        sa.Column("department", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "attendance_sessions",
        sa.Column("department", sa.String(length=100), nullable=True),
    )

    op.execute(
        sa.text(
            """
            UPDATE students
            SET department = departments.code
            FROM departments
            WHERE students.department_id = departments.id
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE faculty
            SET department = departments.code
            FROM departments
            WHERE faculty.department_id = departments.id
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE courses
            SET department = departments.code
            FROM departments
            WHERE courses.department_id = departments.id
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE attendance_sessions
            SET department = departments.code
            FROM departments
            WHERE attendance_sessions.department_id = departments.id
            """
        )
    )

    op.alter_column(
        "students",
        "department",
        existing_type=sa.String(length=100),
        nullable=False,
    )
    op.alter_column(
        "faculty",
        "department",
        existing_type=sa.String(length=100),
        nullable=False,
    )
    op.alter_column(
        "courses",
        "department",
        existing_type=sa.String(length=100),
        nullable=False,
    )
    op.alter_column(
        "attendance_sessions",
        "department",
        existing_type=sa.String(length=100),
        nullable=False,
    )

    op.drop_constraint(
        "fk_students_department_id_departments",
        "students",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_faculty_department_id_departments",
        "faculty",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_courses_department_id_departments",
        "courses",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_attendance_sessions_department_id_departments",
        "attendance_sessions",
        type_="foreignkey",
    )

    op.drop_index("ix_students_department_id", table_name="students")
    op.drop_index("ix_faculty_department_id", table_name="faculty")
    op.drop_index("ix_courses_department_id", table_name="courses")

    op.create_index("ix_students_department", "students", ["department"], unique=False)
    op.create_index("ix_faculty_department", "faculty", ["department"], unique=False)
    op.create_index("ix_courses_department", "courses", ["department"], unique=False)

    op.drop_column("students", "department_id")
    op.drop_column("faculty", "department_id")
    op.drop_column("courses", "department_id")
    op.drop_column("attendance_sessions", "department_id")

    op.drop_table("departments")
