import unittest

test_cases = [
    {
        "x": "kitten",
        "y": "sitten",
        "prefix_weight": 0.1,
        "results": {
            "levenshtein": 1,
            "jaro": 1.0,
            "jaro_winkler": 0,
        },
    },
]


class TestStringSimilarityFunctions(unittest.TestCase):
    def test_levenshtein_distance(self):
        pass
        # dist = Levenshtein().calculate(case.get("x"), case.get("y"))
        # assert dist == case.get("results", {}).get("levenshtein")

    def test_jaro_distance(self):
        pass
        # dist = JaroDistance().calculate(case.get("x"), case.get("y"))
        # assert dist == case.get("results", {}).get("jaro")

    def test_jaro_winkler_distance(self):
        pass
        # dist = JaroWinkler(case.get("prefix_weight")).calculate(case.get("x"), case.get("y"))
        # assert dist == case.get("results", {}).get("jaro_winkler")
