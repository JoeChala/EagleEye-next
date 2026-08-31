import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.session import get_db
from app.features.courses.model import Course
from app.features.departments.model import Department
from app.features.students.model import Student
from app.main import app

load_dotenv()
TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine: AsyncEngine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def clean_database(db_session: AsyncSession):
    yield

    await db_session.execute(text("DELETE FROM attendance_records"))
    await db_session.execute(text("DELETE FROM attendance_sessions"))
    await db_session.execute(text("DELETE FROM enrollments"))
    await db_session.execute(text("DELETE FROM students"))
    await db_session.execute(text("DELETE FROM faculty"))
    await db_session.execute(text("DELETE FROM courses"))
    await db_session.execute(text("DELETE FROM departments"))

    await db_session.commit()


@pytest_asyncio.fixture
async def department(db_session: AsyncSession):
    department = Department(
        code="CSE",
        name="Computer Science and Engineering",
    )

    db_session.add(department)
    await db_session.commit()
    await db_session.refresh(department)

    return department


@pytest_asyncio.fixture
async def department_factory(db_session: AsyncSession):
    async def create_department(
        *,
        code: str,
        name: str,
    ) -> Department:
        department = Department(
            code=code,
            name=name,
        )

        db_session.add(department)
        await db_session.commit()
        await db_session.refresh(department)

        return department

    return create_department


@pytest_asyncio.fixture
async def course(db_session: AsyncSession, department: Department):
    course = Course(
        code="CS501",
        name="Database Management Systems",
        department_id=department.id,
        semester=5,
        credits=4,
    )

    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    return course


@pytest_asyncio.fixture
async def student(
    db_session: AsyncSession,
    department: Department,
) -> Student:
    student = Student(
        roll_number="ENR001",
        name="Enrollment Student",
        email="enrollment@example.com",
        department_id=department.id,
        semester=5,
        section="A",
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    return student
