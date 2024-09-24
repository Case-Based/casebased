# content of test_class.py
import os
from pathlib import Path

from casebased.components.attribute import FeatureAttribute, TargetAttribute
from casebased.components.casebase import CaseBase
from casebased.components.querycase import QueryCase
from casebased.components.similarity_measure import SimilarityMeasure
from casebased.components.vocabulary import Vocabulary

if "tests" in os.getcwd():
    source = Path("../test_data/regen.csv")
else:
    source = Path("test_data/regen.csv")


class TestSimilarityMeasure:
    case_base = CaseBase(None, "df", source)
    temp_attr = FeatureAttribute("Temperatur", (int, float), -50, 50)
    hum_attr = FeatureAttribute("Luftfeuchtigkeit", (int, float), 0, 100)
    press_attr = FeatureAttribute("Luftdruck", (int, float), 900, 1100)
    wind_attr = FeatureAttribute("Windgeschwindigkeit", (int, float), 0, 100)
    long_attr = FeatureAttribute("Laengengrad", (int, float), -180, 180)
    lat_attr = FeatureAttribute("Breitengrad", (int, float), -90, 90)

    target_attr = TargetAttribute("Regen?", (bool), 0, 1)

    features = [temp_attr, hum_attr, press_attr, wind_attr, long_attr, lat_attr]
    targets = [target_attr]
    vocabulary = Vocabulary(features, targets)

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
