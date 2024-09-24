from typing import List, Union

from casebased.components.attribute import FeatureAttribute, TargetAttribute
from casebased.components.casebase import CaseBase


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
            retrieval_attributes = self.feature_names
        self.retrieval_attributes: List[str] = retrieval_attributes
        return

    def add_feature(
        self, feature: FeatureAttribute, position: int = -1, is_retrieval=True
    ):
        """
        Add a feature to the vocabulary and updates the feature names and weights.
        Args:
            feature: FeatureAttribute: The feature to add to the vocabulary
            position: int: The position to insert the feature in the list of features
            is_retrieval: bool: Whether the feature is a retrieval attribute
        Returns:

        """
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
        self.__sync_weights()
        if is_retrieval:
            self.add_retrieval_attribute(f_name)
        return

    def remove_feature(self, remove_feats: Union[str, int, list[str], list[int]]):
        """
        Remove a feature from the vocabulary and updates the feature names and weights.
        Args:
            remove_feats: str | int | list[str] | list[int]: The feature to remove from the vocabulary
        """
        if len(self.features) == 1:
            raise ValueError("Cannot remove the last target from the vocabulary")
        self.features = self.__remove_attribute(remove_feats, self.features)
        self.__sync_features()
        self.__sync_weights()

    def add_retrieval_attribute(
        self, attribute: Union[FeatureAttribute, str], position: int = -1
    ):
        """
        Add a retrieval attribute to the vocabulary.
        Retrieval attributes are the selected features that are used to retrieve cases from the case base.
        These attributes are used to determine the similarity between cases.
        Args:
            attribute: FeatureAttribute | str: The attribute to add to the vocabulary by name or object
            position: int: The position to insert the attribute in the list of retrieval attributes
        """
        if isinstance(attribute, str):
            ra_name = attribute
        else:
            ra_name = attribute.name
        if ra_name in self.retrieval_attributes:
            raise ValueError(
                f"Retrieval Attribute with name {ra_name} already exists in the vocabulary"
            )
        if ra_name not in self.feature_names:
            raise ValueError(
                f"Retrieval Attribute with name {ra_name} is not a feature in the vocabulary"
                f"hint: add the attribute as a feature first"
            )
        if position == -1:
            self.retrieval_attributes.append(ra_name)
        else:
            self.retrieval_attributes.insert(position, ra_name)
        return

    def compile_weights(self, casebase: CaseBase, method="korr"):
        """
        Compile the weights for the features in the vocabulary.
        Args:
            casebase: CaseBase: The case base for which the weights are compiled
            method: str: The method to use to compile the weights (default: "korr")
        """
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

    def add_target(self, target: TargetAttribute, position: int = -1):
        """
        Add a target to the vocabulary.
        Args:
            target: TargetAttribute: The target to add to the vocabulary
            position: int: The position to insert the target in the list of targets
        """
        t_name = target.name
        if t_name in self.feature_names:
            raise ValueError(
                f"Target with name {t_name} already exists in the vocabulary"
            )
        self.targets = self.__add_attribute(target, self.targets, position)
        self.__sync_targets()
        return

    def remove_target(self, remove_targets: Union[str, int, list[str], list[int]]):
        """
        Remove a target from the vocabulary.
        Args:
            remove_targets: str | int | list[str] | list[int]: The target to remove from the vocabulary
        """
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
    def __remove_attribute(
        remove_attr: Union[str, int, list[str], list[int]], attributes
    ):
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

    @staticmethod
    def __add_attribute(attribute, attributes, position: int = -1):
        if position == -1:
            attributes.append(attribute)
        else:
            attributes.insert(position, attribute)
        return attributes

    # TODO: Logic for virtual attributes
    # TODO: Logic for subcontainers: Retrieval
    #  Attributes,
    #  Input Attributes,
    #  Output Attributes.
