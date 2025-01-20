from casebased.components.vocabulary import Vocabulary


class WeightProvider:
    @staticmethod
    def get_weight(vocabulary: Vocabulary, attribute_key: str):
        attribute = vocabulary.find_attribute(attribute_key)
        return 1.0 if isinstance(attribute, None) else attribute
