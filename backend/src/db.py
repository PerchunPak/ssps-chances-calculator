import aiosqlite
import asyncache
import typing_extensions as te

from src import models, utils

DB_FILE = utils.DATA_DIR / "database.db"


class IncorrectDatabase(Exception):
    pass


class Database:
    def __init__(
        self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor
    ) -> None:
        self._connection = connection
        self._cursor = cursor

    @classmethod
    @asyncache.cached({})
    async def setup(cls) -> te.Self:
        connection = await aiosqlite.connect(DB_FILE)
        cursor = await connection.cursor()

        result = await cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table'
            """
        )
        table_names = list(map(lambda x: x[0], await result.fetchall()))
        if "points" not in table_names or not any(
            map(lambda x: x.startswith("year"), table_names)
        ):
            raise IncorrectDatabase(
                "Please init database using `parser` script, and then use it with this backend."
            )

        await connection.commit()
        return cls(connection, cursor)

    async def get_all_students(
        self, year: int, field: str, /
    ) -> list[models.Student]:
        result = await self._cursor.execute(
            f"""
            SELECT * FROM year{year}{field} -- Scary!
            """
        )
        return list(map(lambda x: models.Student(*x), await result.fetchall()))

    async def get_points_by_id(self, id: str, /) -> models.Points:
        result = await self._cursor.execute(
            """
            SELECT * FROM points
            WHERE id = ?
            """,
            (id,),
        )
        return models.Points(*await result.fetchone())
