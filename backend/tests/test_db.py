import dataclasses
import json
import typing as t

import pytest

from src.db import Database
from src.models import Points, Student
from src.utils import DATA_DIR

TEST_DB_FILE = DATA_DIR / "test_db.json"


@dataclasses.dataclass
class StudentWithPoints(Student):
    original_points: Points
    school_points: Points

    def as_student(self) -> Student:
        as_dict = dataclasses.asdict(self)
        del as_dict["original_points"], as_dict["school_points"]
        return Student(**as_dict)


@pytest.fixture(scope="session")
async def db() -> Database:
    return await Database.setup()


def get_years_and_fields_to_test() -> t.Iterable[tuple[int, str]]:
    with TEST_DB_FILE.open("r") as f:
        test_db = json.load(f)

    for year, value in test_db.items():
        for field in value.keys():
            yield year, field


def get_all_students(year: int, field: str) -> list[StudentWithPoints]:
    with TEST_DB_FILE.open("r") as f:
        list_as_dict = json.load(f)
        list_as_dict = list_as_dict[str(year)][field]

    students: list[StudentWithPoints] = []
    for as_dict in list_as_dict.values():
        as_dict["original_points"] = Points(id=as_dict["original_points_id"], **as_dict["original_points"])
        as_dict["school_points"] = Points(id=as_dict["school_points_id"], **as_dict["school_points"])

        students.append(StudentWithPoints(**as_dict))

    return students


@pytest.mark.parametrize("year,field", get_years_and_fields_to_test())
async def test_get_all_students(db: Database, year: int, field: str) -> None:
    """That table must not change, and if it will - it is an error."""
    students_from_db = await db.get_all_students(year, field)
    students_that_should_exist = get_all_students(year, field)
    students_that_should_exist = list(map(lambda x: x.as_student(), students_that_should_exist))
    assert students_from_db == students_that_should_exist


@pytest.mark.parametrize("year,field", get_years_and_fields_to_test())
async def test_student_points(db: Database, year: int, field: str) -> None:
    students_from_db = await db.get_all_students(year, field)
    students_that_should_exist = get_all_students(year, field)
    for i, student in enumerate(students_from_db):
        original_points = await db.get_points_by_id(student.original_points_id)
        school_points = await db.get_points_by_id(student.school_points_id)

        assert original_points == students_that_should_exist[i].original_points
        assert school_points == students_that_should_exist[i].school_points
