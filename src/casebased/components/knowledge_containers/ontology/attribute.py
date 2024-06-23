from typing import Any, Optional, Type, Union

import numpy as np

from casebased.utils.errors import InvalidAttributeTypeError, InvalidAttributeValueError


class Attribute:
    def __init__(
        self,
        name: str,
        min_value: Union[float, int],
        max_value: Union[float, int],
        weight: Optional[float],
        data_type: tuple[Type[Any]],
        exclusive_min: bool = False,
        exclusive_max: bool = False,
    ):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.weight = weight
        self.data_type = data_type
        self.exclusive_min = exclusive_min
        self.exclusive_max = exclusive_max

    @staticmethod
    def from_dict(attribute_dict: dict):
        return Attribute(
            name=attribute_dict["name"],
            min_value=attribute_dict["min_value"],
            max_value=attribute_dict["max_value"],
            weight=attribute_dict["weight"],
            data_type=attribute_dict["data_type"],
            exclusive_min=attribute_dict["exclusive_min"],
            exclusive_max=attribute_dict["exclusive_max"],
        )

    @staticmethod
    def from_name_string(name: str):
        return Attribute(
            name=name,
            min_value=-np.Inf,
            max_value=np.Inf,
            weight=1.0,
            data_type=Any,
            exclusive_min=False,
            exclusive_max=False,
        )

    def validate_value(self, value: Union[float, int], hard_val=False) -> bool:
        """
        Validate the value of the attribute
        Args:
            value: Union[float, int] : Value to be validated
            hard_val: bool : Whether to raise an exception or not
        Returns:
            bool : Whether the value is valid or not
            raises InvalidAttributeValueError : If the value is invalid
        """
        if hard_val:
            return self.__validate_value_hard(value)
        else:
            return self.__validate_value_soft(value)

    def validate_type(self, value: Union[float, int], hard_val=False) -> bool:
        """
        Validate the type of the attribute
        Args:
            value: Union[float, int] : Value to be validated
            hard_val: bool : Whether to raise an exception or not
        Returns:
            bool : Whether the value is valid or not
            raises InvalidAttributeTypeError : If the value is invalid
        """
        if Any in self.data_type:
            return True
        if hard_val:
            return self.__validate_type_hard(value)
        else:
            return self.__validate_type_soft(value)

    def validate(self, value: Union[float, int], hard=False) -> bool:
        """
        Validate the value of the attribute
        Args:
            value: Union[float, int] : Value to be validated
            hard: bool : Whether to raise an exception or not
        Returns:
            bool : Whether the value is valid or not
            raises InvalidAttributeValueError : If the value is invalid
        """
        if hard:
            return self.__validate_hard(value)
        else:
            return self.__validate_soft(value)

    def __validate_value_hard(self, value: Union[float, int]) -> bool:
        if self.exclusive_max and value == self.max_value:
            raise InvalidAttributeValueError(
                f"Value {value} is equal to the maximum value \
                {self.max_value} with exclusive max"
            )
        if self.exclusive_min and value == self.min_value:
            raise InvalidAttributeValueError(
                f"Value {value} is equal to the minimum \
                     value {self.min_value} with exclusive min"
            )
        if value < self.min_value:
            raise InvalidAttributeValueError(
                f"Value {value} is less than the minimum value {self.min_value}"
            )
        if value > self.max_value:
            raise InvalidAttributeValueError(
                f"Value {value} is greater than the maximum value {self.max_value}"
            )
        return True

    def __validate_value_soft(self, value: Union[float, int]) -> bool:
        if self.exclusive_max and (value == self.max_value or value == self.min_value):
            return False
        if value < self.min_value or value > self.max_value:
            return False
        return True

    def __validate_type_hard(self, value: Union[float, int]) -> bool:
        if not isinstance(value, self.data_type):
            raise InvalidAttributeTypeError(
                f"Value {value} is not of attribute type {self.data_type}"
            )
        return True

    def __validate_type_soft(self, value: Union[float, int]) -> bool:
        return isinstance(value, self.data_type)

    def __validate_hard(self, value: Union[float, int]) -> bool:
        if not self.__validate_type_hard(value):
            return False
        return self.__validate_value_hard(value)

    def __validate_soft(self, value: Union[float, int]) -> bool:
        return self.__validate_type_soft(value) and self.__validate_value_soft(value)


class TargetAttribute(Attribute):
    def __init__(
        self,
        name: str,
        data_type: tuple[Type[Any]],
        min_value: Union[float, int] = -np.Inf,
        max_value: Union[float, int] = np.Inf,
        exclusive_min: bool = False,
        exclusive_max: bool = False,
    ):
        super().__init__(
            name, min_value, max_value, None, data_type, exclusive_min, exclusive_max
        )
        self.target = True


class FeatureAttribute(Attribute):
    def __init__(
        self,
        name: str,
        data_type: tuple[Type[Any]],
        min_value: Union[float, int] = -np.Inf,
        max_value: Union[float, int] = np.Inf,
        weight: float = 1.0,
        exclusive_min: bool = False,
        exclusive_max: bool = False,
    ):
        super().__init__(
            name, min_value, max_value, weight, data_type, exclusive_min, exclusive_max
        )
        self.target = False
