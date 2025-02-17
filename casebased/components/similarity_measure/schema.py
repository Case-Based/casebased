from typing import Mapping

from dataclasses import dataclass

from casebased.components.vocabulary import Case, Vocabulary

from .types import SimilarityFunction
from .weight import WeightProvider


@dataclass(frozen=True)
class SimilaritySchema:
    attributes: Mapping[str, SimilarityFunction]
    vocabulary: Vocabulary

    def calculate(self, x: Case, y: Case) -> Mapping[str, float]:
        result = 0.0
        similarities = {}

        for feature_key in x.get_feature_keys():
            y_feature = y.get_feature_value_by_key(feature_key)
            x_feature = x.get_feature_value_by_key(feature_key)

            similarity = self.attributes[feature_key].calculate(x_feature, y_feature)

            similarities[feature_key] = (
                WeightProvider.get_weight(self.vocabulary, feature_key) * similarity
            )

        for val in similarities.values():
            result += val

        return result
