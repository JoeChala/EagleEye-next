from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import (
    CourseNotFoundError,
    EnrollmentAlreadyExistsError,
    EnrollmentNotFoundError,
    InvalidEnrollmentError,
    StudentCourseEnrollmentNotFoundError,
    StudentNotFoundError,
)
from app.features.courses.repository import CourseRepository
from app.features.enrollments.model import Enrollment
from app.features.enrollments.repository import EnrollmentRepository
from app.features.students.repository import StudentRepository


class EnrollmentService:
    def __init__(self, session: AsyncSession):
        self.repository = EnrollmentRepository(session)
        self.student_repository = StudentRepository(session)
        self.course_repository = CourseRepository(session)

    async def create_enrollment(
        self,
        student_id: UUID,
        course_id: UUID,
    ) -> Enrollment:
        # Check student exists
        student = await self.student_repository.get_by_id(student_id)

        if student is None:
            raise StudentNotFoundError(student_id)

        # Check course exists
        course = await self.course_repository.get_by_id(course_id)

        if course is None:
            raise CourseNotFoundError(course_id)

        # Student and course must belong to the same department
        if student.department_id != course.department_id:
            raise InvalidEnrollmentError(
                "Student and course must belong to the same department"
            )

        # Student and course must belong to the same semester
        if student.semester != course.semester:
            raise InvalidEnrollmentError(
                "Student and course must belong to the same semester"
            )

        # Check whether enrollment already exists
        existing = await self.repository.get_by_student_and_course(
            student_id,
            course_id,
        )

        if existing is not None:
            if existing.is_active:
                raise EnrollmentAlreadyExistsError(
                    student_id,
                    course_id,
                )

            # Reactivate an existing inactive enrollment
            reactivated = await self.repository.update(
                existing.id,
                {"is_active": True},
            )

            if reactivated is None:
                raise EnrollmentNotFoundError(existing.id)

            return reactivated

        # Create new enrollment
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
        )

        return await self.repository.create(enrollment)

    async def get_enrollment(
        self,
        enrollment_id: UUID,
    ) -> Enrollment:
        enrollment = await self.repository.get_by_id(enrollment_id)

        if enrollment is None:
            raise EnrollmentNotFoundError(enrollment_id)

        return enrollment

    async def get_student_enrollment(
        self,
        student_id: UUID,
        course_id: UUID,
    ) -> Enrollment:
        # Verify student exists
        student = await self.student_repository.get_by_id(student_id)

        if student is None:
            raise StudentNotFoundError(student_id)

        # Verify course exists
        course = await self.course_repository.get_by_id(course_id)

        if course is None:
            raise CourseNotFoundError(course_id)

        enrollment = await self.repository.get_by_student_and_course(
            student_id,
            course_id,
        )

        if enrollment is None:
            raise StudentCourseEnrollmentNotFoundError(student_id, course_id)

        return enrollment

    async def list_student_enrollments(
        self,
        student_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Enrollment], int]:
        student = await self.student_repository.get_by_id(student_id)

        if student is None:
            raise StudentNotFoundError(student_id)

        enrollments = await self.repository.list_by_student(
            student_id,
            offset=offset,
            limit=limit,
        )

        total = await self.repository.count_by_student(student_id)

        return enrollments, total

    async def list_course_enrollments(
        self,
        course_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Enrollment], int]:
        course = await self.course_repository.get_by_id(course_id)

        if course is None:
            raise CourseNotFoundError(course_id)

        enrollments = await self.repository.list_by_course(
            course_id,
            offset=offset,
            limit=limit,
        )

        total = await self.repository.count_by_course(course_id)

        return enrollments, total

    async def update_enrollment(
        self,
        enrollment_id: UUID,
        updates: dict,
    ) -> Enrollment:
        enrollment = await self.repository.get_by_id(enrollment_id)

        if enrollment is None:
            raise EnrollmentNotFoundError(enrollment_id)

        updated_enrollment = await self.repository.update(
            enrollment_id,
            updates,
        )

        if updated_enrollment is None:
            raise EnrollmentNotFoundError(enrollment_id)

        return updated_enrollment

    async def deactivate_enrollment(
        self,
        enrollment_id: UUID,
    ) -> Enrollment:
        enrollment = await self.repository.get_by_id(enrollment_id)

        if enrollment is None:
            raise EnrollmentNotFoundError(enrollment_id)

        deactivated_enrollment = await self.repository.deactivate(
            enrollment_id,
        )

        if deactivated_enrollment is None:
            raise EnrollmentNotFoundError(enrollment_id)

        return deactivated_enrollment
