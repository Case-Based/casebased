from dataclasses import dataclass

from .attribute import FeatureAttribute, TargetAttribute
from typing import Mapping, Union, Optional


@dataclass(frozen=True)
class CaseDefinition:
    feature_attributes: list[FeatureAttribute]
    target_attributes: list[TargetAttribute]
    

@dataclass(frozen=True)
class Case:
    feature_attributes: Mapping[str, Union[str, int, float]]
    target_attributes: Mapping[str, Optional[Union[str, int, float]]]
    utility: int = 0
    
