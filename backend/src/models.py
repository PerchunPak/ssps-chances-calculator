# for documentation see src/strawberry/schema.py
import dataclasses

import typing_extensions as te


@dataclasses.dataclass
class Student:
    place: int
    school_id: str
    original_points_id: str
    school_points_id: str
    total_points: float
    reduced_ranking: int | None


@dataclasses.dataclass
class Points:
    id: str
    mat: float
    czl: float | None
    ict: int
    other: int
