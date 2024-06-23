from typing import List

import numpy as np

from casebased.components.knowledge_containers.case_base.casebase import CaseBase
from casebased.components.knowledge_containers.ontology.attribute import (
    FeatureAttribute,
    TargetAttribute,
)


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

    def __init__(
        self,
        features: List[FeatureAttribute],
        targets: List[TargetAttribute],
        retrieval_attributes=None,
    ):
        self.features = features
        self.feature_names: List[str] = [x.name for x in features]
        self.targets = targets
        self.target_names: List[str] = [x.name for x in targets]
        self.weights = [x.weight for x in features]
        if retrieval_attributes is None:
            retrieval_attributes = self.features
        else:
            self.retrieval_attributes = retrieval_attributes
        return

    def add_feature(self, feature: FeatureAttribute, position: int = -1):
        f_name = feature.name
        if f_name in self.feature_names:
            raise ValueError(
                f"Feature with name {f_name} already exists in the vocabulary"
            )
        if position == -1:
            self.features.append(feature)
        else:
            self.features.insert(position, feature)
        self.__sync_features()
        return

    def remove_feature(self, remove_feats: str | int | list[str] | list[int]):
        if len(self.features) == 1:
            raise ValueError("Cannot remove the last target from the vocabulary")
        self.features = self.__remove_attribute(remove_feats, self.features)
        self.__sync_features()
        self.__sync_weights()

    def compile_weights(self, casebase: CaseBase, method="korr"):
        if method == "korr":
            # TODO: Find solution for when targets are not in the data
            #   or when targets are not the last columns
            corr_mat = (
                casebase.data[self.feature_names + self.target_names]
                .corr()[self.targets]
                .iloc[:-1]
            )
            self.weights = corr_mat.values.flatten()
        elif method == "auto":
            self.weights = [1] * len(self.feature_names)
        return

    def add_target(self, target, position: int = -1):
        t_name = target.name
        if t_name in self.feature_names:
            raise ValueError(
                f"Target with name {t_name} already exists in the vocabulary"
            )
        if position == -1:
            self.features.append(target)
        else:
            self.features.insert(position, target)
        self.__sync_targets()
        return

    def remove_target(self, remove_targets: str | int | list[str] | list[int]):
        if len(self.targets) == 1:
            raise ValueError("Cannot remove the last target from the vocabulary")
        self.features = self.__remove_attribute(remove_targets, self.targets)
        self.__sync_targets()

    def __sync_features(self):
        self.feature_names = [x.name for x in self.features]
        return

    def __sync_targets(self):
        self.target_names = [x.name for x in self.targets]
        return

    def __sync_weights(self):
        self.weights = [x.weight for x in self.features]
        return

    @staticmethod
    def __remove_attribute(remove_attr: str | int | list[str] | list[int], attributes):
        if isinstance(remove_attr, str):
            attributes = [x for x in attributes if x.name != remove_attr]
        elif isinstance(remove_attr, int):
            attributes = [x for i, x in enumerate(attributes) if i != remove_attr]
        elif isinstance(remove_attr, list):
            if isinstance(remove_attr[0], str):
                attributes = [x for x in attributes if x.name not in remove_attr]
            elif isinstance(remove_attr[0], int):
                attributes = [
                    x for i, x in enumerate(attributes) if i not in remove_attr
                ]
        return attributes

    # TODO: Logic for virtual attributes
    # TODO: Logic for subcontainers: Retrieval
    #  Attributes,
    #  Input Attributes,
    #  Output Attributes.
