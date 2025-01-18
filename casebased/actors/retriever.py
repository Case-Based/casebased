from typing import Mapping, Optional

from dataclasses import dataclass

from casebased import CaseBaseAdapter
from casebased.components.similarity_measure import SimilaritySchema
from casebased.components.vocabulary import Case, Vocabulary


@dataclass()
class Retriever:
    """
    The retriever component is used to calculate similarities using the provided similarity schema
    and retrieve the k most similar cases from the case base.
    """

    similarity_schema: SimilaritySchema
    """
    Used to define how similarity is calculated between cases.
    """
    case_base: CaseBaseAdapter
    """
    Used to get all cases from the case base.
    """
    k: int
    """
    How many cases should be returned.
    """

    def get_least_similar(self, cases: Mapping[Case, float]) -> Optional[Case]:
        """
        Get the least similar case in a list of cases with their respective similarity value.

        Args:
            cases: A dictionary with cases as keys and their similarity value as values.

        Returns:
            The least similar case or None.
        """
        least_similar = None

        if len(cases.keys()) == 0:
            return least_similar

        for key, val in cases.items():
            if least_similar is None:
                least_similar = key
            elif val < cases[least_similar]:
                least_similar = key

        return least_similar

    def retrieve(self, case: Case) -> Mapping[Case, float]:
        """
        Simply retrieve the k most similar cases to the provided case.

        Args:
            case: The case for which to retrieve the k most similar cases.

        Returns:
            A dictionary with the k most similar cases as keys and their similarity value as values.
        """
        cases: list[Case] = self.case_base.get_all_cases()

        k_best_cases: Mapping[Case, float] = dict()

        for prev_case in cases:
            similarity = self.similarity_schema.calculate(case, prev_case)

            if len(k_best_cases.keys()) < self.k:
                k_best_cases[prev_case] = similarity
            elif len(k_best_cases.keys()) >= self.k:
                least_similar = self.get_least_similar(k_best_cases)

                if least_similar and similarity < k_best_cases[least_similar]:
                    del k_best_cases[least_similar]
                    k_best_cases[prev_case] = similarity

        return k_best_cases
