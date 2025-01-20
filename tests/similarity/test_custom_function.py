from typing import TypeVar

import unittest

from casebased.components.similarity_measure import SimilarityFunction

T = TypeVar("T")


class CustomFunction(SimilarityFunction):
    def __init__(self, growth: float):
        self.__growth = growth

    def calculate(self, x: T, y: T) -> float:
        return x * y * self.__growth


TEST_CASES = [
    {
        "x": 20,
        "y": 12.134,
        "growth": 2.420,
        "result": 587.2856,
    }
]


class TestCustomSimilarityFunction(unittest.TestCase):
    def test_custom_distance_function(self):
        for case in TEST_CASES:
            dist = CustomFunction(case.get("growth")).calculate(
                case.get("x"), case.get("y")
            )
            self.assertEqual(dist, case.get("result"))
