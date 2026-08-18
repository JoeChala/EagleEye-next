class StudentAlreadyExistsError(Exception):
    def __init__(self, roll_number: str):
        super().__init__(f"Student with roll number '{roll_number}' already exists")
