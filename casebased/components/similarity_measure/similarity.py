from typing import Any, AnyStr, Callable, Literal, Optional, Union

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

from casebased.components.casebase.casebase import CaseBase
from casebased.components.casebase.query_case import QueryCase
from casebased.components.vocabulary.vocabulary import Vocabulary
from casebased.config import Configuration
from casebased.utils.k_algorithm import KAlgorithm


class SimilarityMeasure:
    k: Optional[int]
    k_optimizer: Union[KAlgorithm, Callable[[Any], int]]
    similarity_measure: Union[SimilarityMeasureMetric, Callable[[list, list], int]]

    def __init__(
        self,
        config: Configuration,
        decision_type,
    ):
        self.config = config
        self.decision_type: Literal["semantic", "numeric", "equality", "text"] = (
            decision_type
        )

    def get_global_similarity(self, case, compare_case):
        """
        Compute the global similarity between two cases
        """
        pass

    def get_local_similarity(
        self, new_case_feature: AnyStr, compare_case_feature: AnyStr
    ):
        """
        Compute the similarity between two local features
        """

    def get_word_similarity(
        self, new_case_feature: AnyStr, compare_case_feature: AnyStr
    ):
        """
        Compute the similarity between two words
        """
        pass

    def get_text_similarity(
        self, new_case_feature: AnyStr, compare_case_feature: AnyStr
    ):
        """
        Compute the similarity between two pieces of text
        """
        pass
