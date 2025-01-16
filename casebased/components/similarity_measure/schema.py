from typing import Mapping, Any

from dataclasses import dataclass

from .types import SimilarityFunction
from casebased.components.vocabulary import Vocabulary
from .weight import WeightProvider


@dataclass(frozen=True)
class SimilaritySchema:
    attributes: Mapping[str, SimilarityFunction]
    vocabulary: Vocabulary
    
    def calculate(self, x: Mapping[str, Any], y: Mapping[str, Any]) -> Mapping[str, float]:
        results = {}
        
        for feature_key in x:
            y_feature = y[feature_key]
            x_feature = x[feature_key]
            
            similarity = self.attributes[feature_key].calculate(x_feature, y_feature)
            
            results[feature_key] = WeightProvider.get_weight(self.vocabulary, feature_key) * similarity
        
        return results
