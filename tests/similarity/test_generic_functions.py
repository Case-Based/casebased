from casebased.components.similarity_measure.functions import (
    Equality,
    Static,
    VectorDifference,
)

test_cases_equality = [
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

test_cases_vector_distance = [
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


def test_equality_distance():
    for case in test_cases_equality:
        dist = Equality().calculate(case.get("x"), case.get("y"))
        assert dist == case.get("result")


def test_static_distance():
    dist = Static(0.5).calculate(10, 5)
    assert dist == 0.5


def test_vector_distance():
    for case in test_cases_vector_distance:
        dist = VectorDifference().calculate(case.get("x"), case.get("y"))
        assert dist == case.get("result")
