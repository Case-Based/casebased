import pytest

from casebased.components.querycase import QueryCase

feature_obj = {"A": 1, "B": 2, "C": 3}


def make_case():
    return QueryCase(feature_obj)


class TestQueryCase:
    def test__init__reg(self):
        case = make_case()
        assert case.features == feature_obj
        assert case.feature_values == [1, 2, 3]

    def test__init__value_error(self):
        feature_obj_mixed = {"A": "eins", "B": "zwei", "C": 3}
        with pytest.raises(ValueError) as ve:
            case = QueryCase(feature_obj_mixed)

    def test__init__list(self):
        feature_arr = [1, 2, 3]
        with pytest.raises(ValueError) as ve:
            case = QueryCase(feature_arr)

    def test_get_1d_feature_array(self):
        case = make_case()
        feat_arr_1d = case.get_1d_feature_array()
        assert (feat_arr_1d == [1, 2, 3]).all()

    def test_get_2d_feature_array(self):
        case = make_case()
        feat_arr_2d = case.get_2d_feature_array()
        assert (feat_arr_2d == [[1, 2, 3]]).all()
