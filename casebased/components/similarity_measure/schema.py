from dataclasses import dataclass
from typing import Optional, Mapping
from .types import SimilarityFunction


@dataclass(frozen=True)
class SimilaritySchema():
    attributes: Mapping[str, SimilarityFunction]
    threshold: Optional[int]
    limit: Optional[int] = 5
