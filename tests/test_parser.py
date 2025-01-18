import unittest

from casebased.components.vocabulary import Parser
from casebased.components.vocabulary.conditions import ConditionType


class TestParser(unittest.TestCase):

    def test__generate_vocabulary_from_toml(self):
        vocab = Parser.generate_vocabulary_from_toml(
            "./examples/vocabulary/credit_score.toml"
        )
        self.assertEqual(len(vocab.features), 5)
        self.assertEqual(len(vocab.targets), 1)

        for attr in vocab.features:
            if attr.name == "income":
                self.assertEqual(attr.weight, 1.23)
                self.assertIs(attr.data_type, float)
                self.assertEqual(len(attr.conditions), 1)
                self.assertEqual(
                    attr.conditions[0].con_type, ConditionType.GREATER_THAN_EQUALS
                )
                self.assertEqual(attr.conditions[0].check_val, 0.0)
                self.assertIs(attr.is_target, False)
            elif attr.name == "account_balance":
                self.assertEqual(attr.weight, 1.5)
                self.assertIs(attr.data_type, float)
                self.assertEqual(len(attr.conditions), 0)
                self.assertIs(attr.is_target, False)
            elif attr.name == "average_expenses":
                self.assertEqual(attr.weight, 1.75)
                self.assertIs(attr.data_type, float)
                self.assertEqual(len(attr.conditions), 1)
                self.assertEqual(
                    attr.conditions[0].con_type, ConditionType.GREATER_THAN_EQUALS
                )
                self.assertEqual(attr.conditions[0].check_val, 0.0)
                self.assertIs(attr.is_target, False)
            elif attr.name == "age":
                self.assertEqual(attr.weight, 1.0)
                self.assertIs(attr.data_type, int)
                self.assertEqual(len(attr.conditions), 1)
                self.assertEqual(attr.conditions[0].check_val, 0)
                self.assertEqual(
                    attr.conditions[0].con_type, ConditionType.GREATER_THAN_EQUALS
                )
                self.assertIs(attr.is_target, False)
            elif attr.name == "count_balance_in_dispo":
                self.assertEqual(attr.weight, 2.5)
                self.assertIs(attr.data_type, int)
                self.assertEqual(len(attr.conditions), 1)
                self.assertEqual(attr.conditions[0].check_val, 0)
                self.assertEqual(
                    attr.conditions[0].con_type, ConditionType.GREATER_THAN_EQUALS
                )
                self.assertIs(attr.is_target, False)
        for attr in vocab.targets:
            if attr.name == "credit_score":
                self.assertEqual(attr.weight, 1.0)
                self.assertIs(attr.data_type, float)
                self.assertEqual(len(attr.conditions), 2)
                self.assertEqual(attr.conditions[0].check_val, 0.0)
                self.assertEqual(
                    attr.conditions[0].con_type, ConditionType.GREATER_THAN_EQUALS
                )
                self.assertEqual(attr.conditions[1].check_val, 100.0)
                self.assertEqual(
                    attr.conditions[1].con_type, ConditionType.LOWER_THAN_EQUALS
                )
                self.assertIs(attr.is_target, True)

    def test__generate_toml_file(self):
        pass
