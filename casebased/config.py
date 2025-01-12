from typing import Callable, Optional, Union

from dataclasses import dataclass

from .components.similarity_measure.types import SimilarityFunction
from .utils.k_algorithm import KAlgorithm


@dataclass
class Configuration:
    """
    In the configuration you can define how the case-base system should calculate for example the similarity between cases or the optimal number of cases that should be retrieved from the case base.

    Attributes:
    -----------
        similarity_measure_algorithm
            Define the algorithm that should be used to calculate the similarity between cases.
            Since this is an optional attribute you can just leave it as None and the default similarity measure, Euclidean distance, will be taken.
            However, you can also choose from the built-in similarity measurement algorithms or provide your own function.
        k_algorithm
            Define the algorithm that should be used to find the optimal number of cases to retrieve from the case base.
            Here you can also just set it to None or leave it blank, and it will use the Elbow method to get a k.
            But you can also choose between different built-in algorithms or define your own algorithm.
        k
            You can also manually define the number of cases that should be retrieved with this attribute.
            However, unless you are not using an algorithm to find the optimal k yourself, we discourage people to manually type in the k, because the solution may be bad.
    """

    similarity_measure_algorithm: Union[
        None, SimilarityFunction, Callable[[list, list], int]
    ] = None
    """
    This attribute determines which algorithm will be used to calculate the distance between cases, which is a key point in CBR.
    You can choose from a list of built-in algorithms or write your own algorithm and provide the function here.
    Alternatively, you can leave the field blank and the system will use the default algorithm, which is the Euclidean distance.
    """
    k_optimizer: Union[None, KAlgorithm, Callable] = None
    """
    Define the algorithm that should be used to find the optimal number of cases to retrieve from the case base.
    Here you can also just set it to None or leave it blank, and it will use the Elbow method to get a k.
    But you can also choose between different built-in algorithms or define your own algorithm.
    """
    k: Optional[int] = None
    """
    You can also manually define the number of cases that should be retrieved with this attribute.
    However, unless you are not using an algorithm to find the optimal k yourself, we discourage people to manually type in the k, because the solution may be bad.
    """
