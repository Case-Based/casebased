from typing import Union


class InvalidAttributeValueError(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidAttributeTypeError(Exception):
    message: str

    def __init__(
        self, actual_type: type, expected_type: type, actual_value: Union[int, float]
    ):
        msg = (
            f"Value {actual_value} must be of type {expected_type} but is {actual_type}"
        )
        super().__init__(msg)
        self.message = msg


class MissingConditionParametersError(Exception):
    message: str

    def __init__(self, missing_attribute_name: str):
        msg = f"Parameter '{missing_attribute_name}' is missing for the condition creation"
        super().__init__(msg)
        self.message = msg


class AttributeAlreadyExists(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AttributeNotFound(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
