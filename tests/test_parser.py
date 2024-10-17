from casebased.components.vocabulary import Parser
from casebased.components.vocabulary.conditions import ConditionType


def test__generate_vocabulary_from_toml():
    vocab = Parser.generate_vocabulary_from_toml(
        "./examples/vocabulary/credit_score.toml"
    )
    assert len(vocab.features) == 5
    assert len(vocab.targets) == 1
    for attr in vocab.features:
        if attr.name == "income":
            assert attr.weight == 1.23
            assert attr.data_type is float
            assert len(attr.conditions) == 1
            assert attr.conditions[0].con_type == ConditionType.GREATER_THAN_EQUALS
            assert attr.conditions[0].check_val == 0.0
            assert attr.is_target is False
        elif attr.name == "account_balance":
            assert attr.weight == 1.5
            assert attr.data_type is float
            assert len(attr.conditions) == 0
            assert attr.is_target is False
        elif attr.name == "average_expenses":
            assert attr.weight == 1.75
            assert attr.data_type is float
            assert len(attr.conditions) == 1
            assert attr.conditions[0].con_type == ConditionType.GREATER_THAN_EQUALS
            assert attr.conditions[0].check_val == 0.0
            assert attr.is_target is False
        elif attr.name == "age":
            assert attr.weight == 1.0
            assert attr.data_type is int
            assert len(attr.conditions) == 1
            assert attr.conditions[0].check_val == 0
            assert attr.conditions[0].con_type == ConditionType.GREATER_THAN_EQUALS
            assert attr.is_target is False
        elif attr.name == "count_balance_in_dispo":
            assert attr.weight == 2.5
            assert attr.data_type is int
            assert len(attr.conditions) == 1
            assert attr.conditions[0].con_type == ConditionType.GREATER_THAN_EQUALS
            assert attr.conditions[0].check_val == 0
            assert attr.is_target is False
    for attr in vocab.targets:
        if attr.name == "credit_score":
            assert attr.data_type is float
            assert attr.weight == 1.0
            assert len(attr.conditions) == 2
            assert attr.conditions[0].con_type == ConditionType.GREATER_THAN_EQUALS
            assert attr.conditions[0].check_val == 0.0
            assert attr.conditions[1].con_type == ConditionType.LOWER_THAN_EQUALS
            assert attr.conditions[1].check_val == 100.0
            assert attr.is_target is True


def test__generate_toml_file():
    pass
