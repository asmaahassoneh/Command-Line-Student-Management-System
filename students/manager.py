import json
from pathlib import Path

from students.utils import (
    InvalidStudentError,
    validate_email,
    validate_grade,
    validate_name,
    validate_student_id,
)

DEFAULT_STUDENTS = {}


def load_students(file_path: str = "students.json") -> dict:
    path = Path(file_path)

    if not path.exists():
        save_students(DEFAULT_STUDENTS, file_path)
        return DEFAULT_STUDENTS.copy()

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            save_students(DEFAULT_STUDENTS, file_path)
            return DEFAULT_STUDENTS.copy()

        return data

    except json.JSONDecodeError:
        save_students(DEFAULT_STUDENTS, file_path)
        return DEFAULT_STUDENTS.copy()


def save_students(students: dict, file_path: str = "students.json") -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def _get_students(file_path: str) -> dict:
    return load_students(file_path)


def _get_existing_student(students: dict, student_id: str) -> dict:
    validate_student_id(student_id)

    if student_id not in students:
        raise ValueError("Student not found")

    return students[student_id]


def add_student(
    name: str,
    student_id: str,
    email: str,
    grades: list[float],
    file_path: str = "students.json",
) -> None:
    validate_name(name)
    validate_student_id(student_id)
    validate_email(email)

    if not isinstance(grades, list) or not grades:
        raise InvalidStudentError("Grades must be a non-empty list")

    for grade in grades:
        validate_grade(grade)

    students = _get_students(file_path)

    if student_id in students:
        raise ValueError("A student with this ID already exists")

    if any(info["email"] == email for info in students.values()):
        raise ValueError("A student with this email already exists")

    students[student_id] = {
        "name": name,
        "email": email,
        "grades": grades,
    }

    save_students(students, file_path)


def remove_student(student_id: str, file_path: str = "students.json") -> None:
    students = _get_students(file_path)
    _get_existing_student(students, student_id)

    del students[student_id]
    save_students(students, file_path)


def search_student_by_id(
    student_id: str,
    file_path: str = "students.json",
) -> dict | None:
    validate_student_id(student_id)

    students = _get_students(file_path)
    info = students.get(student_id)

    if info is None:
        return None

    return {
        "id": student_id,
        "name": info["name"],
        "email": info["email"],
        "grades": info["grades"],
    }


def update_grade(
    student_id: str,
    grade_index: int,
    new_grade: float,
    file_path: str = "students.json",
) -> None:
    validate_grade(new_grade)

    if not isinstance(grade_index, int):
        raise ValueError("Grade index must be an integer")

    students = _get_students(file_path)
    student = _get_existing_student(students, student_id)
    grades = student["grades"]

    if grade_index < 0 or grade_index >= len(grades):
        raise ValueError("Invalid grade index")

    grades[grade_index] = new_grade
    save_students(students, file_path)


def add_grade(
    student_id: str,
    grade: float,
    file_path: str = "students.json",
) -> None:
    validate_grade(grade)

    students = _get_students(file_path)
    student = _get_existing_student(students, student_id)

    student["grades"].append(grade)
    save_students(students, file_path)


def remove_grade(
    student_id: str,
    grade_index: int,
    file_path: str = "students.json",
) -> None:
    if not isinstance(grade_index, int):
        raise ValueError("Grade index must be an integer")

    students = _get_students(file_path)
    student = _get_existing_student(students, student_id)
    grades = student["grades"]

    if len(grades) == 1:
        raise ValueError("Cannot remove the last grade")

    if grade_index < 0 or grade_index >= len(grades):
        raise ValueError("Invalid grade index")

    del grades[grade_index]
    save_students(students, file_path)


def list_students(file_path: str = "students.json") -> list[dict]:
    students = _get_students(file_path)
    result = []

    for student_id, info in sorted(
        students.items(),
        key=lambda item: item[1]["name"],
    ):
        grades = info["grades"]
        average = round(sum(grades) / len(grades), 2)

        result.append(
            {
                "id": student_id,
                "name": info["name"],
                "email": info["email"],
                "grades": grades,
                "average": average,
            }
        )

    return result


def get_top_students(
    file_path: str = "students.json",
    limit: int = 3,
) -> list[dict]:
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer")

    students = list_students(file_path)
    return sorted(
        students,
        key=lambda student: student["average"],
        reverse=True,
    )[:limit]
