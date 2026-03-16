import csv
import json

from students.manager import list_students


def export_to_json(
    output_file: str = "students_export.json", file_path: str = "students.json"
) -> None:
    students = list_students(file_path)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def export_to_csv(
    output_file: str = "students_export.csv", file_path: str = "students.json"
) -> None:
    students = list_students(file_path)

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Email", "Grades", "Average"])

        for student in students:
            writer.writerow(
                [
                    student["id"],
                    student["name"],
                    student["email"],
                    ", ".join(map(str, student["grades"])),
                    student["average"],
                ]
            )
