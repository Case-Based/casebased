import pandas as pd

from ..knowledge_containers.ontology.vocabulary import Vocabulary


class Case:
    """
    A Case is a Vector of Features and Targets located in the Case Base.
    Cases are experiences consisting of features and targets.

    features and targets can be formulated as problem and solution.
    """

    def __init__(
        self, features: object, targets: object, vocabulary: Vocabulary, utility=0
    ):
        # man könnte sagen, dass hier einfach ein data object übergeben wird
        # was features und targets sind enthält das vocabulary
        self.features = features
        self.targets = targets

        # The amount of times the case is found in kNN or used otherwise
        #   (needed to prune unused cases in optimization)
        self.utility = utility

    def get_features(self):
        return self.features

    def get_targets(self):
        return self.targets

    def __repr__(self):
        return f"Case: {self.features} -> {self.targets}"
