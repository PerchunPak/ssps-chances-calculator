import strawberry


@strawberry.type
class Points:
    mat: int | float
    czl: int | float | None  # CZech Language
    ict: int
    other: int  # portfolio, motivation letter, interview


@strawberry.type
class Student:
    place: int  # WARN: Is not unique when total_points are equal; but only if two people (see it 2023 103)
    school_id: str
    original_points: Points
    school_points: Points
    total_points: float
    reduced_ranking: (
        int | None
    )  # redukované pořadí; can be 0 if student was accepted


@strawberry.type
class Year:
    it: list[Student]
    hacking: list[Student]
    gymnasium: list[Student]


@strawberry.type
class Query:
    year2023: Year


schema = strawberry.Schema(query=Query)
