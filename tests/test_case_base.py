import pytest
import pandas as pd
from pathlib import Path
import tempfile
from pandas._typing import FilePath
from casebased.components.constants import CBTypes
from casebased.components.casebase.casebase import CaseBase
import pandas.testing as pd_testing


def read_csv_to_pd(file_path: FilePath) -> pd.DataFrame:
    """
    Parameters:
    file path to the csv

    Returns:
    pandas dataframe
    """
    return pd.read_csv(file_path)


class TestCaseBase:
    """
    Tests for case base + case base maintainer.
    """

    setup_cases_dataframe = read_csv_to_pd(Path("test_data/regenSetup.csv"))
    regen_cases_dataframe = read_csv_to_pd(Path("test_data/regen.csv"))
    regen_duplicate_dataframe = read_csv_to_pd(Path("test_data/regenDuplicate.csv"))
    regen_empty_dataframe = read_csv_to_pd(Path("test_data/regenEmpty.csv"))
    regen_clean_up_dataframe = read_csv_to_pd(Path("test_data/regenCleanUp.csv"))

    def test_setUp(self):

        data = {
            "Fallnummer": [1, 2, 3, 4],
            "Temperatur": [22.5, 20.0, 25.0, 30.0],
            "Luftfeuchtigkeit": [85, 60, 90, 50],
            "Luftdruck": [1012, 1015, 1009, 1010],
            "Windgeschwindigkeit": [15, 10, 20, 5],
            "Laengengrad": [13.404954, 11.581981, 9.993682, 8.682127],
            "Breitengrad": [52.520008, 48.135125, 53.551086, 50.110924],
            "Regen": [1, 0, 1, 0],
            "utility": [0, 0, 0, 0],
        }

        case_base_instance1 = CaseBase(cases=self.setup_cases_dataframe)
        case_base_instance2 = pd.DataFrame(data)

        pd_testing.assert_frame_equal(case_base_instance2, case_base_instance1.cases)

    def test_add_case(self):
        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)
        new_case = {
            "Fallnummer": 5,
            "Temperatur": 20.0,
            "Luftfeuchtigkeit": 40,
            "Luftdruck": 5,
            "Windgeschwindigkeit": 23,
            "Laengengrad": 56.0,
            "Breitengrad": 34.2,
            "Regen?": 1,
        }

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen?": 0,
                "utility": 0,
            },
            {
                "Fallnummer": 5,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 40,
                "Luftdruck": 5,
                "Windgeschwindigkeit": 23,
                "Laengengrad": 56.0,
                "Breitengrad": 34.2,
                "Regen?": 1,
                "utility": 0,
            },
        ]

        case_base_instance.add_case(new_case)
        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test_add_list_of_cases(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        new_cases = [
            {
                "Fallnummer": 5,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 1,
                "Luftdruck": 1,
                "Windgeschwindigkeit": 1,
                "Laengengrad": 1,
                "Breitengrad": 1,
                "Regen?": 1,
            },
            {
                "Fallnummer": 6,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 1,
                "Luftdruck": 1,
                "Windgeschwindigkeit": 1,
                "Laengengrad": 1,
                "Breitengrad": 1,
                "Regen?": 1,
            },
        ]

        case_base_instance.add_list_of_cases(new_cases)

        expected_case_base = {
            "Fallnummer": [1, 2, 3, 4, 5, 6],
            "Temperatur": [22.5, 25.0, 20.0, 30.0, 20.0, 20.0],
            "Luftfeuchtigkeit": [85, 60, 90, 50, 1, 1],
            "Luftdruck": [1012, 1015, 1009, 1010, 1, 1],
            "Windgeschwindigkeit": [15, 10, 20, 5, 1, 1],
            "Laengengrad": [13.404954, 11.581981, 9.993682, 8.682127, 1, 1],
            "Breitengrad": [52.520008, 48.135125, 53.551086, 50.110924, 1, 1],
            "Regen?": [1, 0, 1, 0, 1, 1],
            "utility": [0, 0, 0, 0, 0, 0],
        }

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test_update_case(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        case_base_instance.update_case(1, {"Temperatur": 50.0})

        expected_case_base = {
            "Fallnummer": [1, 2, 3, 4],
            "Temperatur": [22.5, 25.0, 20.0, 30.0],
            "Luftfeuchtigkeit": [85, 60, 90, 50],
            "Luftdruck": [1012, 1015, 1009, 1010],
            "Windgeschwindigkeit": [15, 10, 20, 5],
            "Laengengrad": [13.404954, 11.581981, 9.993682, 8.682127],
            "Breitengrad": [52.520008, 48.135125, 53.551086, 50.110924],
            "Regen?": [1, 0, 1, 0],
            "utility": [0, 0, 0, 0],
        }

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test_prune(self):

        list_of_cases = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen": 1,
                "utility": 2,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen": 0,
                "utility": 3,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen": 1,
                "utility": 1,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen": 0,
                "utility": 0,
            },
        ]
        list_of_cases_df = pd.DataFrame(list_of_cases)
        case_base_instance = CaseBase(cases=list_of_cases_df)

        case_base_instance.prune(2)

        expected_values = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen": 1,
                "utility": 2,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen": 0,
                "utility": 3,
            },
        ]

        expected_values_df = pd.DataFrame(expected_values)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_values_df)

    def test_return_case_base_instance(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen?": 0,
                "utility": 0,
            },
        ]

        current_case_base_instance = case_base_instance.get_current_casebase()

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(current_case_base_instance, expected_case_base_df)

    def test_remove_case_by_case(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        case_to_remove = {
            "Fallnummer": 2,
            "Temperatur": 25.0,
            "Luftfeuchtigkeit": 60,
            "Luftdruck": 1015,
            "Windgeschwindigkeit": 10,
            "Laengengrad": 11.581981,
            "Breitengrad": 48.135125,
            "Regen": 0,
            "utility": 0,
        }

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen?": 0,
                "utility": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)
        case_base_instance.remove_case_by_case(case_to_remove)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test__verify_case_structure_true(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        case_true = {
            "Fallnummer": 5,
            "Temperatur": 20.0,
            "Luftfeuchtigkeit": 1,
            "Luftdruck": 1,
            "Windgeschwindigkeit": 1,
            "Laengengrad": 1,
            "Breitengrad": 1,
            "Regen": 1,
        }

        if case_base_instance._verify_case_structure(case_true):
            assert True

    def test__verify_case_structure_false(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        case_true = {
            "Fallnummer": 5,
            "Temperatur": 20.0,
            "Luftfeuchtigkeit": 1,
            "Luftdruck": 1,
            "Windgeschwindigkeit": 1,
            "Laengengrad": 1,
            "Regen": 1,
        }

        if case_base_instance._verify_case_structure(case_true):
            assert False

    def test__get_index_case_of_value(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        value_to_find = 20.0
        positions = case_base_instance._get_index_of_case(value_to_find)
        assert positions == [2]

    def test_remove_case_by_index(self):

        case_base_instance = CaseBase(cases=self.regen_cases_dataframe)

        case_base_instance.remove_case_by_index(1)

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen?": 0,
                "utility": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test__remove_cases_with_missing_values(self):

        case_base_instance = CaseBase(cases=self.regen_empty_dataframe)

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)
        case_base_instance._remove_cases_with_missing_values()

        pd.testing.assert_frame_equal(
            case_base_instance.cases, pd.DataFrame(expected_case_base_df)
        )

    def test__drop_duplicate_cases(self):

        case_base_instance = CaseBase(cases=self.regen_duplicate_dataframe)

        case_base_instance._drop_duplicate_cases(["Fallnummer"])

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 28.0,
                "Luftfeuchtigkeit": 40,
                "Luftdruck": 1310,
                "Windgeschwindigkeit": 9,
                "Laengengrad": 8.482127,
                "Breitengrad": 40.110924,
                "Regen?": 1,
                "utility": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test__drop_duplicate_cases_no_columns_to_ignore(self):
        """
        Test _drop_duplicate_cases when no columns are provided to ignore.
        All columns should be used to identify duplicates.
        """

        case_base_instance = CaseBase(cases=self.regen_duplicate_dataframe)

        case_base_instance._drop_duplicate_cases()

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 28.0,
                "Luftfeuchtigkeit": 40,
                "Luftdruck": 1310,
                "Windgeschwindigkeit": 9,
                "Laengengrad": 8.482127,
                "Breitengrad": 40.110924,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 5,
                "Temperatur": 28.0,
                "Luftfeuchtigkeit": 40,
                "Luftdruck": 1310,
                "Windgeschwindigkeit": 9,
                "Laengengrad": 8.482127,
                "Breitengrad": 40.110924,
                "Regen?": 1,
                "utility": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test__fill_missing_values_with_zero(self):

        case_base_instance = CaseBase(cases=self.regen_empty_dataframe)

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 0,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 0,
                "Breitengrad": 50.110924,
                "Regen?": 0,
                "utility": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)

        case_base_instance._fill_missing_values_with_zero()

        pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)

    def test__raise_error_if_casebase_is_None(self):

        test_case_base = None

        with pytest.raises(ValueError, match="Case base cannot be None"):
            case_base_instance = CaseBase(cases=test_case_base)

    # def test_clean_up_case_base(self):

    #     case_base_instance = CaseBase(cases=self.regen_clean_up_dataframe)

    #     expected_case_base = [
    #         {
    #             "Fallnummer": 1,
    #             "Temperatur": 22.5,
    #             "Luftfeuchtigkeit": 85,
    #             "Luftdruck": 1012,
    #             "Windgeschwindigkeit": 15,
    #             "Laengengrad": 13.404954,
    #             "Breitengrad": 52.520008,
    #             "Regen?": 1,
    #             "utility": 0,
    #         },
    #         {
    #             "Fallnummer": 2,
    #             "Temperatur": 25.0,
    #             "Luftfeuchtigkeit": 60,
    #             "Luftdruck": 1015,
    #             "Windgeschwindigkeit": 10,
    #             "Laengengrad": 11.581981,
    #             "Breitengrad": 48.135125,
    #             "Regen?": 0,
    #             "utility": 0,
    #         },
    #         {
    #             "Fallnummer": 4,
    #             "Temperatur": 28.0,
    #             "Luftfeuchtigkeit": 40,
    #             "Luftdruck": 1010,
    #             "Windgeschwindigkeit": 5,
    #             "Laengengrad": 0,
    #             "Breitengrad": 50.110924,
    #             "Regen?": 0,
    #             "utility": 0,
    #         },
    #     ]

    #     expected_case_base_df = pd.DataFrame(expected_case_base)

    #     case_base_instance.clean_up_casebase(["Fallnummer"])

    #     print("expected data frame", expected_case_base_df)
    #     print("case base instance", case_base_instance.cases)

    #     pd.testing.assert_frame_equal(case_base_instance.cases, expected_case_base_df)
