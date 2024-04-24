import dataclasses
import hashlib

import typing_extensions as te


def parse_reduced_ranking(as_list: list[str]) -> int | None:
    if len(as_list) < 13:
        return None

    if as_list[12] == "Uchazeč přijat na základě redukovaného pořadí":
        return 0

    return int(
        as_list[12]
        .removeprefix("Uchazeč se umístil na základě redukovaného pořadí na ")
        .removesuffix(". místě.")
    )


@dataclasses.dataclass
class Points:
    mat: int | float
    czl: int | float | None
    ict: int
    other: int

    @classmethod
    def parse_original(cls, as_list: list[str]) -> te.Self:
        return cls(
            mat=int(as_list[2]),
            czl=int(as_list[3]) if as_list[3] != -1 else None,
            ict=int(as_list[4]),
            other=int(as_list[5]),
        )

    @classmethod
    def parse_school(cls, as_list: list[str]) -> te.Self:
        return cls(
            mat=float(as_list[6].replace(",", ".")),
            czl=float(as_list[7].replace(",", ".")),
            ict=int(as_list[9]),
            other=int(as_list[10]),
        )

    def as_hash(self) -> str:
        hash = hashlib.sha256()
        hash.update(str(self).encode())
        return hash.hexdigest()


@dataclasses.dataclass
class ParentStudent:  # for tests
    place: int
    school_id: str
    total_points: float
    reduced_ranking: int | None  # redukované pořadí


@dataclasses.dataclass
class Student(ParentStudent):
    original_points: Points
    school_points: Points

    @classmethod
    def parse(cls, as_list: list[str]) -> te.Self:
        if as_list[3] == "JPZ":  # means it is Ukrainian, skipped Czech exam
            as_list[3] = -1
            del as_list[4]

        return cls(
            place=int(as_list[0]),
            school_id=as_list[1],
            original_points=Points.parse_original(as_list),
            school_points=Points.parse_school(as_list),
            total_points=float(as_list[11].replace(",", ".")),
            reduced_ranking=parse_reduced_ranking(as_list),
        )
