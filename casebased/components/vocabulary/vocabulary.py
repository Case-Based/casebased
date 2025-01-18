from typing import Union

from casebased.utils.errors import AttributeAlreadyExists, AttributeNotFound

from .attribute import FeatureAttribute, TargetAttribute
from .parser import Parser
from .case import Case


class Vocabulary:
    """
    The vocabulary is used to manage the structure of cases used in a case-based reasoning system.
    Attributes along with conditions for each attribute can be defined, which values entered into the case base have to meet.
    """

    def __init__(
        self, features: list[FeatureAttribute], targets: list[TargetAttribute]
    ):
        """
        Create a new vocabulary by providing a list of feature and target attributes.

        Args:
            features: list[FeatureAttribute] :
                A list of feature attributes. Feature attributes are used to calculate the similarity between cases.
            targets: list[TargetAttribute] :
                A list of target attributes. These attributes are reflecting a case's solution.
        """
        self.__features = features
        self.__targets = targets

    def add_attribute(self, attr: Union[FeatureAttribute, TargetAttribute]):
        """
        Add an attribute to the vocabulary.

        Args:
            attr: FeatureAttribute or TargetAttribute :
                Attribute to add to the vocabulary
        """
        if self.find_attribute(key=attr.name) is None:
            raise AttributeAlreadyExists(
                f"Attribute with name {attr.name} already exists in vocabulary"
            )
        (
            self.__features.append(attr)
            if isinstance(attr, FeatureAttribute)
            else self.__targets.append(attr)
        )

    def remove_attribute(self, key: str):
        """
        Remove an attribute from the vocabulary using the attribute's unique key/name.
        An exception will be raised when the attribute couldn't be found.

        Args:
            key: str :
                Unique attribute key
        """
        found_attr = self.find_attribute(key)
        if found_attr is None:
            raise AttributeNotFound(f"Attribute {key} was not found in vocabulary")
        if isinstance(found_attr, FeatureAttribute):
            self.__features = [item for item in self.__features if item.name != key]
        else:
            self.__targets = [item for item in self.__targets if item.name != key]

    def save(self, file_path: str):
        """
        Save the current vocabulary state into a TOML file.

        Args:
            file_path: str :
                Define where the vocabulary should be stored
        """
        Parser.generate_toml_file(self, file_path)

    def to_dict(self):
        """
        Convert the vocabulary instance to a dictionary.

        Returns:
            dict
        """
        return {item.to_dict() for item in self.__targets + self.__features}

    def find_attribute(self, key: str):
        """
        Find an attribute using the attribute's unique key/name.
        This function will search in the target and feature attribute list.
        If the function couldn't find an attribute, it returns None.

        Args:
            key: str :
                Attribute's unique key/name
        Returns:
            FeatureAttribute or TargetAttribute or None
        """
        for attr in self.__targets + self.__features:
            if attr.name == key:
                return attr
        return None
    
    def validate_case(self, case: Case) -> bool:
        """
        Validate a case by checking whether all attributes are given 
        and whether the defined data type and conditions are met.

        Args:
            case: Case :
                The case to validate

        Returns:
            bool
        """
        success = True
        success = self.__validate_completeness(case)
        success = self.__validate_attributes(case)
        return success
    
    def __validate_completeness(self, case: Case) -> bool:
        """
        Validate a case by checking if all feature and target attributes are present.

        Args:
            case: Case :
                The case to validate

        Returns:
            bool
        """
        for feature in self.__features:
            if feature.name not in case.keys():
                return False
        for target in self.__targets:
            if target.name not in case.keys():
                return False
        return True
    
    def __validate_attributes(self, case: Case) -> bool:
        """
        Validate a case by checking if all attributes meet the defined conditions and data type.
        
        Args:
            case: Case : Case to be checked
            
        Returns:
            bool
        """
        success = True
        for key, value in case.feature_attributes:
            if success:
                attr_definition = self.find_attribute(key)
                success = attr_definition and attr_definition.validate(value)
            else:
                break
        
        if success:
            for key, value in case.target_attributes:
                if success and not isinstance(value, None):
                    attr_definition = self.find_attribute(key)
                    success = attr_definition and attr_definition.validate(value)
                else:
                    break
                    
        return success

    @property
    def features(self):
        """
        Get the list of feature attributes.

        Returns:
            list of FeatureAttributes
        """
        return self.__features

    @property
    def targets(self):
        """
        Get the list of target attributes.

        Returns:
            list of TargetAttributes
        """
        return self.__targets
