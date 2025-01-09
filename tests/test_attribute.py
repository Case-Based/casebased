import pytest

from casebased.components.vocabulary.attribute import (
    Attribute,
)
from casebased.components.vocabulary.conditions import Condition, ConditionType
from casebased.utils.errors import InvalidAttributeTypeError, InvalidAttributeValueError

ATTRIBUTE_FROM_DICT_TEST_PROPS = [
    {
        "test_props": {
            "name": "Data type int, is target True, weight 10.0, conditions 1, condition equals to 10",
            "type": int,
            "is_target": True,
            "weight": 10.0,
            "conditions": [
                {
                    "operator": "eq",
                    "value": 10,
                }
            ],
        },
        "expected_result": {
            "attr_type": Attribute,
            "condition_length": 1,
            "conditions": [
                Condition(
                    con_type=ConditionType.EQUALS,
                    check_val=10,
                )
            ],
        },
    },
    {
        "test_props": {
            "name": "Data type int, is target False, weight 10.0, conditions 2, condition one greater than 10, condition two lower than 12",
            "type": int,
            "is_target": False,
            "weight": 10.0,
            "conditions": [
                {
                    "operator": "gt",
                    "value": 10,
                },
                {
                    "operator": "lt",
                    "value": 12.0,
                },
            ],
        },
        "expected_result": {
            "attr_type": Attribute,
            "condition_length": 2,
            "conditions": [
                Condition(
                    con_type=ConditionType.GREATER_THAN,
                    check_val=10,
                ),
                Condition(
                    con_type=ConditionType.LOWER_THAN,
                    check_val=12,
                ),
            ],
        },
    },
    {
        "test_props": {
            "name": "Data type float, is target True, weight 12.0, conditions 0",
            "type": float,
            "is_target": True,
            "weight": 12.0,
            "conditions": [],
        },
        "expected_result": {
            "attr_type": Attribute,
            "condition_length": 0,
            "conditions": [],
        },
    },
]

TEST_CASES_CHECK_VALUES = [
    {
        "condition": Attribute(
            name="age",
            data_type=int,
            weight=1.0,
            is_target=False,
            conditions=[
                Condition(
                    con_type=ConditionType.GREATER_THAN_EQUALS,
                    check_val=0,
                ),
            ],
        ),
        "expected_soft": [
            {"value": 10, "expected_result": True},
            {"value": 0, "expected_result": True},
            {"value": -1, "expected_result": False},
        ],
        "expected_hard": [
            {
                "value": -1,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value -1 should be greater than or equals 0",
            },
        ],
    },
    {
        "condition": Attribute(
            name="day",
            data_type=int,
            weight=1.0,
            is_target=False,
            conditions=[
                Condition(
                    con_type=ConditionType.GREATER_THAN,
                    check_val=0,
                ),
                Condition(
                    con_type=ConditionType.LOWER_THAN,
                    check_val=32,
                ),
            ],
        ),
        "expected_soft": [
            {"value": 10, "expected_result": True},
            {"value": 0, "expected_result": False},
            {"value": -1, "expected_result": False},
            {"value": 32, "expected_result": False},
        ],
        "expected_hard": [
            {
                "value": 0,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value 0 should be greater than 0",
            },
            {
                "value": -1,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value -1 should be greater than 0",
            },
            {
                "value": 32,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value 32 should be lower than 32",
            },
        ],
    },
    {
        "condition": Attribute(
            name="dividend",
            data_type=int,
            weight=1.0,
            is_target=False,
            conditions=[
                Condition(
                    con_type=ConditionType.NOT_EQUALS,
                    check_val=0,
                ),
            ],
        ),
        "expected_soft": [
            {"value": 10, "expected_result": True},
            {"value": 0, "expected_result": False},
            {"value": -1, "expected_result": True},
            {"value": 32, "expected_result": True},
        ],
        "expected_hard": [
            {
                "value": 0,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value 0 shouldn't be equal to 0",
            },
        ],
    },
    {
        "condition": Attribute(
            name="item_upper_bound",
            data_type=int,
            weight=1.0,
            is_target=False,
            conditions=[
                Condition(
                    con_type=ConditionType.LOWER_THAN_EQUALS,
                    check_val=10,
                ),
                Condition(
                    con_type=ConditionType.GREATER_THAN,
                    check_val=-1,
                ),
            ],
        ),
        "expected_soft": [
            {"value": 10, "expected_result": True},
            {"value": 0, "expected_result": True},
            {"value": -1, "expected_result": False},
            {"value": 32, "expected_result": False},
        ],
        "expected_hard": [
            {
                "value": -1,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value -1 should be greater than -1",
            },
            {
                "value": 32,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value 32 should be lower than or equals 10",
            },
        ],
    },
]

