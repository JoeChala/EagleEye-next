from uuid import UUID


class StudentAlreadyExistsError(Exception):
    def __init__(self, roll_number: str):
        super().__init__(f"Student with roll number '{roll_number}' already exists")


class StudentNotFoundError(Exception):
    def __init__(self, student_id: UUID):
        super().__init__(f"Student with id '{student_id}' was not found")
