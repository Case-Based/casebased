"""
The Explainer class is responsible for generating explanations for the user. Based on the solution found by the CBR system,
the Explainer will generate a human-readable explanation that describes the reasoning behind the solution. The explanation
will be presented to the user in a clear and concise manner, allowing them to understand why the system made the decision it did.

The explainer uses a local llm model to generate explanations. It uses the attributes of the case and the k-similar cases as input.
"""

from typing import List, Tuple

import ollama

from casebased.components.knowledge_containers.case_base.casebase import CaseBase
from src.casebased.components.explanation.explanation import Explanation
from src.casebased.components.knowledge_containers.ontology.vocabulary import Vocabulary


class Explainer:
    def __init__(
        self, case_base: CaseBase, vocab: Vocabulary, model: str, k_nearest: List[int]
    ) -> None:
        self.case_base = case_base
        self.vocab = vocab
        self.__model = model
        self.__k_nearest = k_nearest

    def explain(self, case, k_similar_cases) -> Explanation:
        """
        Generate an explanation for the solution
        """
        content = self.generate_explanation_content(case, k_similar_cases)
        adapted_from = self.get_adapted_from(case, k_similar_cases)
        return Explanation(content, adapted_from)

    def generate_explanation_content(self, case, k_similar_cases) -> str:
        """
        Generate the content of the explanation
        """

        explanation = "The solution was generated based on the following attributes:\n"
        explanation += self.generate_case_attributes(case)
        explanation += "\n\n"
        explanation += "The solution was adapted from the following similar cases:\n"
        explanation += self.generate_similar_cases_attributes(k_similar_cases)
        return explanation

    def generate_case_attributes(self, case) -> str:
        """
        Generate a string representation of the case attributes
        """
        attributes = ""
        for key, value in case.items():
            attributes += f"{key}: {value}\n"
        return attributes

    def generate_similar_cases_attributes(self, k_similar_cases) -> str:
        """
        Generate a string representation of the attributes of the k-similar cases
        """
        attributes = ""
        for i, case_index in enumerate(k_similar_cases):
            case = self.case_base.get_case(case_index)
            attributes += f"Case {i + 1}:\n"
            for key, value in case.items():
                attributes += f"{key}: {value}\n"
            attributes += "\n"
        return attributes

    def get_adapted_from(self, case, k_similar_cases) -> List[int]:
        """
        Get the list of case indices that the solution was adapted from
        """
        adapted_from = [case["index"]]
        for case_index in k_similar_cases:
            adapted_from.append(case_index)
        return adapted_from
