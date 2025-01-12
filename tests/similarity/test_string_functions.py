from casebased.components.similarity_measure.functions import Levenshtein, JaroDistance, JaroWinkler


test_cases = [
    { "x": "kitten", "y": "sitten", "prefix_weight": .1, "results": { "levenshtein": 1, "jaro": 1.0, "jaro_winkler": 0, }, },
]

for case in test_cases: 
    def test_levenshtein_distance():
        pass
        # dist = Levenshtein().calculate(case.get("x"), case.get("y"))
        # assert dist == case.get("results", {}).get("levenshtein")

    def test_jaro_distance():
        pass
        # dist = JaroDistance().calculate(case.get("x"), case.get("y"))
        # assert dist == case.get("results", {}).get("jaro")

    def test_jaro_winkler_distance():
        pass
        # dist = JaroWinkler(case.get("prefix_weight")).calculate(case.get("x"), case.get("y"))
        # assert dist == case.get("results", {}).get("jaro_winkler")
