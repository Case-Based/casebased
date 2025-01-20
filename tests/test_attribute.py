import unittest

from casebased.components.vocabulary.attribute import (
    Attribute,
    FeatureAttribute,
    TargetAttribute,
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


class TestAttribute(unittest.TestCase):
    def test__target_attribute_creation(self):
        attr = TargetAttribute(
            name="Test attribute",
            conditions=[],
            data_type=int,
        )

        self.assertIsNotNone(attr)
        self.assertIs(attr.is_target, True)
        self.assertEqual(attr.weight, 1.0)
        self.assertEqual(attr.name, "Test attribute")
        self.assertIs(attr.data_type, int)
        self.assertEqual(len(attr.conditions), 0)

    def test__feature_attribute_creation(self):
        attr = FeatureAttribute(
            name="Feature attr",
            conditions=[],
            data_type=float,
            weight=10.0,
        )

        self.assertIsNotNone(attr)
        self.assertIs(attr.is_target, False)
        self.assertEqual(attr.weight, 10.0)
        self.assertEqual(attr.name, "Feature attr")
        self.assertIs(attr.data_type, float)
        self.assertEqual(len(attr.conditions), 0)

    def test__attribute_from_dict(self):
        for test in ATTRIBUTE_FROM_DICT_TEST_PROPS:
            attr_dict = test["test_props"]
            expected_values = test["expected_result"]
            attr = Attribute.from_dict(attr_dict)

            self.assertIsInstance(attr, expected_values["attr_type"])
            self.assertEqual(attr.name, attr_dict["name"])
            self.assertEqual(attr.weight, attr_dict["weight"])
            self.assertIs(attr.data_type, attr_dict["type"])
            self.assertIs(attr.is_target, attr_dict["is_target"])
            self.assertEqual(len(attr.conditions), expected_values["condition_length"])

            for i in range(len(attr.conditions)):
                actual_attr = attr.conditions[i]
                expected_attr = expected_values["conditions"][i]

                self.assertEqual(actual_attr.con_type, expected_attr.con_type)
                self.assertEqual(actual_attr.check_val, expected_attr.check_val)

    def test__attribute_from_str_name(self):
        name = "age"
        attr = Attribute.from_name_string(name)

        self.assertIsNotNone(attr)
        self.assertEqual(attr.name, name)
        self.assertEqual(attr.weight, 1.0)
        self.assertIs(attr.data_type, int)
        self.assertIs(attr.is_target, False)
        self.assertEqual(len(attr.conditions), 0)

    def test__validate_value_soft(self):
        for test in TEST_CASES_CHECK_VALUES:
            attr = test["condition"]

            for case in test["expected_soft"]:
                self.assertIs(
                    attr.validate_value(case["value"]), case["expected_result"]
                )

    def test__validate_value_hard(self):
        for test in TEST_CASES_CHECK_VALUES:
            attr = test["condition"]
            for case in test["expected_hard"]:
                with self.assertRaises(case["expected_exception"]) as err:
                    attr.validate(case["value"], True)
                self.assertEqual(str(err.exception), case["expected_message"])

    def test__validate_type_soft(self):
        for test in TEST_CASES_CHECK_TYPE:
            attr = test["condition"]
            for case in test["expected_soft"]:
                self.assertIs(
                    attr.validate_type(case["value"], False), case["expected_type"]
                )

    def test__validate_type_hard(self):
        for test in TEST_CASES_CHECK_TYPE:
            attr = test["condition"]
            for case in test["expected_hard"]:
                with self.assertRaises(case["expected_exception"]) as err:
                    attr.validate_type(case["value"], True)
                self.assertEqual(str(err.exception), case["expected_message"])

    def test__validate_all_soft(self):
        for test in TEST_CASES_CHECK_ALL:
            attr = test["attribute"]
            for case in test["expected_soft"]:
                self.assertIs(
                    attr.validate(case["value"], False), case["expected_output"]
                )

    def test__validate_all_hard(self):
        for test in TEST_CASES_CHECK_ALL:
            attr = test["attribute"]
            for case in test["expected_hard"]:
                with self.assertRaises(case["expected_exception"]) as err:
                    attr.validate(case["value"], True)
                self.assertEqual(str(err.exception), case["expected_message"])
