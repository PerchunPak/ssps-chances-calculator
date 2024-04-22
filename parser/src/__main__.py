import re
import sys
from pathlib import Path

from src.db import Database
from src.student import Student

SEPARATOR_REGEX = re.compile(r"\s+")


def main() -> None:
    csv_table_path = Path(sys.argv[1])
    db_table_name = sys.argv[2]
    result_db_path = Path(sys.argv[3])

    students: list[Student] = []
    with csv_table_path.open("r") as csv_table_file:
        for line in csv_table_file.readlines():
            as_list = re.split(SEPARATOR_REGEX, line.rstrip("\n"), 13)
            students.append(Student.parse(as_list))
    print(f"Found {len(students)} students, last is on {students[-1].place} place!")

    db = Database(result_db_path, db_table_name)
    for student in students:
        db.add_student(student)


if __name__ == "__main__":
    main()
