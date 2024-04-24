import sqlite3
from pathlib import Path

from src.student import Student
from src.utils import DATA_DIR

DB_PATH = DATA_DIR / "database.db"


class Database:
    def __init__(self, table_name: str) -> None:
        self._table_name = table_name

        self._connection = sqlite3.connect(str(DB_PATH))
        self._cursor = self._connection.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS points (
                id      TEXT PRIMARY KEY,
                mat     REAL NOT NULL,
                czl     REAL,
                ict     NUMBER NOT NULL,
                other   NUMBER NOT NULL
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
                reduced_ranking       INTEGER,

                FOREIGN KEY(original_points_id) REFERENCES points(id),
                FOREIGN KEY(school_points_id) REFERENCES points(id)
            )
            """,
        )

    def add_student(self, student: Student) -> None:
        original_points_id, school_points_id = (
            student.original_points.as_hash(),
            student.school_points.as_hash(),
        )

        for id, points in (
            (original_points_id, student.original_points),
            (school_points_id, student.school_points),
        ):
            try:
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
            except sqlite3.IntegrityError as e:
                # two students have completely identical points!
                if e.args != ("UNIQUE constraint failed: points.id",):
                    raise

        self._cursor.execute(
            f"""
            INSERT INTO {self._table_name} (place, school_id, original_points_id, school_points_id, total_points, reduced_ranking)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student.place,
                student.school_id,
                original_points_id,
                school_points_id,
                student.total_points,
                student.reduced_ranking,
            ),
        )
        self._connection.commit()
