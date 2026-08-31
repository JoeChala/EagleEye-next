from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import check_database_connection
from app.features.attendance.router import record_router
from app.features.attendance.router import router as attendance_router
from app.features.courses.router import router as course_router
from app.features.departments.router import router as department_router
from app.features.enrollments.router import router as enrollment_router
from app.features.faculty.router import router as faculty_router
from app.features.students.router import router as student_router
from app.utils.responses import error_response, success_response

api_router = APIRouter(prefix=settings.api_prefix)
api_router.include_router(department_router)
api_router.include_router(student_router)
api_router.include_router(faculty_router)
api_router.include_router(course_router)
api_router.include_router(attendance_router)
api_router.include_router(record_router)
api_router.include_router(enrollment_router)


@api_router.get("/health")
async def health() -> JSONResponse:
    database_status = await check_database_connection()
    if database_status["connected"]:
        return success_response(
            message="Health check successful",
            data={
                "application": {"status": "ok"},
                "database": database_status,
            },
        )

    return error_response(
        message="Health check degraded",
        status_code=503,
        errors=[
            {
                "application": {"status": "ok"},
                "database": database_status,
            }
        ],
    )


@api_router.get("/version")
async def version() -> JSONResponse:
    return success_response(
        message="Application version",
        data={"name": settings.app_name, "version": settings.app_version},
    )
