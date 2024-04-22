import sqlite3
import uuid
from pathlib import Path

from src.student import Student


class Database:
    def __init__(self, db_path: Path, table_name: str) -> None:
        self._db_path = db_path
        self._table_name = table_name

        self._connection = sqlite3.connect(str(db_path))
        self._cursor = self._connection.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS points (
                id      TEXT PRIMARY KEY,
                mat     REAL NOT NULL,
                czl     REAL,
                ict     NUMBER,
                other   NUMBER
            )
            """
        )
        self._cursor.execute(
            f"""
            CREATE TABLE {self._table_name} (
                place                 INTEGER NOT NULL,
                school_id             TEXT PRIMARY KEY,
                original_points_id    TEXT NOT NULL,
                school_points_id      TEXT NOT NULL,
                total_points          REAL NOT NULL,

                FOREIGN KEY(original_points_id) REFERENCES points(id),
                FOREIGN KEY(school_points_id) REFERENCES points(id)
            )
            """,
        )

    def add_student(self, student: Student) -> None:
        original_points_id, school_points_id = str(uuid.uuid4()), str(uuid.uuid4())

        for id, points in (
            (original_points_id, student.original_points),
            (school_points_id, student.school_points),
        ):
            self._cursor.execute(
                """
                INSERT INTO points (id, mat, czl, ict, other)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    id,
                    points.mat,
                    points.czl,
                    points.ict,
                    points.other,
                ),
            )

        self._cursor.execute(
            f"""
            INSERT INTO {self._table_name} (place, school_id, original_points_id, school_points_id, total_points)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student.place,
                student.school_id,
                original_points_id,
                school_points_id,
                student.total_points,
            ),
        )
        self._connection.commit()
