import unittest

from casebased.components.casebase.query_case import QueryCase


class TestQueryCase(unittest.TestCase):
    feature_obj = {"A": 1, "B": 2, "C": 3}

    def setUp(self) -> None:
        self.case = QueryCase(self.feature_obj)

    def test__init__reg(self):
        self.assertEqual(self.case.features, self.feature_obj)
        self.assertEqual(self.case.feature_values, [1, 2, 3])

    def test__init__value_error(self):
        feature_obj_mixed = {"A": "eins", "B": "zwei", "C": 3}
        with self.assertRaises(ValueError):
            QueryCase(feature_obj_mixed)

    def test__init__list(self):
        feature_arr = [1, 2, 3]
        with self.assertRaises(ValueError):
            QueryCase(feature_arr)

    def test_get_1d_feature_array(self):
        feat_arr_1d = self.case.get_1d_feature_array()
        self.assertEqual(feat_arr_1d.tolist(), [1, 2, 3])

    def test_get_2d_feature_array(self):
        feat_arr_2d = self.case.get_2d_feature_array()
        self.assertEqual(feat_arr_2d.tolist(), [[1, 2, 3]])
