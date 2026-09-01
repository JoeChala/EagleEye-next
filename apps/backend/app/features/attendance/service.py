from uuid import UUID

from app.exceptions.errors import (
    AttendanceAlreadyExistsError,
    AttendanceSessionDepartmentMismatchError,
    AttendanceSessionNotFoundError,
    CourseNotFoundError,
    DepartmentNotFoundError,
    StudentNotEnrolledError,
    StudentNotFoundError,
    StudentSessionMismatchError,
)
from app.features.attendance.model import AttendanceRecord, AttendanceSession
from app.features.attendance.repository import (
    AttendanceRecordRepository,
    AttendanceSessionRepository,
)
from app.features.courses.repository import CourseRepository
from app.features.departments.repository import DepartmentRepository
from app.features.enrollments.repository import EnrollmentRepository
from app.features.students.repository import StudentRepository


class AttendanceSessionService:
    def __init__(
        self,
        repository: AttendanceSessionRepository,
        course_repository: CourseRepository,
        department_repository: DepartmentRepository,
    ):
        self.repository = repository
        self.course_repository = course_repository
        self.department_repository = department_repository

    async def create_session(
        self,
        attendance_session: AttendanceSession,
    ) -> AttendanceSession:
        department = await self.department_repository.get_by_id(
            attendance_session.department_id
        )

        if department is None:
            raise DepartmentNotFoundError(attendance_session.department_id)

        course = await self.course_repository.get_by_id(attendance_session.course_id)

        if course is None:
            raise CourseNotFoundError(attendance_session.course_id)

        if course.department_id != attendance_session.department_id:
            raise AttendanceSessionDepartmentMismatchError(
                attendance_session.course_id,
                attendance_session.department_id,
            )

        return await self.repository.create(attendance_session)

    async def get_session(
        self,
        session_id: UUID,
    ) -> AttendanceSession | None:
        return await self.repository.get_by_id(session_id)


class AttendanceRecordService:
    def __init__(
        self,
        repository: AttendanceRecordRepository,
        session_repository: AttendanceSessionRepository,
        student_repository: StudentRepository,
        enrollment_repository: EnrollmentRepository,
    ):
        self.repository = repository
        self.session_repository = session_repository
        self.student_repository = student_repository
        self.enrollment_repository = enrollment_repository

    async def create_record(self, record: AttendanceRecord) -> AttendanceRecord:
        session = await self.session_repository.get_by_id(record.session_id)

        if session is None:
            raise AttendanceSessionNotFoundError(record.session_id)

        student = await self.student_repository.get_by_id(record.student_id)

        if student is None:
            raise StudentNotFoundError(record.student_id)

        enrollment = await self.enrollment_repository.get_by_student_and_course(
            record.student_id,
            session.course_id,
        )

        if enrollment is None or not enrollment.is_active:
            raise StudentNotEnrolledError(
                record.student_id,
                session.course_id,
            )

        existing = await self.repository.get_by_session_and_student(
            record.session_id,
            record.student_id,
        )

        if existing is not None:
            raise AttendanceAlreadyExistsError(
                session_id=record.session_id,
                student_id=record.student_id,
            )

        return await self.repository.create(record)

    async def get_record(self, record_id: UUID) -> AttendanceRecord | None:
        return await self.repository.get_by_id(record_id)

    async def create_bulk_records(
        self,
        session_id: UUID,
        records: list[AttendanceRecord],
    ) -> list[AttendanceRecord]:

        session = await self.session_repository.get_by_id(session_id)

        if session is None:
            raise AttendanceSessionNotFoundError(session_id)

        # Validate students FIRST
        for record in records:
            student = await self.student_repository.get_by_id(record.student_id)

            if student is None:
                raise StudentNotFoundError(record.student_id)

            if (
                student.department_id != session.department_id
                or student.semester != session.semester
                or student.section != session.section
            ):
                raise StudentSessionMismatchError(student.id)

            enrollment = await self.enrollment_repository.get_by_student_and_course(
                record.student_id, session.course_id
            )
            if enrollment is None or not enrollment.is_active:
                raise StudentNotEnrolledError(record.student_id, session.course_id)

        # Check duplicates SECOND
        seen_students: set[UUID] = set()

        for record in records:
            if record.student_id in seen_students:
                raise AttendanceAlreadyExistsError(
                    session_id=session_id,
                    student_id=record.student_id,
                )

            seen_students.add(record.student_id)

            existing = await self.repository.get_by_session_and_student(
                session_id,
                record.student_id,
            )

            if existing is not None:
                raise AttendanceAlreadyExistsError(
                    session_id=session_id,
                    student_id=record.student_id,
                )

        # Assign session ID
        for record in records:
            record.session_id = session_id

        # Create only after ALL validation passes
        created_records = []

        for record in records:
            created_record = await self.repository.create(record)
            created_records.append(created_record)

        return created_records
