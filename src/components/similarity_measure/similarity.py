from typing import Optional, Union, Callable, Any
from .types import SimilarityMeasureAlgorithm
from utils.k_algorithm import KAlgorithm


class SimilarityMeasure:
    k: Optional[int]
    k_finding: Union[KAlgorithm, Callable[[Any], int]]
    similarity_measure: Union[SimilarityMeasureAlgorithm, Callable[[list, list], int]]

    def __init__(
            self,
            k=None,
            k_finding: Union[KAlgorithm, Callable[[Any], int]] = KAlgorithm.ELBOW,
            similarity_measure: Union[SimilarityMeasureAlgorithm, Callable[[list, list], int]] = SimilarityMeasureAlgorithm.EUCLIDEAN
    ):
        self.k = k
        self.k_finding = k_finding
        self.similarity_measure = similarity_measure
