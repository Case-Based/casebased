from typing import Mapping, Optional, Union

from dataclasses import dataclass

from casebased import CaseBaseAdapter
from casebased.actors.adapter import Adapter
from casebased.actors.retriever import Retriever
from casebased.components.similarity_measure import SimilaritySchema
from casebased.components.vocabulary import Case, Vocabulary


@dataclass()
class CaseBasedSystem:
    similarity_schema: SimilaritySchema
    """
    In the similarity schema you can define how the similarity between cases is calculated.
    Within the schema you can define the calculation function for every attribute of the case.
    Additionally, each attribute can have a weight, which is defined in the case base's vocabulary.
    """
    vocabulary: Vocabulary
    """
    The vocabulary serves as a definition for the cases in CBR. You can define attributes, their values, conditions they have to meet, and their weights.
    This can currently be done through a TOML file. More information can be found in the vocabulary documentation section.
    """
    case_base: CaseBaseAdapter
    """
    The case base is the storage for all cases in the CBR system. It can be implemented in different ways, e.g. as a list, a database, or a file.
    Since we're not in position to define which technologies you have to use, we provide you an interface to implement your own case base.
    For this you have to implement the CaseBaseAdapter with its basic functions (not much more than CRUD).
    """
    threshold: Optional[float]
    """
    Using the threshold you can define your quality standard. If the similarity is above this theshold the case is cut out because it's not similar enough.
    """
    adapter: Adapter
    """
    Used to adapt previous solutions to the new case.
    """
    k: int = 5
    """
    Define how many cases you want to retrieve. For now this is only a static variable you can define.
    """
    # case_base_maintainer: Optional[CaseBaseMaintainer] = None
    
    def train(self):
        feature_attribute_keys = [feature.name for feature in self.vocabulary.features]
        
        self._retriever = Retriever(
            similarity_schema=self.similarity_schema, case_base=self.case_base, k=self.k
        )
        self._retriever.train(feature_attribute_keys)

    def retrieve(self, case: Case):
        """
        Using the retriever function you can retrieve the k most similar cases to the given case.
        """
        if self.vocabulary.validate_case(case) is False:
            raise ValueError("Case is not valid.")

        return self._retriever.retrieve(case)

    def adapt(
        self, case: Case, similar_cases: Union[list[Case], list[tuple[Case, float]]]
    ) -> Case:
        """
        Used to adapt a previous case solution to solve the new case.
        """
        return self.adapter.adapt(case, similar_cases)

    def reuse(self, case: Case) -> None:
        """
        This function will add the new case to the case base.
        """
        result = self.case_base.create_case(case)
        if not result is None and result is False:
            raise RuntimeError("Case creation task faile")
