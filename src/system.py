from typing import Optional

from components.casebase.casebase import CaseBase
from components.similarity_measure.similarity import SimilarityMeasure
from components.vocabulary.vocabulary import Vocabulary
from config import Configuration


class CaseBaseSystem:
    """
    Using this CaseBaseSystem class you can manage the entire CBR cycle and decide how you operate the case-base system.
    """

    configuration: Optional[Configuration]
    """
    With the configuration you can change the behavior of the case-base system.
    """
    similarity_measure: SimilarityMeasure
    case_base: CaseBase
    vocabulary: Vocabulary

    def __init__(self, configuration=None):
        """
        Create a case-based system with whom you can solve new cases based on a database of old cases called the case base.

        Parameters:
        ----------
            configuration : Optional[Configuration]
                Provide the configuration that will define which algorithms to use.
        """
        self.configuration = configuration
        if self.configuration is None:
            self.similarity_measure = SimilarityMeasure()
        else:
            self.similarity_measure = SimilarityMeasure(
                k=self.configuration.k,
                similarity_measure=self.configuration.similarity_measure_algorithm,
                k_finding=self.configuration.k_algorithm,
            )
        self.case_base = CaseBase()
        self.vocabulary = Vocabulary()

    def change_config(self, config: Configuration):
        """
        Replace the current configuration of the case-base system with the new configuration provided.

        Changing the configuration will change the behavior of the case-base system.
        For example the time taken to measure the similarity between cases can increase or the accuracy can differ when changing the similarity measure algorithm.

        Also, when changing the k-finding algorithm the amount of the nearest cases can differ as well as when a manual k is changed.

        Parameters:
        ----------
            config: Configuration
                Provide the configuration that will define which algorithms to use.

        Returns:
        --------
            None
        """
        self.configuration = config
        if self.configuration is None:
            self.similarity_measure = SimilarityMeasure()
        else:
            self.similarity_measure = SimilarityMeasure(
                k_finding=self.configuration.k_algorithm,
                k=self.configuration.k,
                similarity_measure=self.configuration.similarity_measure_algorithm,
            )
