# Command-Line Student Management System

This mini project implements a **Student Management System** that runs from the command line.

The system allows users to register students, manage their grades, list top students, and export student data to JSON or CSV files.

Student data is stored in a **`students.json`** file so it persists between program runs.

---

# Project Modules

The project is organized into modules inside the `students/` package.

- `student_cli.py` → command-line entry point  
- `students/manager.py` → student management logic  
- `students/utils.py` → validation functions and custom exceptions  
- `students/export.py` → export student data to JSON or CSV  
- `students.json` → persistent student storage

---

# Features

The system supports the following operations:

- Register a new student (name, ID, email, grades)
- Prevent duplicate **student IDs** and **emails**
- Validate student data
- Update an existing grade
- Add a new grade
- Remove a grade
- Remove a student
- List all students sorted by name
- Show **top students based on average grade**
- Export student data to **JSON**
- Export student data to **CSV**
- Handle invalid input using **custom exceptions**

---

# Example Student Structure

Students are stored in `students.json` in the following format:

```json
{
    "101": {
        "name": "Asmaa",
        "email": "asmaa@gmail.com",
        "grades": [90, 95]
    },
    "102": {
        "name": "Ali",
        "email": "ali@gmail.com",
        "grades": [70, 80]
    }
}
```
Each student contains:
- ID (dictionary key)
- name
- email
- grades (list of numbers between 0 and 100)
---

# Run the Student Management System
All commands are executed using the CLI script:
```python
python student_cli.py <command>
```
## List all students
```python
python student_cli.py list
```

Example output:
```
------ STUDENT ------
ID      : 101
Name    : Asmaa
Email   : asmaa@gmail.com
Grades  : [90, 95]
Average : 92.5
---------------------
```
---
## Search for a student by ID
```python
python student_cli.py search <student_id>
```
```python
python student_cli.py search 101
```

Example output:
```
------ STUDENT ------
ID      : 101
Name    : Asmaa
Email   : asmaa@gmail.com
Grades  : [90, 95]
---------------------
```

---
## Add a new student
CLI Script
```python
python student_cli.py add <name> <id> <email> <grade1> [grade2 ...]
```
```python
python student_cli.py add Lina 103 lina@gmail.com 88 91
```

Output:
```
Student added successfully
```
---

## Update a grade
CLI Script
```python
python student_cli.py update-grade <id> <grade_index> <new_grade>
```
```python
python student_cli.py update-grade 101 1 100
```

Output:
```
Grade updated successfully
```
---

## Add a grade
CLI Script
```python
python student_cli.py add-grade <student_id> <grade>
```
```python
python student_cli.py add-grade 101 85
```

Output:
```
Grade added successfully
```
---

## Remove a grade
CLI Script
```python
python student_cli.py remove-grade <student_id> <grade_index>
```
```python
python student_cli.py remove-grade 101 0
```

Output:
```
Grade removed successfully
```
---

## Remove a student
CLI Script
```python
python student_cli.py remove-student <student_id>
```
```python
python student_cli.py remove-student 101
```

Output:
```
Student removed successfully
```
---

## Show top students

```python
python student_cli.py top
```

The system returns the **top 3 students** based on their **average grade**.

---
## Export students to JSON
```python
python student_cli.py export-json
```
Creates:
```
students_export.json
```
## Export students to CSV
```python
python student_cli.py export-csv
```
Creates:
```
students_export.csv
```

---

## Input Validation

The system validates the following inputs:

- **student name**
- **student ID**
- **email format**
- **grades must be between 0 and 100**

Invalid inputs raise a custom exception:

```python
InvalidStudentError
```
Example error:
```
Invalid input: Email must be valid
```
---

## Testing

Unit tests are implemented using pytest.

Test files are located in:
```
tests/test_students.py
```
Run tests with:
```python
python -m pytest tests/test_students.py
```
Expected output:
```
tests/test_students.py ................
25 passed
```

---


# Project Structure

```
Command-Line Student Management System
│
├── student_cli.py
├── students.json
│
├── students
│   ├── __init__.py
│   ├── manager.py
│   ├── utils.py
│   └── export.py
│
├── tests
│   └── test_students.py
│
├── .gitignore
└── README.md
```
---

# Tools Used

* Python 3
* Virtual Environment (`venv`)
* flake8 (linting)
* black (code formatting)
* pytest (unit testing)

---

# Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install required tools:

```bash
pip install flake8 black pytest
```

Run linting and formatting:

```bash
flake8 .
black .
```

Run tests:

```bash
python -m pytest 
```