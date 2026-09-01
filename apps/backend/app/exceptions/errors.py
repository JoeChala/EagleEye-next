from uuid import UUID


class StudentAlreadyExistsError(Exception):
    def __init__(self, roll_number: str):
        super().__init__(f"Student with roll number '{roll_number}' already exists")


class StudentNotFoundError(Exception):
    def __init__(self, student_id: UUID):
        super().__init__(f"Student with id '{student_id}' was not found")


class DepartmentAlreadyExistsError(Exception):
    def __init__(self, code: str):
        super().__init__(f"Department with code '{code}' already exists")


class DepartmentNotFoundError(Exception):
    def __init__(self, department_id: UUID):
        super().__init__(f"Department with id '{department_id}' was not found")


class FacultyAlreadyExistsError(Exception):
    def __init__(self, employee_id: str):
        super().__init__(f"Faculty with employee id '{employee_id}' already exists")


class FacultyNotFoundError(Exception):
    def __init__(self, faculty_id: UUID):
        super().__init__(f"Faculty with id '{faculty_id}' was not found")


class CourseAlreadyExistsError(Exception):
    def __init__(self, code: str):
        super().__init__(f"Course with code '{code}' already exists")


class CourseNotFoundError(Exception):
    def __init__(self, course_id: UUID):
        super().__init__(f"Course with id '{course_id}' was not found")


class AttendanceAlreadyExistsError(Exception):
    def __init__(self, session_id, student_id):
        self.session_id = session_id
        self.student_id = student_id

        super().__init__(
            f"Attendance already exists for student '{student_id}' "
            f"in session '{session_id}'"
        )


class AttendanceSessionNotFoundError(Exception):
    def __init__(self, session_id):
        self.session_id = session_id

        super().__init__(f"Attendance session with id '{session_id}' was not found")


class AttendanceSessionDepartmentMismatchError(Exception):
    def __init__(self, course_id, department_id):
        self.course_id = course_id
        self.department_id = department_id

        super().__init__(
            "Attendance session department must match the course department "
            f"for course '{course_id}' and department '{department_id}'"
        )


class EnrollmentAlreadyExistsError(Exception):
    def __init__(self, student_id: UUID, course_id: UUID):
        super().__init__(
            f"Student '{student_id}' is already enrolled in course '{course_id}'"
        )


class EnrollmentNotFoundError(Exception):
    def __init__(self, enrollment_id: UUID):
        super().__init__(f"Enrollment with id '{enrollment_id}' was not found")


class InvalidEnrollmentError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class StudentCourseEnrollmentNotFoundError(Exception):
    def __init__(self, student_id: UUID, course_id: UUID):
        super().__init__(
            f"Enrollment for student '{student_id}' "
            f"in course '{course_id}' was not found"
        )


class StudentNotEnrolledError(Exception):
    def __init__(self, student_id: UUID, course_id: UUID):
        super().__init__(
            f"Student '{student_id}' is not enrolled in course '{course_id}'"
        )


class StudentSessionMismatchError(Exception):
    def __init__(self, student_id: UUID):
        super().__init__(
            f"Student '{student_id}' does not belong to "
            "the session's department, semester, and section"
        )
