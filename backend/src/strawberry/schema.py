import strawberry


@strawberry.type
class Points:
    mat: int | float
    czl: int | float | None  # CZech Language
    ict: int
    other: int  # portfolio, motivation letter, interview


@strawberry.type
class Student:
    # WARN:
    # Place can be not unique, if TWO people have the same `total_points`
    # If three people have the same total score, it is two places
    # (see 2023 IT place 203 for what I mean)
    place: int
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
