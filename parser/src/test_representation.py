import dataclasses
import json
from pathlib import Path

from src.student import Student


class TestRepresentation:
    def __init__(self, result_file: Path, year: str, field: str) -> None:
        self._result_file = result_file
        self._year = year
        self._field = field

        if result_file.exists():
            with result_file.open("r") as f:
                self._parsed = json.load(f)
        else:
            self._parsed = {}

        self._parsed.setdefault(year, {})
        self._parsed[year].setdefault(field, {})
        self._data = self._parsed[year][field]

    def save(self) -> None:
        with self._result_file.open("w") as f:
            json.dump(self._parsed, f, indent=2, ensure_ascii=False)

    def add_student(self, student: Student) -> None:
        self._data[student.school_id] = dataclasses.asdict(student)
        self._data[student.school_id].update(
            {
                "original_points_id": student.original_points.as_hash(),
                "school_points_id": student.school_points.as_hash(),
            }
        )
