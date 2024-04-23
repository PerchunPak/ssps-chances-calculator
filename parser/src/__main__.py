import dataclasses
import json
import re
import sys
import typing as t
from pathlib import Path

from src.db import Database
from src.student import Student
from src.test_representation import TestRepresentation

SEPARATOR_REGEX = re.compile(r"\s+")


def main() -> None:
    csv_table_path = Path(sys.argv[1])
    year = int(sys.argv[2])
    field = sys.argv[3]
    result_path = Path(sys.argv[4])

    students: list[Student] = []
    with csv_table_path.open("r") as csv_table_file:
        for line in csv_table_file.readlines():
            as_list = re.split(SEPARATOR_REGEX, line.rstrip("\n"), 13)
            students.append(Student.parse(as_list))
    print(f"Found {len(students)} students, last is on {students[-1].place} place!")

    db = Database(result_path / "database.db", f"year{year}{field}")
    test_representation = TestRepresentation(result_path / "test_db.json", str(year), field)
    for student in students:
        original_points_id, school_points_id = db.add_student(student)
        test_representation.add_student(student, original_points_id, school_points_id)

    test_representation.write()


if __name__ == "__main__":
    main()
