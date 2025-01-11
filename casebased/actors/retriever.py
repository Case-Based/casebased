from casebased.components.casebase.casebase import CaseBase
from casebased.components.casebase.query_case import QueryCase
from casebased.components.similarity_measure.similarity import SimilarityMeasure
from casebased.components.vocabulary import Vocabulary


class Retriever:
    def __init__(self, case_base, similarity_measure, vocab):
        self.case_base: CaseBase = case_base
        self.similarity_measure: SimilarityMeasure = similarity_measure
        self.vocab: Vocabulary = vocab

    def retrieve(
        self,
        query: QueryCase,
        k: int,
        algorithm="auto",
        weighted=False,
        return_distance: bool = False,
    ):
        cases = self.similarity_measure.get_k_similar_cases(
            query=query,
            k=k,
            algorithm="auto",
            return_distance=return_distance,
            weighted=weighted,
        )
        for case in cases:
            self.case_base.cases["utility"] += 1 # increment utility count
        return cases
