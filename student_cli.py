import sys

from students.export import export_to_csv, export_to_json
from students.manager import (
    add_student,
    add_grade,
    remove_grade,
    remove_student,
    get_top_students,
    list_students,
    search_student_by_id,
    update_grade,
)
from students.utils import InvalidStudentError


def print_student(student: dict) -> None:
    print("------ STUDENT ------")
    print(f"ID      : {student['id']}")
    print(f"Name    : {student['name']}")
    print(f"Email   : {student['email']}")
    print(f"Grades  : {student['grades']}")
    if "average" in student:
        print(f"Average : {student['average']}")
    print("---------------------")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print("python student_cli.py list")
        print("python student_cli.py search <student_id>")
        print("python student_cli.py add <name> <id> <email> <grade1> [grade2 ...]")
        print("python student_cli.py update-grade <id> <grade_index> <new_grade>")
        print("python student_cli.py add-grade <student_id> <grade>")
        print("python student_cli.py remove-grade <student_id> <grade_index>")
        print("python student_cli.py remove-student <student_id>")
        print("python student_cli.py top")
        print("python student_cli.py export-json")
        print("python student_cli.py export-csv")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "list":
            students = list_students()
            if not students:
                print("No students found")
            else:
                for student in students:
                    print_student(student)

        elif command == "search":
            if len(sys.argv) != 3:
                print("Usage: python student_cli.py search <student_id>")
                sys.exit(1)

            student = search_student_by_id(sys.argv[2])
            if student is None:
                print("Student not found")
            else:
                print_student(student)

        elif command == "add":
            if len(sys.argv) < 6:
                print(
                    "Usage: python student_cli.py add <name> <id> <email> <grade1> [grade2 ...]"
                )
                sys.exit(1)

            name = sys.argv[2]
            student_id = sys.argv[3]
            email = sys.argv[4]
            grades = [float(grade) for grade in sys.argv[5:]]

            add_student(name, student_id, email, grades)
            print("Student added successfully")

        elif command == "update-grade":
            if len(sys.argv) != 5:
                print(
                    "Usage: python student_cli.py update-grade <id> <grade_index> <new_grade>"
                )
                sys.exit(1)

            update_grade(
                sys.argv[2],
                int(sys.argv[3]),
                float(sys.argv[4]),
            )

            print("Grade updated successfully")

        elif command == "add-grade":
            if len(sys.argv) != 4:
                print("Usage: python student_cli.py add-grade <student_id> <grade>")
                sys.exit(1)

            add_grade(
                sys.argv[2],
                float(sys.argv[3]),
            )

            print("Grade added successfully")

        elif command == "remove-grade":
            if len(sys.argv) != 4:
                print(
                    "Usage: python student_cli.py remove-grade <student_id> <grade_index>"
                )
                sys.exit(1)

            remove_grade(
                sys.argv[2],
                int(sys.argv[3]),
            )

            print("Grade removed successfully")

        elif command == "remove-student":
            if len(sys.argv) != 3:
                print("Usage: python student_cli.py remove-student <student_id>")
                sys.exit(1)

            remove_student(sys.argv[2])

            print("Student removed successfully")

        elif command == "top":
            students = get_top_students()

            if not students:
                print("No students found")
            else:
                for student in students:
                    print_student(student)

        elif command == "export-json":
            export_to_json()
            print("Students exported to JSON successfully")

        elif command == "export-csv":
            export_to_csv()
            print("Students exported to CSV successfully")

        else:
            print("Invalid command")
            sys.exit(1)

    except InvalidStudentError as error:
        print(f"Invalid input: {error}")
        sys.exit(1)
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
