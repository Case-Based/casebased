from typing import Union

from enum import Enum

from casebased.utils.errors import (
    InvalidAttributeValueError,
    MissingConditionParametersError,
)


class ConditionType(Enum):
    """
    The condition type defines how values are getting checked by the vocabulary validater.
    You have six different operators that you can choose from.

    The values will be checked as follows. If you for example provide the type "eq" for equals and the check value 10 the system would do the following check.

    10 == x

    x is provided by the user or validater that validates the case base, meaning it's a dynamic value.

    Operators:
    - Equals (eq)
    - Not Equals (neq)
    - Greater than (gt)
    - Greater than or equals (gte)
    - Lower than (lt)
    - Lower than or equals (lte)
    """

    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER_THAN = "gt"
    GREATER_THAN_EQUALS = "gte"
    LOWER_THAN = "lt"
    LOWER_THAN_EQUALS = "lte"


# Lambda functions to validate values
CHECK_FUNCTIONS = {
    "eq": lambda val, check_val: val == check_val,
    "neq": lambda val, check_val: val != check_val,
    "gt": lambda val, check_val: val > check_val,
    "gte": lambda val, check_val: val >= check_val,
    "lt": lambda val, check_val: val < check_val,
    "lte": lambda val, check_val: val <= check_val,
}

# Used to generate the exception message for hard validation mode
ERROR_TEXT_FN = {
    "eq": lambda val, check_val: f"Value {val} should be equal to {check_val}",
    "neq": lambda val, check_val: f"Value {val} shouldn't be equal to {check_val}",
    "gt": lambda val, check_val: f"Value {val} should be greater than {check_val}",
    "gte": lambda val, check_val: f"Value {val} should be greater than or equals {check_val}",
    "lt": lambda val, check_val: f"Value {val} should be lower than {check_val}",
    "lte": lambda val, check_val: f"Value {val} should be lower than or equals {check_val}",
}


class Condition:
    """
    Conditions are part of the internal vocabulary validater.
    Users can define certain conditions that a specific attribute in the vocabulary structure has to fulfill.
    The condition class consists of two attributes namely the condition type and check value, which the validater is checking against.
    However, all attributes are private and shouldn't be touched by users.
    They can only be accessed by the con_type and check_val methods.

    Attributes:
        __con_type: ConditionType
            Type of the comparison.
        __check_val: Union[int, float]
            Value the validater checks against.
    """

    __con_type: ConditionType
    __check_val: Union[int, float]

    def __init__(self, con_type: ConditionType, check_val: Union[int, float]):
        """
        Create a condition instance that you can use in the vocabulary definition.

        Parameters:
            con_type: ConditionType
            check_val: Union[int, float]
        """
        self.__con_type = con_type
        self.__check_val = check_val

    @staticmethod
    def from_dict(con: dict, hard_validation: bool = False):
        """
        Generate a condition instance from a dictionary.
        You can choose between hard and soft (by default) validation.
        When you chose hard validation the method will raise an exception, otherwise it will return None.

        Args:
            con: dict
            hard_validation: bool
        Returns:
            Condition or None
        """
        operator = con.get("operator")
        check_val = con.get("value")
        if hard_validation and operator is None:
            raise MissingConditionParametersError(
                missing_attribute_name="condition type",
            )
        if hard_validation and check_val is None:
            raise MissingConditionParametersError(
                missing_attribute_name="check value",
            )
        return (
            None
            if None in (operator, check_val)
            else Condition(
                con_type=ConditionType(operator),
                check_val=check_val,
            )
        )

    def to_dict(self):
        """
        Receive the condition object as dictionary.
        Values in the return documentation are examples.

        Returns:
            {
                "type": "eq",
                "check_value": 10,
            }
        """
        return {
            "type": self.con_type.value,
            "check_value": self.check_val,
        }

    def check_value(self, value: Union[int, float], hard_validation: bool = False):
        """
        Check a value you provide against the defined condition.
        The value can either be checked in hard or soft mode, where the soft mode is the default.
        When validating using the hard mode, an exception will be raised when one of the conditions fails.

        Args:
            value: Union[int, float]: The value that should be checked against the condition.
            hard_validation: bool: Hard validation will raise an exception when the value doesn't meet the condition.

        Returns:
            boolean
        """
        check_fn = CHECK_FUNCTIONS[self.con_type.value]
        result: bool = check_fn(value, self.check_val)
        if hard_validation and result is False:
            raise InvalidAttributeValueError(
                message=ERROR_TEXT_FN[self.con_type.value](value, self.check_val),
            )
        return result

    @property
    def con_type(self):
        """
        Get the condition type.

        Returns:
            ConditionType
        """
        return self.__con_type

    @property
    def check_val(self):
        """
        Get the check value which the condition is checked against.

        Returns:
            Union[int, float]
        """
        return self.__check_val
