from typing import Mapping, Optional, Union

from dataclasses import dataclass

from .attribute import FeatureAttribute, TargetAttribute


@dataclass(frozen=True)
class CaseDefinition:
    feature_attributes: list[FeatureAttribute]
    target_attributes: list[TargetAttribute]


@dataclass(frozen=True)
class Case:
    feature_attributes: Mapping[str, Union[str, int, float]]
    target_attributes: Mapping[str, Optional[Union[str, int, float]]]
    utility: int = 0

    def get_feature_keys(self) -> list[str]:
        return self.feature_attributes.keys()

    def get_feature_value_by_key(self, key: str) -> Union[str, int, float]:
        return self.feature_attributes[key]
