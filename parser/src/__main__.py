import re
import sys
from pathlib import Path

from src.student import Student

SEPARATOR_REGEX = re.compile(r"\s+")


def main() -> None:
    csv_table_path = Path(sys.argv[1])
    db_table_name = sys.argv[2]
    result_db_path = Path(sys.argv[3])

    with csv_table_path.open("r") as csv_table_file:
        for line in csv_table_file.readlines():
            as_list = re.split(SEPARATOR_REGEX, line.rstrip("\n"), 13)
            student = Student.parse(as_list)
            print(student)


if __name__ == "__main__":
    main()
