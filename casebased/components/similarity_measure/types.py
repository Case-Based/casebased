from typing import Protocol, TypeVar

T = TypeVar("T")


class SimilarityFunction(Protocol):
    def calculate(self, x: T, y: T) -> float: ...
