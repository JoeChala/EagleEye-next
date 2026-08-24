from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import CourseAlreadyExistsError, CourseNotFoundError
from app.features.courses.model import Course
from app.features.courses.repository import CourseRepository


class CourseService:
    def __init__(self, session: AsyncSession):
        self.repository = CourseRepository(session)
        self.session = session

    async def create_course(self, course: Course) -> Course:
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
