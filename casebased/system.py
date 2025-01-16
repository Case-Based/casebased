from casebased.components.similarity_measure import SimilaritySchema
from casebased import CaseBaseAdapter
from dataclasses import dataclass
from casebased.components.vocabulary import Vocabulary, Case
from typing import Optional
from casebased.actors.retriever import Retriever


@dataclass()
class CaseBasedSystem():
    similarity_schema: SimilaritySchema
    vocabulary: Vocabulary
    case_base: CaseBaseAdapter
    threshold: Optional[float]
    k: int = 5
    # case_base_maintainer: Optional[CaseBaseMaintainer] = None
    
    def retrieve(self, case: Case):
        retriever = Retriever(similarity_schema=self.similarity_schema, case_base=self.case_base, k=self.k)
        return retriever.retrieve(case)
    
    def adapt(self): ...
    
    def reuse(self): ...
