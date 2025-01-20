from typing import Optional, Union

from dataclasses import dataclass

from casebased.utils.errors import InvalidAttributeTypeError

from .conditions import Condition


@dataclass(frozen=True)
class Attribute:
    """
    A case consists of several attributes that define how the case is structured and which values the case can take.
    Essentially, a case is like a Python dictionary that has attributes, however these attributes are streamlined within a vocabulary to ensure data quality.

    Attributes:
        name: str : Name of the attribute that acts as a unique identifier
        weight: None or float : Multiplier of the attribute value. This is by default 1.0
        data_type: int or float : Defines the type of the value. This property is mainly used to validate values
        conditions: list of Conditions : Defines which values the attribute can take
        is_target: bool : Defines whether the attribute is a target attribute
    """

    name: str
    weight: Optional[float]
    data_type: type[Union[int, float, str, bool]]
    conditions: list[Condition]
    is_target: bool

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
            name=attribute_dict.get("name"),
            weight=attribute_dict.get("weight") or 1.0,
            data_type=attribute_dict.get("type") or int,
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

    def validate(
        self, value: Union[int, float, str, bool], hard_validation: bool = False
    ):
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

    def validate_value(
        self, value: Union[int, float, str, bool], hard_validation: bool = False
    ):
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

    def validate_type(
        self, value: Union[int, float, str, bool], hard_validation: bool = False
    ):
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

    def __validate_value(
        self, value: Union[int, float, str, bool], hard_validation: bool = False
    ):
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
        for condition in self.conditions:
            result: bool = condition.check_value(value, hard_validation)
            if result is False:
                return False
        return True

    def __validate_type_hard(self, value: Union[int, float, str, bool]):
        """
        Validate the value's type by using the hard validation mode.

        Args:
            value: int or float :
                Value to be validated
        Returns:
            bool
        """
        if isinstance(value, self.data_type):
            return True
        else:
            raise InvalidAttributeTypeError(
                actual_type=type(value),
                actual_value=value,
                expected_type=self.data_type,
            )

    def __validate_type_soft(self, value: Union[int, float, str, bool]):
        """
        Validate the value's type by using the soft validation mode.

        Args:
            value: int or float :
                Value to be validated
        Returns:
            bool
        """
        return isinstance(value, self.data_type)

    def to_dict(self):
        """
        Convert an attribute instance to a dictionary.

        Returns:
            dict
        """
        return {
            self.name: {
                "weight": self.weight,
                "type": self.data_type,
                "is_target": self.is_target,
                "conditions": [con.to_dict() for con in self.conditions],
            }
        }


@dataclass(frozen=True)
class TargetAttribute(Attribute):
    """
    Target attributes describe the solution of a case.
    """

    def __init__(
        self,
        name: str,
        data_type: type[Union[int, float, str, bool]],
        conditions: list[Condition],
    ):
        """
        Create a target attribute by providing the name, data_type and conditions.

        Args:
            name: str :
                Unique attribute key
            data_type: int or float type :
                The type a value should have
            conditions: list of Conditions :
                Conditions a new value has to meet
        """
        super().__init__(
            name=name,
            data_type=data_type,
            conditions=conditions,
            weight=1.0,
            is_target=True,
        )


@dataclass(frozen=True)
class FeatureAttribute(Attribute):
    """
    Feature attributes are used to calculate the similarity between cases.
    These attributes are used to reason the fitting solution, specifically the target attribute.
    """

    def __init__(
        self,
        name: str,
        data_type: type[Union[int, float, str, bool]],
        conditions: list[Condition],
        weight: float = 1.0,
    ):
        """
        Create a feature attribute by providing the name, data_type, weight, and conditions.

        Args:
            name: str :
                Unique attribute key
            data_type: int or float type :
                The type a value should have
            conditions: list of Conditions :
                Conditions a new value has to meet
            weight: float :
                Multiplier of the value
        """
        super().__init__(
            name=name,
            data_type=data_type,
            weight=weight,
            is_target=False,
            conditions=conditions,
        )
