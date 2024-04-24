import dataclasses
import json
import sqlite3
import typing as t

import pytest
import typing_extensions as te

from src.db import DB_PATH
from src.student import ParentStudent, Points, Student
from src.test_representation import TEST_DB_FILE


@dataclasses.dataclass
class DBStudent(ParentStudent):
    original_points_id: str
    school_points_id: str

    @classmethod
    def from_tuple(cls, as_tuple: tuple[t.Any, ...]) -> te.Self:  # type: ignore[misc]
        return cls(
            place=as_tuple[0],
            school_id=as_tuple[1],
            original_points_id=as_tuple[2],
            school_points_id=as_tuple[3],
            total_points=as_tuple[4],
            reduced_ranking=as_tuple[5],
        )


@dataclasses.dataclass
class StudentWithPointIds(Student, DBStudent):
    def as_student(self) -> Student:
        as_dict = dataclasses.asdict(self)
        del as_dict["original_points_id"], as_dict["school_points_id"]
        return Student(**as_dict)

    def as_db_student(self) -> DBStudent:
        as_dict = dataclasses.asdict(self)
        del as_dict["original_points"], as_dict["school_points"]
        return DBStudent(**as_dict)


@pytest.fixture(scope="session")
def db() -> sqlite3.Cursor:
    connection = sqlite3.connect(str(DB_PATH))
    return connection.cursor()


def get_years_and_fields_to_test() -> t.Iterable[tuple[int, str]]:
    with TEST_DB_FILE.open("r") as f:
        test_db = json.load(f)

    for year, value in test_db.items():
        for field in value.keys():
            yield year, field


def get_all_students(year: int, field: str) -> list[StudentWithPointIds]:
    with TEST_DB_FILE.open("r") as f:
        list_as_dict = json.load(f)
        list_as_dict = list_as_dict[str(year)][field]

    students: list[StudentWithPointIds] = []
    for as_dict in list_as_dict.values():
        as_dict["original_points"] = Points(**as_dict["original_points"])
        as_dict["school_points"] = Points(**as_dict["school_points"])

        students.append(StudentWithPointIds(**as_dict))

    return students


def get_points_by_id(db: sqlite3.Cursor, id: str) -> Points:
    result = db.execute("SELECT * FROM points WHERE id = ?", (id,)).fetchone()
    result = result[1:]
    return Points(*result)


@pytest.mark.parametrize("year,field", get_years_and_fields_to_test())
def test_get_all_students(db: sqlite3.Cursor, year: int, field: str) -> None:
    result = db.execute(f"SELECT * FROM year{year}{field}").fetchall()
    students_from_db = list(map(lambda s: DBStudent.from_tuple(s), result))

    students_that_should_exist = get_all_students(year, field)
    students_that_should_exist = list(
        map(lambda x: x.as_db_student(), students_that_should_exist)
    )

    assert students_from_db == students_that_should_exist


@pytest.mark.parametrize("year,field", get_years_and_fields_to_test())
def test_student_points(db: sqlite3.Cursor, year: int, field: str) -> None:
    result = db.execute(f"SELECT * FROM year{year}{field}").fetchall()
    students_from_db = list(map(lambda s: DBStudent.from_tuple(s), result))

    students_that_should_exist = get_all_students(year, field)
    for i, student in enumerate(students_from_db):
        original_points = get_points_by_id(db, student.original_points_id)
        school_points = get_points_by_id(db, student.school_points_id)

        assert original_points == students_that_should_exist[i].original_points
        assert school_points == students_that_should_exist[i].school_points
