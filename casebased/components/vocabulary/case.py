from dataclasses import dataclass
from .attribute import FeatureAttribute, TargetAttribute


@dataclass(frozen=True)
class Case:
    feature_attributes: list[FeatureAttribute]
    target_attributes: list[TargetAttribute]
    utility: int = 0
