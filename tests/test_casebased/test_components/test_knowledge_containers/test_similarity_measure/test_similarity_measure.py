# content of test_class.py
from pathlib import Path

from casebased.components.case.querycase import QueryCase
from casebased.components.knowledge_containers import (
    CaseBase,
    SimilarityMeasure,
    Vocabulary,
)


class TestSimilarityMeasure:
    case_base = CaseBase(None, "df", Path("test_data/regen.csv"))
    features = [
        "Temperatur",
        "Luftfeuchtigkeit",
        "Luftdruck",
        "Windgeschwindigkeit",
        "Laengengrad",
        "Breitengrad",
    ]
    targets = ["Regen?"]
    vocabulary = Vocabulary(features, targets, [1, 1, 1, 1, 1, 1])
    print(case_base.data)

    def test_get_k_similar_cases(self):
        similarity_measure = SimilarityMeasure(self.case_base, self.vocabulary)
        features = {
            "Temperatur": 18.5,
            "Luftfeuchtigkeit": 95,
            "Luftdruck": 1007,
            "Windgeschwindigkeit": 25,
            "Laengengrad": 7.465298,
            "Breitengrad": 51.5134,
        }
        query = QueryCase(features)
        k = 2
        indices = similarity_measure.get_k_similar_cases(query, k)
        assert (indices == [[2, 0]]).all()
