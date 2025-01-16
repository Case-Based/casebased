from casebased.components.vocabulary import Case
from casebased.components.similarity_measure import SimilaritySchema
from casebased import CaseBaseAdapter
from dataclasses import dataclass
from typing import Mapping


@dataclass()
class Retriever:
    similarity_schema: SimilaritySchema
    case_base: CaseBaseAdapter
    k: int

    def retrieve(self, case: Case) -> Mapping[Case, float]:
        cases: list[Case] = self.case_base.get_all_cases()
        
        k_best_cases: Mapping[Case, float] = dict()
       
        for prev_case in cases:
            similarity = self.similarity_schema.calculate(case, prev_case)
            
            if len(k_best_cases.keys()) < self.k:
                k_best_cases[prev_case] = similarity
            elif len(k_best_cases.keys()) >= self.k:
                for key, val in enumerate(k_best_cases):
                    if val < similarity:
                        del k_best_cases[key]
                        k_best_cases[prev_case] = similarity
        return k_best_cases
