# from src.casebased.components.knowledge_containers.case_base import casebase
from case_base import casebase
import unittest
import os 
import pandas as pd
from io import StringIO
from pathlib import Path
import tempfile
from pandas._typing import FilePath

class TestCaseBase(unittest.TestCase):

    def test_case_base(self):
        cb_type = cb_type.DF
        file_path = os.path.join(os.path.dirname(__file__), 'test_data/regen.csv')
        case_base = casebase(cb_type=cb_type, source=file_path)

        self.assertEqual(case_base.data, None)
        self.assertEqual(case_base.cb_type, None)
        self.assertEqual(case_base.source, None)

    def test_case_base_with_data(self):
        case_base = casebase.CaseBase()
        csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data/regen.csv')

        expected_data = pd.read_csv(csv_file_path)
        case_base.read_from_csv(csv_file_path)

        pd.testing.assert_frame_equal(case_base.data, expected_data)

    def setUp(self):
        case_base = casebase.CaseBase()
        csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data/regen.csv')

        case_base = pd.read_csv(csv_file_path)

        dataframe = { 
            'Fallnummer': [1, 2, 3, 4],
            'Temperatur': [22.5, 25.0, 20.0, 30.0],
            'Luftfeuchtigkeit': [85, 60, 90, 50],
            'Luftdruck': [1012, 1015, 1009, 1010],
            'Windgeschwindigkeit': [15, 10, 20, 5],
            'Laengengrad': [13.404954, 11.581981, 9.993682, 8.682127],
            'Breitengrad': [52.520008, 48.135125, 53.551086, 50.110924],
            'Regen?': [1, 0, 1, 0]
        }

    def test_verify_case_structure(self):

        case = {
            'Fallnummer': 1,
            'Temperatur': 22.5,
            'Luftfeuchtigkeit': 85,
            'Luftdruck': 1012,
            'Windgeschwindigkeit': 15,
            'Laengengrad': 13.404954,
            'Breitengrad': 52.520008,
            'Regen?': 1
        }

        cb = casebase.CaseBase(self.df)
        result = cb.verify_case_structure(case)
        self.assertTrue(result)

    def test_get_index_case(self):

        file_path = os.path.join(os.path.dirname(__file__), 'test_data/regen.csv')

        casebase = casebase.CaseBase(file_path)

        value_to_find = 20.0
        positions = casebase.get_position_of_case(value_to_find)
        self.assertEqual(positions, [2])

    def test_add_case(self):

        new_case = {
            "Fallnummer": 0, "Temperatur": 20.0, "Luftfeuchtigkeit": 1, "Luftdruck": 1,
            "Windgeschwindigkeit": 1, "Laengengrad": 1, "Breitengrad": 1, "Regen?": 1
        }
        
        updated_df = casebase.add_case(new_case)

        # Check if the new case is added correctly
        self.assertEqual(len(updated_df), 5)  # Check the length of the DataFrame
        self.assertEqual(updated_df.iloc[-1]["Fallnummer"], 5)  # Check the new case number
        self.assertEqual(updated_df.iloc[-1]["Temperatur"], 20.0)  # Check the temperature
        self.assertEqual(updated_df.iloc[-1]["Luftfeuchtigkeit"], 1)  # Check the humidity
        self.assertEqual(updated_df.iloc[-1]["Luftdruck"], 1)  # Check the air pressure
        self.assertEqual(updated_df.iloc[-1]["Windgeschwindigkeit"], 1)  # Check the wind speed
        self.assertEqual(updated_df.iloc[-1]["Laengengrad"], 1)  # Check the longitude
        self.assertEqual(updated_df.iloc[-1]["Breitengrad"], 1)  # Check the latitude
        self.assertEqual(updated_df.iloc[-1]["Regen?"], 1)  # Check the rain value

    def test_remove_case_with_missing_value(self): 

        casebase.remove_case(new_case, updated_df)
        self.assertEqual(len(updated_df), 5)  # Check the length of the DataFrame
        self.assertEqual(updated_df.iloc[-1]["Fallnummer"], 5)  # Check the new case number
        self.assertEqual(updated_df.iloc[-1]["Temperatur"], 20.0)  # Check the temperature
        self.assertEqual(updated_df.iloc[-1]["Luftfeuchtigkeit"], 1)  # Check the humidity
        self.assertEqual(updated_df.iloc[-1]["Luftdruck"], 1)  # Check the air pressure
        self.assertEqual(updated_df.iloc[-1]["Windgeschwindigkeit"], 1)  # Check the wind speed
        self.assertEqual(updated_df.iloc[-1]["Laengengrad"], 1)  # Check the longitude
        self.assertEqual(updated_df.iloc[-1]["Breitengrad"], 1)  # Check the latitude
        self.assertEqual(updated_df.iloc[-1]["Regen?"], 1)  # Check the rain value

    def test_remove_duplicate_cases(self): 

        casebase = casebase.CaseBase()

        csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data/regen.csv')


class TestCaseBaseInitialization(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory and files for testing
        self.test_dir = tempfile.TemporaryDirectory()

        # Create a temporary CSV file
        self.csv_file = Path(self.test_dir.name) / "test.csv"
        pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}).to_csv(self.csv_file, index=False)

        # Create a temporary Excel file
        self.excel_file = Path(self.test_dir.name) / "test.xlsx"
        pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}).to_excel(self.excel_file, index=False)

        # Create a temporary JSON file
        self.json_file = Path(self.test_dir.name) / "test.json"
        pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}).to_json(self.json_file)

        # Create a temporary unsupported file
        self.unsupported_file = Path(self.test_dir.name) / "test.txt"
        with open(self.unsupported_file, 'w') as f:
            f.write("This is a test file with unsupported format.")

    def tearDown(self):
        # Cleanup the temporary directory and files
        self.test_dir.cleanup()

    def test_csv_initialization(self):
        case_base_csv = casebase(cb_type=CBTypes.DF.value, source=self.csv_file)
        self.assertIsNotNone(case_base_csv.data, "CSV data should be loaded")
        self.assertFalse(case_base_csv.data.empty, "CSV data should not be empty")

    def test_excel_initialization(self):
        case_base_excel = casebase(cb_type=CBTypes.DF.value, source=self.excel_file)
        self.assertIsNotNone(case_base_excel.data, "Excel data should be loaded")
        self.assertFalse(case_base_excel.data.empty, "Excel data should not be empty")

    def test_json_initialization(self):
        case_base_json = casebase(cb_type=CBTypes.DF.value, source=self.json_file)
        self.assertIsNotNone(case_base_json.data, "JSON data should be loaded")
        self.assertFalse(case_base_json.data.empty, "JSON data should not be empty")

    def test_unsupported_file_initialization(self):
        with self.assertRaises(ValueError, msg="No valid file extension"):
            casebase(cb_type=CBTypes.DF.value, source=self.unsupported_file)

    

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
