import strawberry


@strawberry.type
class Points:
    mat: int
    czl: int  # CZech Language
    school_test: int
    other: int  # portfolio, not. letter, interview
    total: int  # provided by school, max 100


@strawberry.type
class Student:
    place: int  # TODO: is unique?
    school_id: str  # Identifikační číslo
    points: Points


@strawberry.type
class Year:
    it: list[Student]
    hacking: list[Student]
    gymnasium: list[Student]


@strawberry.type
class Query:
    year2023: Year


schema = strawberry.Schema(query=Query)
