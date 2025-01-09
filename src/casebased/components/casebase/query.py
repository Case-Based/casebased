import numpy as np


class Query:
    """
    A Case is a Vector of Features and Targets located in the Case Base.
    Cases are experiences consisting of features and targets.

    features and targets can be formulated as problem and solution.
    """

    def __init__(self, features: dict, utility=0):
        # man könnte sagen, dass hier einfach ein data object übergeben wird
        # was features und targets sind enthält das vocabulary
        if not isinstance(features, dict):
            raise ValueError("Features must be a dictionary")

        self.features = features
        self.feature_values = list(features.values())

        if not all(isinstance(value, (int, float)) for value in self.feature_values):
            raise ValueError("All features must be of type int or float")

        # The amount of times the case is found in kNN or used otherwise
        #   (needed to prune unused cases in optimization)
        self.utility = utility

    def get_features(self):
        return self.features

    def get_1d_feature_array(self):
        return np.array(self.feature_values)

    def get_2d_feature_array(self):
        return np.array(self.feature_values).reshape(1, -1)

    def __repr__(self):
        return f"Case: {self.features}"