TEST_CASES_CHECK_TYPE = [
    {
        "condition": Attribute(
            name="item_upper_bound",
            data_type=int,
            weight=1.0,
            is_target=False,
            conditions=[
                Condition(
                    con_type=ConditionType.LOWER_THAN_EQUALS,
                    check_val=10,
                ),
                Condition(
                    con_type=ConditionType.GREATER_THAN,
                    check_val=-1,
                ),
            ],
        ),
        "expected_soft": [
            {"value": 10, "expected_type": True},
            {"value": 11.5, "expected_type": False},
        ],
        "expected_hard": [
            {
                "value": 11.5,
                "expected_exception": InvalidAttributeTypeError,
                "expected_message": "Value 11.5 must be of type <class 'int'> but is <class 'float'>",
            },
        ],
    },
    {
        "condition": Attribute(
            name="item_upper_bound",
            data_type=float,
            weight=1.0,
            is_target=False,
            conditions=[
                Condition(
                    con_type=ConditionType.LOWER_THAN_EQUALS,
                    check_val=11.5,
                ),
                Condition(
                    con_type=ConditionType.GREATER_THAN,
                    check_val=-1.5,
                ),
            ],
        ),
        "expected_soft": [
            {"value": 10, "expected_type": False},
            {"value": 11.5, "expected_type": True},
        ],
        "expected_hard": [
            {
                "value": 11,
                "expected_exception": InvalidAttributeTypeError,
                "expected_message": "Value 11 must be of type <class 'float'> but is <class 'int'>",
            },
        ],
    },
]

TEST_CASES_CHECK_ALL = [
    {
        "attribute": Attribute(
            name="item",
            is_target=False,
            data_type=int,
            conditions=[
                Condition(
                    con_type=ConditionType.GREATER_THAN,
                    check_val=-1,
                ),
            ],
            weight=1.0,
        ),
        "expected_soft": [
            {"value": -1.5, "expected_output": False},
            {"value": -1, "expected_output": False},
            {"value": 2.5, "expected_output": False},
            {"value": 2, "expected_output": True},
        ],
        "expected_hard": [
            {
                "value": -1.5,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value -1.5 should be greater than -1",
            },
            {
                "value": -1,
                "expected_exception": InvalidAttributeValueError,
                "expected_message": "Value -1 should be greater than -1",
            },
            {
                "value": 2.5,
                "expected_exception": InvalidAttributeTypeError,
                "expected_message": "Value 2.5 must be of type <class 'int'> but is <class 'float'>",
            },
        ],
    }
]

def test__attribute_from_dict():
    for test in ATTRIBUTE_FROM_DICT_TEST_PROPS:
        attr_dict = test["test_props"]
        expected_values = test["expected_result"]
        attr = Attribute.from_dict(attr_dict)
        assert isinstance(attr, expected_values["attr_type"])
        assert attr.name == attr_dict["name"]
        assert attr.weight == attr_dict["weight"]
        assert attr.data_type is attr_dict["type"]
        assert attr.is_target is attr_dict["is_target"]
        assert len(attr.conditions) == expected_values["condition_length"]
        for i in range(len(attr.conditions)):
            actual_attr = attr.conditions[i]
            expected_attr = expected_values["conditions"][i]
            assert actual_attr.con_type == expected_attr.con_type
            assert actual_attr.check_val == expected_attr.check_val


def test__attribute_from_str_name():
    name = "age"
    attr = Attribute.from_name_string(name)
    assert attr is not None
    assert attr.name == name
    assert attr.weight == 1.0
    assert attr.data_type is int
    assert attr.is_target is False
    assert len(attr.conditions) == 0


def test__validate_value_soft():
    for test in TEST_CASES_CHECK_VALUES:
        attr = test["condition"]
        for case in test["expected_soft"]:
            assert attr.validate_value(case["value"]) is case["expected_result"]


def test__validate_value_hard():
    for test in TEST_CASES_CHECK_VALUES:
        attr = test["condition"]
        for case in test["expected_hard"]:
            with pytest.raises(case["expected_exception"]) as err:
                attr.validate(case["value"], True)
            assert err.value.args[0] == case["expected_message"]


def test__validate_type_soft():
    for test in TEST_CASES_CHECK_TYPE:
        attr = test["condition"]
        for case in test["expected_soft"]:
            assert attr.validate_type(case["value"], False) is case["expected_type"]


def test__validate_type_hard():
    for test in TEST_CASES_CHECK_TYPE:
        attr = test["condition"]
        for case in test["expected_hard"]:
            with pytest.raises(case["expected_exception"]) as err:
                attr.validate_type(case["value"], True)
            assert err.value.args[0] == case["expected_message"]


def test__validate_all_soft():
    for test in TEST_CASES_CHECK_ALL:
        attr = test["attribute"]
        for case in test["expected_soft"]:
            print(f'res {attr.validate(case["value"], False)}')
            assert attr.validate(case["value"], False) is case["expected_output"]


def test__validate_all_hard():
    for test in TEST_CASES_CHECK_ALL:
        attr = test["attribute"]
        for case in test["expected_hard"]:
            with pytest.raises(case["expected_exception"]) as err:
                attr.validate(case["value"], True)
            assert err.value.args[0] == case["expected_message"]
