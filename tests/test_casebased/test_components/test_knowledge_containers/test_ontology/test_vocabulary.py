from src.casebased.components.knowledge_containers.ontology.vocabulary import Vocabulary


class TestVocabulary:
    features = ["latitude", "longitude", "humidity", "temperature"]
    targets = ["rain"]
    weights = [0.7, 0.7, 1.6, 2]

    def test__init__(self):
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        assert vocabulary.features == self.features
        assert vocabulary.targets == self.targets
        assert vocabulary.weights == self.weights

    def test_add_feature_default(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = "pressure"
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        vocabulary.add_feature(feature)
        assert vocabulary.features == [
            "latitude",
            "longitude",
            "humidity",
            "temperature",
            "pressure",
        ]

    def test_add_feature_default_m1(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = "pressure"
        vocabulary_def = Vocabulary(self.features, self.targets, self.weights)
        vocabulary_def.add_feature(feature)
        vocabulary_last = Vocabulary(self.features, self.targets, self.weights)
        vocabulary_last.add_feature(feature, -1)
        assert vocabulary_def.features == vocabulary_last.features

    def test_add_feature_insert(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = "pressure"
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        vocabulary.add_feature(feature, 2)
        assert vocabulary.features == [
            "latitude",
            "longitude",
            "pressure",
            "humidity",
            "temperature",
        ]

    def test_add_feature_duplicate(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = "latitude"
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        vocabulary.add_feature(feature)
        assert vocabulary.features == self.features

    def test_remove_feature_name(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = "humidity"
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        vocabulary.remove_feature(feature)
        assert vocabulary.features == ["latitude", "longitude", "temperature"]

    def test_remove_feature_index(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = 2
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        vocabulary.remove_feature(feature)
        assert vocabulary.features == ["latitude", "longitude", "temperature"]

    def test_remove_feature_list(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = ["latitude", "humidity"]
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        vocabulary.remove_feature(feature)
        assert vocabulary.features == ["longitude", "temperature"]

    def test_remove_feature_list_index(self):
        self.features = ["latitude", "longitude", "humidity", "temperature"]
        feature = [0, 2]
        vocabulary = Vocabulary(self.features, self.targets, self.weights)
        vocabulary.remove_feature(feature)
        assert vocabulary.features == ["longitude", "temperature"]
