from typing import TypeVar

from casebased.components.similarity_measure import SimilarityFunction

T = TypeVar("T")


class CustomFunction(SimilarityFunction):
    def __init__(self, growth: float):
        self.__growth = growth

    def calculate(self, x: T, y: T) -> float:
        return x * y * self.__growth


test_cases = [
    {
        "x": 20,
        "y": 12.134,
        "growth": 2.420,
        "result": 587.2856,
    }
]


def test_custom_distance_function():
    for case in test_cases:
        dist = CustomFunction(case.get("growth")).calculate(
            case.get("x"), case.get("y")
        )
        assert dist == case.get("result")
