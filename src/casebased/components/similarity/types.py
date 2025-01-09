import dataclasses
from enum import Enum
from pathlib import Path
from typing import Mapping, Protocol, Sequence, Type, runtime_checkable
from ..casebase import Casebase
from ._similarity_measure import similarity_measure


class SimilarityMeasureAlgorithm(Enum):
    EUCLIDEAN = (0,)
    MANHATTAN = (1,)

type JsonEntry = (
    Mapping[str, "JsonEntry"] | Sequence["JsonEntry"] | str | int | float | bool | None
)

# A JSON dictionary with string keys and JSON values
type JsonDict = dict[str, JsonEntry]

# FilePath is either a string or a Path object
type FilePath = str | Path

# SimMap is a mapping from keys of type K to values of type S
# where S is a float
type SimMap[K, S: float] = Mapping[K, S]

# Sequence of similarity values
type SimSeq[S: float] = Sequence[S]

# SimSeqOrMap is either a SimMap or a SimSeq
type SimSeqOrMap[K, S: float] = SimMap[K, S] | SimSeq[S]

type SimilarityMeasure[V, S: float] = Type[similarity_measure[V, S]]

class SimMapFunc[K, V, S: float]:
    # __call__ method that takes a mapping and a value and returns a mapping of keys to similarity values
    def __call__(self, x_map: Mapping[K, V], y: V, /) -> SimMap[K, S]: ...


class SimSeqFunc[V, S: float]:
    # __call__ method that takes a sequence of pairs and returns a sequence of similarity values
    def __call__(self, pairs: Sequence[tuple[V, V]], /) -> SimSeq[S]: ...



class SimPairFunc[V, S: float]:
    # __call__ method that takes two values and returns a similarity value
    def __call__(self, x: V, y: V, /) -> S: ...


type AnySimFunc[V, S: float] = SimPairFunc[V, S] | SimSeqFunc[V, S]

@runtime_checkable
class SupportsMetadata(Protocol):
    @property
    def metadata(self) -> JsonDict:
        if dataclasses.is_dataclass(self):
            return dataclasses.asdict(self)

        return {}

class RetrieverFunc[K, V, S: float](Protocol):
    def __call__(
        self,
        casebase: Mapping[K, V],
        query: V,
        processes: int,
    ) -> SimMap[K, S]: ...


class AdaptPairFunc[V](Protocol):
    def __call__(
        self,
        case: V,
        query: V,
    ) -> V: ...


class AdaptMapFunc[K, V](Protocol):
    def __call__(
        self,
        casebase: Casebase,
        query: V,
    ) -> Casebase[K, V]: ...


class AdaptReduceFunc[K, V](Protocol):
    def __call__(
        self,
        casebase: Casebase,
        query: V,
    ) -> tuple[K, V]: ...


type AnyAdaptFunc[K, V] = AdaptPairFunc[V] | AdaptMapFunc[K, V] | AdaptReduceFunc[K, V]


class ReuserFunc[K, V, S: float](Protocol):
    def __call__(
        self,
        casebase: Casebase,
        query: V,
        processes: int,
    ) -> Casebase[K, tuple[V | None, S]]: ...


class AggregatorFunc[K, S: float](Protocol):
    def __call__(
        self,
        similarities: SimSeqOrMap[K, S],
        /,
    ) -> float: ...


class PoolingFunc(Protocol):
    def __call__(
        self,
        similarities: SimSeq[float],
        /,
    ) -> float: ...
