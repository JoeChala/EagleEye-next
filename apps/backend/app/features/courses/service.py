from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import (
    CourseAlreadyExistsError,
    CourseNotFoundError,
    DepartmentNotFoundError,
)
from app.features.courses.model import Course
from app.features.courses.repository import CourseRepository
from app.features.departments.repository import DepartmentRepository


class CourseService:
    def __init__(self, session: AsyncSession):
        self.repository = CourseRepository(session)
        self.department_repository = DepartmentRepository(session)
        self.session = session

    async def create_course(self, course: Course) -> Course:
        department = await self.department_repository.get_by_id(course.department_id)

        if department is None:
            raise DepartmentNotFoundError(course.department_id)

        existing_course = await self.repository.get_by_code(course.code)

        if existing_course is not None:
            raise CourseAlreadyExistsError(course.code)

        return await self.repository.create(course)

    async def get_course(self, course_id: UUID) -> Course:
        course = await self.repository.get_by_id(course_id)

        if course is None:
            raise CourseNotFoundError(course_id)

        return course

    async def list_courses(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Course], int]:
        courses = await self.repository.list(
            offset=offset,
            limit=limit,
        )

        total = await self.repository.count()

        return courses, total

    async def update_course(self, course_id: UUID, updates: dict) -> Course:
        if "department_id" in updates:
            department = await self.department_repository.get_by_id(
                updates["department_id"]
            )

            if department is None:
                raise DepartmentNotFoundError(updates["department_id"])

        course = await self.repository.update(
            course_id,
            updates,
        )

        if course is None:
            raise CourseNotFoundError(course_id)

        return course

    async def deactivate_course(self, course_id: UUID) -> Course:
        course = await self.repository.deactivate(course_id)

        if course is None:
            raise CourseNotFoundError(course_id)

        return course
