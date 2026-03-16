class InvalidStudentError(Exception):
    """Raised when student data is invalid."""


def validate_name(name: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise InvalidStudentError("Name must be a non-empty string")


def validate_student_id(student_id: str) -> None:
    if not isinstance(student_id, str) or not student_id.strip():
        raise InvalidStudentError("Student ID must be a non-empty string")


def validate_email(email: str) -> None:
    if not isinstance(email, str) or not email.strip():
        raise InvalidStudentError("Email must be valid")

    email = email.strip()

    if email.count("@") != 1:
        raise InvalidStudentError("Email must be valid")

    local, domain = email.split("@")

    if not local or not domain or "." not in domain:
        raise InvalidStudentError("Email must be valid")


def validate_grade(grade: float) -> None:
    if not isinstance(grade, (int, float)):
        raise InvalidStudentError("Grade must be a number")

    if not 0 <= grade <= 100:
        raise InvalidStudentError("Grade must be between 0 and 100")
