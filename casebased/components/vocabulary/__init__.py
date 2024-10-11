from typing import Union

import toml

from casebased.utils.errors import AttributeAlreadyExists, AttributeNotFound

from .attribute import Attribute, FeatureAttribute, TargetAttribute


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


class Parser:
    @staticmethod
    def generate_toml_file(vocabulary: Vocabulary, file_path: str):
        """
        Generate a TOML file from a vocabulary instance.

        Args:
            vocabulary: Vocabulary
            file_path: str
        """
        raw_vocab = vocabulary.to_dict()
        path_list = file_path.split("/")
        file_comps = path_list[-1].split(".")
        folder_path = path_list[:-1]
        new_path = (
            folder_path + [".".join(file_comps + ["toml"])]
            if file_comps[-1] != "toml"
            else path_list
        )
        with open("/".join(new_path), "w") as file:
            toml.dump(raw_vocab, file)

    @staticmethod
    def generate_vocabulary_from_toml(file_path: str):
        """
        Generate a vocabulary instance from a TOML file.
        The TOML file needs to have a specific format. It consists of attributes that have certain characteristics.
        An attribute needs to have the following fields 'type' (data type), 'conditions' (list of object with fields 'operator' and 'value'), and 'is_target'.
        Feature attributes also can have a weight field acting as a multiplier for attribute values.

        Args:
            file_path: str :
                Path to the TOML file
        Returns:
            Vocabulary
        """
        raw_vocab = toml.load(file_path)
        target_attributes = []
        feature_attributes = []
        for key, val in raw_vocab.items():
            raw_attr = {
                "name": key,
                "weight": val.get("weight"),
                "conditions": val.get("conditions"),
                "type": val.get("type"),
                "is_target": val.get("is_target"),
            }
            attr = Attribute.from_dict(raw_attr)
            (
                target_attributes.append(attr)
                if val.get("is_target") == "true"
                else feature_attributes.append(attr)
            )
        return Vocabulary(
            features=feature_attributes,
            targets=target_attributes,
        )
