from typing import List


class Vocabulary:
    """
    Vocabulary consists of key value pairs that define the features
    and targets and their possible values.

    E.g.
    features: ["latitude", "longitude", "humidity", "temperature"],
    targets: ["rain"],
    weights: [0.7, 0.7, 1.6, 2]


    @params: attributes: dict, targets: dict

    """

    def __init__(self, features: List, targets: List, weights: List):
        self.features = features
        self.targets = targets
        self.weights = weights
        return

    def add_feature(self, feature):
        if feature in self.features:
            return
        self.features.append(feature)
        return

    def remove_feature(self, feature):
        if feature in self.features:
            self.features.pop(feature)
        return

    # TODO: Logic for virtual attributes
    # TODO: Logic for subcontainers: Retrieval
    #  Attributes,
    #  Input Attributes,
    #  Output Attributes.
