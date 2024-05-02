from typing import AnyStr

from metrics import SimilarityMetrics
from sklearn.neighbors import NearestNeighbors

from ..case_base.casebase import CaseBase
from ..ontology.vocabulary import Vocabulary

# TODO: Alter das wird komplizierter als ich dachte... Wie berechnet man die ähnlichkeit von 2 Wörtern??
#  Wir müssen dann auch unbedigt einen weg finden, dass
#  Nutzer typisieren müssen im vocabulary (Word, Sentence, Text, Number, ...)


class SimilarityMeasure:
    def __init__(self, metric: SimilarityMetrics):
        self.metric = metric

    def kNN(self, case, vocabulary: Vocabulary, algorithm: str, k, cb: CaseBase):
        return NearestNeighbors(n_neighbors=k, algorithm=algorithm).fit(cb)

    def hamming(self, case, vocabulary: Vocabulary):
        """
        Calculates the Hamming Distance between two cases
        """
        pass

    def euler(self, case, vocabulary: Vocabulary):
        """
        Calculates the Euler Distance between two cases
        """
        pass

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
