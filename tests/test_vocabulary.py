from casebased.components.vocabulary import Vocabulary, FeatureAttribute, TargetAttribute, Case
import unittest

TEST_DATA = {
    "features": [
        FeatureAttribute(name="feature1", data_type=int, conditions=[]),
        FeatureAttribute(name="feature2", data_type=int, conditions=[]),
        FeatureAttribute(name="feature3", data_type=int, conditions=[])
    ],
    "targets": [
        TargetAttribute(name="target1", data_type=int, conditions=[]),
    ],
    "case": Case(
        feature_attributes={
            "feature1": 1,
            "feature2": 2,
            "feature3": 3
        },
        target_attributes={
            "target1": 4
        }
    )
}

class TestVocabulary(unittest.TestCase):
    def test__vocabulary_creation(self):
        vocab = Vocabulary(features=TEST_DATA["features"], targets=TEST_DATA["targets"])
        is_valid = vocab.validate_case(TEST_DATA["case"])
        self.assertTrue(is_valid)