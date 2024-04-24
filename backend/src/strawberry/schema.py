import typing as t

import typing_extensions as te

import strawberry
from src import models
from src.db import Database


@strawberry.type
class IntContainer:
    content: int


@strawberry.type
class FloatContainer:
    content: float


@strawberry.type
class Points:
    mat: t.Annotated[
        IntContainer | FloatContainer, strawberry.union("IntOrFloat")
    ]
    # CZech Language
    czl: t.Annotated[
        IntContainer | FloatContainer | None,
        strawberry.union("IntOrFloatOrNone"),
    ]
    ict: int
    other: int  # portfolio, motivation letter, interview

    @classmethod
    def from_db_model(cls, points: models.Points) -> te.Self:
        return cls(
            mat=points.mat,
            czl=points.czl,
            ict=points.ict,
            other=points.other,
        )


@strawberry.type
class Student:
    # WARN:
    # Place can be not unique, if TWO people have the same `total_points`
    # If three people have the same total score, it is two places
    # (see 2023 IT place 203 for what I mean)
    place: int
    school_id: str
    original_points_id: strawberry.Private[str]
    school_points_id: strawberry.Private[str]
    total_points: float
    reduced_ranking: (  # redukované pořadí; can be 0 if student was accepted
        t.Annotated[IntContainer | None, strawberry.union("IntOrNone")]
    )

    @classmethod
    def from_db_model(cls, student: models.Student) -> te.Self:
        return cls(
            place=student.place,
            school_id=student.school_id,
            original_points_id=student.original_points_id,
            school_points_id=student.school_points_id,
            total_points=student.total_points,
            reduced_ranking=student.reduced_ranking,
        )

    @strawberry.field
    async def original_points(self) -> Points:
        db = await Database.setup()
        return Points.from_db_model(
            await db.get_points_by_id(self.original_points_id)
        )

    @strawberry.field
    async def school_points(self) -> Points:
        db = await Database.setup()
        return Points.from_db_model(
            await db.get_points_by_id(self.school_points_id)
        )


@strawberry.type
class Year:
    _year: strawberry.Private[int]
    # hacking: list[Student]
    # gymnasium: list[Student]

    @strawberry.field
    async def it(self, info: strawberry.Info) -> list[Student]:
        db = await Database.setup()
        students = await db.get_all_students(self._year, info.field_name)

        to_return: list[Students] = []
        for student in students:
            to_return.append(Student.from_db_model(student))
        return to_return


@strawberry.type
class Query:
    @strawberry.field
    async def year2023(self, info: strawberry.Info) -> Year:
        return Year(_year=int(info.field_name.removeprefix("year")))


schema = strawberry.Schema(query=Query)
