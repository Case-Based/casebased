from typing import Mapping, Protocol, Union

from casebased.components.vocabulary import Case


class Adapter(Protocol):
    def adapt(
        self, case: Case, similar_cases: Union[list[Case], Mapping[Case, float]]
    ) -> Case:
        """
        Currently we're not having built-in adaptation techniques you can use.
        But using this interface you can define your own adaptation function which will change the given case and output the mutated case.

        Args:
            case: Case : Case to be modified
            similar_cases: Union[list[Case], Mapping[Case, float]] : List of most similar cases in knowledge base. Can also be a dict (mapping) of the Case as key and the similarity value (type of float) as value.

        Returns:
            Case
        """
        ...
