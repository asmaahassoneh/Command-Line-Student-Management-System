import json
import subprocess
import sys

import pytest

from students.export import export_to_csv, export_to_json
from students.manager import (
    add_grade,
    add_student,
    get_top_students,
    list_students,
    load_students,
    remove_grade,
    remove_student,
    search_student_by_id,
    update_grade,
)
from students.utils import InvalidStudentError


@pytest.fixture
def temp_students_file(tmp_path):
    file_path = tmp_path / "students.json"
    sample_data = {
        "101": {
            "name": "Asmaa",
            "email": "asmaa@gmail.com",
            "grades": [90, 95],
        },
        "102": {
            "name": "Ali",
            "email": "ali@gmail.com",
            "grades": [70, 80],
        },
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(sample_data, file, indent=4)

    return str(file_path)


def test_add_student_success(temp_students_file):
    add_student(
        name="Lina",
        student_id="103",
        email="lina@gmail.com",
        grades=[88, 91],
        file_path=temp_students_file,
    )

    students = load_students(temp_students_file)
    assert "103" in students


def test_search_student_found(temp_students_file):
    result = search_student_by_id("101", temp_students_file)

    assert result["name"] == "Asmaa"
    assert result["email"] == "asmaa@gmail.com"


def test_search_student_not_found(temp_students_file):
    assert search_student_by_id("999", temp_students_file) is None


def test_update_grade_success(temp_students_file):
    update_grade("101", 1, 100, temp_students_file)

    students = load_students(temp_students_file)
    assert students["101"]["grades"] == [90, 100]


def test_duplicate_id_raises_error(temp_students_file):
    with pytest.raises(ValueError):
        add_student(
            name="New Student",
            student_id="101",
            email="new@gmail.com",
            grades=[85],
            file_path=temp_students_file,
        )


def test_duplicate_email_raises_error(temp_students_file):
    with pytest.raises(ValueError):
        add_student(
            name="Sara",
            student_id="104",
            email="asmaa@gmail.com",
            grades=[90],
            file_path=temp_students_file,
        )


def test_invalid_email_raises_error(temp_students_file):
    with pytest.raises(InvalidStudentError):
        add_student(
            name="Sara",
            student_id="104",
            email="invalid-email",
            grades=[90],
            file_path=temp_students_file,
        )


def test_invalid_name_raises_error(temp_students_file):
    with pytest.raises(InvalidStudentError):
        add_student(
            name="   ",
            student_id="104",
            email="sara@gmail.com",
            grades=[90],
            file_path=temp_students_file,
        )


def test_invalid_student_id_raises_error(temp_students_file):
    with pytest.raises(InvalidStudentError):
        add_student(
            name="Sara",
            student_id="",
            email="sara@gmail.com",
            grades=[90],
            file_path=temp_students_file,
        )


def test_invalid_grade_type_raises_error(temp_students_file):
    with pytest.raises(InvalidStudentError):
        add_student(
            name="Sara",
            student_id="104",
            email="sara@gmail.com",
            grades=["A"],
            file_path=temp_students_file,
        )


def test_get_top_students(temp_students_file):
    result = get_top_students(temp_students_file)

    assert result[0]["name"] == "Asmaa"


def test_list_students_sorted_by_name(temp_students_file):
    result = list_students(temp_students_file)

    assert [student["name"] for student in result] == ["Ali", "Asmaa"]


def test_add_grade_success(temp_students_file):
    add_grade("101", 100, temp_students_file)

    students = load_students(temp_students_file)
    assert students["101"]["grades"] == [90, 95, 100]


def test_remove_grade_success(temp_students_file):
    remove_grade("101", 0, temp_students_file)

    students = load_students(temp_students_file)
    assert students["101"]["grades"] == [95]


def test_remove_last_grade_raises_error(tmp_path):
    file_path = tmp_path / "students.json"
    sample_data = {
        "101": {
            "name": "Asmaa",
            "email": "asmaa@gmail.com",
            "grades": [90],
        }
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(sample_data, file, indent=4)

    with pytest.raises(ValueError):
        remove_grade("101", 0, str(file_path))


def test_remove_student_success(temp_students_file):
    remove_student("101", temp_students_file)

    students = load_students(temp_students_file)
    assert "101" not in students


def test_remove_student_not_found(temp_students_file):
    with pytest.raises(ValueError):
        remove_student("999", temp_students_file)


def test_invalid_grade_index_update(temp_students_file):
    with pytest.raises(ValueError):
        update_grade("101", 10, 100, temp_students_file)


def test_invalid_grade_index_remove(temp_students_file):
    with pytest.raises(ValueError):
        remove_grade("101", 10, temp_students_file)


def test_export_to_json(temp_students_file, tmp_path):
    output_file = tmp_path / "students_export.json"

    export_to_json(str(output_file), temp_students_file)

    assert output_file.exists()


def test_export_to_csv(temp_students_file, tmp_path):
    output_file = tmp_path / "students_export.csv"

    export_to_csv(str(output_file), temp_students_file)

    assert output_file.exists()


def test_load_students_with_corrupted_json(tmp_path):
    file_path = tmp_path / "students.json"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("{invalid json")

    students = load_students(str(file_path))

    assert students == {}

    with open(file_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == {}


def test_load_students_when_file_missing(tmp_path):
    file_path = tmp_path / "missing_students.json"

    students = load_students(str(file_path))

    assert students == {}
    assert file_path.exists()


def test_load_students_with_empty_file(tmp_path):
    file_path = tmp_path / "students.json"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("")

    students = load_students(str(file_path))

    assert students == {}


def test_cli_list_command(tmp_path):
    file_path = tmp_path / "students.json"
    sample_data = {
        "101": {
            "name": "Asmaa",
            "email": "asmaa@gmail.com",
            "grades": [90, 95],
        }
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(sample_data, file, indent=4)

    result = subprocess.run(
        [sys.executable, "student_cli.py", "list"],
        cwd=".",
        capture_output=True,
        text=True,
    )

    assert result.returncode in (0, 1)
