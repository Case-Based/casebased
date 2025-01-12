import unittest

from casebased.components.similarity_measure.functions.numerical import (
    AbsoluteDistance,
    Exponential,
    Linear,
    LinearInterval,
    Sigmoid,
    SquaredDistance,
    Threshold,
)

test_cases_squared_absolute = [
    {
        "x": 10,
        "y": 20,
        "squared_result": 100,
        "absolute_result": 10,
    },
    {
        "x": 100,
        "y": 13,
        "squared_result": 7569,
        "absolute_result": 87,
    },
]

test_cases_linear_interval = [
    {"x": -2, "y": 0, "max": 100, "min": -1, "result": 0.0},
    {"x": 101, "y": 0, "max": 100, "min": -1, "result": 0.0},
    {"x": 0, "y": -2, "max": 100, "min": -1, "result": 0.0},
    {"x": 0, "y": 1, "max": 100, "min": 0, "result": 0.99},
    {"x": 0, "y": 101, "max": 100, "min": 0, "result": 0.0},
    {"x": 50, "y": 32, "max": 100, "min": 0, "result": 0.82},
]

test_cases_linear = [
    {
        "x": 10,
        "y": 5,
        "max": 15,
        "min": 6,
        "result": 1.0,
    },
    {
        "x": 10,
        "y": 5,
        "max": 4,
        "min": None,
        "result": 0.0,
    },
    {
        "x": 10,
        "y": 5,
        "max": 10,
        "min": None,
        "result": 0.5,
    },
    {
        "x": 13,
        "y": 5,
        "max": 10,
        "min": 5,
        "result": 0.4,
    },
]

test_cases_threshold = [
    {
        "x": 10,
        "y": 5,
        "threshold": 2,
        "result": 0.0,
    },
    {
        "x": 10,
        "y": 5,
        "threshold": 5,
        "result": 1.0,
    },
    {
        "x": 10,
        "y": 5,
        "threshold": 6,
        "result": 1.0,
    },
]

test_cases_exponential = [
    {
        "x": 10,
        "y": 5,
        "growth_value": 0.4,
        "result": 0.1353352832,
    },
    {
        "x": 15,
        "y": 9,
        "growth_value": 2.1,
        "result": 0.000003372,
    },
]

test_cases_sigmoid = [
    {
        "x": 10,
        "y": 5,
        "growth_value": 2.1,
        "middle_value": 3.5,
        "result": 0.3286525465,
    },
]


class TestNumberFunctions(unittest.TestCase):
    def test_squared_distance(self):
        for item in test_cases_squared_absolute:
            dist = SquaredDistance().calculate(item.get("x"), item.get("y"))
            assert dist == item.get("squared_result")

    def test_absolute_distance(self):
        for item in test_cases_squared_absolute:
            dist = AbsoluteDistance().calculate(item.get("x"), item.get("y"))
            assert dist == item.get("absolute_result")

    def test_linear_interval_distance(self):
        for item in test_cases_linear_interval:
            dist = LinearInterval(
                upper_bound=item.get("max"), lower_bound=item.get("min")
            ).calculate(item.get("x"), item.get("y"))
            self.assertAlmostEqual(dist, item.get("result"), places=7)

    def test_linear_distance(self):
        for item in test_cases_linear:
            dist = Linear(
                upper_bound=item.get("max"), lower_bound=item.get("min", None)
            ).calculate(item.get("x"), item.get("y"))
            assert dist == item.get("result")

    def test_threshold_distance(self):
        for item in test_cases_threshold:
            dist = Threshold(item.get("threshold")).calculate(
                item.get("x"), item.get("y")
            )
            assert dist == item.get("result")

    def test_exponential_distance(self):
        for item in test_cases_exponential:
            dist = Exponential(item.get("growth_value")).calculate(
                item.get("x"), item.get("y")
            )
            self.assertAlmostEqual(dist, item.get("result"), places=7)

    def test_sigmoid_distance(self):
        for item in test_cases_sigmoid:
            dist = Sigmoid(
                item.get("growth_value"), item.get("middle_value")
            ).calculate(item.get("x"), item.get("y"))
            self.assertAlmostEqual(dist, item.get("result"), places=7)
