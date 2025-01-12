from ..types import SimilarityFunction
from typing import Optional, TypeVar
from math import exp


N = TypeVar("N", float, int)

class SquaredDistance(SimilarityFunction):
    def calculate(self, x: N, y: N) -> float:
        return (x - y)**2

class AbsoluteDistance(SimilarityFunction):
    def calculate(self, x: N, y: N) -> float:
        return abs(x - y)
    
class LinearInterval(SimilarityFunction):
    def __init__(self, lower_bound: N, upper_bound: N) -> None:
        if lower_bound >= upper_bound:
            raise Exception("Lower bound cannot be higher or equal to the upper bound in the linear interval similarity measure")
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
    
    def calculate(self, x: N, y: N) -> float:
        if x < self.__lower_bound or x > self.__upper_bound or y < self.__lower_bound or y > self.__upper_bound:
            return .0
        return 1.0 - abs(x - y) / (self.__upper_bound - self.__lower_bound)

class Linear(SimilarityFunction):
    def __init__(self, lower_bound: Optional[N], upper_bound: N) -> None:
        if (lower_bound or .0) >= upper_bound:
            raise Exception("Lower bound cannot be higher or equal to the upper bound in the linear similarity measure")
        self.__lower_bound = lower_bound or .0
        self.__upper_bound = upper_bound
    
    def calculate(self, x: N, y: N) -> float:
        distance = abs(x - y)
        if distance < self.__lower_bound:
            return 1.0
        elif distance > self.__upper_bound:
            return .0
        return (self.__upper_bound - distance) / (self.__upper_bound - self.__lower_bound)
    
class Threshold(SimilarityFunction):
    def __init__(self, threshold: N) -> None:
        self.__threshold = threshold
    
    def calculate(self, x: N, y: N) -> float:
        return 1.0 if abs(x - y) <= self.__threshold else .0
    
class Exponential(SimilarityFunction):
    def __init__(self, growth_value: N) -> None:
        self.__growth = growth_value
    
    def calculate(self, x: N, y: N) -> float:
        return exp(-self.__growth * abs(x - y))
    
class Sigmoid(SimilarityFunction):
    def __init__(self, growth_value: N, middle_value: N) -> None:
        self.__growth = growth_value
        self.__middle = middle_value
    
    def calculate(self, x: N, y: N) -> float:
        return 1.0 / (1.0 + exp((abs(x - y) - self.__middle) / self.__growth))
