import toml

from .attribute import Attribute
from .vocabulary import Vocabulary


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
