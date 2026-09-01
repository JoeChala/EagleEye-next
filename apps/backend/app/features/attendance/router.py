from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.attendance.model import AttendanceRecord, AttendanceSession
from app.features.attendance.repository import (
    AttendanceRecordRepository,
    AttendanceSessionRepository,
)
from app.features.attendance.schema import (
    AttendanceRecordCreate,
    AttendanceRecordResponse,
    AttendanceSessionCreate,
    AttendanceSessionResponse,
    AttendanceSummaryResponse,
    BulkAttendanceCreate,
    BulkAttendanceResponse,
)
from app.features.attendance.service import (
    AttendanceRecordService,
    AttendanceSessionService,
)
from app.features.courses.repository import CourseRepository
from app.features.departments.repository import DepartmentRepository
from app.features.enrollments.repository import EnrollmentRepository
from app.features.students.repository import StudentRepository

router = APIRouter(
    prefix="/attendance/sessions",
    tags=["Attendance"],
)
record_router = APIRouter(
    prefix="/attendance/records",
    tags=["Attendance"],
)
attendance_router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


def get_attendance_service(
    db: AsyncSession = Depends(get_db),
) -> AttendanceSessionService:
    repository = AttendanceSessionRepository(db)
    course_repository = CourseRepository(db)
    department_repository = DepartmentRepository(db)
    return AttendanceSessionService(
        repository,
        course_repository,
        department_repository,
    )


def get_attendance_record_service(
    db: AsyncSession = Depends(get_db),
) -> AttendanceRecordService:
    record_repository = AttendanceRecordRepository(db)
    session_repository = AttendanceSessionRepository(db)
    student_repository = StudentRepository(db)
    enrollment_repository = EnrollmentRepository(db)

    return AttendanceRecordService(
        record_repository, session_repository, student_repository, enrollment_repository
    )


@router.post(
    "",
    response_model=AttendanceSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_attendance_session(
    data: AttendanceSessionCreate,
    service: AttendanceSessionService = Depends(get_attendance_service),
):
    session = AttendanceSession(**data.model_dump())

    return await service.create_session(session)


@router.get(
    "/{session_id}",
    response_model=AttendanceSessionResponse,
)
async def get_attendance_session(
    session_id: UUID,
    service: AttendanceSessionService = Depends(get_attendance_service),
):
    session = await service.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance session with id '{session_id}' was not found",
        )

    return session


@record_router.post(
    "",
    response_model=AttendanceRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_attendance_record(
    data: AttendanceRecordCreate,
    service: AttendanceRecordService = Depends(get_attendance_record_service),
):
    record = AttendanceRecord(**data.model_dump())

    return await service.create_record(record)


@record_router.get(
    "/{record_id}",
    response_model=AttendanceRecordResponse,
)
async def get_attendance_record(
    record_id: UUID,
    service: AttendanceRecordService = Depends(get_attendance_record_service),
):
    record = await service.get_record(record_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with id '{record_id}' was not found",
        )

    return record


@record_router.post(
    "/sessions/{session_id}/records",
    response_model=BulkAttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_bulk_attendance(
    session_id: UUID,
    data: BulkAttendanceCreate,
    service: AttendanceRecordService = Depends(get_attendance_record_service),
):
    records = [
        AttendanceRecord(
            session_id=session_id,
            student_id=record.student_id,
            status=record.status,
        )
        for record in data.records
    ]

    created_records = await service.create_bulk_records(
        session_id,
        records,
    )

    return BulkAttendanceResponse(
        session_id=session_id,
        records=[
            AttendanceRecordResponse.model_validate(record)
            for record in created_records
        ],
    )


@attendance_router.get(
    "",
    response_model=AttendanceSummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_attendance_summary(
    student: UUID,
    course: UUID,
    session: AsyncSession = Depends(get_db),
) -> AttendanceSummaryResponse:
    service = AttendanceRecordService(
        AttendanceRecordRepository(session),
        AttendanceSessionRepository(session),
        StudentRepository(session),
        EnrollmentRepository(session),
    )

    summary = await service.get_student_course_summary(
        student,
        course,
    )

    return AttendanceSummaryResponse(**summary)
