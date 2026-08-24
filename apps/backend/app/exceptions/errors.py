from uuid import UUID


class StudentAlreadyExistsError(Exception):
    def __init__(self, roll_number: str):
        super().__init__(f"Student with roll number '{roll_number}' already exists")


class StudentNotFoundError(Exception):
    def __init__(self, student_id: UUID):
        super().__init__(f"Student with id '{student_id}' was not found")


class FacultyAlreadyExistsError(Exception):
    def __init__(self, employee_id: str):
        super().__init__(f"Faculty with employee id '{employee_id}' already exists")


class FacultyNotFoundError(Exception):
    def __init__(self, faculty_id: UUID):
        super().__init__(f"Faculty with id '{faculty_id}' was not found")


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
