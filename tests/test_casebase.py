import unittest

import pandas as pd

from casebased.components.casebase.casebase import CaseBase


class TestCaseBase(unittest.TestCase):
    def test_caseBase_initialization(self):
        caseBase = CaseBase()
        assert isinstance(caseBase.cases, pd.DataFrame)
        assert len(caseBase.cases) == 0

    def test_add_case(self):
        casebase = CaseBase(pd.DataFrame(columns=["feature1", "feature2", "utility"]))

        new_case = {"feature1": "value1", "feature2": "value2"}
        casebase.add_case(new_case)

        # Check if case was added
        assert len(casebase.cases) == 1, "CaseBase should have one case after adding"
        assert (
            casebase.cases.loc[0, "feature1"] == "value1"
        ), "Feature1 should match the added case"
        assert (
            casebase.cases.loc[0, "feature2"] == "value2"
        ), "Feature2 should match the added case"
        assert (
            casebase.cases.loc[0, "utility"] == 0
        ), "Utility should be initialized to 0"

    def test_case_structure_validation(self):
        casebase = CaseBase(pd.DataFrame(columns=["feature1", "feature2", "utility"]))

        # Correct structure
        valid_case = {"feature1": "value1", "feature2": "value2"}
        casebase.add_case(valid_case)

        # Incorrect structure
        invalid_case = {"feature1": "value1"}  # Missing "feature2"
        with self.assertRaises(ValueError) as err:
            casebase.add_case(invalid_case)
        self.assertEqual(
            str(err.exception), "Case structure does not match dataframe structure"
        )
