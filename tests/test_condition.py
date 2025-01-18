import unittest

from casebased.components.vocabulary.conditions import Condition, ConditionType

TEST_CASES_CREATION = [
    {
        "condition": {
            "type": "eq",
            "check_value": 10,
        },
        "tests": [
            {"value": 10, "result": True},
            {"value": 10.0, "result": True},
            {"value": 9, "result": False},
            {"value": 11, "result": False},
            {"value": 9.9999999, "result": False},
        ],
    },
    {
        "condition": {
            "type": "eq",
            "check_value": 10.5,
        },
        "tests": [
            {"value": 10.5, "result": True},
            {"value": 10, "result": False},
            {"value": 10.5000001, "result": False},
            {"value": 11.0, "result": False},
        ],
    },
    {
        "condition": {
            "type": "neq",
            "check_value": 20,
        },
        "tests": [
            {"value": 19, "result": True},
            {"value": 21, "result": True},
            {"value": 20, "result": False},
            {"value": 20.0, "result": False},
            {"value": 19.99999, "result": True},
        ],
    },
    {
        "condition": {
            "type": "neq",
            "check_value": 20.7,
        },
        "tests": [
            {"value": 20.6, "result": True},
            {"value": 21.0, "result": True},
            {"value": 20.7, "result": False},
            {"value": 20.69999, "result": True},
        ],
    },
    {
        "condition": {
            "type": "gt",
            "check_value": 5,
        },
        "tests": [
            {"value": 10, "result": True},
            {"value": 5.0, "result": False},
            {"value": 4.9, "result": False},
            {"value": 5.0001, "result": True},
            {"value": 6, "result": True},
        ],
    },
    {
        "condition": {
            "type": "gt",
            "check_value": 5.5,
        },
        "tests": [
            {"value": 6.5, "result": True},
            {"value": 5.5, "result": False},
            {"value": 5.4, "result": False},
            {"value": 5.50001, "result": True},
        ],
    },
    {
        "condition": {
            "type": "gte",
            "check_value": 5,
        },
        "tests": [
            {"value": 5, "result": True},
            {"value": 5.0, "result": True},
            {"value": 4.9, "result": False},
            {"value": 6, "result": True},
            {"value": 4.9999, "result": False},
        ],
    },
    {
        "condition": {
            "type": "gte",
            "check_value": 5.5,
        },
        "tests": [
            {"value": 5.5, "result": True},
            {"value": 5.49999, "result": False},
            {"value": 6.0, "result": True},
            {"value": 5.6, "result": True},
        ],
    },
    {
        "condition": {
            "type": "lt",
            "check_value": 100,
        },
        "tests": [
            {"value": 99, "result": True},
            {"value": 100, "result": False},
            {"value": 100.0, "result": False},
            {"value": 101, "result": False},
            {"value": 99.99999, "result": True},
        ],
    },
    {
        "condition": {
            "type": "lt",
            "check_value": 100.5,
        },
        "tests": [
            {"value": 100, "result": True},
            {"value": 100.5, "result": False},
            {"value": 101, "result": False},
            {"value": 100.49999, "result": True},
        ],
    },
    {
        "condition": {
            "type": "lte",
            "check_value": 100,
        },
        "tests": [
            {"value": 100, "result": True},
            {"value": 101, "result": False},
            {"value": 99.9, "result": True},
            {"value": 100.0, "result": True},
            {"value": 100.00001, "result": False},
        ],
    },
    {
        "condition": {
            "type": "lte",
            "check_value": 100.5,
        },
        "tests": [
            {"value": 100.5, "result": True},
            {"value": 100.4999, "result": True},
            {"value": 101.0, "result": False},
            {"value": 100.6, "result": False},
        ],
    },
]

TEST_CASES_DICT_CONVERSION = [
    {
        "condition": Condition(
            con_type=ConditionType.EQUALS,
            check_val=10,
        ),
        "result": {
            "type": "eq",
            "check_value": 10,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.EQUALS,
            check_val=10.5,
        ),
        "result": {
            "type": "eq",
            "check_value": 10.5,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.NOT_EQUALS,
            check_val=20,
        ),
        "result": {
            "type": "neq",
            "check_value": 20,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.NOT_EQUALS,
            check_val=22.5,
        ),
        "result": {
            "type": "neq",
            "check_value": 22.5,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.GREATER_THAN,
            check_val=0,
        ),
        "result": {
            "type": "gt",
            "check_value": 0,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.GREATER_THAN,
            check_val=1.1,
        ),
        "result": {
            "type": "gt",
            "check_value": 1.1,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.GREATER_THAN_EQUALS,
            check_val=10,
        ),
        "result": {
            "type": "gte",
            "check_value": 10,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.GREATER_THAN_EQUALS,
            check_val=10.5,
        ),
        "result": {
            "type": "gte",
            "check_value": 10.5,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.LOWER_THAN,
            check_val=101,
        ),
        "result": {
            "type": "lt",
            "check_value": 101,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.LOWER_THAN,
            check_val=112.5,
        ),
        "result": {
            "type": "lt",
            "check_value": 112.5,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.LOWER_THAN_EQUALS,
            check_val=122,
        ),
        "result": {
            "type": "lte",
            "check_value": 122,
        },
    },
    {
        "condition": Condition(
            con_type=ConditionType.LOWER_THAN_EQUALS,
            check_val=212.5,
        ),
        "result": {
            "type": "lte",
            "check_value": 212.5,
        },
    },
]


class TestCondition(unittest.TestCase):
    def test__condition_check_values(self):
        for test in TEST_CASES_CREATION:
            condition_dict = test["condition"]
            cond = Condition(
                con_type=ConditionType(condition_dict["type"]),
                check_val=condition_dict["check_value"],
            )
            for case in test["tests"]:
                self.assertIs(cond.check_val(case["value"]), case["result"])

    def test__condition_as_dict(self):
        for test in TEST_CASES_DICT_CONVERSION:
            cond = test["condition"]
            self.assertEqual(cond.to_dict(), test["result"])
