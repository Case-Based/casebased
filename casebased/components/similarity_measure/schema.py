from typing import Mapping, Optional

from dataclasses import dataclass

from .types import SimilarityFunction


@dataclass(frozen=True)
class SimilaritySchema:
    attributes: Mapping[str, SimilarityFunction]
    threshold: Optional[int]
    limit: Optional[int] = 5
