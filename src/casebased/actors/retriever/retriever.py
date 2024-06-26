from casebased.components.case.querycase import QueryCase
from casebased.components.knowledge_containers.case_base.casebase import CaseBase
from casebased.components.knowledge_containers.ontology.vocabulary import Vocabulary
from casebased.components.knowledge_containers.similarity_measure.similarity_measure import (
    SimilarityMeasure,
)


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
        return self.similarity_measure.get_k_similar_cases(
            query=query,
            k=k,
            algorithm="auto",
            return_distance=return_distance,
            weighted=weighted,
        )
