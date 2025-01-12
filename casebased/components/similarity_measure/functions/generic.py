from ..types import SimilarityFunction
from typing import TypeVar


V = TypeVar("V", float, int)
T = TypeVar("T")

class Equality(SimilarityFunction):
    def calculate(self, x: T, y: T) -> float:
        return 1.0 if x == y else .0
    
class Static(SimilarityFunction):
    def __init__(self, value: float) -> None:
        self.__value = value
        
    def calculate(self, x: T, y: T) -> float:
        return self.__value
    
class VectorDifference(SimilarityFunction):
    def calculate(self, x: list[V], y: list[V]) -> float:
        if len(x) < len(y):
            temp = x
            x = y
            y = temp
        
        result = .0
        for i, item in enumerate(x):
            result += abs(item - (y[i] if len(y) >= i + 1 else 0))
        return result
