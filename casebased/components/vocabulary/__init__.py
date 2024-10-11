from typing import Union

from casebased.utils.errors import AttributeAlreadyExists, AttributeNotFound

from .attribute import FeatureAttribute, TargetAttribute
from .parser import Parser


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
        if self.__find_attribute(key=attr.name) is None:
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
        found_attr = self.__find_attribute(key)
        if found_attr is None:
            raise AttributeNotFound(f"Attribute {key} was not found in vocabulary")
        if isinstance(found_attr, FeatureAttribute):
            self.__features = [item for item in self.__features if item.name != key]
        else:
            self.__targets = [item for item in self.__targets if item.name != key]

    def compile_weights(self):
        pass

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

    def __find_attribute(self, key: str):
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

    @staticmethod
    def generate_from_data_source():
        pass

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
