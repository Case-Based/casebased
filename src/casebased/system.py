from typing import Optional

from .components import CaseBase
from .components import Vocabulary
from .config import Configuration
from .components import aggregator
from .components.similarity import similarity_measure
from .components.similarity.types import SimilarityMeasure

class CBR:
    """
    Using this CaseBaseSystem class you can manage the entire CBR cycle and decide how you operate the case-base system.
    """

    _configuration: Optional[Configuration]
    """
    With the configuration you can change the behavior of the case-base system.
    """
    _similarity_measure: SimilarityMeasure
    _case_base: CaseBase
    _case_basevocabulary: Vocabulary

    def __init__(self, configuration=None):
        """
        Create a case-based system with whom you can solve new cases based on a database of old cases called the case base.

        Parameters:
        ----------
            configuration : Optional[Configuration]
                Provide the configuration that will define which algorithms to use.
        """
        self._configuration = configuration
        self._case_base = CaseBase()
        self._vocabulary = Vocabulary([], [])
        self._similarity_measure = similarity_measure()

    @property
    def configuration(self):
        return self._configuration
    
    @configuration.setter
    def configuration(self, config: Configuration):
        self._configuration = config

    @configuration.deleter
    def configuration(self):
        del self._configuration
    
    @property
    def similarity_measure(self):
        return self._similarity_measure
    
    @similarity_measure.setter
    def similarity_measure(self, sim_measure: SimilarityMeasure):
        self._similarity_measure = sim_measure

    @similarity_measure.deleter
    def similarity_measure(self):
        del self._similarity_measure

    @property
    def case_base(self):
        return self._case_base
    
    @case_base.setter
    def case_base(self, case_base: CaseBase):
        self._case_base = case_base

    @case_base.deleter
    def case_base(self):
        del self._case_base

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, vocab: Vocabulary):
        self._vocabulary = vocab

    @vocabulary.deleter
    def vocabulary(self):
        del self._vocabulary
    
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
            self.similarity_measure = SimilarityMeasure(Configuration())
        else:
            self.similarity_measure = SimilarityMeasure(self.configuration)
