import unittest

from casebased.components.similarity_measure.functions import (
    Equality,
    Static,
    VectorDifference,
)

TEST_CASES_EQUALITY = [
    {
        "x": 10,
        "y": 5,
        "result": 0.0,
    },
    {
        "x": 5,
        "y": 5,
        "result": 1.0,
    },
]

TEST_CASES_VECTOR_DISTANCE = [
    {
        "x": [12, 1, 3],
        "y": [1, 25, 10],
        "result": 42.0,
    },
    {
        "x": [12, 1, 3],
        "y": [1, 25],
        "result": 38.0,
    },
]


class TestGenericSimilarityFunctions(unittest.TestCase):
    def test_equality_distance(self):
        for case in TEST_CASES_EQUALITY:
            dist = Equality().calculate(case.get("x"), case.get("y"))
            self.assertEqual(dist, case.get("result"))

    def test_static_distance(self):
        dist = Static(0.5).calculate(10, 5)
        self.assertEqual(dist, 0.5)

    def test_vector_distance(self):
        for case in TEST_CASES_VECTOR_DISTANCE:
            dist = VectorDifference().calculate(case.get("x"), case.get("y"))
            self.assertEqual(dist, case.get("result"))
