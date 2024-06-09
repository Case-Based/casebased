from typing import List

from casebased.components.knowledge_containers.case_base.casebase import CaseBase


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
        features: List[str],
        targets: List,
        weights: List,
        retrieval_attributes=None,
    ):
        self.features = features
        self.targets = targets
        self.weights = weights
        if retrieval_attributes is None:
            retrieval_attributes = features
        else:
            self.retrieval_attributes = retrieval_attributes
        return

    def add_feature(self, feature, position: int = -1):
        if feature in self.features:
            return
        if position == -1:
            self.features.append(feature)
        else:
            self.features.insert(position, feature)
        return

    def remove_feature(self, remove_feats: str | int | list[str] | list[int]):
        if isinstance(remove_feats, str):
            self.features.remove(remove_feats)
        elif isinstance(remove_feats, int):
            self.features.pop(remove_feats)
        elif isinstance(remove_feats, list):
            if isinstance(remove_feats[0], str):
                self.features = [x for x in self.features if x not in remove_feats]
            elif isinstance(remove_feats[0], int):
                remove_feat_names = [
                    x for i, x in enumerate(self.features) if i in remove_feats
                ]
                self.features = [x for x in self.features if x not in remove_feat_names]

    def compile_weights(self, casebase: CaseBase, method="korr"):
        if method == "korr":
            # TODO: Find solution for when targets are not in the data
            #   or when targets are not the last columns
            corr_mat = (
                casebase.data[self.features + self.targets]
                .corr()[self.targets]
                .iloc[:-1]
            )
            print(corr_mat)
            self.weights = corr_mat.values.flatten()
        elif method == "auto":
            self.weights = [1] * len(self.features)
        return

    def add_target(self, target, position: int = -1):
        if target in self.targets:
            return
        if position == -1:
            self.targets.append(target)
        else:
            self.targets.insert(position, target)
        return

    # TODO: Logic for virtual attributes
    # TODO: Logic for subcontainers: Retrieval
    #  Attributes,
    #  Input Attributes,
    #  Output Attributes.
