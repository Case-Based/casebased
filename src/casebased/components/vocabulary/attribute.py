from typing import Optional, Union

from casebased.utils.errors import (
    InvalidAttributeTypeError,
    MissingConditionParametersError,
)

from .conditions import Condition, ConditionType


class Attribute:
    """
    A case consists of several attributes that define how the case is structured and which values the case can take.
    Essentially, a case is like a Python dictionary that has attributes, however these attributes are streamlined within a vocabulary to ensure data quality.

    Attributes:
        __name: str : Name of the attribute that acts as a unique identifier
        __weight: None or float : Multiplier of the attribute value. This is by default 1.0
        __data_type: int or float : Defines the type of the value. This property is mainly used to validate values
        __conditions: list of Conditions : Defines which values the attribute can take
        __is_target: bool : Defines whether the attribute is a target attribute
    """

    __name: str
    __weight: Optional[float]
    __data_type: int | float
    __conditions: list[Condition]
    __is_target: bool

    def __init__(
        self,
        name: str,
        weight: Optional[float],
        data_type: int | float,
        conditions: list[Condition],
        is_target: Optional[bool],
    ):
        """
        Create an Attribute instance.

        Args:
            name: str :
                Unique identifier in case structure
            weight: None or float :
                Multiplier of the attribute value. Default is 1.0
            data_type: int or float :
                Used to validate attribute values. Can either be int or float
            conditions: list of Condition objects :
                Conditions that the attribute value has to meet
            is_target: bool :
                Defines whether the attribute is a target
        """
        self.__name = name
        self.__weight = weight or 1.0
        self.__data_type = data_type
        self.__conditions = conditions
        self.__is_target = is_target or False

    @staticmethod
    def from_dict(attribute_dict: dict):
        """
        Create an attribute instance based on a dictionary structure.
        The dictionary should at least include the column 'name' which is used to clearly identify an attribute in a vocabulary.
        All other columns like 'weight', 'data_type', 'conditions' and 'is_target' will receive a default value when being empty.

        Default values:
            weight: 1.0 \n
            data_type: int \n
            conditions: [] \n
            is_target: False

        Args:
            attribute_dict: dict
        Returns:
            Attribute
        """
        conditions = Attribute.convert_conditions_from_dict_list(
            attribute_dict.get("conditions") or []
        )
        return Attribute(
            name=attribute_dict["name"],
            weight=attribute_dict.get("weight") or 1.0,
            data_type=float if attribute_dict.get("type") in ("float", float) else int,
            conditions=conditions,
            is_target=(
                True if attribute_dict.get("is_target") in (True, "true") else False
            ),
        )

    @staticmethod
    def convert_conditions_from_dict_list(
        con_list: list[dict], hard_validation: bool = False
    ):
        """
        Using this method you can generate conditions from a list of dictionaries.
        Each dictionary has to have the fields 'type' and 'check_value'.
        If one of the fields is not given, the function will fail based on the validation mode you chose (by default soft).
        When the validation mode is set to hard, the method will raise an exception whenever one of the fields is missing.

        Args:
            con_list: list of dictionaries :
                Define the conditions
            hard_validation: bool :
                Switch between hard and soft validation mode
        Returns:
            list of Conditions
        """
        return [Condition.from_dict(con, hard_validation) for con in con_list]

    @staticmethod
    def from_name_string(name: str):
        """
        Create an attribute from a string name.
        The method will only take the name as input and uses default values for the fields 'weight', 'data_type', 'conditions', and 'is_target'.

        Default values:
            weight: 1.0 \n
            data_type: int \n
            conditions: [] \n
            is_target: False

        Args:
            name: str :
                Unique name of the attribute
        Returns:
            Attribute
        """
        return Attribute(
            name=name,
            weight=1.0,
            data_type=int,
            conditions=[],
            is_target=False,
        )

    def validate(self, value: Union[int, float], hard_validation: bool = False):
        """
        Validate type and conditions for the given value.
        You can choose the validation mode by setting the hard validation argument to either True or False.
        When set to True, the method will raise an exception when either the value type or one of the conditions aren't met.

        Args:
            value: int or float :
                Numerical value the attribute should take
            hard_validation: bool :
                Switch the validation mode to either hard or soft validation
        Returns:
            bool
        """
        return self.__validate_value(value, hard_validation) and (
            self.__validate_type_hard(value)
            if hard_validation
            else self.__validate_type_soft(value)
        )

    def validate_value(self, value: Union[int, float], hard_validation: bool = False):
        """
        Only validate the value using the conditions, not the type.
        You can choose the validation mode by setting the hard validation argument to either True or False.
        When set to True, the method will raise an exception when one of the conditions isn't met.

        Args:
            value: int or float :
                Value to be validated
            hard_validation: bool :
                Validation mode that can be either True (hard) or False (soft). Soft mode by default.
        Returns:
            bool
        """
        return self.__validate_value(value, hard_validation)

    def validate_type(self, value: Union[int, float], hard_validation: bool = False):
        """
        Only validate the value's type, but not the conditions.
        You can choose the validation mode by setting the hard validation argument to either True or False.
        When set to True, the method will raise an exception when one of the conditions isn't met.

        Args:
            value: int or float :
                Value to be validated
            hard_validation: bool :
                Validation mode that can be either True (hard) or False (soft). Soft mode by default.
        Returns:
            bool
        """
        return (
            self.__validate_type_hard(value)
            if hard_validation
            else self.__validate_type_soft(value)
        )

    def __validate_value(self, value: Union[int, float], hard_validation: bool = False):
        """
        Only validate the value using the conditions, not the type.
        You can choose the validation mode by setting the hard validation argument to either True or False.
        When set to True, the method will raise an exception when one of the conditions isn't met.

        Args:
            value: int or float :
                Value to be validated
            hard_validation: bool :
                Validation mode that can be either True (hard) or False (soft). Soft mode by default.
        Returns:
            bool
        """
        for condition in self.__conditions:
            result: bool = condition.check_value(value, hard_validation)
            if result is False:
                return False
        return True

    def __validate_type_hard(self, value: Union[int, float]):
        """
        Validate the value's type by using the hard validation mode.

        Args:
            value: int or float :
                Value to be validated
        Returns:
            bool
        """
        if isinstance(value, self.__data_type):
            return True
        else:
            raise InvalidAttributeTypeError(
                actual_type=type(value),
                actual_value=value,
                expected_type=self.__data_type,
            )

    def __validate_type_soft(self, value: Union[int, float]):
        """
        Validate the value's type by using the soft validation mode.

        Args:
            value: int or float :
                Value to be validated
        Returns:
            bool
        """
        return isinstance(value, self.__data_type)

    def to_dict(self):
        """
        Convert an attribute instance to a dictionary.

        Returns:
            dict
        """
        return {
            self.__name: {
                "weight": self.__weight,
                "type": self.__data_type,
                "is_target": self.__is_target,
                "conditions": [con.to_dict() for con in self.__conditions],
            }
        }

    @property
    def name(self):
        """
        Return the attribute name.

        Returns:
            str
        """
        return self.__name

    @property
    def weight(self):
        """
        Return the attribute weight.

        Returns:
            float
        """
        return self.__weight

    @property
    def data_type(self):
        """
        Returns the attribute data type.

        Returns:
            type
        """
        return self.__data_type

    @property
    def is_target(self):
        """
        Returns whether the attribute is a target attribute.

        Returns:
            bool
        """
        return self.__is_target

    @property
    def conditions(self):
        """
        Returns the conditions a value has to meet.

        Returns:
            list of conditions
        """
        return self.__conditions
