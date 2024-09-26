import pytest

from casebased.components.vocabulary.attribute import FeatureAttribute, TargetAttribute
from casebased.components.vocabulary.vocabulary import Vocabulary


class TestVocabulary:
    features = [
        FeatureAttribute("latitude", (int, float), -90, 90),
        FeatureAttribute("longitude", (int, float), -180, 180),
        FeatureAttribute("humidity", (int, float), 0, 100),
        FeatureAttribute("temperature", (int, float), -50, 50),
    ]
    targets = [
        TargetAttribute("rain", (bool), False, True),
    ]
    feature = FeatureAttribute("pressure", (int, float), 900, 1100)

    def test__init__(self):
        vocabulary = Vocabulary(self.features, self.targets)
        assert vocabulary.features == self.features
        assert vocabulary.feature_names == [x.name for x in self.features]
        assert vocabulary.targets == self.targets

    def test_add_feature_default(self):
        vocabulary = Vocabulary(self.features.copy(), self.targets.copy())
        vocabulary.add_feature(self.feature)
        assert vocabulary.feature_names == [
            "latitude",
            "longitude",
            "humidity",
            "temperature",
            "pressure",
        ]
        assert vocabulary.weights == [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ]  # default weight for pressure was added
        assert vocabulary.retrieval_attributes == vocabulary.feature_names

    def test_add_feature_default_m1(self):
        vocabulary_def = Vocabulary(self.features.copy(), self.targets.copy())
        vocabulary_last = Vocabulary(self.features.copy(), self.targets)
        vocabulary_def.add_feature(self.feature)
        vocabulary_last.add_feature(self.feature, -1)
        assert vocabulary_def.feature_names == vocabulary_last.feature_names

    def test_add_feature_insert(self):
        vocabulary = Vocabulary(self.features.copy(), self.targets.copy())
        vocabulary.add_feature(self.feature, 2)
        assert vocabulary.feature_names == [
            "latitude",
            "longitude",
            "pressure",
            "humidity",
            "temperature",
        ]

    def test_add_feature_duplicate(self):
        vocabulary = Vocabulary(self.features.copy(), self.targets.copy())
        with pytest.raises(ValueError):
            vocabulary.add_feature(FeatureAttribute("latitude", (int, float), -90, 90))

    def test_remove_feature_name(self):
        vocabulary = Vocabulary(self.features.copy(), self.targets.copy())
        vocabulary.remove_feature("humidity")
        assert vocabulary.feature_names == ["latitude", "longitude", "temperature"]

    def test_remove_feature_index(self):
        feature = 2
        vocabulary = Vocabulary(self.features.copy(), self.targets.copy())
        vocabulary.remove_feature(feature)
        assert vocabulary.feature_names == ["latitude", "longitude", "temperature"]

    def test_remove_feature_list(self):
        feature = ["latitude", "humidity"]
        vocabulary = Vocabulary(self.features.copy(), self.targets.copy())
        vocabulary.remove_feature(feature)
        assert vocabulary.feature_names == ["longitude", "temperature"]

    def test_remove_feature_list_index(self):
        feature = [0, 2]
        vocabulary = Vocabulary(self.features.copy(), self.targets.copy())
        vocabulary.remove_feature(feature)
        assert vocabulary.feature_names == ["longitude", "temperature"]
